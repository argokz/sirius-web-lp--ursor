<template>
  <DocsShell>
    <nav class="breadcrumbs" aria-label="Навигационная цепочка">
      <NuxtLink to="/docs">Документация</NuxtLink>
      <UIcon name="i-lucide-chevron-right" />
      <span>Если не получается</span>
    </nav>

    <h1>Если не получается</h1>
    <p class="lead">
      Частые сообщения и ситуации из всех инструкций: что они значат и что сделать. Ответа нет —
      <NuxtLink to="/contacts">напишите в поддержку</NuxtLink>.
    </p>

    <div class="trouble-filter">
      <UIcon name="i-lucide-filter" />
      <input v-model="filter" type="search" placeholder="Фильтр: например, «права» или «сохранить»" aria-label="Фильтр">
    </div>

    <section v-for="group in visibleGroups" :key="group.section" class="trouble-group">
      <h2>{{ sectionTitle(group.section) }}</h2>
      <article v-for="item in group.items" :key="item.id" class="trouble-card">
        <NuxtLink :to="item.url" class="trouble-title">
          {{ item.title }}
          <UIcon name="i-lucide-arrow-up-right" />
        </NuxtLink>
        <ul>
          <li v-for="(text, index) in item.troubles" :key="index">{{ text }}</li>
        </ul>
      </article>
    </section>

    <p v-if="!visibleGroups.length" class="lead">Ничего не нашлось — попробуйте другое слово.</p>
  </DocsShell>
</template>

<script setup lang="ts">
const { data: catalog } = await useManualCatalog()
const { data: troubles } = await useFetch('/docs-data/troubles', { key: 'docs-troubles' })

const filter = ref('')
const sectionTitle = (id: string) => catalog.value?.sections.find((section) => section.id === id)?.title || ''

const visibleGroups = computed(() => {
  const words = filter.value.toLowerCase().split(/\s+/).filter(Boolean)
  const groups = new Map<string, NonNullable<typeof troubles.value>>()
  for (const item of troubles.value || []) {
    const lines = words.length
      ? item.troubles.filter((text) => words.every((word) => `${item.title} ${text}`.toLowerCase().includes(word)))
      : item.troubles
    if (!lines.length) continue
    const list = groups.get(item.section) || []
    list.push({ ...item, troubles: lines })
    groups.set(item.section, list)
  }
  return [...groups].map(([section, items]) => ({ section, items }))
})

useSEO({
  title: 'Если не получается — справка ТГИД',
  description: 'Частые сообщения об ошибках веб-ТГИД и что с ними делать: права, сохранение, расчёт, импорт, ИИ.'
})
</script>

<style scoped>
.breadcrumbs {
  display: flex;
  align-items: center;
  gap: 6px;
  color: var(--muted);
  font-size: 0.9rem;
}

h1 {
  margin: 14px 0 0;
  color: var(--ink);
  font-size: clamp(1.9rem, 3.8vw, 2.7rem);
  font-family: var(--serif);
  font-weight: 400;
  letter-spacing: -0.01em;
}

.lead a {
  color: var(--accent);
  font-weight: 600;
}

.trouble-filter {
  display: flex;
  align-items: center;
  gap: 10px;
  max-width: 560px;
  min-height: 46px;
  margin-top: 24px;
  padding: 0 14px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--surface);
  color: var(--muted);
}

.trouble-filter:focus-within {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(28, 27, 24, 0.12);
}

.trouble-filter input {
  width: 100%;
  border: 0;
  outline: none;
  color: var(--ink);
}

.trouble-group {
  margin-top: 36px;
}

.trouble-group h2 {
  margin: 0;
  font-size: 1.3rem;
  font-family: var(--serif);
  font-weight: 400;
  letter-spacing: -0.01em;
}

.trouble-card {
  margin-top: 12px;
  padding: 16px 18px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--surface);
}

.trouble-title {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--ink);
  font-weight: 650;
}

.trouble-title:hover {
  color: var(--accent);
}

.trouble-card ul {
  margin: 10px 0 0;
  padding-left: 20px;
  color: var(--ink-2);
  line-height: 1.6;
  list-style: disc;
}

.trouble-card li + li {
  margin-top: 6px;
}
</style>
