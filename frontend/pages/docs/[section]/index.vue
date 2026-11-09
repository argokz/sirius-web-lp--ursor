<template>
  <DocsShell :section-slug="sectionSlug">
    <nav class="breadcrumbs" aria-label="Навигационная цепочка">
      <NuxtLink to="/docs">Документация</NuxtLink>
      <UIcon name="i-lucide-chevron-right" />
      <span>{{ section.title }}</span>
    </nav>

    <header class="section-head">
      <div class="icon-box">
        <UIcon :name="module?.icon || 'i-lucide-folder'" />
      </div>
      <div>
        <h1>{{ section.title }}</h1>
        <p class="lead">{{ section.description }}</p>
      </div>
    </header>

    <div class="page-list">
      <NuxtLink v-for="page in sectionPages" :key="page.id" :to="page.url" class="page-card card">
        <div class="page-card-media">
          <img
            v-if="page.cover"
            :src="page.cover.src"
            :alt="page.cover.alt"
            :width="page.cover.width"
            :height="page.cover.height"
            loading="lazy"
            decoding="async"
          >
          <UIcon v-else :name="module?.icon || 'i-lucide-file-text'" class="page-card-placeholder" />
          <span v-if="page.video" class="video-badge"><UIcon name="i-lucide-play" /> Видео</span>
        </div>
        <div class="page-card-body">
          <strong>{{ page.title }}</strong>
          <span>{{ page.summary }}</span>
        </div>
      </NuxtLink>
    </div>
  </DocsShell>
</template>

<script setup lang="ts">
const route = useRoute()
const sectionSlug = computed(() => String(route.params.section))
const { data: catalog } = await useManualCatalog()

const found = catalog.value?.sections.find((item) => item.slug === sectionSlug.value)
if (!found) {
  throw createError({ statusCode: 404, statusMessage: 'Раздел справки не найден', fatal: true })
}

const section = computed(() => catalog.value!.sections.find((item) => item.slug === sectionSlug.value)!)
const module = computed(() => productModuleBySection[section.value.id])
const sectionPages = computed(() => section.value.pageIds.map((id) => catalog.value!.pages[id]))

useSEO({
  title: `${section.value.title} — справка ТГИД`,
  description: section.value.description
})
</script>

<style scoped>
.breadcrumbs {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px;
  color: var(--muted);
  font-size: 0.9rem;
}

.breadcrumbs a:hover {
  color: var(--accent);
}

.section-head {
  display: grid;
  grid-template-columns: 46px minmax(0, 1fr);
  gap: 18px;
  margin-top: 18px;
}

.section-head h1 {
  margin: 0;
  color: var(--ink);
  font-size: clamp(1.8rem, 3.6vw, 2.6rem);
  font-family: var(--serif);
  font-weight: 400;
  letter-spacing: -0.01em;
  line-height: 1.15;
}

.section-head .lead {
  margin-top: 10px;
}

.page-list {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
  margin-top: 32px;
}

.page-card {
  display: grid;
  grid-template-columns: 180px minmax(0, 1fr);
  overflow: hidden;
}

.page-card-media {
  position: relative;
  display: grid;
  place-items: center;
  min-height: 112px;
  background: var(--panel-soft);
  border-right: 1px solid var(--line);
}

.page-card-media img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: top left;
}

.page-card-placeholder {
  color: var(--accent);
  font-size: 2rem;
}

.video-badge {
  position: absolute;
  left: 8px;
  bottom: 8px;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 8px;
  border-radius: 999px;
  color: white;
  background: rgba(9, 9, 11, 0.78);
  font-size: 0.75rem;
  font-weight: 600;
}

.page-card-body {
  display: grid;
  align-content: center;
  gap: 6px;
  padding: 16px 18px;
}

.page-card-body strong {
  color: var(--ink);
  font-size: 1.02rem;
}

.page-card-body span {
  color: var(--muted);
  font-size: 0.93rem;
  line-height: 1.5;
}

@media (max-width: 1180px) {
  .page-list {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .section-head {
    grid-template-columns: 1fr;
  }

  .page-card {
    grid-template-columns: 112px minmax(0, 1fr);
  }
}
</style>
