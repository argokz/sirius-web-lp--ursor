<template>
  <div>
    <h1 class="text-h4 mb-4">Заявки на демо</h1>
    
    <v-card elevation="2">
      <v-data-table
        :headers="headers"
        :items="requests"
        :loading="loading"
      >
        <template v-slot:item.status="{ item }">
          <v-chip :color="getStatusColor(item.status)" size="small">
            {{ getStatusText(item.status) }}
          </v-chip>
        </template>
        <template v-slot:item.actions="{ item }">
          <v-menu>
            <template v-slot:activator="{ props }">
              <v-btn icon="mdi-dots-vertical" v-bind="props" size="small" />
            </template>
            <v-list>
              <v-list-item
                v-for="status in statuses"
                :key="status.value"
                @click="updateStatus(item, status.value)"
              >
                <v-list-item-title>{{ status.label }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>
        </template>
      </v-data-table>
    </v-card>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'admin',
  middleware: 'auth'
})

useHead({
  title: 'Заявки на демо - Сириус'
})

const { token } = useAuth()
const config = useRuntimeConfig()

const loading = ref(false)
const requests = ref([])

const headers = [
  { title: 'ID', key: 'id' },
  { title: 'ФИО', key: 'full_name' },
  { title: 'Email', key: 'email' },
  { title: 'Телефон', key: 'phone' },
  { title: 'Компания', key: 'company' },
  { title: 'Статус', key: 'status' },
  { title: 'Дата', key: 'created_at' },
  { title: 'Действия', key: 'actions', sortable: false }
]

const statuses = [
  { value: 'pending', label: 'Ожидает' },
  { value: 'contacted', label: 'Связались' },
  { value: 'completed', label: 'Завершено' },
  { value: 'cancelled', label: 'Отменено' }
]

const getStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    pending: 'warning',
    contacted: 'info',
    completed: 'success',
    cancelled: 'error'
  }
  return colors[status] || 'grey'
}

const getStatusText = (status: string) => {
  const texts: Record<string, string> = {
    pending: 'Ожидает',
    contacted: 'Связались',
    completed: 'Завершено',
    cancelled: 'Отменено'
  }
  return texts[status] || status
}

const fetchRequests = async () => {
  loading.value = true
  try {
    requests.value = await $fetch(`${config.public.apiBase}/api/admin/demo-requests`, {
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })
  } catch (error) {
    console.error('Error fetching requests:', error)
  } finally {
    loading.value = false
  }
}

const updateStatus = async (item: any, status: string) => {
  try {
    await $fetch(`${config.public.apiBase}/api/admin/demo-requests/${item.id}`, {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${token.value}`
      },
      body: { status }
    })
    fetchRequests()
  } catch (error) {
    console.error('Error updating status:', error)
  }
}

onMounted(() => {
  fetchRequests()
})
</script>

