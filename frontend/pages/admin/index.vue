<template>
  <div class="admin-page">
    <div class="admin-page-header">
      <div>
        <span class="eyebrow">Обзор</span>
        <h1 class="admin-title">Дашборд CRM</h1>
        <p class="admin-subtitle">Заявки, страницы, блоки и просмотры сайта в одном рабочем контуре.</p>
      </div>
      <NuxtLink to="/admin/builder" class="btn-link btn-primary">
        <UIcon name="i-lucide-panels-top-left" />
        Открыть конструктор
      </NuxtLink>
    </div>

    <p v-if="error" class="status-chip status-danger">{{ error }}</p>

    <div class="grid grid-4">
      <article v-for="stat in stats" :key="stat.title" class="card card-pad metric-card">
        <div class="icon-box"><UIcon :name="stat.icon" /></div>
        <strong>{{ loading ? '...' : stat.value }}</strong>
        <h2>{{ stat.title }}</h2>
        <p>{{ stat.subtitle }}</p>
      </article>
    </div>

    <div class="grid grid-2 dashboard-grid">
      <article class="card card-pad quick-card">
        <h2>Быстрые действия</h2>
        <div class="quick-actions">
          <NuxtLink class="btn-link btn-secondary" to="/admin/builder">Конструктор</NuxtLink>
          <NuxtLink class="btn-link btn-secondary" to="/admin/seo">SEO</NuxtLink>
          <NuxtLink class="btn-link btn-secondary" to="/admin/demo-requests">Заявки</NuxtLink>
          <NuxtLink class="btn-link btn-secondary" to="/">Сайт</NuxtLink>
        </div>
      </article>

      <article class="card card-pad quick-card">
        <h2>Топ страниц</h2>
        <div v-if="analytics.top_pages?.length" class="mini-list">
          <div v-for="page in analytics.top_pages" :key="page.path">
            <span>{{ page.path }}</span>
            <strong>{{ page.views }}</strong>
          </div>
        </div>
        <p v-else class="muted">Данные появятся после первых просмотров.</p>
      </article>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

definePageMeta({ layout: 'admin', middleware: 'auth' })
useHead({ title: 'CRM Sirius' })

const { token } = useAuth()
const config = useRuntimeConfig()
const loading = ref(false)
const error = ref('')
const analytics = ref<any>({})

const stats = computed(() => [
  { title: 'Всего заявок', value: analytics.value.total_demo_requests || 0, icon: 'i-lucide-mails', subtitle: 'За все время' },
  { title: 'Ожидают обработки', value: analytics.value.pending_requests || 0, icon: 'i-lucide-clock-alert', subtitle: 'Нужно связаться' },
  { title: 'Страницы CMS', value: analytics.value.total_pages || 0, icon: 'i-lucide-file-stack', subtitle: `${analytics.value.active_pages || 0} активных` },
  { title: 'Просмотры сегодня', value: analytics.value.views_today || 0, icon: 'i-lucide-chart-no-axes-combined', subtitle: `${analytics.value.page_views || 0} всего` }
])

const load = async () => {
  loading.value = true
  error.value = ''
  try {
    analytics.value = await $fetch(`${config.public.apiBase}/api/admin/analytics`, {
      headers: { Authorization: `Bearer ${token.value}` }
    })
  } catch (err: any) {
    error.value = err?.data?.detail || 'Не удалось загрузить аналитику'
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.metric-card strong {
  display: block;
  margin-top: 18px;
  font-size: 2.5rem;
  line-height: 1;
}

.metric-card h2 {
  margin: 10px 0 5px;
  font-size: 1.1rem;
  font-weight: 920;
}

.metric-card p,
.muted {
  margin: 0;
  color: var(--muted);
}

.dashboard-grid {
  align-items: start;
}

.quick-card h2 {
  margin: 0 0 16px;
  font-weight: 920;
}

.quick-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.mini-list {
  display: grid;
  gap: 10px;
}

.mini-list div {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid var(--line);
}

.mini-list span {
  color: #334155;
  font-weight: 800;
}

.mini-list strong {
  color: var(--sirius-red-dark);
}
</style>
