<template>
  <div class="admin-page">
    <div class="admin-page-header">
      <div>
        <span class="eyebrow">CMS</span>
        <h1 class="admin-title">Контент сайта</h1>
        <p class="admin-subtitle">Редактируйте ключевые тексты сайта без деплоя.</p>
      </div>
      <button class="btn-link btn-primary" type="button" @click="openCreate">Добавить</button>
    </div>

    <p v-if="message" :class="['status-chip', messageType === 'error' ? 'status-danger' : 'status-ok']">{{ message }}</p>

    <div class="card card-pad">
      <div class="toolbar">
        <input v-model="search" class="field" placeholder="Поиск по ключу или тексту">
        <span class="pill">{{ filteredItems.length }} элементов</span>
      </div>
      <div class="table-wrap">
        <table class="data-table">
          <thead>
            <tr><th>Ключ</th><th>Тип</th><th>Значение</th><th></th></tr>
          </thead>
          <tbody>
            <tr v-for="item in filteredItems" :key="item.id">
              <td><strong>{{ item.content_key }}</strong></td>
              <td><span class="pill">{{ item.content_type }}</span></td>
              <td class="preview">{{ item.content_value }}</td>
              <td class="actions">
                <button type="button" @click="editItem(item)">Изменить</button>
                <button type="button" class="danger" @click="deleteItem(item)">Удалить</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-if="dialogOpen" class="modal">
      <form class="modal-card card card-pad" @submit.prevent="saveItem">
        <h2>{{ editingItem ? 'Редактировать контент' : 'Добавить контент' }}</h2>
        <label class="field-label">Ключ</label>
        <input v-model="form.content_key" class="field" required>
        <label class="field-label">Тип</label>
        <select v-model="form.content_type" class="field" required>
          <option value="text">text</option>
          <option value="heading">heading</option>
          <option value="title">title</option>
        </select>
        <label class="field-label">Значение</label>
        <textarea v-model="form.content_value" class="field" rows="7" required></textarea>
        <div class="modal-actions">
          <button class="btn-link btn-secondary" type="button" @click="closeDialog">Отмена</button>
          <button class="btn-link btn-primary" type="submit" :disabled="saving">{{ saving ? 'Сохраняем...' : 'Сохранить' }}</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'admin', middleware: 'auth' })
useHead({ title: 'Контент - CRM Sirius' })

const { token } = useAuth()
const config = useRuntimeConfig()
const loading = ref(false)
const saving = ref(false)
const search = ref('')
const dialogOpen = ref(false)
const editingItem = ref<any>(null)
const items = ref<any[]>([])
const message = ref('')
const messageType = ref<'success' | 'error'>('success')
const form = reactive({ content_key: '', content_type: 'text', content_value: '' })

const filteredItems = computed(() => {
  const q = search.value.trim().toLowerCase()
  if (!q) return items.value
  return items.value.filter((item) => `${item.content_key} ${item.content_type} ${item.content_value}`.toLowerCase().includes(q))
})

const notify = (text: string, type: 'success' | 'error' = 'success') => {
  message.value = text
  messageType.value = type
}

const resetForm = () => Object.assign(form, { content_key: '', content_type: 'text', content_value: '' })
const openCreate = () => { editingItem.value = null; resetForm(); dialogOpen.value = true }
const closeDialog = () => { dialogOpen.value = false; editingItem.value = null; resetForm() }

const fetchItems = async () => {
  loading.value = true
  try {
    items.value = await $fetch<any[]>(`${config.public.apiBase}/api/admin/content`, {
      headers: { Authorization: `Bearer ${token.value}` }
    })
  } catch (err: any) {
    notify(err?.data?.detail || 'Не удалось загрузить контент', 'error')
  } finally {
    loading.value = false
  }
}

const editItem = (item: any) => {
  editingItem.value = item
  Object.assign(form, {
    content_key: item.content_key,
    content_type: item.content_type,
    content_value: item.content_value
  })
  dialogOpen.value = true
}

const saveItem = async () => {
  saving.value = true
  try {
    const url = editingItem.value
      ? `${config.public.apiBase}/api/admin/content/${editingItem.value.id}`
      : `${config.public.apiBase}/api/admin/content`
    await $fetch(url, {
      method: editingItem.value ? 'PUT' : 'POST',
      headers: { Authorization: `Bearer ${token.value}` },
      body: form
    })
    notify('Контент сохранён')
    closeDialog()
    await fetchItems()
  } catch (err: any) {
    notify(err?.data?.detail || 'Не удалось сохранить контент', 'error')
  } finally {
    saving.value = false
  }
}

const deleteItem = async (item: any) => {
  if (!confirm(`Удалить ${item.content_key}?`)) return
  try {
    await $fetch(`${config.public.apiBase}/api/admin/content/${item.id}`, {
      method: 'DELETE',
      headers: { Authorization: `Bearer ${token.value}` }
    })
    notify('Контент удалён')
    await fetchItems()
  } catch (err: any) {
    notify(err?.data?.detail || 'Не удалось удалить контент', 'error')
  }
}

onMounted(fetchItems)
</script>

<style scoped>
.toolbar { display: flex; gap: 12px; align-items: center; margin-bottom: 18px; }
.toolbar .field { max-width: 520px; }
.preview { max-width: 640px; color: var(--muted); line-height: 1.5; }
.actions { display: flex; gap: 10px; justify-content: flex-end; }
.actions button { color: var(--sirius-red-dark); font-weight: 850; }
.actions .danger { color: #991b1b; }
.modal { position: fixed; inset: 0; z-index: 70; display: grid; place-items: center; padding: 20px; background: rgba(9, 9, 11, 0.45); }
.modal-card { width: min(100%, 680px); display: grid; gap: 10px; }
.modal-card h2 { margin: 0 0 8px; font-weight: 920; }
.modal-actions { display: flex; justify-content: flex-end; gap: 10px; margin-top: 10px; }
@media (max-width: 640px) { .toolbar { flex-direction: column; align-items: stretch; } .toolbar .field { max-width: none; } }
</style>
