<template>
  <div v-if="hasCmsBlocks" class="page dynamic-page">
    <CmsBlockRenderer v-for="block in leadingBlocks" :key="block.id" :block="block" :page-slug="slug" />
    <slot name="append" />
    <CmsBlockRenderer v-if="ctaBlock" :key="ctaBlock.id" :block="ctaBlock" :page-slug="slug" />
  </div>
  <template v-else>
    <slot />
    <slot name="append" />
  </template>
</template>

<script setup lang="ts">
import type { CmsBlock } from '~/components/CmsBlockRenderer.vue'

interface CmsPageResponse {
  page: {
    id: number
    slug: string
    title: string
  }
  blocks: CmsBlock[]
}

const props = defineProps<{
  slug: string
}>()

const config = useRuntimeConfig()

const { data: pageData } = useAsyncData<CmsPageResponse | null>(
  `cms-page-override-${props.slug}`,
  async () => {
    try {
      return await $fetch<CmsPageResponse>(`${config.public.apiBase}/api/site/pages/${props.slug}`, {
        timeout: 3000
      })
    } catch {
      return null
    }
  },
  {
    default: () => null
  }
)

const blocks = computed(() => pageData.value?.blocks || [])
const hasCmsBlocks = computed(() => blocks.value.length > 0)

// Дополнительные секции страницы (слот append) встают перед завершающим призывом к действию.
const ctaBlock = computed(() => {
  const last = blocks.value[blocks.value.length - 1]
  return last?.block_type === 'cta' ? last : null
})
const leadingBlocks = computed(() => (ctaBlock.value ? blocks.value.slice(0, -1) : blocks.value))
</script>
