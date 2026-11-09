// Переносит инструкцию веб-ТГИД (docs/manual репозитория tgid-app) в справку сайта:
// тексты — в server/data/manual.json, снимки и видео — в public/manual/<раздел>/.
// Запуск: npm run manual:sync [-- <путь к docs/manual>] или MANUAL_SRC=<путь> npm run manual:sync
import { promises as fs } from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { marked } from 'marked'

const here = path.dirname(fileURLToPath(import.meta.url))
const frontendDir = path.resolve(here, '..')
const sourceDir = path.resolve(
  process.argv[2] || process.env.MANUAL_SRC || path.join(frontendDir, '../../tgid-app/web-itwin-v4/docs/manual')
)
const publicDir = path.join(frontendDir, 'public/manual')
const dataFile = path.join(frontendDir, 'server/data/manual.json')

const MEDIA_DIRS = ['img', 'video']
const SEARCH_TEXT_LIMIT = 600

const sectionSlug = (sectionId) => sectionId.replace(/^\d+-/, '')
const pageUrl = (sectionId, pageId) => `/docs/${sectionSlug(sectionId)}/${pageId}`
const mediaUrl = (sectionId, rel) => `/manual/${sectionId}/${rel}`

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

// Таблица «| [Функция](file.md) | Коротко |» из README раздела.
const parseSummaryTable = (md) => {
  const summaries = new Map()
  for (const line of md.split('\n')) {
    const match = line.match(/^\|\s*\[([^\]]+)]\(([^)]+)\.md\)\s*\|\s*(.+?)\s*\|\s*$/)
    if (match) summaries.set(path.basename(match[2]), stripInline(match[3]))
  }
  return summaries
}

const parseRootSections = (md) => {
  const rows = []
  for (const line of md.split('\n')) {
    const match = line.match(/^\|\s*(\d+)\s*\|\s*\[([^\]]+)]\(([^/]+)\/README\.md\)\s*\|\s*(.+?)\s*\|\s*$/)
    if (match) rows.push({ id: match[3], title: stripInline(match[2]), contents: stripInline(match[4]) })
  }
  return rows
}

const copyMedia = async (sectionId) => {
  let copied = 0
  for (const dir of MEDIA_DIRS) {
    const from = path.join(sourceDir, sectionId, dir)
    if (!(await exists(from))) continue
    const to = path.join(publicDir, sectionId, dir)
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

const convertPage = async ({ sectionId, pageId, md, idToSection, warnings }) => {
  const sectionDir = path.join(sourceDir, sectionId)
  const lines = md.replace(/\r\n/g, '\n').split('\n')

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

    if (!currentH2 && !lead && line.trim() && !line.startsWith('#')) {
      lead = line.trim()
      continue
    }
    if (currentH2 === 'Что умеет' && line.startsWith('- ')) abilities.push(stripInline(line.slice(2)))
    if (currentH2 === 'Если не получается' && line.startsWith('- ')) troubles.push(stripInline(line.slice(2)))
    if (currentH2 === 'Видео') {
      const src = line.match(/<video[^>]*src="([^"]+)"/)?.[1]
      if (src && (await exists(path.join(sectionDir, src)))) video = mediaUrl(sectionId, src)
      continue
    }
    if (currentH2 === 'Связанные функции') {
      const link = line.match(/\]\(([^)]+)\.md\)/)?.[1]
      if (link) {
        const relId = path.basename(link)
        if (idToSection.has(relId)) related.push(relId)
        else warnings.push(`${sectionId}/${pageId}: связанная страница ${link} не найдена`)
      }
      continue
    }
    body.push(line)
  }

  // «Видео» и «Связанные функции» страница показывает отдельными блоками, в тело они не попадают.
  let bodyMd = body.join('\n')

  const images = []
  const imageRefs = [...bodyMd.matchAll(/!\[([^\]]*)]\((img\/[^)\s]+)\)/g)]
  for (const [whole, alt, rel] of imageRefs) {
    const file = path.join(sectionDir, rel)
    if (!(await exists(file))) {
      warnings.push(`${sectionId}/${pageId}: нет снимка ${rel}`)
      bodyMd = bodyMd.replace(whole, '')
      continue
    }
    const size = rel.endsWith('.webp') ? await readWebpSize(file) : null
    images.push({ src: mediaUrl(sectionId, rel), alt: stripInline(alt), ...size })
  }

  bodyMd = bodyMd.replace(/\]\(([^)\s]+)\)/g, (whole, href) => {
    if (/^(https?:|mailto:|#)/.test(href)) return whole
    if (/^(img|video)\//.test(href)) return `](${mediaUrl(sectionId, href)})`
    const target = href.match(/(?:\.\.\/([^/]+)\/)?([^/]+)\.md$/)
    if (!target) return whole
    const [, linkedSection, linkedId] = target
    if (linkedId === 'README') return `](/docs${linkedSection ? `/${sectionSlug(linkedSection)}` : ''})`
    const resolvedSection = linkedSection || idToSection.get(linkedId) || sectionId
    return `](${pageUrl(resolvedSection, linkedId)})`
  })

  const imageBySrc = new Map(images.map((image) => [image.src, image]))
  const usedIds = new Set()
  const toc = []
  let html = marked.parse(bodyMd, { async: false })
    .replace(/<h2>(.*?)<\/h2>/g, (whole, text) => {
      const plain = text.replace(/<[^>]+>/g, '')
      const id = slugifyHeading(plain, usedIds)
      toc.push({ id, text: plain })
      return `<h2 id="${id}">${text}</h2>`
    })
    .replace(/<img src="([^"]+)" alt="([^"]*)">/g, (whole, src, alt) => {
      const size = imageBySrc.get(src)
      const dims = size?.width ? ` width="${size.width}" height="${size.height}"` : ''
      return `<img src="${src}" alt="${alt}"${dims} loading="lazy" decoding="async">`
    })
    .replace(/<a href="(https?:[^"]+)"/g, '<a href="$1" target="_blank" rel="noopener noreferrer"')

  // Ссылки внутри «Где найти» и «Права» — обычный текст, разметку жирным оставляем.
  const metaHtml = (text) => marked.parseInline(escapeHtml(stripInline(text)), { async: false })

  const cover = images[1] || images[0] || null
  return {
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
  if (!(await exists(path.join(sourceDir, 'README.md')))) {
    throw new Error(`Не найдена инструкция: ${sourceDir}. Укажите путь аргументом или MANUAL_SRC.`)
  }

  const rootMd = await fs.readFile(path.join(sourceDir, 'README.md'), 'utf8')
  const index = JSON.parse(await fs.readFile(path.join(sourceDir, 'index.json'), 'utf8'))
  const rootSections = parseRootSections(rootMd)
  const warnings = []

  const idToSection = new Map()
  for (const entry of index) {
    if (idToSection.has(entry.id)) throw new Error(`Повтор id страницы: ${entry.id}`)
    idToSection.set(entry.id, entry.section)
  }

  const sections = []
  const pages = {}
  let copied = 0

  for (const root of rootSections) {
    const readme = await fs.readFile(path.join(sourceDir, root.id, 'README.md'), 'utf8')
    const description = stripInline(readme.split('\n').find((line, i, all) => i > 0 && line.trim() && !line.startsWith('#') && !line.startsWith('|')) || '')
    const summaries = parseSummaryTable(readme)
    const order = [...summaries.keys()]
    const sectionPages = index
      .filter((entry) => entry.section === root.id)
      .sort((a, b) => {
        const ia = order.indexOf(a.id)
        const ib = order.indexOf(b.id)
        return (ia === -1 ? 999 : ia) - (ib === -1 ? 999 : ib)
      })

    for (const entry of sectionPages) {
      const md = await fs.readFile(path.join(sourceDir, entry.file), 'utf8')
      const page = await convertPage({ sectionId: root.id, pageId: entry.id, md, idToSection, warnings })
      page.summary = summaries.get(entry.id) || page.lead
      page.keywords = entry.keywords || []
      page.search = [page.title, page.summary, page.lead, ...page.abilities, ...page.keywords]
        .join(' ')
        .toLowerCase()
        .replace(/ё/g, 'е')
        .slice(0, SEARCH_TEXT_LIMIT)
      pages[entry.id] = page
    }

    copied += await copyMedia(root.id)
    sections.push({
      id: root.id,
      slug: sectionSlug(root.id),
      num: root.id.slice(0, 2),
      title: root.title,
      description,
      contents: root.contents,
      pageIds: sectionPages.map((entry) => entry.id)
    })
  }

  const data = { generatedAt: new Date().toISOString(), sections, pages }
  await fs.mkdir(path.dirname(dataFile), { recursive: true })
  await fs.writeFile(dataFile, JSON.stringify(data))

  const pageCount = Object.keys(pages).length
  const stat = await fs.stat(dataFile)
  console.log(`Справка: ${sections.length} разделов, ${pageCount} страниц, ${Math.round(stat.size / 1024)} КБ; скопировано файлов: ${copied}`)
  for (const warning of warnings) console.warn(`  ! ${warning}`)
}

main().catch((error) => {
  console.error(error.message)
  process.exit(1)
})
