<template>
  <div class="docs-shell container">
    <aside class="docs-nav" aria-label="Разделы справки">
      <form class="docs-nav-search" role="search" @submit.prevent="goSearch">
        <UIcon name="i-lucide-search" />
        <input v-model="query" type="search" placeholder="Поиск по справке" aria-label="Поиск по справке">
      </form>

      <button class="docs-nav-toggle" type="button" :aria-expanded="navOpen" @click="navOpen = !navOpen">
        <UIcon name="i-lucide-list" />
        {{ currentSection ? currentSection.title : 'Все разделы' }}
        <UIcon :name="navOpen ? 'i-lucide-chevron-up' : 'i-lucide-chevron-down'" class="ml-auto" />
      </button>

      <nav class="docs-nav-list" :class="{ open: navOpen }">
        <NuxtLink to="/docs" class="docs-nav-home">
          <UIcon name="i-lucide-book-open" />
          Документация
        </NuxtLink>
        <div v-for="section in catalog?.sections || []" :key="section.id" class="docs-nav-group">
          <NuxtLink
            :to="`/docs/${section.slug}`"
            class="docs-nav-section"
            :class="{ active: section.id === currentSection?.id }"
          >
            <UIcon :name="docSectionIcon(section.id)" />
            <span class="docs-nav-label">{{ section.title }}</span>
            <small>{{ section.pageIds.length }}</small>
          </NuxtLink>
          <ul v-if="section.id === currentSection?.id">
            <li v-for="id in section.pageIds" :key="id">
              <NuxtLink :to="catalog!.pages[id].url" :class="{ active: id === currentPageId }">
                {{ catalog!.pages[id].title }}
              </NuxtLink>
            </li>
          </ul>
        </div>
        <NuxtLink to="/docs/troubleshooting" class="docs-nav-section">
          <UIcon name="i-lucide-life-buoy" />
          <span class="docs-nav-label">Если не получается</span>
        </NuxtLink>
      </nav>
    </aside>

    <div class="docs-main">
      <slot />
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  sectionSlug?: string
  pageId?: string
}>()

const router = useRouter()
const route = useRoute()
const { data: catalog } = await useManualCatalog()

const query = ref('')
const navOpen = ref(false)
const currentSection = computed(() => catalog.value?.sections.find((section) => section.slug === props.sectionSlug))
/** Ключ открытой страницы «раздел/id»: id уникален только внутри раздела */
const currentPageId = computed(() => (currentSection.value && props.pageId ? `${currentSection.value.id}/${props.pageId}` : null))

watch(() => route.fullPath, () => {
  navOpen.value = false
})

const goSearch = () => {
  const q = query.value.trim()
  router.push(q ? { path: '/docs', query: { q } } : '/docs')
}
</script>

<style scoped>
.docs-shell {
  display: grid;
  grid-template-columns: 270px minmax(0, 1fr);
  gap: 40px;
  padding: 112px 0 72px;
}

.docs-nav {
  position: sticky;
  top: 96px;
  align-self: start;
  max-height: calc(100vh - 116px);
  overflow-y: auto;
  padding-right: 6px;
}

.docs-nav-search {
  display: flex;
  align-items: center;
  gap: 8px;
  min-height: 42px;
  padding: 0 12px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--surface);
  color: var(--muted);
}

.docs-nav-search:focus-within {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(28, 27, 24, 0.12);
}

.docs-nav-search input {
  width: 100%;
  border: 0;
  outline: none;
  background: transparent;
  color: var(--ink);
}

.docs-nav-toggle {
  display: none;
}

.docs-nav-list {
  display: grid;
  gap: 2px;
  margin-top: 16px;
}

.docs-nav-home,
.docs-nav-section {
  display: flex;
  align-items: center;
  gap: 10px;
  min-height: 38px;
  padding: 6px 10px;
  border-radius: 8px;
  color: var(--ink-2);
  font-size: 0.93rem;
  font-weight: 600;
}

.docs-nav-label {
  flex: 1;
  line-height: 1.3;
}

.docs-nav-section small {
  color: var(--muted);
  font-weight: 500;
}

.docs-nav-home:hover,
.docs-nav-section:hover {
  background: var(--panel-soft);
}

.docs-nav-section.active,
.docs-nav-home.router-link-exact-active {
  color: var(--ink);
  background: var(--paper-2);
}

.docs-nav-group ul {
  margin: 4px 0 8px 22px;
  padding: 0 0 0 12px;
  border-left: 1px solid var(--line);
  list-style: none;
}

.docs-nav-group li a {
  display: block;
  padding: 6px 8px;
  border-radius: 6px;
  color: var(--muted);
  font-size: 0.9rem;
  line-height: 1.35;
}

.docs-nav-group li a:hover {
  color: var(--ink);
}

.docs-nav-group li a.active {
  color: var(--ink);
  font-weight: 600;
}

.docs-main {
  min-width: 0;
}

@media (max-width: 980px) {
  .docs-shell {
    grid-template-columns: 1fr;
    gap: 24px;
    padding-top: 96px;
  }

  .docs-nav {
    position: static;
    max-height: none;
    overflow: visible;
    padding: 0;
  }

  .docs-nav-toggle {
    display: flex;
    align-items: center;
    gap: 10px;
    width: 100%;
    min-height: 44px;
    margin-top: 10px;
    padding: 0 12px;
    border: 1px solid var(--line);
    border-radius: 8px;
    background: var(--surface);
    color: var(--ink);
    font-weight: 600;
  }

  .docs-nav-list {
    display: none;
    margin-top: 8px;
    padding: 8px;
    border: 1px solid var(--line);
    border-radius: 8px;
    background: var(--surface);
  }

  .docs-nav-list.open {
    display: grid;
  }
}
</style>
