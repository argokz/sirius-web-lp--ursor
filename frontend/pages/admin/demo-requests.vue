<template>
  <div class="admin-page">
    <div class="admin-page-header">
      <div>
        <span class="eyebrow">CRM</span>
        <h1 class="admin-title">Заявки на демо (Канбан)</h1>
        <p class="admin-subtitle">Обрабатывайте лиды, перетаскивая их между колонками.</p>
      </div>
      <button class="btn-link btn-secondary" type="button" @click="fetchRequests">Обновить</button>
    </div>

    <p v-if="message" :class="['status-chip', messageType === 'error' ? 'status-danger' : 'status-ok']">{{ message }}</p>

    <div class="kanban-board">
      <div 
        v-for="col in columns" 
        :key="col.value" 
        class="kanban-col"
        @dragover.prevent
        @drop="handleDrop($event, col.value)"
      >
        <div class="kanban-col-header" :class="col.cls">
          <div class="kanban-col-title">
            {{ col.label }}
            <span class="kanban-badge">{{ requestsByStatus[col.value]?.length || 0 }}</span>
          </div>
        </div>
        
        <div class="kanban-items">
          <div 
            v-for="item in requestsByStatus[col.value] || []" 
            :key="item.id" 
            class="kanban-card card card-pad"
            draggable="true"
            @dragstart="handleDragStart($event, item)"
          >
            <div class="kanban-card-header">
              <strong>{{ item.name || item.full_name || 'Без имени' }}</strong>
            </div>
            <div class="kanban-card-body">
              <div v-if="item.company" class="kanban-field"><UIcon name="i-lucide-building" /> {{ item.company }}</div>
              <div class="kanban-field"><UIcon name="i-lucide-mail" /> <a :href="`mailto:${item.email}`">{{ item.email }}</a></div>
              <div v-if="item.phone" class="kanban-field"><UIcon name="i-lucide-phone" /> <a :href="`tel:${item.phone}`">{{ item.phone }}</a></div>
              <div v-if="item.message" class="kanban-message">{{ item.message }}</div>
            </div>
            <div class="kanban-card-footer">
              <small>{{ formatDate(item.created_at) }}</small>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'admin', middleware: 'auth' })
useHead({ title: 'Заявки (Канбан) - CRM Sirius' })

const { token } = useAuth()
const config = useRuntimeConfig()
const requests = ref<any[]>([])
const message = ref('')
const messageType = ref<'success' | 'error'>('success')

const statuses = [
  { value: 'new', label: 'Новые', cls: 'status-danger' },
  { value: 'pending', label: 'Ожидает', cls: 'status-warn' },
  { value: 'contacted', label: 'В работе', cls: 'status-info' },
  { value: 'completed', label: 'Завершено', cls: 'status-ok' }
]
// Use mapping if old statuses exist
const columns = statuses

const requestsByStatus = computed(() => {
  const map: Record<string, any[]> = {}
  columns.forEach(c => map[c.value] = [])
  requests.value.forEach(r => {
    // map "new" vs others
    const status = r.status || 'new'
    if (map[status]) {
      map[status].push(r)
    } else {
      map['new'].push(r)
    }
  })
  return map
})

const notify = (text: string, type: 'success' | 'error' = 'success') => {
  message.value = text
  messageType.value = type
  setTimeout(() => message.value = '', 3000)
}

const formatDate = (value?: string) => value ? new Date(value).toLocaleDateString('ru-RU', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' }) : '-'

const fetchRequests = async () => {
  try {
    requests.value = await $fetch<any[]>(`${config.public.apiBase}/api/admin/demo-requests`, {
      headers: { Authorization: `Bearer ${token.value}` }
    })
  } catch (err: any) {
    notify(err?.data?.detail || 'Не удалось загрузить заявки', 'error')
  }
}

// Drag & Drop state
const handleDragStart = (e: DragEvent, item: any) => {
  if (e.dataTransfer) {
    e.dataTransfer.setData('text/plain', item.id.toString())
    e.dataTransfer.effectAllowed = 'move'
  }
}

const handleDrop = async (e: DragEvent, targetStatus: string) => {
  const itemId = e.dataTransfer?.getData('text/plain')
  if (!itemId) return
  
  const item = requests.value.find(r => r.id.toString() === itemId)
  if (!item || item.status === targetStatus) return

  // Optimistic update
  const oldStatus = item.status
  item.status = targetStatus

  try {
    await $fetch(`${config.public.apiBase}/api/admin/demo-requests/${item.id}`, {
      method: 'PUT',
      headers: { Authorization: `Bearer ${token.value}` },
      body: { status: targetStatus }
    })
    notify('Статус заявки изменен')
  } catch (err: any) {
    // Revert on error
    item.status = oldStatus
    notify(err?.data?.detail || 'Не удалось обновить статус', 'error')
  }
}

onMounted(fetchRequests)
</script>

<style scoped>
.kanban-board {
  display: flex;
  gap: 20px;
  overflow-x: auto;
  padding-bottom: 20px;
  min-height: calc(100vh - 200px);
  align-items: flex-start;
}
.kanban-col {
  flex: 0 0 320px;
  background: #f1f5f9;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  height: 100%;
  max-height: calc(100vh - 200px);
}
.kanban-col-header {
  padding: 16px;
  border-bottom: 1px solid var(--line);
  font-weight: 700;
  font-size: 1.05rem;
}
.kanban-col-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.kanban-badge {
  background: white;
  color: var(--ink);
  padding: 2px 8px;
  border-radius: 99px;
  font-size: 0.8rem;
  font-weight: 800;
  box-shadow: 0 1px 2px rgba(0,0,0,0.05);
}
.kanban-items {
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  overflow-y: auto;
  flex-grow: 1;
}
.kanban-card {
  cursor: grab;
  padding: 16px;
  margin: 0;
  border: 1px solid var(--line);
  box-shadow: 0 2px 4px rgba(0,0,0,0.02);
}
.kanban-card:active {
  cursor: grabbing;
}
.kanban-card-header {
  margin-bottom: 12px;
  font-size: 1.05rem;
  color: var(--ink);
}
.kanban-card-body {
  display: flex;
  flex-direction: column;
  gap: 8px;
  font-size: 0.9rem;
  color: var(--muted);
}
.kanban-field {
  display: flex;
  align-items: center;
  gap: 8px;
}
.kanban-field a {
  color: var(--muted);
  text-decoration: none;
}
.kanban-field a:hover {
  color: var(--sirius-red);
}
.kanban-message {
  margin-top: 8px;
  padding: 8px;
  background: #f8fafc;
  border-radius: 6px;
  font-size: 0.85rem;
  line-height: 1.4;
  white-space: pre-wrap;
}
.kanban-card-footer {
  margin-top: 16px;
  padding-top: 12px;
  border-top: 1px solid var(--line);
  display: flex;
  justify-content: space-between;
  color: var(--muted);
}
</style>
