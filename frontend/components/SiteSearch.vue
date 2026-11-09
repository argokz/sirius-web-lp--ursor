<template>
  <Teleport to="body">
    <Transition name="palette">
      <div v-if="open" class="palette-backdrop" @click.self="close">
        <div class="palette" role="dialog" aria-modal="true" aria-label="Поиск по сайту, справке и курсу">
          <label class="palette-input">
            <UIcon name="i-lucide-search" />
            <input
              ref="inputEl"
              v-model="query"
              type="search"
              placeholder="Расчёт, отключение, опрессовка, API…"
              autocomplete="off"
              spellcheck="false"
              @keydown.down.prevent="move(1)"
              @keydown.up.prevent="move(-1)"
              @keydown.enter.prevent="go(flat[active])"
              @keydown.esc.prevent="close"
            >
            <kbd>Esc</kbd>
          </label>

          <div ref="listEl" class="palette-body">
            <p v-if="loading" class="palette-note">Загружаю справку и курс…</p>

            <template v-for="group in groups" :key="group.title">
              <p class="palette-group">{{ group.title }} <span>{{ group.items.length }}</span></p>
              <button
                v-for="item in group.items"
                :key="item.url"
                type="button"
                class="palette-item"
                :class="{ active: flat[active]?.url === item.url }"
                :data-url="item.url"
                @mouseenter="active = flat.indexOf(item)"
                @click="go(item)"
              >
                <UIcon :name="item.icon" class="palette-icon" />
                <span class="palette-text">
                  <strong>{{ item.title }}</strong>
                  <small v-if="item.hint">{{ item.hint }}</small>
                </span>
                <span class="palette-kind">{{ item.kind }}</span>
              </button>
            </template>

            <div v-if="!loading && query.trim() && !flat.length" class="palette-empty">
              <p>По запросу «{{ query }}» ничего не нашлось.</p>
              <NuxtLink to="/docs/troubleshooting" @click="close">Частые неполадки</NuxtLink>
              ·
              <NuxtLink to="/contacts" @click="close">Спросить у нас</NuxtLink>
            </div>
          </div>

          <footer class="palette-foot">
            <span><kbd>↑</kbd><kbd>↓</kbd> выбрать</span>
            <span><kbd>Enter</kbd> открыть</span>
            <span class="palette-foot-right">{{ countsText }}</span>
          </footer>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
/**
 * Поиск по всему сайту (Ctrl K / ⌘K или «/»): страницы витрины, справка и уроки курса.
 * Справка и курс грузятся только при первом открытии — в HTML страниц они не попадают.
 */
import type { ManualCatalog, ManualSearchIndex } from '~~/types/manual'
import type { CourseCatalog } from '~~/types/course'

interface PaletteItem {
  title: string
  hint?: string
  url: string
  icon: string
  kind: string
  text: string
}

const MAX_PER_GROUP = 7
const MIN_STEM_LENGTH = 5

const SITE_PAGES: PaletteItem[] = [
  { title: 'Продукт ТГИД-07', url: '/product', icon: 'i-lucide-box', hint: 'Из чего состоит платформа', text: 'продукт платформа модули состав' },
  { title: 'Все возможности', url: '/features', icon: 'i-lucide-layout-grid', hint: 'Витрина функций по разделам', text: 'возможности функции витрина модули' },
  { title: 'Теплогидравлическое моделирование', url: '/modeling', icon: 'i-lucide-chart-no-axes-combined', hint: 'Расчёт режимов, наладка, пьезометр', text: 'моделирование расчет режим наладка пьезометр гидравлика heatnet' },
  { title: 'ГИС и карта сети', url: '/gis', icon: 'i-lucide-map', hint: 'Схема, слои, паспорта объектов', text: 'гис карта слои паспорт объекты схема' },
  { title: 'Эксплуатация и ТОиР', url: '/maintenance', icon: 'i-lucide-wrench', hint: 'Дефекты, наряды, опрессовки, отключения', text: 'эксплуатация тоир дефекты наряды опрессовка отключения ремонт' },
  { title: 'Решения', url: '/solutions', icon: 'i-lucide-network', hint: 'Для теплосетей, водоканалов, городов', text: 'решения теплосеть водоканал город' },
  { title: 'Веб-версия', url: '/web-version', icon: 'i-lucide-globe', hint: 'Работа в браузере и в поле', text: 'веб браузер web полевое приложение' },
  { title: 'Справка', url: '/docs', icon: 'i-lucide-book-open', hint: 'Инструкция веб-ТГИД по разделам', text: 'справка документация инструкция' },
  { title: 'Частые неполадки', url: '/docs/troubleshooting', icon: 'i-lucide-life-buoy', hint: 'Что делать, если не работает', text: 'неполадки ошибка не работает проблемы' },
  { title: 'Обучение', url: '/learn', icon: 'i-lucide-graduation-cap', hint: 'Курс: треки, уроки, тесты', text: 'обучение курс уроки тест экзамен' },
  { title: 'Запросить демо', url: '/demo', icon: 'i-lucide-play', hint: 'Покажем на ваших данных', text: 'демо демонстрация пилот заявка' },
  { title: 'Контакты', url: '/contacts', icon: 'i-lucide-mail', hint: 'Телефон, почта, адрес', text: 'контакты телефон почта адрес связаться' },
  { title: 'О компании', url: '/about', icon: 'i-lucide-building-2', hint: 'ПКФ «Сириус»', text: 'компания сириус о нас история' }
].map((item) => ({ ...item, kind: 'Сайт' }))

const SUGGESTED = ['/docs', '/learn', '/modeling', '/maintenance', '/demo']

const open = useState('site-search-open', () => false)
const query = ref('')
const active = ref(0)
const loading = ref(false)
const inputEl = ref<HTMLInputElement | null>(null)
const listEl = ref<HTMLElement | null>(null)

const manual = shallowRef<ManualCatalog | null>(null)
const manualIndex = shallowRef<ManualSearchIndex | null>(null)
const course = shallowRef<CourseCatalog | null>(null)

const normalize = (text: string) => text.toLowerCase().replace(/ё/g, 'е')
const stem = (word: string) => (word.length > MIN_STEM_LENGTH ? word.slice(0, -2) : word)
const queryWords = computed(() => normalize(query.value).split(/\s+/).filter((word) => word.length > 1).map(stem))

const loadData = async () => {
  if (manual.value || loading.value) return
  loading.value = true
  const [catalog, index, courseCatalog] = await Promise.all([
    $fetch<ManualCatalog>('/docs-data/catalog').catch(() => null),
    $fetch<ManualSearchIndex>('/docs-data/search-index').catch(() => null),
    $fetch<CourseCatalog>('/docs-data/course/catalog').catch(() => null)
  ])
  manual.value = catalog
  manualIndex.value = index
  course.value = courseCatalog
  loading.value = false
}

/** Все слова запроса нашлись; совпадение в заголовке ценится втрое. */
const rank = (items: PaletteItem[]) => {
  const words = queryWords.value
  return items
    .map((item) => {
      const title = normalize(item.title)
      const haystack = `${title} ${item.text}`
      if (!words.every((word) => haystack.includes(word))) return null
      return { item, score: words.reduce((sum, word) => sum + (title.includes(word) ? 3 : 1), 0) }
    })
    .filter((hit): hit is NonNullable<typeof hit> => Boolean(hit))
    .sort((a, b) => b.score - a.score)
    .map((hit) => hit.item)
}

const manualItems = computed<PaletteItem[]>(() => {
  const catalog = manual.value
  if (!catalog) return []
  const sectionTitle = new Map(catalog.sections.map((section) => [section.id, `${section.num} ${section.title}`]))
  return Object.values(catalog.pages).map((page) => ({
    title: page.title,
    hint: sectionTitle.get(page.section) || page.summary,
    url: page.url,
    icon: page.video ? 'i-lucide-circle-play' : 'i-lucide-file-text',
    kind: 'Справка',
    text: manualIndex.value?.[page.key] || normalize(`${page.title} ${page.summary}`)
  }))
})

const courseItems = computed<PaletteItem[]>(() => {
  const catalog = course.value
  if (!catalog) return []
  const tracks = catalog.tracks.map((track) => ({
    title: `Трек «${track.title}»`,
    hint: `${track.lessons.length} уроков · ${Math.round(track.minutes / 60)} ч · итоговый тест`,
    url: `/learn/${track.id}`,
    icon: 'i-lucide-route',
    kind: 'Курс',
    text: normalize(`${track.title} ${track.summary} трек курс`)
  }))
  const lessons = Object.values(catalog.lessons).map((lesson) => ({
    title: lesson.title,
    hint: `${lesson.kind === 'practice' ? 'Практика' : 'Урок'} · ${lesson.minutes} мин`,
    url: lesson.url,
    icon: lesson.kind === 'practice' ? 'i-lucide-flask-conical' : 'i-lucide-graduation-cap',
    kind: 'Курс',
    text: normalize(`${lesson.title} ${lesson.summary}`)
  }))
  return [...tracks, ...lessons]
})

const groups = computed(() => {
  if (!queryWords.value.length) {
    return [{ title: 'Куда пойти', items: SUGGESTED.map((url) => SITE_PAGES.find((page) => page.url === url)!).filter(Boolean) }]
  }
  return [
    { title: 'Справка', items: rank(manualItems.value).slice(0, MAX_PER_GROUP) },
    { title: 'Курс', items: rank(courseItems.value).slice(0, MAX_PER_GROUP) },
    { title: 'Сайт', items: rank(SITE_PAGES).slice(0, MAX_PER_GROUP) }
  ].filter((group) => group.items.length)
})

const flat = computed(() => groups.value.flatMap((group) => group.items))

const countsText = computed(() => {
  if (!manual.value) return 'Справка · Курс · Сайт'
  const pages = Object.keys(manual.value.pages).length
  const lessons = course.value ? Object.keys(course.value.lessons).length : 0
  return `${pages} страниц справки · ${lessons} уроков`
})

watch(query, () => { active.value = 0 })

const move = (step: number) => {
  if (!flat.value.length) return
  active.value = (active.value + step + flat.value.length) % flat.value.length
  nextTick(() => {
    const url = flat.value[active.value]?.url
    listEl.value?.querySelector(`[data-url="${CSS.escape(url || '')}"]`)?.scrollIntoView({ block: 'nearest' })
  })
}

const close = () => { open.value = false }

const go = (item?: PaletteItem) => {
  if (!item) return
  close()
  navigateTo(item.url)
}

watch(open, (value) => {
  if (!value) return
  loadData()
  nextTick(() => inputEl.value?.focus())
})

const isTyping = (target: EventTarget | null) => {
  const el = target as HTMLElement | null
  return Boolean(el && (el.isContentEditable || ['INPUT', 'TEXTAREA', 'SELECT'].includes(el.tagName)))
}

const onKey = (event: KeyboardEvent) => {
  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') {
    event.preventDefault()
    open.value = !open.value
    return
  }
  if (event.key === '/' && !open.value && !isTyping(event.target)) {
    event.preventDefault()
    open.value = true
  }
}

const route = useRoute()
watch(() => route.fullPath, close)

onMounted(() => window.addEventListener('keydown', onKey))
onBeforeUnmount(() => window.removeEventListener('keydown', onKey))
</script>

<style scoped>
.palette-backdrop {
  position: fixed;
  inset: 0;
  z-index: 80;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 12vh 16px 16px;
  background: rgba(28, 27, 24, 0.42);
  backdrop-filter: blur(3px);
}

.palette {
  width: min(680px, 100%);
  max-height: 72vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border: 1px solid var(--line-strong);
  border-radius: 10px;
  background: var(--surface);
  box-shadow: 0 30px 80px -20px rgba(28, 27, 24, 0.45);
}

.palette-input {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 18px;
  border-bottom: 1px solid var(--line);
  color: var(--muted);
}

.palette-input svg {
  width: 20px;
  height: 20px;
  flex: 0 0 auto;
}

.palette-input input {
  flex: 1;
  min-width: 0;
  border: 0;
  outline: 0;
  color: var(--ink);
  background: transparent;
  font-size: 1.05rem;
}

.palette-input input::-webkit-search-cancel-button {
  display: none;
}

kbd {
  display: inline-grid;
  place-items: center;
  min-width: 22px;
  height: 22px;
  padding: 0 6px;
  border: 1px solid var(--line-strong);
  border-bottom-width: 2px;
  border-radius: 4px;
  color: var(--muted);
  background: var(--paper);
  font-family: var(--mono);
  font-size: 0.68rem;
}

.palette-body {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
  overscroll-behavior: contain;
}

.palette-group {
  margin: 10px 10px 6px;
  color: var(--accent);
  font-family: var(--mono);
  font-size: 0.68rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.palette-group span {
  color: var(--muted);
}

.palette-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 12px;
  border: 0;
  border-radius: 6px;
  color: var(--ink-2);
  background: transparent;
  text-align: left;
  cursor: pointer;
}

.palette-item.active {
  color: var(--ink);
  background: var(--paper-2);
  box-shadow: inset 2px 0 0 var(--sirius-red);
}

.palette-icon {
  width: 18px;
  height: 18px;
  flex: 0 0 auto;
  color: var(--muted);
}

.palette-text {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.palette-text strong {
  overflow: hidden;
  font-weight: 500;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.palette-text small {
  overflow: hidden;
  color: var(--muted);
  font-size: 0.8rem;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.palette-kind {
  color: var(--muted);
  font-family: var(--mono);
  font-size: 0.66rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.palette-note,
.palette-empty {
  margin: 14px 12px;
  color: var(--muted);
  font-size: 0.92rem;
}

.palette-empty a {
  color: var(--ink);
  text-decoration: underline;
  text-underline-offset: 3px;
}

.palette-foot {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 10px 16px;
  border-top: 1px solid var(--line);
  color: var(--muted);
  background: var(--paper);
  font-size: 0.76rem;
}

.palette-foot span {
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.palette-foot-right {
  margin-left: auto;
  font-family: var(--mono);
  font-size: 0.68rem;
}

.palette-enter-active,
.palette-leave-active {
  transition: opacity 0.18s ease;
}

.palette-enter-active .palette,
.palette-leave-active .palette {
  transition: transform 0.22s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.palette-enter-from,
.palette-leave-to {
  opacity: 0;
}

.palette-enter-from .palette,
.palette-leave-to .palette {
  transform: translateY(-10px) scale(0.98);
}

@media (max-width: 640px) {
  .palette-backdrop {
    padding-top: 72px;
  }

  .palette-foot span:not(.palette-foot-right) {
    display: none;
  }
}
</style>
