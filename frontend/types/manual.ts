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
  /** Ключи страниц «раздел/id» по порядку */
  pageIds: string[]
}

export interface ManualVideo {
  src: string
  /** Субтитры .vtt (сквозные сценарии) */
  track: string | null
}

export type ManualLevel = 'user' | 'admin' | 'dev'

export interface ManualPage {
  /** «раздел/id»: id уникален только внутри раздела */
  key: string
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
  video: ManualVideo | null
  cover: ManualImage | null
  imageCount: number
  toc: Array<{ id: string; text: string; level: ManualLevel | null }>
  html: string
  summary: string
  keywords: string[]
  /** Для кого страница: у всех user, admin и dev — если есть разделы «Для администратора» / «Для разработчика» */
  level: ManualLevel[]
  /** Ключи сквозных сценариев, где показана функция */
  journeys: string[]
  search: string
}

export interface ManualData {
  generatedAt: string
  sections: ManualSection[]
  pages: Record<string, ManualPage>
}

/** Страница в каталоге: только то, что нужно спискам. Каталог встраивается в каждую страницу сайта. */
export type ManualPageCard = Pick<ManualPage, 'key' | 'id' | 'section' | 'url' | 'title' | 'summary' | 'cover' | 'video' | 'level'>

/** Текст для поиска по ключу страницы: заголовок, описание, возможности, ключевые слова, разделы. */
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
  journeys: ManualPageCard[]
  prev: ManualPageCard | null
  next: ManualPageCard | null
}

export interface ManualJourneys {
  featured: { key: string; title: string; summary: string; url: string; video: ManualVideo } | null
  items: ManualPageCard[]
}
