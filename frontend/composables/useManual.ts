import type { ManualCatalog, ManualPageCard, ManualPageResponse, ManualSearchIndex } from '~~/types/manual'

export const useManualCatalog = () => useFetch<ManualCatalog>('/docs-data/catalog', {
  key: 'docs-catalog'
})

export const useManualPage = (section: Ref<string>, id: Ref<string>) => useFetch<ManualPageResponse>(
  () => `/docs-data/page/${section.value}/${id.value}`,
  { key: computed(() => `docs-page-${section.value}-${id.value}`) }
)

/** Текст для поиска грузится только в браузере и только когда начали искать. */
export const useManualSearchIndex = (enabled: Ref<boolean>) => {
  const index = ref<ManualSearchIndex | null>(null)
  watch(enabled, async (on) => {
    if (!on || index.value || import.meta.server) return
    index.value = await $fetch<ManualSearchIndex>('/docs-data/search-index').catch(() => null)
  }, { immediate: true })
  return index
}

// Грубое усечение окончаний: «опрессовка» находит и «опрессовок», и «опрессовки».
const MIN_STEM_LENGTH = 5
const stem = (word: string) => (word.length > MIN_STEM_LENGTH ? word.slice(0, -2) : word)
const normalize = (text: string) => text.toLowerCase().replace(/ё/g, 'е')

/** Поиск по справке: все слова запроса должны найтись, совпадение в заголовке поднимает страницу выше. */
export const searchManual = (
  catalog: ManualCatalog | null | undefined,
  index: ManualSearchIndex | null | undefined,
  query: string
): ManualPageCard[] => {
  const words = normalize(query).split(/\s+/).filter((word) => word.length > 1).map(stem)
  if (!catalog || !words.length) return []

  return Object.values(catalog.pages)
    .map((page) => {
      const title = normalize(page.title)
      const text = index?.[page.key] || `${title} ${normalize(page.summary)}`
      if (!words.every((word) => text.includes(word) || title.includes(word))) return null
      const score = words.reduce((sum, word) => sum + (title.includes(word) ? 3 : 0), 0)
      return { page, score }
    })
    .filter((hit): hit is NonNullable<typeof hit> => Boolean(hit))
    .sort((a, b) => b.score - a.score)
    .map((hit) => hit.page)
}
