<template>
  <div class="admin-page">
    <div class="admin-page-header">
      <div>
        <span class="eyebrow">Доступ</span>
        <h1 class="admin-title">Пользователи CRM</h1>
        <p class="admin-subtitle">Управляйте активностью аккаунтов и правами администратора.</p>
      </div>
      <button class="btn-link btn-primary" type="button" @click="dialogOpen = true">Добавить пользователя</button>
    </div>

    <p v-if="message" :class="['status-chip', messageType === 'error' ? 'status-danger' : 'status-ok']">{{ message }}</p>

    <div class="card card-pad table-wrap">
      <table class="data-table">
        <thead>
          <tr><th>Email</th><th>ФИО</th><th>Активен</th><th>Админ</th><th>Создан</th><th></th></tr>
        </thead>
        <tbody>
          <tr v-for="item in users" :key="item.id">
            <td><strong>{{ item.email }}</strong></td>
            <td>{{ item.full_name }}</td>
            <td><span :class="['status-chip', item.is_active ? 'status-ok' : 'status-danger']">{{ item.is_active ? 'Да' : 'Нет' }}</span></td>
            <td><span :class="['status-chip', item.is_superuser ? 'status-info' : 'status-warn']">{{ item.is_superuser ? 'Админ' : 'Пользователь' }}</span></td>
            <td>{{ formatDate(item.created_at) }}</td>
            <td class="actions">
              <button type="button" @click="updateUser(item, { is_active: !item.is_active })">
                {{ item.is_active ? 'Отключить' : 'Включить' }}
              </button>
              <button type="button" @click="toggleSuperuser(item)">
                {{ item.is_superuser ? 'Снять роль' : 'Сделать админом' }}
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="dialogOpen" class="modal">
      <form class="modal-card card card-pad" @submit.prevent="createUser">
        <h2>Добавить пользователя</h2>
        <label class="field-label">Email</label>
        <input v-model="form.email" class="field" type="email" required>
        <label class="field-label">ФИО</label>
        <input v-model="form.full_name" class="field" required>
        <label class="field-label">Пароль</label>
        <input v-model="form.password" class="field" type="password" required minlength="8">
        <label class="check"><input v-model="form.is_active" type="checkbox"> Активен</label>
        <label class="check"><input v-model="form.is_superuser" type="checkbox"> Администратор</label>
        <div class="modal-actions">
          <button class="btn-link btn-secondary" type="button" @click="closeDialog">Отмена</button>
          <button class="btn-link btn-primary" type="submit" :disabled="saving">{{ saving ? 'Создаём...' : 'Создать' }}</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'admin', middleware: 'auth' })
useHead({ title: 'Пользователи - CRM Sirius' })

const { token, user, fetchUser } = useAuth()
const config = useRuntimeConfig()
const users = ref<any[]>([])
const dialogOpen = ref(false)
const saving = ref(false)
const message = ref('')
const messageType = ref<'success' | 'error'>('success')
const form = reactive({ email: '', full_name: '', password: '', is_active: true, is_superuser: false })

const notify = (text: string, type: 'success' | 'error' = 'success') => {
  message.value = text
  messageType.value = type
}

const resetForm = () => Object.assign(form, { email: '', full_name: '', password: '', is_active: true, is_superuser: false })
const closeDialog = () => { dialogOpen.value = false; resetForm() }
const formatDate = (value?: string) => value ? new Date(value).toLocaleString('ru-RU') : '-'

const fetchUsers = async () => {
  try {
    users.value = await $fetch<any[]>(`${config.public.apiBase}/api/admin/users`, {
      headers: { Authorization: `Bearer ${token.value}` }
    })
  } catch (err: any) {
    notify(err?.data?.detail || 'Не удалось загрузить пользователей', 'error')
  }
}

const createUser = async () => {
  saving.value = true
  try {
    await $fetch(`${config.public.apiBase}/api/admin/users`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token.value}` },
      body: form
    })
    notify('Пользователь создан')
    closeDialog()
    await fetchUsers()
  } catch (err: any) {
    notify(err?.data?.detail || 'Не удалось создать пользователя', 'error')
  } finally {
    saving.value = false
  }
}

const updateUser = async (item: any, payload: Record<string, any>) => {
  try {
    await $fetch(`${config.public.apiBase}/api/admin/users/${item.id}`, {
      method: 'PUT',
      headers: { Authorization: `Bearer ${token.value}` },
      body: payload
    })
    notify('Пользователь обновлён')
    await fetchUsers()
    await fetchUser()
  } catch (err: any) {
    notify(err?.data?.detail || 'Не удалось обновить пользователя', 'error')
  }
}

const toggleSuperuser = async (item: any) => {
  if (user.value?.id === item.id && item.is_superuser) {
    notify('Нельзя снять роль администратора у текущего пользователя', 'error')
    return
  }
  await updateUser(item, { is_superuser: !item.is_superuser })
}

onMounted(fetchUsers)
</script>

<style scoped>
.actions { display: flex; gap: 10px; justify-content: flex-end; }
.actions button { color: var(--sirius-red-dark); font-weight: 850; }
.modal { position: fixed; inset: 0; z-index: 70; display: grid; place-items: center; padding: 20px; background: rgba(9, 9, 11, 0.45); }
.modal-card { width: min(100%, 540px); display: grid; gap: 10px; }
.modal-card h2 { margin: 0 0 8px; font-weight: 920; }
.modal-actions { display: flex; justify-content: flex-end; gap: 10px; margin-top: 10px; }
.check { display: flex; gap: 8px; align-items: center; font-weight: 800; color: #334155; }
</style>
