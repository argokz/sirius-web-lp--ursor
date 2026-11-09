<template>
  <header class="site-header" :class="{ 'site-header-scrolled': isScrolled }">
    <SiteHud class="header-hud" />
    <div class="container header-inner">
      <NuxtLink to="/" class="brand" aria-label="Sirius">
        <SiriusLogo :width="146" />
      </NuxtLink>

      <nav class="desktop-nav" aria-label="Основная навигация">
        <template v-for="item in navItems" :key="item.to">
          <a v-if="item.isExternal" :href="item.to" target="_blank" rel="noopener noreferrer">
            {{ item.title }}
          </a>
          <NuxtLink v-else :to="item.to">
            {{ item.title }}
          </NuxtLink>
        </template>
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
        <UButton to="/contacts" variant="ghost" color="neutral" class="desktop-action">
          Контакты
        </UButton>
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
import { computed, onMounted, onUnmounted, ref } from 'vue'

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

const handleScroll = () => {
  isScrolled.value = window.scrollY > 12
}

onMounted(() => {
  handleScroll()
  window.addEventListener('scroll', handleScroll, { passive: true })
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
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

.desktop-nav {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  flex: 1;
  min-width: 0;
}

.desktop-nav a {
  position: relative;
  padding: 8px 9px;
  white-space: nowrap;
  color: var(--ink-2);
  font-size: 0.92rem;
  font-weight: 500;
  transition: color 0.2s ease;
}

/* Черта под пунктом выезжает слева направо. */
.desktop-nav a::after {
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

.desktop-nav a:hover {
  color: var(--ink);
}

.desktop-nav a:hover::after {
  transform: scaleX(1);
}

.desktop-nav a.router-link-active {
  color: var(--ink);
}

.desktop-nav a.router-link-active::after {
  height: 2px;
  background: var(--sirius-red);
  transform: scaleX(1);
}

/* Девять пунктов меню занимают почти всю ширину: поиск — только значком, подсказка Ctrl K — во всплывающей подписи. */
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

/* Контакты остаются в подвале и мобильном меню; в шапке им не хватает места рядом с девятью пунктами. */
@media (max-width: 1299px) {
  .desktop-action {
    display: none;
  }
}

/* Полоса координат — только на широком экране: на телефоне она съедает первый экран. */
@media (max-width: 767px) {
  .header-hud {
    display: none;
  }
}

/* Девять пунктов меню, логотип, поиск и «Демо» занимают около 1140 px — уже этого меню уходит в боковую панель. */
@media (max-width: 1199px) {
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
