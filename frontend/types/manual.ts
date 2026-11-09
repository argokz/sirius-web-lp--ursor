export interface ManualImage {
  src: string
  alt: string
  width?: number
  height?: number
}

export interface ManualSection {
  id: string
  slug: string
  num: string
  title: string
  description: string
  contents: string
  pageIds: string[]
}

export interface ManualPage {
  id: string
  section: string
  url: string
  title: string
  lead: string
  where: string
  rights: string
  abilities: string[]
  troubles: string[]
  related: string[]
  video: string | null
  cover: ManualImage | null
  imageCount: number
  toc: Array<{ id: string; text: string }>
  html: string
  summary: string
  keywords: string[]
  search: string
}

export interface ManualData {
  generatedAt: string
  sections: ManualSection[]
  pages: Record<string, ManualPage>
}

/** Страница в каталоге: только то, что нужно спискам. Каталог встраивается в каждую страницу сайта. */
export type ManualPageCard = Pick<ManualPage, 'id' | 'section' | 'url' | 'title' | 'summary' | 'cover' | 'video'>

/** Текст для поиска по id страницы: заголовок, описание, «Что умеет», ключевые слова. */
export type ManualSearchIndex = Record<string, string>

export interface ManualCatalog {
  generatedAt: string
  sections: ManualSection[]
  pages: Record<string, ManualPageCard>
}

export interface ManualPageResponse {
  section: ManualSection
  page: ManualPage
  related: ManualPageCard[]
  prev: ManualPageCard | null
  next: ManualPageCard | null
}
