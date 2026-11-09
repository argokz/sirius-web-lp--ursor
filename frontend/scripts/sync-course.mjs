// Переносит обучающий курс веб-ТГИД (docs/course репозитория web-itwin) на сайт:
// треки, уроки и тесты — в server/data/course.json, снимки — в public/course/img/.
// Ссылки на инструкцию ведут на /docs (нужен server/data/manual.json — сначала npm run manual:sync),
// ссылки на уроки — на /learn/<трек>/<урок> (трек — первый, в который урок входит).
// node scripts/sync-course.mjs [папка курса]   (или COURSE_SRC); предупреждения роняют синхронизацию, если не COURSE_STRICT=0
import { promises as fs } from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { marked } from 'marked'

const DEFAULT_SOURCE = 'H:/projects/tgid-app/web-itwin/docs/course'
const frontendDir = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const sourceDir = path.resolve(process.argv[2] || process.env.COURSE_SRC || DEFAULT_SOURCE)
const manualFile = path.join(frontendDir, 'server/data/manual.json')
const outFile = path.join(frontendDir, 'server/data/course.json')
const publicDir = path.join(frontendDir, 'public/course')
const strict = process.env.COURSE_STRICT !== '0'

const warnings = []
const warn = (text) => warnings.push(text)

const escapeHtml = (text) => String(text)
  .replace(/&/g, '&amp;')
  .replace(/</g, '&lt;')
  .replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;')

const slugifyHeading = (text, used) => {
  const base = text.toLowerCase().replace(/[^\p{L}\p{N}]+/gu, '-').replace(/^-|-$/g, '') || 'section'
  let slug = base
  for (let i = 2; used.has(slug); i++) slug = `${base}-${i}`
  used.add(slug)
  return slug
}

const stripFrontmatter = (md) => md.replace(/^---\n[\s\S]*?\n---\n/, '')

const index = JSON.parse(await fs.readFile(path.join(sourceDir, 'index.json'), 'utf8'))
const manual = JSON.parse(await fs.readFile(manualFile, 'utf8'))

const lessonById = new Map(index.lessons.map((lesson) => [lesson.id, lesson]))
const lessonByFile = new Map(index.lessons.map((lesson) => [lesson.file, lesson]))
/** Урок → первый трек, где он урок или практика: туда ведут ссылки между уроками */
const homeTrack = new Map()
for (const track of index.tracks) {
  for (const id of [...track.lessons, track.practice].filter(Boolean)) {
    if (!lessonById.has(id)) warn(`трек ${track.id}: нет урока ${id}`)
    if (!homeTrack.has(id)) homeTrack.set(id, track.id)
  }
}
const lessonUrl = (id) => `/learn/${homeTrack.get(id)}/${id}`

/** «../manual/05-analysis/calculation.md#якорь» или «05-hydraulic-calculation.md» → адрес на сайте */
const resolveHref = (href, where) => {
  if (/^(https?:|mailto:|#)/.test(href)) return href
  const [file, anchor] = href.split('#')
  const hash = anchor ? `#${anchor}` : ''
  // снимки инструкции уже лежат на сайте в public/manual (npm run manual:sync)
  const manualImage = file.match(/^\.\.\/manual\/([^/]+)\/(img\/[\w.-]+)$/)
  if (manualImage) return `/manual/${manualImage[1]}/${manualImage[2]}`
  const manualReadme = file.match(/^\.\.\/manual\/([^/]+)\/README\.md$/)
  if (manualReadme) {
    const section = manual.sections.find((item) => item.id === manualReadme[1])
    if (section) return `/docs/${section.slug}${hash}`
    warn(`${where}: нет раздела инструкции ${manualReadme[1]}`)
    return null
  }
  const manualLink = file.match(/^\.\.\/manual\/([^/]+)\/([^/]+)\.md$/)
  if (manualLink) {
    const page = manual.pages[`${manualLink[1]}/${manualLink[2]}`]
    if (page) return page.url + hash
    warn(`${where}: нет страницы инструкции ${manualLink[1]}/${manualLink[2]}`)
    return null
  }
  if (/^img\//.test(file)) return `/course/${file}`
  const lesson = lessonByFile.get(file)
  if (lesson) {
    if (homeTrack.has(lesson.id)) return lessonUrl(lesson.id) + hash
    warn(`${where}: урок ${lesson.id} не входит ни в один трек`)
    return null
  }
  // README, отчёт, скрипты репозитория — на сайте их нет: ссылка становится текстом
  if (!/^(README|REPORT)\.md$|^\.\.\/\.\.\//.test(file)) warn(`${where}: неизвестная ссылка ${href}`)
  return null
}

/** Ссылки markdown переписываются до разбора; неразрешимые остаются текстом */
const rewriteLinks = (md, where) => md.replace(/(!?)\[([^\]]*)]\(([^)\s]+)\)/g, (whole, bang, text, href) => {
  const url = resolveHref(href, where)
  if (url) return `${bang}[${text}](${url})`
  return bang ? '' : text
})

const renderHtml = (md, where) => {
  const usedIds = new Set()
  const toc = []
  const html = marked.parse(rewriteLinks(md, where), { async: false })
    .replace(/<h2>(.*?)<\/h2>/g, (whole, text) => {
      const plain = text.replace(/<[^>]+>/g, '')
      const id = slugifyHeading(plain, usedIds)
      toc.push({ id, text: plain })
      return `<h2 id="${id}">${text}</h2>`
    })
    .replace(/<img src="([^"]+)" alt="([^"]*)">/g, '<img src="$1" alt="$2" loading="lazy" decoding="async">')
    .replace(/<a href="(https?:[^"]+)"/g, '<a href="$1" target="_blank" rel="noopener noreferrer"')
  return { html, toc }
}

const inlineHtml = (md, where) => marked.parseInline(rewriteLinks(escapeHtml(md), where), { async: false })

const quizOf = (lesson) => (lesson.quiz || []).map((item, i) => {
  const where = `${lesson.id}: вопрос ${i + 1}`
  if (!Array.isArray(item.options) || item.options.length < 2 || !(item.answer in item.options)) warn(`${where}: неверный формат`)
  return {
    id: item.id || `${lesson.id}-${i + 1}`,
    q: inlineHtml(item.q, where),
    options: item.options.map((option) => inlineHtml(option, where)),
    answer: item.answer,
    explain: inlineHtml(item.explain || '', where)
  }
})

const lessons = {}
for (const lesson of index.lessons) {
  if (!homeTrack.has(lesson.id)) {
    warn(`урок ${lesson.id} не входит ни в один трек — на сайт не попадёт`)
    continue
  }
  const md = (await fs.readFile(path.join(sourceDir, lesson.file), 'utf8')).replace(/\r\n/g, '\n')
  const body = stripFrontmatter(md).replace(/^# .*\n+/, '')
  const { html, toc } = renderHtml(body, lesson.id)
  lessons[lesson.id] = {
    id: lesson.id,
    kind: lesson.kind,
    module: lesson.module,
    title: lesson.title,
    summary: lesson.summary,
    level: lesson.level,
    minutes: lesson.minutes,
    url: lessonUrl(lesson.id),
    html,
    toc,
    manual: (lesson.manual || []).map((link) => {
      const readme = link.ref.match(/^([^/]+)\/README$/)
      const section = readme && manual.sections.find((item) => item.id === readme[1])
      if (section) return { title: section.title, url: `/docs/${section.slug}` }
      const page = manual.pages[link.ref]
      if (!page) warn(`${lesson.id}: нет страницы инструкции ${link.ref}`)
      return page ? { title: page.title, url: page.url } : null
    }).filter(Boolean),
    // разделы инструкции, о которых урок: по ним витрина «Возможности» ставит ссылки на курс
    sections: [...new Set((lesson.manual || []).map((link) => link.ref.split('/')[0]))],
    related: (lesson.related || []).filter((id) => homeTrack.has(id)).map((id) => ({ id, title: lessonById.get(id).title, url: lessonUrl(id) })),
    quiz: quizOf(lesson),
    tasks: lesson.tasks || 0,
    keywords: lesson.keywords || [],
    updated: lesson.updated || null
  }
}

const tracks = index.tracks.map((track) => ({
  id: track.id,
  title: track.title,
  summary: track.summary,
  level: track.level,
  start: track.start,
  lessons: track.lessons.filter((id) => lessons[id]),
  practice: lessons[track.practice] ? track.practice : null,
  exam: track.exam,
  minutes: track.minutes,
  questions: [...track.lessons, track.practice].reduce((sum, id) => sum + (lessons[id]?.quiz.length || 0), 0)
}))
for (const track of tracks) {
  if (track.questions < track.exam.questions) warn(`трек ${track.id}: в банке ${track.questions} вопросов, а в итоговом тесте ${track.exam.questions}`)
}

// снимки курса
await fs.rm(publicDir, { recursive: true, force: true })
const imgDir = path.join(sourceDir, 'img')
let copied = 0
if (await fs.access(imgDir).then(() => true, () => false)) {
  await fs.cp(imgDir, path.join(publicDir, 'img'), { recursive: true })
  copied = (await fs.readdir(imgDir)).length
}

const course = { generatedAt: new Date().toISOString(), source: index.generated, tracks, lessons }
await fs.mkdir(path.dirname(outFile), { recursive: true })
await fs.writeFile(outFile, JSON.stringify(course))

const quizCount = Object.values(lessons).reduce((sum, lesson) => sum + lesson.quiz.length, 0)
console.log(`Курс: ${tracks.length} треков, ${Object.keys(lessons).length} уроков, ${quizCount} вопросов; снимков: ${copied}`)
if (warnings.length) {
  console.warn(warnings.map((text) => `  ! ${text}`).join('\n'))
  if (strict) process.exit(1)
}
