import manualJson from '../data/manual.json'
import type { ManualCatalog, ManualData, ManualPage, ManualPageCard, ManualSearchIndex } from '~~/types/manual'

// Данные собирает scripts/sync-manual.mjs из docs/manual репозитория tgid-app.
const manual = manualJson as unknown as ManualData

const toCard = (page: ManualPage): ManualPageCard => ({
  key: page.key,
  id: page.id,
  section: page.section,
  url: page.url,
  title: page.title,
  summary: page.summary,
  cover: page.cover,
  video: page.video,
  level: page.level
})

const catalog: ManualCatalog = {
  generatedAt: manual.generatedAt,
  sections: manual.sections,
  pages: Object.fromEntries(Object.values(manual.pages).map((page) => [page.key, toCard(page)]))
}

// Сквозной порядок страниц — для кнопок «Назад / Далее».
const pageOrder = manual.sections.flatMap((section) => section.pageIds)

const searchIndex: ManualSearchIndex = Object.fromEntries(
  Object.values(manual.pages).map((page) => [page.key, page.search])
)

export const getManualCatalog = () => catalog

export const getManualSearchIndex = () => searchIndex

export const getManualSection = (slug: string) => manual.sections.find((section) => section.slug === slug)

export const getManualPage = (sectionSlug: string, pageId: string) => {
  const section = getManualSection(sectionSlug)
  if (!section) return null
  const key = `${section.id}/${pageId}`
  const page = manual.pages[key]
  if (!page) return null

  const position = pageOrder.indexOf(key)
  const cardAt = (index: number) => {
    const at = pageOrder[index]
    return at ? catalog.pages[at] : null
  }
  const cards = (keys: string[]) => keys.map((item) => catalog.pages[item]).filter((card): card is ManualPageCard => Boolean(card))

  return {
    section,
    page,
    related: cards(page.related),
    journeys: cards(page.journeys),
    prev: cardAt(position - 1),
    next: cardAt(position + 1)
  }
}

export const getManualTroubles = () => manual.sections.flatMap((section) =>
  section.pageIds
    .map((key) => manual.pages[key])
    .filter((page): page is ManualPage => Boolean(page?.troubles.length))
    .map((page) => ({ section: section.id, id: page.key, url: page.url, title: page.title, troubles: page.troubles }))
)
