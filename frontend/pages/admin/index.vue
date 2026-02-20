<template>
  <div>
    <h1 class="text-h4 mb-4">Панель управления</h1>
    <v-row>
      <v-col
        cols="12"
        md="4"
        v-for="(stat, index) in stats"
        :key="index"
      >
        <v-card elevation="2">
          <v-card-title>
            <v-icon :icon="stat.icon" :color="stat.color" class="mr-2" />
            {{ stat.title }}
          </v-card-title>
          <v-card-text>
            <div class="text-h3">{{ stat.value }}</div>
            <div class="text-caption text-grey">{{ stat.subtitle }}</div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'admin',
  middleware: 'auth'
})

useHead({
  title: 'Панель управления - Сириус'
})

const { token } = useAuth()
const stats = ref([
  { title: 'Всего заявок', value: 0, icon: 'mdi-email', color: 'primary', subtitle: 'За все время' },
  { title: 'Ожидают обработки', value: 0, icon: 'mdi-clock', color: 'warning', subtitle: 'Требуют внимания' },
  { title: 'Элементов контента', value: 0, icon: 'mdi-file-document', color: 'success', subtitle: 'Всего на сайте' }
])

onMounted(async () => {
  if (token.value) {
    try {
      const config = useRuntimeConfig()
      const analytics = await $fetch(`${config.public.apiBase}/api/admin/analytics`, {
        headers: {
          Authorization: `Bearer ${token.value}`
        }
      })
      
      stats.value[0].value = analytics.total_demo_requests || 0
      stats.value[1].value = analytics.pending_requests || 0
      stats.value[2].value = analytics.total_content_items || 0
    } catch (error) {
      console.error('Error fetching analytics:', error)
    }
  }
})
</script>

