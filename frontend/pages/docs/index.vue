<template>
  <div class="page docs-home">
    <section class="docs-hero">
      <div class="container">
        <UBadge color="primary" variant="subtle" size="lg">Документация и справка</UBadge>
        <h1 class="display-title">Справка по веб-ТГИД</h1>
        <p class="lead">
          Одна страница — одна функция: зачем она, где её найти, какие нужны права, шаги со снимками экрана,
          короткое видео и что делать, если не получается.
        </p>

        <form class="docs-search" role="search" @submit.prevent>
          <UIcon name="i-lucide-search" class="docs-search-icon" />
          <input
            v-model="query"
            type="search"
            placeholder="Например: локализация аварии, опрессовка, импорт SHP"
            aria-label="Поиск по справке"
            autocomplete="off"
          >
          <button v-if="query" type="button" class="docs-search-clear" aria-label="Очистить поиск" @click="query = ''">
            <UIcon name="i-lucide-x" />
          </button>
        </form>

        <div class="docs-stats">
          <span><strong>{{ pageCount }}</strong> инструкций</span>
          <span><strong>{{ sections.length }}</strong> разделов</span>
          <span><strong>{{ videoCount }}</strong> видео</span>
          <span><strong>{{ troubleCount }}</strong> ответов «если не получается»</span>
        </div>
      </div>
    </section>

    <section v-if="query.trim()" class="section-tight">
      <div class="container">
        <h2 class="results-title">
          {{ results.length ? `Найдено: ${results.length}` : 'Ничего не нашлось' }}
        </h2>
        <p v-if="!results.length" class="results-empty">
          Попробуйте другое слово или откройте раздел ниже. Если ответа нет —
          <NuxtLink to="/contacts">напишите нам</NuxtLink>.
        </p>
        <div class="results">
          <NuxtLink v-for="page in results" :key="page.id" :to="page.url" class="result card">
            <span class="result-section">{{ sectionTitle(page.section) }}</span>
            <strong>{{ page.title }}</strong>
            <span>{{ page.summary }}</span>
          </NuxtLink>
        </div>
      </div>
    </section>

    <template v-else>
      <section class="section-tight">
        <div class="container">
          <span class="eyebrow">С чего начать</span>
          <h2 class="section-title">Первые шаги в системе</h2>
          <div class="start-grid">
            <NuxtLink v-for="page in startPages" :key="page.id" :to="page.url" class="start-card card">
              <img v-if="page.cover" :src="page.cover.src" :alt="page.cover.alt" :width="page.cover.width" :height="page.cover.height" loading="lazy" decoding="async">
              <div>
                <strong>{{ page.title }}</strong>
                <span>{{ page.summary }}</span>
              </div>
            </NuxtLink>
          </div>
        </div>
      </section>

      <section class="section-tight">
        <div class="container">
          <span class="eyebrow">Разделы</span>
          <h2 class="section-title">Все функции по разделам</h2>
          <div class="section-grid">
            <article v-for="section in sections" :key="section.id" class="section-card card card-pad">
              <NuxtLink :to="`/docs/${section.slug}`" class="section-card-head">
                <div class="icon-box">
                  <UIcon :name="productModuleBySection[section.id]?.icon || 'i-lucide-folder'" />
                </div>
                <div>
                  <h3>{{ section.title }}</h3>
                  <small>{{ section.pageIds.length }} {{ plural(section.pageIds.length) }}</small>
                </div>
              </NuxtLink>
              <p>{{ section.description }}</p>
              <ul>
                <li v-for="id in section.pageIds.slice(0, 4)" :key="id">
                  <NuxtLink :to="pages[id].url">{{ pages[id].title }}</NuxtLink>
                </li>
              </ul>
              <NuxtLink v-if="section.pageIds.length > 4" :to="`/docs/${section.slug}`" class="more-link">
                Ещё {{ section.pageIds.length - 4 }}
                <UIcon name="i-lucide-arrow-right" />
              </NuxtLink>
            </article>
          </div>
        </div>
      </section>

      <section class="section-tight">
        <div class="container">
          <div class="help-band content-band">
            <div>
              <span class="eyebrow">Поддержка</span>
              <h2 class="section-title">Не получается выполнить действие?</h2>
              <p class="lead">
                Частые сообщения об ошибках собраны на одной странице. Если ответа там нет — опишите задачу,
                и инженеры «Сириуса» помогут.
              </p>
            </div>
            <div class="help-actions">
              <UButton to="/docs/troubleshooting" color="primary" size="xl" icon="i-lucide-life-buoy">
                Если не получается
              </UButton>
              <UButton to="/contacts" color="neutral" variant="outline" size="xl" icon="i-lucide-mail">
                Написать в поддержку
              </UButton>
            </div>
          </div>
        </div>
      </section>
    </template>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const router = useRouter()
const { data: catalog } = await useManualCatalog()

const query = ref(typeof route.query.q === 'string' ? route.query.q : '')
watch(query, (value) => {
  router.replace({ query: value.trim() ? { q: value } : {} })
})
watch(() => route.query.q, (value) => {
  const next = typeof value === 'string' ? value : ''
  if (next !== query.value) query.value = next
})

const sections = computed(() => catalog.value?.sections || [])
const pages = computed(() => catalog.value?.pages || {})
const pageCount = computed(() => Object.keys(pages.value).length)
const videoCount = computed(() => Object.values(pages.value).filter((page) => page.video).length)
const searchIndex = useManualSearchIndex(computed(() => Boolean(query.value.trim())))
const results = computed(() => searchManual(catalog.value, searchIndex.value, query.value))
const startPages = computed(() => (sections.value[0]?.pageIds || []).map((id) => pages.value[id]))
const sectionTitle = (id: string) => sections.value.find((section) => section.id === id)?.title || ''

const { data: troubles } = await useFetch('/docs-data/troubles', { key: 'docs-troubles' })
const troubleCount = computed(() => (troubles.value || []).reduce((sum, item) => sum + item.troubles.length, 0))

const plural = (n: number) => {
  const mod10 = n % 10
  const mod100 = n % 100
  if (mod10 === 1 && mod100 !== 11) return 'функция'
  if (mod10 >= 2 && mod10 <= 4 && (mod100 < 12 || mod100 > 14)) return 'функции'
  return 'функций'
}

useSEO({
  title: 'Документация и справка ТГИД — ПКФ «Сириус»',
  description: 'Инструкция пользователя веб-ТГИД: карта сети, эксплуатация, расчёты, реестры, полевое приложение и функции ИИ — пошагово со снимками экрана и видео.'
})
</script>

<style scoped>
.docs-hero {
  padding: 136px 0 56px;
  border-bottom: 1px solid var(--line);
}

.docs-search {
  position: relative;
  display: flex;
  align-items: center;
  max-width: 760px;
  margin-top: 32px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--surface);
}

.docs-search:focus-within {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(28, 27, 24, 0.12);
}

.docs-search-icon {
  position: absolute;
  left: 18px;
  color: var(--muted);
  font-size: 1.2rem;
}

.docs-search input {
  width: 100%;
  min-height: 58px;
  padding: 0 52px;
  border: 0;
  border-radius: var(--radius);
  outline: none;
  background: transparent;
  color: var(--ink);
  font-size: 1.05rem;
}

.docs-search input::-webkit-search-cancel-button {
  display: none;
}

.docs-search-clear {
  position: absolute;
  right: 10px;
  display: grid;
  width: 38px;
  height: 38px;
  place-items: center;
  border: 0;
  border-radius: 8px;
  background: transparent;
  color: var(--muted);
  cursor: pointer;
}

.docs-search-clear:hover {
  background: var(--panel-soft);
}

.docs-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 22px;
  margin-top: 20px;
  color: var(--muted);
  font-size: 0.95rem;
}

.docs-stats strong {
  color: var(--ink);
}

.results-title {
  margin: 0;
  font-size: 1.3rem;
  font-family: var(--serif);
  font-weight: 400;
  letter-spacing: -0.01em;
}

.results-empty {
  color: var(--muted);
}

.results-empty a {
  color: var(--accent);
  font-weight: 600;
}

.results {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin-top: 18px;
}

.result {
  display: grid;
  gap: 6px;
  padding: 18px 20px;
}

.result strong {
  color: var(--ink);
  font-size: 1.05rem;
}

.result span {
  color: var(--muted);
  line-height: 1.5;
}

.result .result-section {
  color: var(--accent);
  font-size: 0.78rem;
  font-weight: 600;
  text-transform: uppercase;
}

.start-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
  margin-top: 28px;
}

.start-card {
  overflow: hidden;
}

.start-card img {
  display: block;
  width: 100%;
  height: auto;
  aspect-ratio: 16 / 10;
  object-fit: cover;
  object-position: top left;
  border-bottom: 1px solid var(--line);
}

.start-card div {
  display: grid;
  gap: 6px;
  padding: 16px;
}

.start-card strong {
  color: var(--ink);
}

.start-card span {
  color: var(--muted);
  font-size: 0.92rem;
  line-height: 1.5;
}

.section-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
  margin-top: 28px;
}

.section-card {
  display: flex;
  flex-direction: column;
}

.section-card-head {
  display: flex;
  align-items: center;
  gap: 14px;
}

.section-card-head h3 {
  margin: 0;
  color: var(--ink);
  font-size: 1.08rem;
  font-weight: 650;
}

.section-card-head small {
  color: var(--muted);
}

.section-card p {
  margin: 14px 0 0;
  color: var(--muted);
  line-height: 1.6;
}

.section-card ul {
  display: grid;
  gap: 6px;
  margin: 14px 0 0;
  padding: 0;
  list-style: none;
}

.section-card li a {
  color: var(--ink-2);
  font-weight: 500;
}

.section-card li a:hover,
.more-link:hover {
  color: var(--accent);
}

.more-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-top: auto;
  padding-top: 12px;
  color: var(--ink);
  font-weight: 600;
}

.help-band {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 34px;
}

.help-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

@media (max-width: 980px) {
  .start-grid,
  .section-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .help-band {
    flex-direction: column;
    align-items: flex-start;
  }
}

@media (max-width: 640px) {
  .docs-hero {
    padding-top: 104px;
  }

  .results,
  .start-grid,
  .section-grid {
    grid-template-columns: 1fr;
  }

  .help-band {
    padding: 22px;
  }
}
</style>
