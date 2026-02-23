<template>
  <div>
    <div class="d-flex justify-space-between align-center mb-4">
      <h1 class="text-h4">Управление пользователями</h1>
      <v-btn color="primary" @click="showDialog = true">
        <v-icon icon="mdi-plus" class="mr-2" />
        Добавить пользователя
      </v-btn>
    </div>

    <v-card elevation="2">
      <v-data-table
        :headers="headers"
        :items="users"
        :loading="loading"
      >
        <template v-slot:item.is_active="{ item }">
          <v-chip :color="item.is_active ? 'success' : 'error'" size="small">
            {{ item.is_active ? 'Активен' : 'Неактивен' }}
          </v-chip>
        </template>
        <template v-slot:item.is_superuser="{ item }">
          <v-icon :color="item.is_superuser ? 'primary' : 'grey'">
            {{ item.is_superuser ? 'mdi-shield-check' : 'mdi-shield-off' }}
          </v-icon>
        </template>
        <template v-slot:item.created_at="{ item }">
          {{ formatDate(item.created_at) }}
        </template>
        <template v-slot:item.actions="{ item }">
          <v-btn
            size="small"
            variant="text"
            :icon="item.is_active ? 'mdi-account-off' : 'mdi-account-check'"
            :color="item.is_active ? 'warning' : 'success'"
            @click="toggleActive(item)"
          />
          <v-btn
            size="small"
            variant="text"
            :icon="item.is_superuser ? 'mdi-shield-off' : 'mdi-shield-plus'"
            color="primary"
            @click="toggleSuperuser(item)"
          />
        </template>
      </v-data-table>
    </v-card>

    <v-dialog v-model="showDialog" max-width="520">
      <v-card>
        <v-card-title>Добавить пользователя</v-card-title>
        <v-card-text>
          <v-form v-model="valid">
            <v-text-field
              v-model="form.email"
              label="Email"
              type="email"
              :rules="[rules.required, rules.email]"
            />
            <v-text-field
              v-model="form.full_name"
              label="ФИО"
              :rules="[rules.required]"
            />
            <v-text-field
              v-model="form.password"
              label="Пароль"
              type="password"
              :rules="[rules.required, rules.minPassword]"
            />
            <v-switch v-model="form.is_active" label="Активный пользователь" color="success" />
            <v-switch v-model="form.is_superuser" label="Администратор" color="primary" />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="closeDialog">Отмена</v-btn>
          <v-btn color="primary" :loading="saving" :disabled="!valid" @click="createUser">
            Создать
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar v-model="snackbar.open" :color="snackbar.color" timeout="3000">
      {{ snackbar.text }}
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'

definePageMeta({
  layout: 'admin',
  middleware: 'auth'
})

useHead({
  title: 'Управление пользователями - Сириус'
})

const { token, user, fetchUser } = useAuth()
const config = useRuntimeConfig()

const loading = ref(false)
const showDialog = ref(false)
const saving = ref(false)
const valid = ref(false)
const users = ref<any[]>([])

const form = reactive({
  email: '',
  full_name: '',
  password: '',
  is_active: true,
  is_superuser: false
})

const snackbar = reactive({
  open: false,
  text: '',
  color: 'success'
})

const headers = [
  { title: 'ID', key: 'id' },
  { title: 'Email', key: 'email' },
  { title: 'ФИО', key: 'full_name' },
  { title: 'Активен', key: 'is_active' },
  { title: 'Администратор', key: 'is_superuser' },
  { title: 'Дата создания', key: 'created_at' },
  { title: 'Действия', key: 'actions', sortable: false }
]

const rules = {
  required: (value: string) => !!value || 'Обязательное поле',
  email: (value: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value) || 'Некорректный email',
  minPassword: (value: string) => value.length >= 8 || 'Минимум 8 символов'
}

const showMessage = (text: string, color: string = 'success') => {
  snackbar.text = text
  snackbar.color = color
  snackbar.open = true
}

const formatDate = (value?: string) => {
  if (!value) return '-'
  return new Date(value).toLocaleString('ru-RU')
}

const fetchUsers = async () => {
  loading.value = true
  try {
    users.value = await $fetch(`${config.public.apiBase}/api/admin/users`, {
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })
  } catch (error: any) {
    showMessage(error?.data?.detail || 'Не удалось загрузить пользователей', 'error')
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  form.email = ''
  form.full_name = ''
  form.password = ''
  form.is_active = true
  form.is_superuser = false
  valid.value = false
}

const closeDialog = () => {
  showDialog.value = false
  resetForm()
}

const createUser = async () => {
  saving.value = true
  try {
    await $fetch(`${config.public.apiBase}/api/admin/users`, {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token.value}`
      },
      body: form
    })
    closeDialog()
    showMessage('Пользователь создан')
    await fetchUsers()
  } catch (error: any) {
    showMessage(error?.data?.detail || 'Не удалось создать пользователя', 'error')
  } finally {
    saving.value = false
  }
}

const updateUser = async (item: any, payload: Record<string, any>) => {
  try {
    await $fetch(`${config.public.apiBase}/api/admin/users/${item.id}`, {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${token.value}`
      },
      body: payload
    })
    await fetchUsers()
    await fetchUser()
  } catch (error: any) {
    showMessage(error?.data?.detail || 'Не удалось обновить пользователя', 'error')
  }
}

const toggleActive = async (item: any) => {
  await updateUser(item, { is_active: !item.is_active })
}

const toggleSuperuser = async (item: any) => {
  if (user.value?.id === item.id && item.is_superuser) {
    showMessage('Нельзя снять роль администратора у текущего пользователя', 'error')
    return
  }
  await updateUser(item, { is_superuser: !item.is_superuser })
}

onMounted(() => {
  fetchUsers()
})
</script>

