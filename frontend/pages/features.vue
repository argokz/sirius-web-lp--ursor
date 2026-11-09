<template>
  <CmsPageRenderer slug="features">
    <div class="page features-page">
      <section class="features-hero">
        <div class="container features-hero-grid">
          <div class="reveal">
            <UBadge color="primary" variant="subtle" size="lg">Возможности ТГИД</UBadge>
            <h1 class="display-title">{{ totalPages }} функций для всей теплосетевой компании</h1>
            <p class="lead">
              Расчётчики, диспетчеры, ПТС, ремонтные службы, бригады и руководство работают в одной модели сети:
              от карты и гидравлики до нарядов, отчётов и помощника ИИ. Каждая функция описана в справке
              со снимками экрана.
            </p>
            <div class="hero-actions">
              <UButton to="/demo" color="primary" size="xl" trailing-icon="i-lucide-arrow-right">
                Запросить демо
              </UButton>
              <UButton to="/docs" color="neutral" variant="outline" size="xl" icon="i-lucide-book-open">
                Открыть справку
              </UButton>
            </div>
          </div>
          <figure v-if="heroImage" class="hero-shot shot-frame scan-line reveal delay-2">
            <img
              :src="heroImage.src"
              :alt="heroImage.alt"
              :width="heroImage.width"
              :height="heroImage.height"
              loading="eager"
              fetchpriority="high"
              decoding="async"
            >
          </figure>
        </div>
      </section>

      <section class="stats-band">
        <div class="container stats-grid">
          <div v-for="stat in stats" :key="stat.label" class="stat">
            <strong>{{ stat.value }}</strong>
            <span>{{ stat.label }}</span>
          </div>
        </div>
      </section>

      <nav class="module-nav" aria-label="Модули">
        <div class="container module-nav-inner">
          <a v-for="module in productModules" :key="module.section" :href="`#${slugOf(module.section)}`">
            <UIcon :name="module.icon" />
            {{ module.name }}
          </a>
        </div>
      </nav>

      <section
        v-for="(module, index) in productModules"
        :id="slugOf(module.section)"
        :key="module.section"
        class="module-section"
        :class="{ alt: index % 2 === 1 }"
      >
        <div class="container module-grid">
          <div class="module-copy">
            <span class="eyebrow">{{ String(index + 1).padStart(2, '0') }} · {{ module.name }}</span>
            <h2 class="section-title">{{ module.headline }}</h2>
            <p class="lead">{{ module.text }}</p>

            <ul class="function-list">
              <li v-for="(page, pageIndex) in pagesOf(module.section)" :key="page.key">
                <NuxtLink :to="page.url">
                  <span class="check">{{ String(pageIndex + 1).padStart(2, '0') }}</span>
                  <span>
                    <strong>{{ page.title }}</strong>
                    <small>{{ page.summary }}</small>
                  </span>
                  <UIcon v-if="page.video" name="i-lucide-play-circle" class="video-mark" aria-label="есть видео" />
                </NuxtLink>
              </li>
            </ul>
          </div>

          <figure v-if="showcaseOf(module)" class="module-shot">
            <NuxtLink :to="showcaseOf(module)!.url" class="module-shot-frame shot-frame">
              <img
                :src="showcaseOf(module)!.cover!.src"
                :alt="showcaseOf(module)!.cover!.alt"
                :width="showcaseOf(module)!.cover!.width"
                :height="showcaseOf(module)!.cover!.height"
                loading="lazy"
                decoding="async"
              >
            </NuxtLink>
            <figcaption>
              {{ showcaseOf(module)!.title }} —
              <NuxtLink :to="showcaseOf(module)!.url">как это работает</NuxtLink>
            </figcaption>
          </figure>
        </div>
      </section>

      <section class="section-tight">
        <div class="container">
          <div class="final-cta dark-panel">
            <div>
              <span class="eyebrow">Следующий шаг</span>
              <h2 class="section-title">Соберём демонстрацию по нужным функциям</h2>
              <p class="lead">
                Выберите приоритет — режимы и расчёты, эксплуатация и наряды, паспорта и отчёты, полевое
                приложение или ИИ — и мы покажем его на данных, похожих на вашу сеть.
              </p>
            </div>
            <div class="final-actions">
              <UButton to="/demo" color="primary" size="xl" icon="i-lucide-calendar-check">
                Назначить демонстрацию
              </UButton>
              <UButton to="/docs" color="neutral" variant="outline" size="xl" class="light-outline">
                Читать справку
              </UButton>
            </div>
          </div>
        </div>
      </section>
    </div>
  </CmsPageRenderer>
</template>

<script setup lang="ts">
import type { ManualCatalog } from '~~/types/manual'
import type { ProductModule } from '~/utils/productModules'

const HERO_PAGE = '05-analysis/hydraulic-thematic'
/** Ключ страницы справки — «раздел/id» */
const showcaseKey = (module: ProductModule) => `${module.section}/${module.showcase}`
const imagePages = new Set([HERO_PAGE, ...productModules.map(showcaseKey)])

// Снимки нужны только витринам модулей и первому экрану — остальное в данные страницы не кладём.
const { data: catalog } = await useFetch('/docs-data/catalog', {
  key: 'docs-features',
  transform: (full: ManualCatalog) => ({
    sections: full.sections.map(({ id, pageIds }) => ({ id, pageIds })),
    pages: Object.fromEntries(Object.values(full.pages).map((page) => [
      page.key,
      { ...page, cover: imagePages.has(page.key) ? page.cover : null }
    ]))
  })
})

const pages = computed(() => catalog.value?.pages || {})
const totalPages = computed(() => Object.keys(pages.value).length)
const slugOf = (sectionId: string) => sectionId.replace(/^\d+-/, '')

const pagesOf = (sectionId: string) => {
  const section = catalog.value?.sections.find((item) => item.id === sectionId)
  return (section?.pageIds || []).map((id) => pages.value[id])
}

const showcaseOf = (module: ProductModule) => {
  const page = pages.value[showcaseKey(module)]
  return page?.cover ? page : null
}

const heroImage = computed(() => pages.value[HERO_PAGE]?.cover)

const stats = computed(() => [
  { value: totalPages.value, label: 'функций с инструкциями' },
  { value: productModules.length, label: 'модулей платформы' },
  { value: pagesOf('10-ai').length, label: 'функций ИИ' },
  { value: Object.values(pages.value).filter((page) => page.video).length, label: 'видеоинструкций' },
  { value: 3, label: 'языка интерфейса: ru, kk, en' }
])

useSEO({
  title: 'Возможности ТГИД — ПКФ «Сириус»',
  description: 'Все функции ТГИД по модулям: карта сети, эксплуатация и аварии, расчёты и прогнозы, паспорта и отчёты, полевое приложение, интеграции и искусственный интеллект.'
})
</script>

<style scoped>
.features-hero {
  padding: 136px 0 80px;
}

.features-hero-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(320px, 0.95fr);
  gap: 44px;
  align-items: center;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 32px;
}

.stats-band {
  border-block: 1px solid var(--line);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
}

.stat {
  display: grid;
  gap: 4px;
  padding: 30px 22px;
  border-left: 1px solid var(--line);
}

.stat:first-child {
  border-left: 0;
  padding-left: 0;
}

.stat strong {
  color: var(--ink);
  font-family: var(--serif);
  font-size: clamp(2.2rem, 4vw, 3.2rem);
  font-weight: 400;
  line-height: 1;
  letter-spacing: -0.02em;
}

.stat span {
  color: var(--muted);
  font-family: var(--mono);
  font-size: 0.72rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.module-nav {
  position: sticky;
  top: 72px;
  z-index: 20;
  border-bottom: 1px solid var(--line);
  background: rgba(246, 244, 238, 0.94);
  backdrop-filter: blur(10px);
}

.module-nav-inner {
  display: flex;
  gap: 6px;
  overflow-x: auto;
  padding: 10px 0;
  scrollbar-width: none;
}

.module-nav-inner::-webkit-scrollbar {
  display: none;
}

.module-nav a {
  display: inline-flex;
  flex: 0 0 auto;
  align-items: center;
  gap: 6px;
  min-height: 34px;
  padding: 0 12px;
  border: 1px solid var(--line-strong);
  border-radius: var(--radius-sm);
  color: var(--ink-2);
  font-size: 0.86rem;
  font-weight: 500;
  transition: background-color 0.2s ease, color 0.2s ease, border-color 0.2s ease;
}

.module-nav a:hover {
  border-color: var(--ink);
  color: var(--on-dark);
  background: var(--ink);
}

.module-section {
  padding: 96px 0;
  border-top: 1px solid var(--line);
  scroll-margin-top: 124px;
}

.module-nav + .module-section {
  border-top: 0;
}

.module-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1.05fr);
  gap: 48px;
  align-items: start;
}

.module-section.alt .module-copy {
  order: 2;
}

.function-list {
  display: grid;
  margin: 30px 0 0;
  border-bottom: 1px solid var(--line);
  padding: 0;
  list-style: none;
}

.function-list a {
  display: grid;
  grid-template-columns: 30px minmax(0, 1fr) auto;
  gap: 12px;
  align-items: start;
  padding: 14px 0;
  border-top: 1px solid var(--line);
  transition: padding-left 0.25s ease, background-color 0.25s ease;
}

.function-list a:hover {
  padding-left: 10px;
  background: var(--paper-2);
}

.function-list .check {
  padding-top: 3px;
  color: var(--accent);
  font-family: var(--mono);
  font-size: 0.74rem;
}

.function-list span {
  display: grid;
  gap: 2px;
}

.function-list strong {
  color: var(--ink);
  font-weight: 650;
}

.function-list small {
  color: var(--muted);
  font-size: 0.9rem;
  line-height: 1.45;
}

.video-mark {
  margin-top: 3px;
  color: var(--muted);
}

.module-shot {
  position: sticky;
  top: 150px;
  margin: 0;
}

.module-shot-frame img {
  transition: transform 0.5s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.module-shot-frame {
  overflow: hidden;
}

.module-shot-frame:hover img {
  transform: scale(1.02);
}

.module-shot figcaption {
  margin-top: 14px;
  color: var(--muted);
  font-family: var(--mono);
  font-size: 0.72rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.module-shot figcaption a {
  color: var(--ink);
  text-decoration: underline;
  text-decoration-color: var(--sirius-red);
  text-underline-offset: 3px;
}

.final-cta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 32px;
  padding: 48px;
  border-radius: var(--radius);
}

.final-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.final-cta :deep(a[class*="bg-primary"]) {
  color: var(--ink);
  background: var(--on-dark);
}

.light-outline {
  color: var(--on-dark);
}

@media (max-width: 980px) {
  .features-hero-grid,
  .module-grid {
    grid-template-columns: 1fr;
  }

  .module-section.alt .module-copy {
    order: 0;
  }

  .module-shot {
    position: static;
  }

  .stats-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .stat:nth-child(4) {
    border-left: 0;
    padding-left: 0;
  }

  .module-nav {
    top: 70px;
  }

  .final-cta {
    flex-direction: column;
    align-items: flex-start;
  }
}

@media (max-width: 640px) {
  .features-hero {
    padding-top: 104px;
  }

  .stats-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .stat {
    border-left: 0;
    padding-left: 0;
  }

  .module-section {
    padding: 56px 0;
  }

  .final-cta {
    padding: 24px;
  }
}
</style>
