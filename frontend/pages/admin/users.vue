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
  title: 'Управление пользователями - Сириус'
})

const loading = ref(false)
const showDialog = ref(false)
const users = ref([])

const headers = [
  { title: 'ID', key: 'id' },
  { title: 'Email', key: 'email' },
  { title: 'ФИО', key: 'full_name' },
  { title: 'Активен', key: 'is_active' },
  { title: 'Администратор', key: 'is_superuser' },
  { title: 'Дата создания', key: 'created_at' }
]

// TODO: Implement user management API endpoints
</script>

