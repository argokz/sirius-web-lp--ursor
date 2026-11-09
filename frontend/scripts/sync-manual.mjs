// Переносит инструкцию веб-ТГИД (docs/manual репозитория web-itwin) в справку сайта:
// тексты — в server/data/manual.json, снимки — в public/manual/<раздел>/img/,
// ролики и субтитры — в manual-media/<раздел>/video/ (их отдаёт server/routes/docs-media с Range:
// встроенная раздача public/ перематывать ролик не даёт).
// Папка роликов на сервере — NUXT_MANUAL_MEDIA_DIR или manual-media в рабочей папке (frontend/).
// Запуск: npm run manual:sync [-- <путь к docs/manual>] или MANUAL_SRC=<путь> npm run manual:sync
//
// Разделы и порядок страниц — из index.json инструкции (его собирает scripts/manual/pages.mjs).
// id страницы уникален только внутри раздела (architecture есть и у администратора, и у разработчика),
// поэтому ключ страницы в справке — «раздел/id».
import { createHash } from 'node:crypto'
import { promises as fs, readFileSync } from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { marked } from 'marked'

const here = path.dirname(fileURLToPath(import.meta.url))
const frontendDir = path.resolve(here, '..')
const DEFAULT_SOURCE = 'H:/projects/tgid-app/web-itwin/docs/manual'
const sourceDir = path.resolve(process.argv[2] || process.env.MANUAL_SRC || DEFAULT_SOURCE)
const publicDir = path.join(frontendDir, 'public/manual')
const mediaDir = path.join(frontendDir, 'manual-media')
const dataFile = path.join(frontendDir, 'server/data/manual.json')

/** Папка инструкции → куда копировать на сайте */
const MEDIA_TARGETS = { img: publicDir, video: mediaDir }
const SEARCH_TEXT_LIMIT = 1500
/** Разделы страницы для администратора и разработчика: читателю-пользователю они свёрнуты */
const LEVEL_SECTIONS = { 'Для администратора': 'admin', 'Для разработчика': 'dev' }
/** «Возможности» — с этапа 1 инструкции, «Что умеет» — прежнее название */
const ABILITY_SECTIONS = new Set(['Возможности', 'Что умеет'])
/** Эти разделы страница показывает отдельными блоками, в тело они не попадают */
const OWN_BLOCKS = new Set(['Видео', 'Связанные функции', 'Функции в ролике'])

const sectionSlug = (sectionId) => sectionId.replace(/^\d+-/, '')
const pageUrl = (sectionId, pageId) => `/docs/${sectionSlug(sectionId)}/${pageId}`
/** Ролики кешируются на неделю — в адрес добавляется версия по содержимому, чтобы переснятый ролик не застревал в кеше */
const videoVersions = new Map()
const videoVersion = (sectionId, rel) => {
  const file = path.join(sourceDir, sectionId, rel)
  if (!videoVersions.has(file)) {
    let version = ''
    try {
      version = createHash('sha1').update(readFileSync(file)).digest('hex').slice(0, 10)
    } catch {
      // файла нет — о битой ссылке предупредит проверка ниже, адрес остаётся без версии
    }
    videoVersions.set(file, version)
  }
  return videoVersions.get(file)
}
const mediaUrl = (sectionId, rel) => {
  if (!rel.startsWith('video/')) return `/manual/${sectionId}/${rel}`
  const version = videoVersion(sectionId, rel)
  return `/docs-media/${sectionId}/${rel}${version ? `?v=${version}` : ''}`
}
const keyOf = (sectionId, pageId) => `${sectionId}/${pageId}`

const exists = async (file) => fs.access(file).then(() => true, () => false)

const stripInline = (md) => md
  .replace(/!\[[^\]]*]\([^)]*\)/g, '')
  .replace(/\[([^\]]+)]\([^)]*\)/g, '$1')
  .replace(/[*_`]/g, '')
  .replace(/\s+/g, ' ')
  .trim()

const escapeHtml = (text) => text
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

/** «1:42» → 102 */
const clockSeconds = (text) => text.split(':').reduce((sum, part) => sum * 60 + Number(part), 0)

// Размер webp без сторонних библиотек: заголовки VP8X / VP8 / VP8L.
const readWebpSize = async (file) => {
  const handle = await fs.open(file, 'r')
  try {
    const buf = Buffer.alloc(30)
    await handle.read(buf, 0, 30, 0)
    if (buf.toString('ascii', 0, 4) !== 'RIFF' || buf.toString('ascii', 8, 12) !== 'WEBP') return null
    const chunk = buf.toString('ascii', 12, 16)
    if (chunk === 'VP8X') {
      return { width: 1 + buf.readUIntLE(24, 3), height: 1 + buf.readUIntLE(27, 3) }
    }
    if (chunk === 'VP8 ') {
      return { width: buf.readUInt16LE(26) & 0x3fff, height: buf.readUInt16LE(28) & 0x3fff }
    }
    if (chunk === 'VP8L') {
      const bits = buf.readUInt32LE(21)
      return { width: 1 + (bits & 0x3fff), height: 1 + ((bits >> 14) & 0x3fff) }
    }
    return null
  } finally {
    await handle.close()
  }
}

/** Заголовок и первый абзац README раздела */
const readSectionInfo = async (sectionId) => {
  const md = (await fs.readFile(path.join(sourceDir, sectionId, 'README.md'), 'utf8')).replace(/\r\n/g, '\n')
  const lines = md.split('\n')
  const title = stripInline(lines.find((line) => line.startsWith('# '))?.slice(2) || sectionId)
  const description = stripInline(lines.find((line) => line.trim() && !/^(#|\||\[|>)/.test(line)) || '')
  return { title, description }
}

const copyMedia = async (sectionId) => {
  let copied = 0
  // ролики прежних синхронизаций лежали в public/ — убрать, чтобы не уезжали в сборку дважды
  await fs.rm(path.join(publicDir, sectionId, 'video'), { recursive: true, force: true })
  for (const [dir, targetRoot] of Object.entries(MEDIA_TARGETS)) {
    const from = path.join(sourceDir, sectionId, dir)
    if (!(await exists(from))) continue
    const to = path.join(targetRoot, sectionId, dir)
    await fs.mkdir(to, { recursive: true })
    for (const name of await fs.readdir(from)) {
      const src = path.join(from, name)
      const dst = path.join(to, name)
      const [srcStat, dstStat] = await Promise.all([fs.stat(src), fs.stat(dst).catch(() => null)])
      if (dstStat && dstStat.size === srcStat.size && dstStat.mtimeMs >= srcStat.mtimeMs) continue
      await fs.copyFile(src, dst)
      copied++
    }
  }
  return copied
}

/**
 * Ссылка на страницу инструкции → ключ «раздел/id». Без раздела — та же папка; в README
 * общего каталога ссылки идут от корня («03-operations/defect.md»).
 */
const resolveLink = (href, sectionId, keys) => {
  const target = href.match(/^(?:(?:\.\.\/)?([^/]+)\/)?([^/]+)\.md$/)
  if (!target) return null
  const [, linkedSection, linkedId] = target
  if (linkedId === 'README') return { readme: linkedSection || sectionId }
  const key = keyOf(linkedSection || sectionId, linkedId)
  return keys.has(key) ? { key } : { missing: key }
}

/** Разделы «Для администратора» / «Для разработчика» — в <details>: открытость задаёт страница по уровню читателя */
const wrapLevelSections = (html) => {
  const parts = html.split(/(?=<h2 id=")/)
  return parts.map((part) => {
    const head = part.match(/^<h2 id="([^"]+)">(.*?)<\/h2>/)
    const level = head && LEVEL_SECTIONS[head[2].replace(/<[^>]+>/g, '')]
    if (!level) return part
    const rest = part.slice(head[0].length)
    return `<details class="doc-level" data-level="${level}" id="${head[1]}"><summary><h2>${head[2]}</h2></summary>${rest}</details>`
  }).join('')
}

const convertPage = async ({ entry, keys, warnings }) => {
  const sectionId = entry.section
  const pageId = entry.id
  const sectionDir = path.join(sourceDir, sectionId)
  const md = await fs.readFile(path.join(sourceDir, entry.file), 'utf8')
  const lines = md.replace(/\r\n/g, '\n').split('\n')
  const where = `${sectionId}/${pageId}`

  const titleLine = lines.findIndex((line) => line.startsWith('# '))
  const title = stripInline(lines[titleLine]?.slice(2) || pageId)

  const meta = { where: '', rights: '' }
  const body = []
  let lead = ''
  let currentH2 = ''
  const abilities = []
  const troubles = []
  const related = []
  let video = null

  for (let i = titleLine + 1; i < lines.length; i++) {
    const line = lines[i]
    const metaMatch = line.match(/^\*\*(Где найти|Права):\*\*\s*(.+)$/)
    if (metaMatch) {
      meta[metaMatch[1] === 'Где найти' ? 'where' : 'rights'] = metaMatch[2].trim()
      continue
    }
    if (line.startsWith('## ')) currentH2 = line.slice(3).trim()
    if (line.startsWith('[← ')) continue

    if (!currentH2 && !lead && line.trim() && !line.startsWith('#')) {
      lead = line.trim()
      continue
    }
    if (ABILITY_SECTIONS.has(currentH2) && line.startsWith('- ')) abilities.push(stripInline(line.slice(2)))
    if (currentH2 === 'Если не получается' && line.startsWith('- ')) troubles.push(stripInline(line.slice(2)))
    if (currentH2 === 'Видео') {
      const src = line.match(/<video[^>]*src="([^"]+)"/)?.[1]
      if (src) {
        if (await exists(path.join(sectionDir, src))) video = { src: mediaUrl(sectionId, src), track: null }
        else warnings.push(`${where}: нет видео ${src}`)
      }
      const track = line.match(/<track[^>]*src="([^"]+)"/)?.[1]
      if (track && video) {
        if (await exists(path.join(sectionDir, track))) video.track = mediaUrl(sectionId, track)
        else warnings.push(`${where}: нет субтитров ${track}`)
      }
      continue
    }
    if (currentH2 === 'Связанные функции' || currentH2 === 'Функции в ролике') {
      const link = line.match(/\]\(([^)]+\.md)\)/)?.[1]
      if (link) {
        const resolved = resolveLink(link, sectionId, keys)
        if (resolved?.key) related.push(resolved.key)
        else warnings.push(`${where}: связанная страница ${link} не найдена`)
      }
      continue
    }
    if (OWN_BLOCKS.has(currentH2)) continue
    body.push(line)
  }

  let bodyMd = body.join('\n')

  const images = []
  for (const [whole, alt, rel] of [...bodyMd.matchAll(/!\[([^\]]*)]\((img\/[^)\s]+)\)/g)]) {
    const file = path.join(sectionDir, rel)
    if (!(await exists(file))) {
      warnings.push(`${where}: нет снимка ${rel}`)
      bodyMd = bodyMd.replace(whole, '')
      continue
    }
    const size = rel.endsWith('.webp') ? await readWebpSize(file) : null
    images.push({ src: mediaUrl(sectionId, rel), alt: stripInline(alt), ...size })
  }

  bodyMd = bodyMd.replace(/\]\(([^)\s]+)\)/g, (whole, href) => {
    if (/^(https?:|mailto:|#)/.test(href)) return whole
    if (/^(img|video)\//.test(href)) return `](${mediaUrl(sectionId, href)})`
    const resolved = resolveLink(href, sectionId, keys)
    if (!resolved) return whole
    if (resolved.readme) return `](/docs/${sectionSlug(resolved.readme)})`
    if (resolved.missing) {
      warnings.push(`${where}: ссылка на несуществующую страницу ${href}`)
      return whole
    }
    const [linkedSection, linkedId] = resolved.key.split('/')
    return `](${pageUrl(linkedSection, linkedId)})`
  })

  const imageBySrc = new Map(images.map((image) => [image.src, image]))
  const usedIds = new Set()
  const toc = []
  let html = marked.parse(bodyMd, { async: false })
    .replace(/<h2>(.*?)<\/h2>/g, (whole, text) => {
      const plain = text.replace(/<[^>]+>/g, '')
      const id = slugifyHeading(plain, usedIds)
      toc.push({ id, text: plain, level: LEVEL_SECTIONS[plain] || null })
      return `<h2 id="${id}">${text}</h2>`
    })
    .replace(/<img src="([^"]+)" alt="([^"]*)">/g, (whole, src, alt) => {
      const size = imageBySrc.get(src)
      const dims = size?.width ? ` width="${size.width}" height="${size.height}"` : ''
      return `<img src="${src}" alt="${alt}"${dims} loading="lazy" decoding="async">`
    })
    .replace(/<a href="(https?:[^"]+)"/g, '<a href="$1" target="_blank" rel="noopener noreferrer"')
    // «Что в ролике»: метка времени перематывает ролик страницы
    .replace(/<li><strong>(\d+:\d{2})<\/strong>/g, (whole, clock) =>
      `<li><button type="button" class="doc-seek" data-seek="${clockSeconds(clock)}">${clock}</button>`)
  html = wrapLevelSections(html)

  // Ссылки внутри «Где найти» и «Права» — обычный текст, разметку жирным оставляем.
  const metaHtml = (text) => marked.parseInline(escapeHtml(stripInline(text)), { async: false })

  const cover = images[1] || images[0] || null
  return {
    key: keyOf(sectionId, pageId),
    id: pageId,
    section: sectionId,
    url: pageUrl(sectionId, pageId),
    title,
    lead: stripInline(lead),
    where: meta.where ? metaHtml(meta.where) : '',
    rights: meta.rights ? metaHtml(meta.rights) : '',
    abilities,
    troubles,
    related,
    video,
    cover,
    imageCount: images.length,
    toc,
    html
  }
}

const main = async () => {
  if (!(await exists(path.join(sourceDir, 'index.json')))) {
    throw new Error(`Не найдена инструкция: ${sourceDir}. Укажите путь аргументом или MANUAL_SRC.`)
  }

  const index = JSON.parse(await fs.readFile(path.join(sourceDir, 'index.json'), 'utf8'))
  const warnings = []

  const keys = new Set()
  for (const entry of index) {
    const key = keyOf(entry.section, entry.id)
    if (keys.has(key)) throw new Error(`Повтор страницы: ${key}`)
    keys.add(key)
  }
  /** Ролик сквозного сценария → ключ его страницы */
  const journeyKey = (id) => keyOf('journeys', id)

  const sectionIds = [...new Set(index.map((entry) => entry.section))]
  const sections = []
  const pages = {}
  let copied = 0

  for (const sectionId of sectionIds) {
    const info = await readSectionInfo(sectionId)
    const sectionPages = index.filter((entry) => entry.section === sectionId)

    for (const entry of sectionPages) {
      const page = await convertPage({ entry, keys, warnings })
      page.summary = entry.summary || page.lead
      page.keywords = entry.keywords || []
      page.level = entry.level || ['user']
      page.journeys = (entry.journeys || []).map(journeyKey).filter((key) => {
        if (keys.has(key)) return true
        warnings.push(`${page.key}: нет сквозного сценария ${key}`)
        return false
      })
      page.search = [page.title, page.summary, page.lead, ...page.abilities, ...page.keywords, ...page.toc.map((item) => item.text)]
        .join(' ')
        .toLowerCase()
        .replace(/ё/g, 'е')
        .slice(0, SEARCH_TEXT_LIMIT)
      pages[page.key] = page
    }

    copied += await copyMedia(sectionId)
    const num = sectionId.match(/^(\d+)-/)?.[1] || ''
    sections.push({
      id: sectionId,
      slug: sectionSlug(sectionId),
      num,
      title: info.title,
      description: info.description,
      contents: sectionPages.slice(0, 6).map((entry) => entry.title).join(', '),
      pageIds: sectionPages.map((entry) => keyOf(sectionId, entry.id))
    })
  }

  const data = { generatedAt: new Date().toISOString(), sections, pages }
  await fs.mkdir(path.dirname(dataFile), { recursive: true })
  await fs.writeFile(dataFile, JSON.stringify(data))

  const pageCount = Object.keys(pages).length
  const stat = await fs.stat(dataFile)
  console.log(`Справка: ${sections.length} разделов, ${pageCount} страниц, ${Math.round(stat.size / 1024)} КБ; скопировано файлов: ${copied}`)
  for (const warning of warnings) console.warn(`  ! ${warning}`)
  if (warnings.length && process.env.MANUAL_STRICT !== '0') {
    console.error(`Предупреждений: ${warnings.length} — справка не должна уходить с битыми ссылками (MANUAL_STRICT=0 — пропустить)`)
    process.exit(1)
  }
}

main().catch((error) => {
  console.error(error.message)
  process.exit(1)
})
