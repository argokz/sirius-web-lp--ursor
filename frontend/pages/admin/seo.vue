<template>
  <div class="admin-page">
    <div class="admin-page-header">
      <div>
        <span class="eyebrow">SEO</span>
        <h1 class="admin-title">Метаданные страниц</h1>
        <p class="admin-subtitle">Управляйте title, description и превью для социальных сетей.</p>
      </div>
      <select v-model="selectedPageSlug" class="field page-select">
        <option v-for="page in pages" :key="page.slug" :value="page.slug">{{ page.title }}</option>
      </select>
    </div>

    <p v-if="message" :class="['status-chip', messageType === 'error' ? 'status-danger' : 'status-ok']">{{ message }}</p>

    <form class="card card-pad seo-form" @submit.prevent="saveSEO">
      <div class="grid grid-2">
        <label>
          <span class="field-label">Title</span>
          <input v-model="seo.title" class="field">
        </label>
        <label>
          <span class="field-label">Keywords</span>
          <input v-model="seo.keywords" class="field">
        </label>
      </div>
      <label>
        <span class="field-label">Description</span>
        <textarea v-model="seo.description" class="field" rows="3"></textarea>
      </label>
      <div class="grid grid-2">
        <label>
          <span class="field-label">OG title</span>
          <input v-model="seo.og_title" class="field">
        </label>
        <label>
          <span class="field-label">OG image</span>
          <input v-model="seo.og_image" class="field">
        </label>
      </div>
      <label>
        <span class="field-label">OG description</span>
        <textarea v-model="seo.og_description" class="field" rows="3"></textarea>
      </label>
      <div class="grid grid-2">
        <label>
          <span class="field-label">Twitter title</span>
          <input v-model="seo.twitter_title" class="field">
        </label>
        <label>
          <span class="field-label">Twitter image</span>
          <input v-model="seo.twitter_image" class="field">
        </label>
      </div>
      <label>
        <span class="field-label">Twitter description</span>
        <textarea v-model="seo.twitter_description" class="field" rows="3"></textarea>
      </label>
      <button class="btn-link btn-primary" type="submit" :disabled="saving">
        {{ saving ? 'Сохраняем...' : 'Сохранить SEO' }}
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
definePageMeta({ layout: 'admin', middleware: 'auth' })
useHead({ title: 'SEO - CRM Sirius' })

const { token } = useAuth()
const config = useRuntimeConfig()
const selectedPageSlug = ref('home')
const pages = ref<{ id: number; slug: string; title: string }[]>([])
const saving = ref(false)
const message = ref('')
const messageType = ref<'success' | 'error'>('success')
const seo = reactive({
  title: '',
  description: '',
  keywords: '',
  og_title: '',
  og_description: '',
  og_image: '',
  og_type: 'website',
  twitter_card: 'summary_large_image',
  twitter_title: '',
  twitter_description: '',
  twitter_image: ''
})

const notify = (text: string, type: 'success' | 'error' = 'success') => {
  message.value = text
  messageType.value = type
}

const applySeo = (data: any = {}) => {
  for (const key of Object.keys(seo) as Array<keyof typeof seo>) {
    ;(seo[key] as string) = data[key] || (key === 'og_type' ? 'website' : key === 'twitter_card' ? 'summary_large_image' : '')
  }
}

const fetchPages = async () => {
  try {
    pages.value = await $fetch(`${config.public.apiBase}/api/admin/pages`, {
      headers: { Authorization: `Bearer ${token.value}` }
    })
    if (pages.value.length && !pages.value.some((page) => page.slug === selectedPageSlug.value)) {
      selectedPageSlug.value = pages.value[0].slug
    }
  } catch (err: any) {
    notify(err?.data?.detail || 'Не удалось загрузить страницы', 'error')
  }
}

const fetchSEO = async () => {
  if (!selectedPageSlug.value) return
  try {
    const data = await $fetch(`${config.public.apiBase}/api/admin/seo`, {
      query: { page_slug: selectedPageSlug.value },
      headers: { Authorization: `Bearer ${token.value}` }
    })
    applySeo(data)
  } catch (err: any) {
    notify(err?.data?.detail || 'Не удалось загрузить SEO', 'error')
  }
}

const saveSEO = async () => {
  saving.value = true
  try {
    await $fetch(`${config.public.apiBase}/api/admin/seo`, {
      method: 'PUT',
      query: { page_slug: selectedPageSlug.value },
      headers: { Authorization: `Bearer ${token.value}` },
      body: seo
    })
    notify('SEO сохранено')
  } catch (err: any) {
    notify(err?.data?.detail || 'Не удалось сохранить SEO', 'error')
  } finally {
    saving.value = false
  }
}

watch(selectedPageSlug, fetchSEO)
onMounted(async () => {
  await fetchPages()
  await fetchSEO()
})
</script>

<style scoped>
.page-select { max-width: 320px; }
.seo-form { display: grid; gap: 16px; }
button { width: fit-content; }
</style>
