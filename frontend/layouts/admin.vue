<template>
  <div class="admin-layout">
    <aside class="admin-sidebar" :class="{ open: sidebarOpen }">
      <div class="admin-brand">
        <SiriusLogo mark-only :size="42" />
        <div>
          <strong>CRM Sirius</strong>
          <span>Конструктор сайта</span>
        </div>
      </div>

      <nav class="admin-nav">
        <NuxtLink v-for="item in menuItems" :key="item.to" :to="item.to" @click="sidebarOpen = false">
          <UIcon :name="item.icon" />
          {{ item.title }}
        </NuxtLink>
      </nav>

      <div class="admin-sidebar-actions">
        <NuxtLink to="/" class="btn-link btn-secondary">
          <UIcon name="i-lucide-external-link" />
          Открыть сайт
        </NuxtLink>
        <button class="btn-link logout-btn" type="button" @click="logout">
          <UIcon name="i-lucide-log-out" />
          Выйти
        </button>
      </div>
    </aside>

    <div v-if="sidebarOpen" class="admin-overlay" @click="sidebarOpen = false"></div>

    <section class="admin-shell">
      <header class="admin-topbar">
        <button class="admin-menu" type="button" @click="sidebarOpen = true">
          <UIcon name="i-lucide-menu" />
        </button>
        <div>
          <strong>Панель управления</strong>
          <span>{{ user?.full_name || 'Администратор' }}</span>
        </div>
      </header>

      <main class="admin-content">
        <slot />
      </main>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

definePageMeta({
  middleware: 'auth'
})

const { logout, user } = useAuth()
const sidebarOpen = ref(false)

const menuItems = [
  { title: 'Дашборд', to: '/admin', icon: 'i-lucide-layout-dashboard' },
  { title: 'Конструктор', to: '/admin/builder', icon: 'i-lucide-panels-top-left' },
  { title: 'Медиа', to: '/admin/media', icon: 'i-lucide-images' },
  { title: 'Контент', to: '/admin/content', icon: 'i-lucide-file-pen-line' },
  { title: 'Настройки', to: '/admin/settings', icon: 'i-lucide-settings' },
  { title: 'SEO', to: '/admin/seo', icon: 'i-lucide-search' },
  { title: 'Заявки', to: '/admin/demo-requests', icon: 'i-lucide-mails' },
  { title: 'Пользователи', to: '/admin/users', icon: 'i-lucide-users' },
  { title: 'Аналитика', to: '/admin/analytics', icon: 'i-lucide-chart-line' }
]
</script>

<style scoped>
.admin-layout {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 288px minmax(0, 1fr);
  background: #f8fafc;
}

.admin-sidebar {
  position: sticky;
  top: 0;
  height: 100vh;
  display: flex;
  flex-direction: column;
  border-right: 1px solid var(--line);
  background: white;
}

.admin-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 20px;
}

.admin-brand strong,
.admin-brand span {
  display: block;
}

.admin-brand strong {
  font-weight: 930;
}

.admin-brand span {
  margin-top: 2px;
  color: var(--muted);
  font-size: 0.84rem;
}

.admin-nav {
  display: grid;
  gap: 4px;
  padding: 0 12px;
}

.admin-nav a {
  display: flex;
  align-items: center;
  gap: 11px;
  padding: 12px;
  border-radius: 8px;
  color: #334155;
  font-weight: 830;
}

.admin-nav a:hover,
.admin-nav a.router-link-active {
  color: var(--sirius-red-dark);
  background: var(--sirius-red-soft);
}

.admin-sidebar-actions {
  display: grid;
  gap: 10px;
  margin-top: auto;
  padding: 16px;
}

.logout-btn {
  color: #991b1b;
  background: #fee2e2;
}

.admin-shell {
  min-width: 0;
}

.admin-topbar {
  height: 70px;
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 0 28px;
  border-bottom: 1px solid var(--line);
  background: rgba(248, 250, 252, 0.88);
  backdrop-filter: blur(14px);
  position: sticky;
  top: 0;
  z-index: 20;
}

.admin-topbar strong,
.admin-topbar span {
  display: block;
}

.admin-topbar span {
  color: var(--muted);
  font-size: 0.86rem;
}

.admin-menu {
  display: none;
  width: 42px;
  height: 42px;
  place-items: center;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: white;
}

.admin-content {
  width: min(100% - 36px, 1380px);
  margin: 0 auto;
  padding: 28px 0 56px;
}

.admin-overlay {
  display: none;
}

@media (max-width: 900px) {
  .admin-layout {
    grid-template-columns: 1fr;
  }

  .admin-sidebar {
    position: fixed;
    inset: 0 auto 0 0;
    z-index: 50;
    width: 288px;
    transform: translateX(-100%);
    transition: transform 0.2s ease;
  }

  .admin-sidebar.open {
    transform: translateX(0);
  }

  .admin-overlay {
    display: block;
    position: fixed;
    inset: 0;
    z-index: 40;
    background: rgba(9, 9, 11, 0.44);
  }

  .admin-menu {
    display: grid;
  }
}
</style>
