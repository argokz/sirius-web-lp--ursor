import manualJson from '../data/manual.json'
import type { ManualCatalog, ManualData, ManualPage, ManualPageCard, ManualSearchIndex } from '~~/types/manual'

// Данные собирает scripts/sync-manual.mjs из docs/manual репозитория tgid-app.
const manual = manualJson as unknown as ManualData

const toCard = (page: ManualPage): ManualPageCard => ({
  id: page.id,
  section: page.section,
  url: page.url,
  title: page.title,
  summary: page.summary,
  cover: page.cover,
  video: page.video
})

const catalog: ManualCatalog = {
  generatedAt: manual.generatedAt,
  sections: manual.sections,
  pages: Object.fromEntries(Object.values(manual.pages).map((page) => [page.id, toCard(page)]))
}

// Сквозной порядок страниц — для кнопок «Назад / Далее».
const pageOrder = manual.sections.flatMap((section) => section.pageIds)

const searchIndex: ManualSearchIndex = Object.fromEntries(
  Object.values(manual.pages).map((page) => [page.id, page.search])
)

export const getManualCatalog = () => catalog

export const getManualSearchIndex = () => searchIndex

export const getManualSection = (slug: string) => manual.sections.find((section) => section.slug === slug)

export const getManualPage = (sectionSlug: string, pageId: string) => {
  const section = getManualSection(sectionSlug)
  const page = manual.pages[pageId]
  if (!section || !page || page.section !== section.id) return null

  const position = pageOrder.indexOf(pageId)
  const cardAt = (index: number) => {
    const id = pageOrder[index]
    return id ? catalog.pages[id] : null
  }

  return {
    section,
    page,
    related: page.related.map((id) => catalog.pages[id]).filter(Boolean),
    prev: cardAt(position - 1),
    next: cardAt(position + 1)
  }
}

export const getManualTroubles = () => manual.sections.flatMap((section) =>
  section.pageIds
    .map((id) => manual.pages[id])
    .filter((page) => page.troubles.length)
    .map((page) => ({ section: section.id, id: page.id, url: page.url, title: page.title, troubles: page.troubles }))
)
