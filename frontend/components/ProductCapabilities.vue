<template>
  <section v-if="catalog" class="section capabilities">
    <div class="container">
      <div class="capabilities-head">
        <div>
          <span class="eyebrow">{{ eyebrow }}</span>
          <h2 class="section-title">{{ heading }}</h2>
          <p class="lead">{{ lead }}</p>
        </div>
        <div class="capabilities-actions">
          <UButton to="/features" color="primary" size="lg" trailing-icon="i-lucide-arrow-right">
            Все возможности
          </UButton>
          <UButton to="/docs" color="neutral" variant="outline" size="lg" icon="i-lucide-book-open">
            Документация
          </UButton>
        </div>
      </div>

      <div v-if="!sections" class="module-grid">
        <NuxtLink
          v-for="(module, index) in productModules"
          :key="module.section"
          :to="`/features#${sectionSlug(module.section)}`"
          class="module-card"
        >
          <span class="module-index">
            {{ String(index + 1).padStart(2, '0') }}
            <UIcon :name="module.icon" />
          </span>
          <strong>{{ module.name }}</strong>
          <span>{{ module.headline }}</span>
          <small>{{ countLabel(module.section) }}</small>
        </NuxtLink>
      </div>

      <div v-else class="function-groups">
        <article v-for="module in selectedModules" :key="module.section" class="function-group">
          <header>
            <div class="icon-box">
              <UIcon :name="module.icon" />
            </div>
            <div>
              <h3>{{ module.name }}</h3>
              <p>{{ module.headline }}</p>
            </div>
          </header>
          <div class="function-list">
            <NuxtLink v-for="page in pagesOf(module.section)" :key="page.id" :to="page.url" class="function-item">
              <strong>
                {{ page.title }}
                <UIcon v-if="page.video" name="i-lucide-play-circle" class="video-mark" aria-label="есть видео" />
              </strong>
              <span>{{ page.summary }}</span>
            </NuxtLink>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const props = defineProps<{
  /** Разделы справки (например, 05-analysis). Без них — сетка всех модулей. */
  sections?: string[]
  eyebrow?: string
  title?: string
  description?: string
}>()

import type { ManualCatalog } from '~~/types/manual'

// Каталог справки целиком в данные страницы не кладём: берём только то, что показывает блок.
const { data: catalog } = await useFetch('/docs-data/catalog', {
  key: `docs-capabilities-${props.sections?.join(',') || 'all'}`,
  transform: (full: ManualCatalog) => ({
    total: Object.keys(full.pages).length,
    counts: Object.fromEntries(full.sections.map((section) => [section.id, section.pageIds.length])),
    pages: Object.fromEntries(
      full.sections
        .filter((section) => props.sections?.includes(section.id))
        .map((section) => [
          section.id,
          section.pageIds.map((id) => {
            const { url, title, summary, video } = full.pages[id]
            return { id, url, title, summary, video: Boolean(video) }
          })
        ])
    )
  })
})

const selectedModules = computed(() => productModules.filter((module) => props.sections?.includes(module.section)))

const eyebrow = computed(() => props.eyebrow || 'Возможности платформы')
const heading = computed(() => props.title || `${catalog.value?.total} функций в ${productModules.length} модулях`)
const lead = computed(() => props.description || 'Каждая функция описана в справке: где найти, шаги со снимками экрана и короткое видео. Ниже — модули платформы, нажмите, чтобы посмотреть подробности.')

const sectionSlug = (id: string) => id.replace(/^\d+-/, '')
const pagesOf = (sectionId: string) => catalog.value?.pages[sectionId] || []
const countLabel = (sectionId: string) => {
  const n = catalog.value?.counts[sectionId] || 0
  const mod10 = n % 10
  const mod100 = n % 100
  if (mod10 === 1 && mod100 !== 11) return `${n} функция`
  if (mod10 >= 2 && mod10 <= 4 && (mod100 < 12 || mod100 > 14)) return `${n} функции`
  return `${n} функций`
}
</script>

<style scoped>
.capabilities {
  border-top: 1px solid var(--line);
}

.capabilities-head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
}

.capabilities-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.module-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0 28px;
  margin-top: 44px;
}

.module-card {
  display: grid;
  align-content: start;
  gap: 8px;
  padding: 16px 0 34px;
  border-top: 1px solid var(--line-strong);
  transition: border-color 0.25s ease;
}

.module-card:hover {
  border-top-color: var(--ink);
}

.module-index {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
  color: var(--accent);
  font-family: var(--mono);
  font-size: 0.76rem;
}

.module-index svg,
.module-index span {
  color: var(--ink-2);
  font-size: 1.1rem;
  transition: transform 0.25s ease;
}

.module-card:hover .module-index > :last-child {
  transform: translateX(4px);
}

.module-card strong {
  color: var(--ink);
  font-family: var(--serif);
  font-size: 1.35rem;
  font-weight: 400;
  line-height: 1.2;
}

.module-card span {
  color: var(--muted);
  font-size: 0.93rem;
  line-height: 1.5;
}

.module-card small {
  margin-top: 4px;
  color: var(--ink);
  font-family: var(--mono);
  font-size: 0.72rem;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.function-groups {
  display: grid;
  gap: 22px;
  margin-top: 34px;
}

.function-group {
  padding: 28px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--surface);
}

.function-group header {
  display: grid;
  grid-template-columns: 46px minmax(0, 1fr);
  gap: 14px;
  align-items: center;
}

.function-group h3 {
  margin: 0;
  color: var(--ink);
  font-family: var(--serif);
  font-size: 1.45rem;
  font-weight: 400;
}

.function-group header p {
  margin: 4px 0 0;
  color: var(--muted);
}

.function-list {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
  margin-top: 20px;
}

.function-item {
  display: grid;
  align-content: start;
  gap: 4px;
  padding: 14px;
  border: 1px solid var(--line);
  border-radius: var(--radius-sm);
  background: var(--paper);
  transition: border-color 0.2s ease, background-color 0.2s ease;
}

.function-item:hover {
  border-color: var(--ink);
  background: #fff;
}

.function-item strong {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--ink);
  font-size: 0.97rem;
}

.video-mark {
  color: var(--accent);
}

.function-item span {
  color: var(--muted);
  font-size: 0.9rem;
  line-height: 1.5;
}

@media (max-width: 980px) {
  .capabilities-head {
    flex-direction: column;
    align-items: flex-start;
  }

  .module-grid,
  .function-list {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .module-grid,
  .function-list {
    grid-template-columns: 1fr;
  }

  .module-card {
    padding-bottom: 22px;
  }

  .function-group {
    padding: 18px;
  }
}
</style>
