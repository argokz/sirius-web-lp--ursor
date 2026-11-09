<template>
  <DocsShell :section-slug="sectionSlug" :page-id="pageId">
    <div v-if="data" class="doc-layout">
      <article class="doc">
        <nav class="breadcrumbs" aria-label="Навигационная цепочка">
          <NuxtLink to="/docs">Документация</NuxtLink>
          <UIcon name="i-lucide-chevron-right" />
          <NuxtLink :to="`/docs/${data.section.slug}`">{{ data.section.title }}</NuxtLink>
        </nav>

        <h1>{{ data.page.title }}</h1>
        <p class="doc-lead">{{ data.page.lead }}</p>

        <dl v-if="data.page.where || data.page.rights" class="doc-meta">
          <div v-if="data.page.where">
            <dt><UIcon name="i-lucide-navigation" /> Где найти</dt>
            <dd v-html="data.page.where" />
          </div>
          <div v-if="data.page.rights">
            <dt><UIcon name="i-lucide-key-round" /> Права</dt>
            <dd v-html="data.page.rights" />
          </div>
        </dl>

        <figure v-if="data.page.video" class="doc-video">
          <video ref="videoRef" :src="data.page.video.src" controls muted playsinline preload="metadata">
            <track v-if="data.page.video.track" :src="data.page.video.track" kind="subtitles" srclang="ru" label="Русский" default>
          </video>
          <figcaption>
            <UIcon name="i-lucide-play-circle" />
            {{ isJourney ? 'Сквозной сценарий: шаги подписаны в кадре и субтитрами' : 'Короткое видео: как это выглядит в системе' }}
          </figcaption>
        </figure>

        <div v-if="data.journeys.length" class="doc-journeys">
          <UIcon name="i-lucide-clapperboard" />
          <span>Функция показана в сквозном сценарии:</span>
          <NuxtLink v-for="item in data.journeys" :key="item.key" :to="item.url">{{ item.title }}</NuxtLink>
        </div>

        <div v-if="hasLevelSections" class="doc-reader" role="group" aria-label="Для кого показывать подробности">
          <span>Читаю как</span>
          <button
            v-for="option in READER_OPTIONS"
            :key="option.value"
            type="button"
            :class="{ active: reader === option.value }"
            :aria-pressed="reader === option.value"
            @click="reader = option.value"
          >
            {{ option.label }}
          </button>
        </div>

        <div ref="bodyRef" class="doc-body" @click="onBodyClick" @keydown="onBodyKeydown" v-html="data.page.html" />

        <section v-if="data.related.length" class="doc-related">
          <h2>{{ isJourney ? 'Функции в ролике' : 'Связанные функции' }}</h2>
          <div class="doc-related-grid">
            <NuxtLink v-for="item in data.related" :key="item.key" :to="item.url" class="detail-card">
              <strong>{{ item.title }}</strong>
              <span>{{ item.summary }}</span>
            </NuxtLink>
          </div>
        </section>

        <nav class="doc-pager" aria-label="Соседние страницы">
          <NuxtLink v-if="data.prev" :to="data.prev.url" class="pager-link">
            <small><UIcon name="i-lucide-arrow-left" /> Назад</small>
            <strong>{{ data.prev.title }}</strong>
          </NuxtLink>
          <span v-else />
          <NuxtLink v-if="data.next" :to="data.next.url" class="pager-link next">
            <small>Далее <UIcon name="i-lucide-arrow-right" /></small>
            <strong>{{ data.next.title }}</strong>
          </NuxtLink>
        </nav>

        <div class="doc-cta">
          <div>
            <strong>Хотите увидеть эту функцию на своих данных?</strong>
            <span>Покажем ТГИД на демонстрации и ответим на вопросы инженеров.</span>
          </div>
          <UButton to="/demo" color="primary" trailing-icon="i-lucide-arrow-right">Запросить демо</UButton>
        </div>
      </article>

      <aside v-if="data.page.toc.length" class="doc-toc" aria-label="На этой странице">
        <span>На странице</span>
        <a v-for="item in data.page.toc" :key="item.id" :href="`#${item.id}`" @click="openLevel(item.id)">{{ item.text }}</a>
        <a v-if="data.related.length" href="#" @click.prevent="scrollToRelated">{{ isJourney ? 'Функции в ролике' : 'Связанные функции' }}</a>
      </aside>
    </div>

    <div v-if="zoomed" class="lightbox" role="dialog" aria-modal="true" aria-label="Снимок экрана" @click="closeZoom">
      <img :src="zoomed.src" :alt="zoomed.alt">
      <button ref="closeRef" type="button" class="lightbox-close" aria-label="Закрыть" @click.stop="closeZoom"><UIcon name="i-lucide-x" /></button>
    </div>
  </DocsShell>
</template>

<script setup lang="ts">
const route = useRoute()
const sectionSlug = computed(() => String(route.params.section))
const pageId = computed(() => String(route.params.page))

const { data, error } = await useManualPage(sectionSlug, pageId)
if (error.value || !data.value) {
  throw createError({ statusCode: 404, statusMessage: 'Страница справки не найдена', fatal: true })
}

const bodyRef = ref<HTMLElement | null>(null)
const videoRef = ref<HTMLVideoElement | null>(null)
const zoomed = ref<{ src: string; alt: string } | null>(null)
const closeRef = ref<HTMLButtonElement | null>(null)
let zoomOpener: HTMLElement | null = null
const isJourney = computed(() => data.value?.section.id === 'journeys')

const { reader, READER_OPTIONS, levelOpen } = useDocsReader()
const hasLevelSections = computed(() => Boolean(data.value?.page.toc.some((item) => item.level)))

/** Снимки в тексте открываются и с клавиатуры: фокус и роль кнопки */
const prepareImages = () => {
  bodyRef.value?.querySelectorAll<HTMLImageElement>('img').forEach((img) => {
    img.tabIndex = 0
    img.setAttribute('role', 'button')
  })
}

/** Ссылка с якорем внутрь свёрнутого раздела (#dlya-administratora…) раскрывает его */
const revealHash = () => {
  const id = decodeURIComponent(route.hash.slice(1))
  const target = id ? document.getElementById(id) : null
  const details = target?.closest('details')
  if (!target || !details || details.open) return
  details.open = true
  target.scrollIntoView()
}

/** Разделы «Для администратора» / «Для разработчика» открыты по выбору «Читаю как» */
const syncLevelSections = () => {
  bodyRef.value?.querySelectorAll<HTMLDetailsElement>('details.doc-level').forEach((details) => {
    details.open = levelOpen(details.dataset.level)
  })
}
const preparePage = () => {
  syncLevelSections()
  prepareImages()
  revealHash()
}
watch(reader, syncLevelSections)
watch(() => data.value?.page.key, () => nextTick(preparePage))
watch(() => route.hash, revealHash)
onMounted(preparePage)

/** Переход из оглавления к свёрнутому разделу раскрывает его */
const openLevel = (id: string) => {
  const target = document.getElementById(id)
  if (target instanceof HTMLDetailsElement) target.open = true
}

const onBodyClick = (event: MouseEvent) => {
  const target = event.target as HTMLElement
  if (target instanceof HTMLImageElement) {
    openZoom(target)
    return
  }
  // «Что в ролике»: метка времени перематывает ролик
  const seek = target.closest<HTMLElement>('.doc-seek')
  if (seek && videoRef.value) {
    videoRef.value.currentTime = Number(seek.dataset.seek) || 0
    videoRef.value.scrollIntoView({ behavior: 'smooth', block: 'center' })
    videoRef.value.play().catch(() => undefined)
  }
}

const onBodyKeydown = (event: KeyboardEvent) => {
  if (!(event.target instanceof HTMLImageElement) || (event.key !== 'Enter' && event.key !== ' ')) return
  event.preventDefault()
  openZoom(event.target)
}

const openZoom = (img: HTMLImageElement) => {
  zoomOpener = img
  zoomed.value = { src: img.src, alt: img.alt }
  nextTick(() => closeRef.value?.focus())
}
const closeZoom = () => {
  zoomed.value = null
  zoomOpener?.focus()
  zoomOpener = null
}

const closeOnEscape = (event: KeyboardEvent) => {
  if (event.key === 'Escape' && zoomed.value) closeZoom()
}
onMounted(() => window.addEventListener('keydown', closeOnEscape))
onUnmounted(() => window.removeEventListener('keydown', closeOnEscape))

const scrollToRelated = () => {
  document.querySelector('.doc-related')?.scrollIntoView({ behavior: 'smooth' })
}

useSEO({
  title: `${data.value.page.title} — справка ТГИД`,
  description: data.value.page.lead || data.value.page.summary,
  image: data.value.page.cover ? `https://itwin.kz${data.value.page.cover.src}` : undefined,
  type: 'article'
})
</script>

<style scoped>
.doc-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 200px;
  gap: 40px;
}

.doc {
  min-width: 0;
  max-width: 820px;
}

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

.doc h1 {
  margin: 14px 0 0;
  color: var(--ink);
  font-size: clamp(1.9rem, 3.8vw, 2.7rem);
  font-family: var(--serif);
  font-weight: 400;
  letter-spacing: -0.01em;
  line-height: 1.12;
  letter-spacing: -0.01em;
}

.doc-lead {
  margin: 14px 0 0;
  color: var(--muted);
  font-size: 1.12rem;
  line-height: 1.6;
}

.doc-meta {
  display: grid;
  gap: 10px;
  margin: 24px 0 0;
  padding: 16px 18px;
  border: 1px solid rgba(227, 6, 19, 0.14);
  border-radius: var(--radius);
  background: var(--paper-2);
}

.doc-meta div {
  display: grid;
  grid-template-columns: 140px minmax(0, 1fr);
  gap: 12px;
}

.doc-meta dt {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--ink);
  font-weight: 650;
}

.doc-meta dd {
  margin: 0;
  color: var(--ink-2);
  line-height: 1.55;
}

.doc-video {
  margin: 28px 0 0;
}

.doc-video video {
  display: block;
  width: 100%;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--dark);
}

.doc-video figcaption {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 8px;
  color: var(--muted);
  font-size: 0.9rem;
}

.doc-body {
  margin-top: 12px;
  color: #1e293b;
  font-size: 1.02rem;
  line-height: 1.7;
}

.doc-body :deep(h2) {
  margin: 40px 0 0;
  padding-top: 8px;
  color: var(--ink);
  font-size: 1.45rem;
  font-family: var(--serif);
  font-weight: 400;
  letter-spacing: -0.01em;
  scroll-margin-top: 96px;
}

.doc-body :deep(h3) {
  margin: 28px 0 0;
  font-size: 1.15rem;
  font-weight: 650;
}

.doc-body :deep(p) {
  margin: 12px 0 0;
}

.doc-body :deep(ul) {
  margin: 14px 0 0;
  padding-left: 22px;
  list-style: disc;
}

.doc-body :deep(ul li) {
  margin-top: 6px;
}

.doc-body :deep(ol) {
  margin: 18px 0 0;
  padding: 0;
  list-style: none;
  counter-reset: step;
}

.doc-body :deep(ol > li) {
  position: relative;
  margin-top: 22px;
  padding-left: 46px;
  counter-increment: step;
}

.doc-body :deep(ol > li::before) {
  content: counter(step, decimal-leading-zero);
  position: absolute;
  top: 0;
  left: 0;
  display: grid;
  width: 32px;
  height: 28px;
  place-items: center;
  border-top: 1px solid var(--ink);
  color: var(--accent);
  font-family: var(--mono);
  font-size: 0.78rem;
  font-weight: 500;
}

.doc-body :deep(ol > li > p:first-child) {
  margin-top: 0;
}

.doc-body :deep(img) {
  display: block;
  width: 100%;
  height: auto;
  margin-top: 4px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  cursor: zoom-in;
}

.doc-body :deep(a) {
  color: var(--ink);
  font-weight: 600;
  text-decoration: underline;
  text-underline-offset: 3px;
}

.doc-body :deep(code) {
  padding: 2px 6px;
  border-radius: 5px;
  background: var(--panel-soft);
  font-size: 0.92em;
}

.doc-body :deep(table) {
  display: block;
  overflow-x: auto;
  width: 100%;
  margin-top: 16px;
  border-collapse: collapse;
}

.doc-body :deep(th),
.doc-body :deep(td) {
  padding: 10px 12px;
  border: 1px solid var(--line);
  text-align: left;
  vertical-align: top;
}

.doc-body :deep(th) {
  background: var(--panel-soft);
  font-weight: 650;
}

.doc-related {
  margin-top: 44px;
  scroll-margin-top: 96px;
}

.doc-related h2 {
  margin: 0;
  font-size: 1.45rem;
  font-family: var(--serif);
  font-weight: 400;
  letter-spacing: -0.01em;
}

.doc-related-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin-top: 16px;
}

.doc-related-grid a {
  display: grid;
  gap: 6px;
  transition: border-color 0.2s ease;
}

.doc-related-grid a:hover {
  border-color: rgba(227, 6, 19, 0.3);
}

.doc-related-grid strong {
  color: var(--ink);
}

.doc-related-grid span {
  color: var(--muted);
  font-size: 0.93rem;
  line-height: 1.5;
}

.doc-pager {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-top: 44px;
  padding-top: 24px;
  border-top: 1px solid var(--line);
}

.pager-link {
  display: grid;
  gap: 4px;
  padding: 14px 16px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--surface);
}

.pager-link:hover {
  border-color: rgba(227, 6, 19, 0.3);
}

.pager-link.next {
  text-align: right;
}

.pager-link small {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: var(--muted);
}

.pager-link.next small {
  justify-content: flex-end;
}

.pager-link strong {
  color: var(--ink);
}

.doc-cta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-top: 28px;
  padding: 20px 22px;
  border-radius: var(--radius);
  color: white;
  background: var(--dark);
}

.doc-cta div {
  display: grid;
  gap: 4px;
}

.doc-cta span {
  color: #cbd5e1;
  font-size: 0.93rem;
}

.doc-toc {
  position: sticky;
  top: 96px;
  align-self: start;
  display: grid;
  gap: 2px;
  padding-left: 14px;
  border-left: 1px solid var(--line);
}

.doc-toc span {
  margin-bottom: 6px;
  color: var(--ink);
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
}

.doc-toc a {
  padding: 5px 0;
  color: var(--muted);
  font-size: 0.9rem;
}

.doc-toc a:hover {
  color: var(--accent);
}

.lightbox {
  position: fixed;
  inset: 0;
  z-index: 80;
  display: grid;
  place-items: center;
  padding: 24px;
  background: rgba(9, 9, 11, 0.86);
  cursor: zoom-out;
}

.lightbox img {
  max-width: 100%;
  max-height: 100%;
  border-radius: 8px;
}

.lightbox-close {
  position: absolute;
  top: 16px;
  right: 16px;
  display: grid;
  width: 42px;
  height: 42px;
  place-items: center;
  border: 0;
  border-radius: 999px;
  color: white;
  background: rgba(255, 255, 255, 0.12);
  font-size: 1.3rem;
  cursor: pointer;
}

@media (max-width: 1180px) {
  .doc-layout {
    grid-template-columns: 1fr;
  }

  .doc-toc {
    display: none;
  }
}

@media (max-width: 640px) {
  .doc-meta div,
  .doc-related-grid {
    grid-template-columns: 1fr;
  }

  .doc-meta div {
    gap: 4px;
  }

  .doc-body :deep(ol > li) {
    padding-left: 0;
  }

  .doc-body :deep(ol > li::before) {
    position: static;
    margin-bottom: 8px;
  }

  .doc-cta {
    flex-direction: column;
    align-items: flex-start;
  }
}
.doc-journeys {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px 12px;
  margin-top: 14px;
  color: var(--muted);
  font-size: 0.95rem;
}

.doc-journeys a {
  color: var(--ink);
  text-decoration: underline;
  text-underline-offset: 3px;
}

.doc-journeys a:hover {
  color: var(--accent);
}

.doc-reader {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px;
  margin-top: 22px;
  color: var(--muted);
  font-size: 0.9rem;
}

.doc-reader button {
  min-height: 36px;
  padding: 4px 12px;
  border: 1px solid var(--line);
  border-radius: 999px;
  background: var(--surface);
  color: var(--ink-2);
  cursor: pointer;
}

.doc-reader button.active {
  border-color: var(--ink);
  background: var(--ink);
  color: var(--paper);
}

.doc-body :deep(details.doc-level) {
  margin-top: 40px;
  border-top: 1px solid var(--line);
  scroll-margin-top: 96px;
}

.doc-body :deep(details.doc-level > summary) {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  list-style: none;
}

.doc-body :deep(details.doc-level > summary::-webkit-details-marker) {
  display: none;
}

.doc-body :deep(details.doc-level > summary::after) {
  content: '+';
  margin-left: auto;
  color: var(--muted);
  font-size: 1.4rem;
}

.doc-body :deep(details.doc-level[open] > summary::after) {
  content: '−';
}

.doc-body :deep(details.doc-level > summary h2) {
  margin-top: 16px;
}

.doc-body :deep(.doc-seek) {
  min-width: 52px;
  margin-right: 6px;
  padding: 2px 8px;
  border: 1px solid var(--line-strong);
  border-radius: var(--radius);
  background: var(--surface);
  color: var(--ink);
  font-family: var(--mono);
  font-size: 0.85rem;
  cursor: pointer;
}

.doc-body :deep(.doc-seek:hover) {
  border-color: var(--accent);
  color: var(--accent);
}
</style>
