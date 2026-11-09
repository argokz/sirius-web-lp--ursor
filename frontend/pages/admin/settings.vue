<template>
  <div>
    <div class="panel-head">
      <div>
        <h1>Настройки сайта</h1>
        <p>Управление глобальной темой и стилями</p>
      </div>
      <UButton :loading="loading" color="primary" @click="saveSettings">
        Сохранить настройки
      </UButton>
    </div>

    <div v-if="error" class="error-msg">{{ error }}</div>

    <div class="card card-pad" style="margin-top: 24px; max-width: 600px;">
      <h2 style="margin-top:0">Глобальная тема</h2>
      
      <div class="form-grid" style="margin-top: 16px;">
        <label>
          <span class="field-label">Основной цвет бренда (HEX)</span>
          <input v-model="settings['theme.primary_color']" type="color" class="field" style="height: 42px; padding: 4px;">
        </label>
        
        <label>
          <span class="field-label">Скругление углов (px)</span>
          <input v-model.number="settings['theme.border_radius']" type="number" class="field" placeholder="8">
        </label>
      </div>
      
      <p style="margin-top: 16px; color: var(--muted); font-size: 0.9rem;">
        Изменения применятся после перезагрузки страницы (F5) на публичном сайте и в админке.
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

definePageMeta({
  layout: 'admin',
  middleware: 'auth'
})

useHead({ title: 'Настройки сайта - Sirius' })

const { token } = useAuth()

const config = useRuntimeConfig()
const loading = ref(false)
const error = ref('')

const settings = ref<Record<string, string>>({
  'theme.primary_color': '#e30613',
  'theme.border_radius': '8'
})

const loadSettings = async () => {
  try {
    const data = await $fetch<Record<string, string>>(`${config.public.apiBase}/api/site-settings`)
    if (data['theme.primary_color']) settings.value['theme.primary_color'] = data['theme.primary_color']
    if (data['theme.border_radius']) settings.value['theme.border_radius'] = data['theme.border_radius']
  } catch (err: any) {
    console.error(err)
  }
}

const saveSettings = async () => {
  loading.value = true
  error.value = ''
  try {
    for (const [key, value] of Object.entries(settings.value)) {
      await $fetch(`${config.public.apiBase}/api/admin/site-settings/${key}`, {
        method: 'PUT',
        headers: {
          Authorization: `Bearer ${token.value}`
        },
        body: { value: String(value) }
      })
    }
    alert('Настройки сохранены. Перезагрузите страницу для применения.')
  } catch (err: any) {
    error.value = err?.data?.detail || 'Ошибка сохранения'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadSettings()
})
</script>

<style scoped>
.error-msg {
  color: #b91c1c;
  background: #fef2f2;
  padding: 12px;
  border-radius: 8px;
  margin-top: 24px;
}
</style>
