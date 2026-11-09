<template>
  <div class="page dynamic-page">
    <template v-if="blocks.length">
      <CmsBlockRenderer v-for="block in blocks" :key="block.id" :block="block" />
    </template>

    <section v-else class="page-hero">
      <div class="container">
        <UBadge color="primary" variant="subtle" size="lg">CMS</UBadge>
        <h1 class="display-title">{{ pageTitle }}</h1>
        <p class="lead">Страница создана в CRM. Добавьте первый блок в конструкторе, чтобы наполнить ее содержанием.</p>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { CmsBlock } from '~/components/CmsBlockRenderer.vue'

interface CmsPageResponse {
  page: {
    id: number
    slug: string
    title: string
  }
  blocks: CmsBlock[]
  seo?: {
    title?: string
    description?: string
    keywords?: string
    og_title?: string
    og_description?: string
    og_image?: string
    twitter_title?: string
    twitter_description?: string
    twitter_image?: string
  } | null
}

const route = useRoute()
const config = useRuntimeConfig()
const slug = computed(() => {
  const value = route.params.slug
  return Array.isArray(value) ? value.join('/') : String(value || '')
})

const { data: pageData, error } = await useAsyncData<CmsPageResponse>(
  `cms-page-${slug.value}`,
  () => $fetch<CmsPageResponse>(`${config.public.apiBase}/api/site/pages/${slug.value}`, {
    timeout: 3000
  }),
  { watch: [slug] }
)

if (error.value) {
  throw createError({ statusCode: 404, statusMessage: 'Страница не найдена' })
}

const blocks = computed(() => pageData.value?.blocks || [])
const pageTitle = computed(() => pageData.value?.page.title || 'Страница')

useHead(() => {
  const seo = pageData.value?.seo
  const title = seo?.title || pageTitle.value
  const description = seo?.description || seo?.og_description || ''

  return {
    title,
    meta: [
      { name: 'description', content: description },
      { name: 'keywords', content: seo?.keywords || '' },
      { property: 'og:title', content: seo?.og_title || title },
      { property: 'og:description', content: seo?.og_description || description },
      { property: 'og:image', content: seo?.og_image || '/og-sirius.jpg' },
      { name: 'twitter:title', content: seo?.twitter_title || title },
      { name: 'twitter:description', content: seo?.twitter_description || description },
      { name: 'twitter:image', content: seo?.twitter_image || seo?.og_image || '/og-sirius.jpg' }
    ]
  }
})
</script>

<style scoped>
.page-hero {
  padding: 132px 0 88px;
}
</style>
