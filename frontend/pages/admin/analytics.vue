<template>
  <div class="admin-page">
    <div class="admin-page-header">
      <div>
        <span class="eyebrow">Аналитика</span>
        <h1 class="admin-title">Показатели сайта и CRM</h1>
        <p class="admin-subtitle">Короткий срез по заявкам, CMS-структуре и посещаемости страниц.</p>
      </div>
      <button class="btn-link btn-secondary" type="button" @click="load">
        <UIcon name="i-lucide-refresh-cw" />
        Обновить
      </button>
    </div>

    <div class="grid grid-4">
      <article v-for="stat in stats" :key="stat.title" class="card card-pad metric-card">
        <span class="pill">{{ stat.badge }}</span>
        <strong>{{ loading ? '...' : stat.value }}</strong>
        <h2>{{ stat.title }}</h2>
        <p>{{ stat.subtitle }}</p>
      </article>
    </div>

    <div class="grid grid-2 analytics-grid">
      <article class="card card-pad">
        <h2>Популярные страницы</h2>
        <div v-if="analytics.top_pages?.length" class="data-list">
          <div v-for="page in analytics.top_pages" :key="page.path">
            <span>{{ page.path }}</span>
            <strong>{{ page.views }}</strong>
          </div>
        </div>
        <p v-else class="muted">Пока нет данных о просмотрах.</p>
      </article>

      <article class="card card-pad">
        <h2>Статусы заявок</h2>
        <div v-if="analytics.requests_by_status?.length" class="data-list">
          <div v-for="status in analytics.requests_by_status" :key="status.status">
            <span>{{ statusLabel(status.status) }}</span>
            <strong>{{ status.count }}</strong>
          </div>
        </div>
        <p v-else class="muted">Заявок пока нет.</p>
      </article>
    </div>

    <article class="card card-pad">
      <h2>Последние заявки</h2>
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr>
              <th>Имя</th>
              <th>Email</th>
              <th>Компания</th>
              <th>Статус</th>
              <th>Дата</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="request in analytics.recent_demo_requests || []" :key="request.id">
              <td>{{ request.full_name }}</td>
              <td>{{ request.email }}</td>
              <td>{{ request.company || '-' }}</td>
              <td>{{ statusLabel(request.status) }}</td>
              <td>{{ request.created_at ? new Date(request.created_at).toLocaleString('ru-RU') : '-' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <p v-if="!(analytics.recent_demo_requests || []).length" class="muted">Новых заявок пока нет.</p>
    </article>

    <p v-if="error" class="status-chip status-danger">{{ error }}</p>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'

definePageMeta({ layout: 'admin', middleware: 'auth' })
useHead({ title: 'Аналитика - CRM Sirius' })

const { token } = useAuth()
const config = useRuntimeConfig()
const loading = ref(false)
const error = ref('')
const analytics = ref<any>({})

const stats = computed(() => [
  { title: 'Всего заявок', value: analytics.value.total_demo_requests || 0, subtitle: 'За все время', badge: 'CRM' },
  { title: 'Ожидают', value: analytics.value.pending_requests || 0, subtitle: 'Нужно обработать', badge: 'Lead' },
  { title: 'Страницы', value: analytics.value.total_pages || 0, subtitle: `${analytics.value.active_pages || 0} активных`, badge: 'CMS' },
  { title: 'Просмотры', value: analytics.value.page_views || 0, subtitle: `${analytics.value.views_today || 0} сегодня`, badge: 'Web' },
  { title: 'Блоки', value: analytics.value.total_blocks || 0, subtitle: `${analytics.value.active_blocks || 0} активных`, badge: 'CMS' },
  { title: 'Пункты меню', value: analytics.value.menu_items || 0, subtitle: `${analytics.value.active_menu_items || 0} активных`, badge: 'Nav' },
  { title: 'Контент', value: analytics.value.total_content_items || 0, subtitle: 'Старый CMS-слой', badge: 'Text' }
])

const statusLabel = (status: string) => ({
  pending: 'Ожидает',
  contacted: 'Связались',
  completed: 'Завершена',
  cancelled: 'Отменена'
}[status] || status)

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
  margin: 18px 0 10px;
  font-size: 2.5rem;
}

.metric-card h2 {
  margin: 0 0 4px;
  font-size: 1.1rem;
  font-weight: 920;
}

.metric-card p,
.muted {
  margin: 0;
  color: var(--muted);
}

.analytics-grid {
  align-items: start;
}

.card h2 {
  margin: 0 0 16px;
  font-size: 1.15rem;
  font-weight: 920;
}

.data-list {
  display: grid;
  gap: 10px;
}

.data-list div {
  display: flex;
  justify-content: space-between;
  gap: 14px;
  padding: 10px 0;
  border-bottom: 1px solid var(--line);
}

.data-list span {
  color: #334155;
  font-weight: 800;
}

.data-list strong {
  color: var(--sirius-red-dark);
}
</style>
