<template>
  <div>
    <div class="d-flex flex-wrap align-center justify-space-between mb-4 ga-4">
      <h1 class="text-h4">SEO метатеги</h1>
      <v-select
        v-model="selectedPageSlug"
        :items="pages"
        item-title="title"
        item-value="slug"
        label="Страница"
        variant="outlined"
        density="comfortable"
        hide-details
        style="max-width: 360px; min-width: 260px;"
      />
    </div>
    
    <v-card elevation="2">
      <v-tabs v-model="tab">
        <v-tab value="general">Общие</v-tab>
        <v-tab value="og">Open Graph</v-tab>
        <v-tab value="twitter">Twitter</v-tab>
      </v-tabs>

      <v-card-text>
        <v-tabs-window v-model="tab">
          <v-tabs-window-item value="general">
            <v-form>
              <v-text-field v-model="seo.title" label="Title" />
              <v-textarea v-model="seo.description" label="Description" rows="3" />
              <v-text-field v-model="seo.keywords" label="Keywords" />
            </v-form>
          </v-tabs-window-item>
          <v-tabs-window-item value="og">
            <v-form>
              <v-text-field v-model="seo.og_title" label="OG Title" />
              <v-textarea v-model="seo.og_description" label="OG Description" rows="3" />
              <v-text-field v-model="seo.og_image" label="OG Image URL" />
              <v-text-field v-model="seo.og_type" label="OG Type" />
            </v-form>
          </v-tabs-window-item>
          <v-tabs-window-item value="twitter">
            <v-form>
              <v-text-field v-model="seo.twitter_title" label="Twitter Title" />
              <v-textarea v-model="seo.twitter_description" label="Twitter Description" rows="3" />
              <v-text-field v-model="seo.twitter_image" label="Twitter Image URL" />
            </v-form>
          </v-tabs-window-item>
        </v-tabs-window>
        
        <v-btn color="primary" class="mt-4" @click="saveSEO" :loading="saving" :disabled="loading">
          Сохранить
        </v-btn>
      </v-card-text>
    </v-card>

    <v-snackbar v-model="snackbar.open" :color="snackbar.color" timeout="3000">
      {{ snackbar.text }}
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, watch, onMounted } from 'vue'

definePageMeta({
  layout: 'admin',
  middleware: 'auth'
})

useHead({
  title: 'SEO метатеги - Сириус'
})

const { token } = useAuth()
const config = useRuntimeConfig()

const tab = ref('general')
const loading = ref(false)
const saving = ref(false)
const pages = ref<{ id: number; slug: string; title: string }[]>([])
const selectedPageSlug = ref('home')

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

const snackbar = reactive({
  open: false,
  text: '',
  color: 'success'
})

const showMessage = (text: string, color: string = 'success') => {
  snackbar.text = text
  snackbar.color = color
  snackbar.open = true
}

const applySeoData = (data: any) => {
  seo.title = data?.title || ''
  seo.description = data?.description || ''
  seo.keywords = data?.keywords || ''
  seo.og_title = data?.og_title || ''
  seo.og_description = data?.og_description || ''
  seo.og_image = data?.og_image || ''
  seo.og_type = data?.og_type || 'website'
  seo.twitter_card = data?.twitter_card || 'summary_large_image'
  seo.twitter_title = data?.twitter_title || ''
  seo.twitter_description = data?.twitter_description || ''
  seo.twitter_image = data?.twitter_image || ''
}

const fetchPages = async () => {
  try {
    const response = await $fetch<{ id: number; slug: string; title: string }[]>(
      `${config.public.apiBase}/api/admin/pages`,
      {
        headers: {
          Authorization: `Bearer ${token.value}`
        }
      }
    )
    pages.value = response
    if (!pages.value.find((page) => page.slug === selectedPageSlug.value) && pages.value.length > 0) {
      selectedPageSlug.value = pages.value[0].slug
    }
  } catch (error: any) {
    showMessage(error?.data?.detail || 'Не удалось загрузить список страниц', 'error')
  }
}

const fetchSEO = async () => {
  if (!token.value || !selectedPageSlug.value) return

  loading.value = true
  try {
    const response = await $fetch(`${config.public.apiBase}/api/admin/seo`, {
      query: { page_slug: selectedPageSlug.value },
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })
    applySeoData(response)
  } catch (error: any) {
    showMessage(error?.data?.detail || 'Не удалось загрузить SEO метаданные', 'error')
  } finally {
    loading.value = false
  }
}

const saveSEO = async () => {
  if (!token.value || !selectedPageSlug.value) return

  saving.value = true
  try {
    await $fetch(`${config.public.apiBase}/api/admin/seo`, {
      method: 'PUT',
      query: { page_slug: selectedPageSlug.value },
      headers: {
        Authorization: `Bearer ${token.value}`
      },
      body: seo
    })
    showMessage('SEO метаданные сохранены')
  } catch (error: any) {
    showMessage(error?.data?.detail || 'Ошибка при сохранении SEO метаданных', 'error')
  } finally {
    saving.value = false
  }
}

watch(selectedPageSlug, () => {
  fetchSEO()
})

onMounted(async () => {
  await fetchPages()
  await fetchSEO()
})
</script>

