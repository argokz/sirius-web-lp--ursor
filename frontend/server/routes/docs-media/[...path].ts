import { createReadStream, promises as fs } from 'node:fs'
import { resolve, sep } from 'node:path'

// Ролики и субтитры справки. Встроенная раздача public/ в Nitro не понимает Range — браузер не может
// перематывать ролик, пока он не скачан, и метки времени «Что в ролике» не работают. Поэтому ролики лежат
// вне public/ — в manual-media/ рядом с .output (туда их кладёт scripts/sync-manual.mjs) — и отдаются здесь.
const MEDIA_FILE = /^[\w-]+\/video\/[\w-]+\.(mp4|webm|vtt)$/
const CONTENT_TYPES: Record<string, string> = { mp4: 'video/mp4', webm: 'video/webm', vtt: 'text/vtt; charset=utf-8' }
const CACHE = 'public, max-age=604800'

/** Папка роликов: NUXT_MANUAL_MEDIA_DIR или manual-media в рабочей папке сервера (frontend/) */
const mediaDir = () => resolve(String(useRuntimeConfig().manualMediaDir || 'manual-media'))

const parseRange = (header: string, size: number): { start: number; end: number } | null => {
  const match = header.match(/^bytes=(\d*)-(\d*)$/)
  if (!match || (!match[1] && !match[2])) return null
  const start = match[1] ? Number(match[1]) : Math.max(0, size - Number(match[2]))
  const end = match[1] && match[2] ? Math.min(Number(match[2]), size - 1) : size - 1
  return start <= end ? { start, end } : null
}

export default defineEventHandler(async (event) => {
  // HEAD тоже: его шлют прокси и проверки ссылок
  assertMethod(event, ['GET', 'HEAD'])
  const head = event.method === 'HEAD'
  const rel = getRouterParam(event, 'path') || ''
  const kind = rel.match(MEDIA_FILE)?.[1]
  if (!kind) throw createError({ statusCode: 404, statusMessage: 'Файл справки не найден' })

  const root = mediaDir()
  const file = resolve(root, rel)
  const stat = file.startsWith(root + sep) ? await fs.stat(file).catch(() => null) : null
  if (!stat?.isFile()) throw createError({ statusCode: 404, statusMessage: 'Файл справки не найден' })

  setResponseHeaders(event, { 'Content-Type': CONTENT_TYPES[kind], 'Accept-Ranges': 'bytes', 'Cache-Control': CACHE })
  const rangeHeader = getRequestHeader(event, 'range')
  if (!rangeHeader) {
    setResponseHeader(event, 'Content-Length', stat.size)
    return head ? send(event) : sendStream(event, createReadStream(file))
  }

  const range = parseRange(rangeHeader, stat.size)
  if (!range) {
    setResponseStatus(event, 416)
    setResponseHeader(event, 'Content-Range', `bytes */${stat.size}`)
    return ''
  }
  setResponseStatus(event, 206)
  setResponseHeaders(event, {
    'Content-Length': String(range.end - range.start + 1),
    'Content-Range': `bytes ${range.start}-${range.end}/${stat.size}`
  })
  return head ? send(event) : sendStream(event, createReadStream(file, { start: range.start, end: range.end }))
})
