<template>
  <header class="site-header" :class="{ 'site-header-scrolled': isScrolled, 'nav-collapsed': navCollapsed }">
    <SiteHud class="header-hud" />
    <div class="container header-inner">
      <NuxtLink to="/" class="brand" aria-label="Sirius">
        <SiriusLogo :width="146" />
      </NuxtLink>

      <!-- Пункты, которым не хватило места, уходят в «Ещё»; сколько влезает — считается по ширине. -->
      <nav ref="navEl" class="desktop-nav" aria-label="Основная навигация">
        <template v-for="(item, i) in navItems" :key="item.to">
          <a v-if="item.isExternal" v-show="i < visibleCount" :href="item.to" class="nav-link" target="_blank" rel="noopener noreferrer">
            {{ item.title }}
          </a>
          <NuxtLink v-else v-show="i < visibleCount" :to="item.to" class="nav-link">
            {{ item.title }}
          </NuxtLink>
        </template>

        <div v-if="moreItems.length" ref="moreEl" class="nav-more">
          <button
            class="nav-more-btn"
            :class="{ active: moreActive }"
            type="button"
            aria-haspopup="true"
            :aria-expanded="moreOpen"
            @click="moreOpen = !moreOpen"
          >
            Ещё
            <UIcon name="i-lucide-chevron-down" class="nav-more-chevron" />
          </button>
          <div v-if="moreOpen" class="nav-more-menu">
            <template v-for="item in moreItems" :key="item.to">
              <a v-if="item.isExternal" :href="item.to" class="nav-more-link" target="_blank" rel="noopener noreferrer">
                <UIcon :name="item.icon" />{{ item.title }}
              </a>
              <NuxtLink v-else :to="item.to" class="nav-more-link">
                <UIcon :name="item.icon" />{{ item.title }}
              </NuxtLink>
            </template>
          </div>
        </div>
      </nav>

      <div class="header-actions">
        <button
          class="search-btn"
          type="button"
          aria-label="Поиск по сайту, справке и курсу"
          title="Поиск по сайту, справке и курсу — Ctrl K"
          @click="searchOpen = true"
        >
          <UIcon name="i-lucide-search" />
        </button>
        <UButton to="/demo" color="primary" trailing-icon="i-lucide-arrow-right">
          Демо
        </UButton>
        <button class="menu-btn" type="button" aria-label="Открыть меню" @click="menuOpen = true">
          <UIcon name="i-lucide-menu" />
        </button>
      </div>
    </div>

    <div v-if="menuOpen" class="mobile-menu" @click.self="menuOpen = false">
      <aside class="mobile-panel">
        <div class="mobile-head">
          <SiriusLogo :width="132" />
          <button class="menu-btn" type="button" aria-label="Закрыть меню" @click="menuOpen = false">
            <UIcon name="i-lucide-x" />
          </button>
        </div>

        <template v-for="item in navItems" :key="item.to">
          <a
            v-if="item.isExternal"
            :href="item.to"
            class="mobile-link"
            target="_blank"
            rel="noopener noreferrer"
            @click="menuOpen = false"
          >
            <UIcon :name="item.icon" />
            {{ item.title }}
          </a>
          <NuxtLink v-else :to="item.to" class="mobile-link" @click="menuOpen = false">
            <UIcon :name="item.icon" />
            {{ item.title }}
          </NuxtLink>
        </template>
        <NuxtLink to="/contacts" class="mobile-link" @click="menuOpen = false">
          <UIcon name="i-lucide-mail" />
          Контакты
        </NuxtLink>

        <UButton to="/demo" color="primary" block size="lg" class="mt-4" @click="menuOpen = false">
          Запросить демо
        </UButton>
      </aside>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from 'vue'

interface RemoteNavItem {
  title: string
  url: string
  icon?: string
  is_external?: boolean
}

const config = useRuntimeConfig()
const menuOpen = ref(false)
const searchOpen = useState('site-search-open', () => false)
const isScrolled = ref(false)

const fallbackNavItems: RemoteNavItem[] = [
  { title: 'Продукт', url: '/product', icon: 'i-lucide-box' },
  { title: 'Возможности', url: '/features', icon: 'i-lucide-layout-grid' },
  { title: 'Моделирование', url: '/modeling', icon: 'i-lucide-chart-no-axes-combined' },
  { title: 'ГИС', url: '/gis', icon: 'i-lucide-map' },
  { title: 'Эксплуатация', url: '/maintenance', icon: 'i-lucide-wrench' },
  { title: 'Решения', url: '/solutions', icon: 'i-lucide-network' },
  { title: 'Web', url: '/web-version', icon: 'i-lucide-globe' },
  { title: 'Документация', url: '/docs', icon: 'i-lucide-book-open' },
  { title: 'Обучение', url: '/learn', icon: 'i-lucide-graduation-cap' }
]

const { data: remoteNavigation } = useAsyncData<RemoteNavItem[]>(
  'site-navigation',
  async () => {
    try {
      return await $fetch<RemoteNavItem[]>(`${config.public.apiBase}/api/navigation`, {
        timeout: 900
      })
    } catch {
      return []
    }
  },
  {
    // Меню приходит уже в HTML: без подмены пунктов после загрузки шапка не перестраивается на глазах.
    default: () => []
  }
)

const navItems = computed(() => {
  const source = remoteNavigation.value?.length ? remoteNavigation.value : fallbackNavItems

  return source.map((item) => ({
    title: item.title,
    to: item.url,
    icon: item.icon || 'i-lucide-circle',
    isExternal: Boolean(item.is_external || /^https?:\/\//.test(item.url))
  }))
})

/*
 * Меню «по приоритету»: ширины пунктов меряются один раз (шрифт и размер не зависят от экрана),
 * дальше при каждом изменении ширины шапки считается, сколько пунктов влезает слева направо.
 * Остальные — в «Ещё». Влезает меньше MIN_VISIBLE — меню целиком уходит в боковую панель.
 */
const NAV_GAP = 4
const MORE_WIDTH = 84
const MIN_VISIBLE = 3

const route = useRoute()
const navEl = ref<HTMLElement | null>(null)
const moreEl = ref<HTMLElement | null>(null)
const moreOpen = ref(false)
const itemWidths = ref<number[]>([])
const visibleCount = ref(Number.POSITIVE_INFINITY)

const moreItems = computed(() => navItems.value.slice(visibleCount.value))
const navCollapsed = computed(() => visibleCount.value < MIN_VISIBLE)
const moreActive = computed(() =>
  moreItems.value.some((item) => !item.isExternal && item.to !== '/' && route.path.startsWith(item.to))
)

const fitNav = () => {
  const nav = navEl.value
  const widths = itemWidths.value
  if (!nav || !widths.length) return
  const available = nav.clientWidth
  const total = widths.reduce((sum, w) => sum + w, 0) + NAV_GAP * (widths.length - 1)
  if (total <= available) {
    visibleCount.value = widths.length
    return
  }
  let used = MORE_WIDTH
  let count = 0
  while (count < widths.length && used + widths[count]! + NAV_GAP <= available) {
    used += widths[count]! + NAV_GAP
    count++
  }
  visibleCount.value = count
}

/** Меряет все пункты: на время замера показывает их все. Скрытое меню (узкий экран) не меряется. */
const measureNav = async () => {
  visibleCount.value = Number.POSITIVE_INFINITY
  await nextTick()
  const links = navEl.value ? [...navEl.value.querySelectorAll<HTMLElement>('.nav-link')] : []
  const widths = links.map((link) => link.offsetWidth)
  if (!widths.length || widths.some((w) => w === 0)) return
  itemWidths.value = widths
  fitNav()
}

const onNavResize = () => {
  if (itemWidths.value.length) fitNav()
  else void measureNav()
}

const closeMoreOutside = (event: PointerEvent) => {
  if (moreOpen.value && moreEl.value && !moreEl.value.contains(event.target as Node)) moreOpen.value = false
}

const closeMoreOnEscape = (event: KeyboardEvent) => {
  if (event.key === 'Escape') moreOpen.value = false
}

watch(() => route.fullPath, () => {
  moreOpen.value = false
  menuOpen.value = false
})

watch(() => navItems.value.map((item) => item.title).join('|'), () => {
  itemWidths.value = []
  void measureNav()
})

const handleScroll = () => {
  isScrolled.value = window.scrollY > 12
}

let navObserver: ResizeObserver | null = null

onMounted(() => {
  handleScroll()
  window.addEventListener('scroll', handleScroll, { passive: true })
  document.addEventListener('pointerdown', closeMoreOutside)
  document.addEventListener('keydown', closeMoreOnEscape)
  void measureNav()
  // Ширины пунктов меняются, когда догружается шрифт, — перемерить.
  void document.fonts?.ready.then(() => {
    itemWidths.value = []
    void measureNav()
  })
  if (typeof ResizeObserver !== 'undefined' && navEl.value) {
    navObserver = new ResizeObserver(onNavResize)
    navObserver.observe(navEl.value)
  }
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  document.removeEventListener('pointerdown', closeMoreOutside)
  document.removeEventListener('keydown', closeMoreOnEscape)
  navObserver?.disconnect()
})
</script>

<style scoped>
.site-header {
  position: fixed;
  inset: 0 0 auto;
  z-index: 50;
  border-bottom: 1px solid transparent;
  background: rgba(246, 244, 238, 0);
  transition: background-color 0.25s ease, border-color 0.25s ease;
}

.site-header-scrolled {
  background: rgba(246, 244, 238, 0.94);
  border-color: var(--line);
  backdrop-filter: blur(10px);
}

.header-inner {
  height: 72px;
  display: flex;
  align-items: center;
  gap: 28px;
}

.brand {
  display: inline-flex;
  align-items: center;
  flex: 0 0 auto;
}

/* Обрезка только по горизонтали: до замера (первый кадр с сервера) лишние пункты не наезжают
   на логотип и кнопки, а выпадающее «Ещё» вниз не обрезается. */
.desktop-nav {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  flex: 1;
  min-width: 0;
  overflow-x: clip;
}

.desktop-nav .nav-link {
  position: relative;
  padding: 8px 9px;
  white-space: nowrap;
  color: var(--ink-2);
  font-size: 0.92rem;
  font-weight: 500;
  transition: color 0.2s ease;
}

/* Черта под пунктом выезжает слева направо. */
.desktop-nav .nav-link::after {
  content: "";
  position: absolute;
  right: 9px;
  bottom: 2px;
  left: 9px;
  height: 1px;
  background: var(--ink);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.25s ease;
}

.desktop-nav .nav-link:hover {
  color: var(--ink);
}

.desktop-nav .nav-link:hover::after {
  transform: scaleX(1);
}

.desktop-nav .nav-link.router-link-active {
  color: var(--ink);
}

.desktop-nav .nav-link.router-link-active::after {
  height: 2px;
  background: var(--sirius-red);
  transform: scaleX(1);
}

/* «Ещё» — тот же вид, что у пунктов, плюс стрелка; активен, если текущая страница внутри. */
.nav-more {
  position: relative;
  flex: none;
}

.nav-more-btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 8px 9px;
  border: 0;
  color: var(--ink-2);
  background: transparent;
  font: inherit;
  font-size: 0.92rem;
  font-weight: 500;
  white-space: nowrap;
  cursor: pointer;
  transition: color 0.2s ease;
}

.nav-more-btn:hover,
.nav-more-btn[aria-expanded="true"] {
  color: var(--ink);
}

.nav-more-btn.active::after {
  content: "";
  position: absolute;
  right: 9px;
  bottom: 2px;
  left: 9px;
  height: 2px;
  background: var(--sirius-red);
}

.nav-more-chevron {
  width: 14px;
  height: 14px;
  transition: transform 0.2s ease;
}

.nav-more-btn[aria-expanded="true"] .nav-more-chevron {
  transform: rotate(180deg);
}

.nav-more-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  z-index: 5;
  min-width: 220px;
  padding: 6px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--paper);
  box-shadow: 0 18px 40px -18px rgba(28, 27, 24, 0.35);
  animation: more-in 0.18s cubic-bezier(0.2, 0.8, 0.2, 1);
}

@keyframes more-in {
  from { opacity: 0; transform: translateY(-4px); }
}

.nav-more-link {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 9px 10px;
  border-radius: var(--radius-sm);
  color: var(--ink-2);
  font-size: 0.92rem;
  font-weight: 500;
  white-space: nowrap;
}

.nav-more-link svg {
  width: 16px;
  height: 16px;
  color: var(--muted);
}

.nav-more-link:hover {
  color: var(--ink);
  background: var(--paper-2);
}

.nav-more-link.router-link-active {
  color: var(--ink);
  box-shadow: inset 2px 0 0 var(--sirius-red);
}

@media (prefers-reduced-motion: reduce) {
  .nav-more-menu {
    animation: none;
  }
}

/* Поиск — только значком, подсказка Ctrl K — во всплывающей подписи. */
.search-btn {
  width: 38px;
  height: 38px;
  display: grid;
  place-items: center;
  border: 1px solid var(--line-strong);
  border-radius: var(--radius-sm);
  color: var(--ink-2);
  background: rgba(251, 250, 247, 0.7);
  cursor: pointer;
  transition: border-color 0.2s ease, color 0.2s ease;
}

.search-btn:hover {
  border-color: var(--ink);
  color: var(--ink);
}

.search-btn svg {
  width: 17px;
  height: 17px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
}

.menu-btn {
  width: 42px;
  height: 42px;
  display: none;
  place-items: center;
  border: 1px solid var(--line-strong);
  border-radius: var(--radius-sm);
  color: var(--ink);
  background: transparent;
}

.menu-btn svg {
  width: 20px;
  height: 20px;
}

.mobile-menu {
  position: fixed;
  inset: 0;
  z-index: 60;
  display: flex;
  justify-content: flex-end;
  background: rgba(28, 27, 24, 0.4);
  animation: fade-in 0.2s ease;
}

.mobile-panel {
  width: min(88vw, 360px);
  height: 100%;
  padding: 20px;
  overflow-y: auto;
  border-left: 1px solid var(--line);
  background: var(--paper);
  animation: slide-in 0.28s cubic-bezier(0.2, 0.8, 0.2, 1);
}

@keyframes fade-in {
  from { opacity: 0; }
}

@keyframes slide-in {
  from { transform: translateX(40px); opacity: 0; }
}

.mobile-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 18px;
}

.mobile-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 4px;
  border-bottom: 1px solid var(--line);
  color: var(--ink-2);
  font-weight: 500;
}

.mobile-link:hover,
.mobile-link.router-link-active {
  color: var(--ink);
}

.mobile-link.router-link-active {
  box-shadow: inset 2px 0 0 var(--sirius-red);
  padding-left: 12px;
}

/* Полоса координат — только на широком экране: на телефоне она съедает первый экран. */
@media (max-width: 767px) {
  .header-hud {
    display: none;
  }
}

/* Влезает меньше трёх пунктов — меню целиком в боковой панели. Место под меню остаётся,
   чтобы при расширении окна снова посчитать, сколько пунктов влезает. */
.nav-collapsed .desktop-nav {
  visibility: hidden;
}

.nav-collapsed .menu-btn {
  display: grid;
}

/* Телефоны и узкие планшеты — сразу боковая панель, без замера. */
@media (max-width: 899px) {
  .desktop-nav {
    display: none;
  }

  .header-inner {
    height: 64px;
  }

  .menu-btn {
    display: grid;
  }
}
</style>
