<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'

const { fetchUser } = useAuth()
const { data: settings } = useSiteSettings()

onMounted(() => {
  fetchUser()
})

useHead({
  style: [
    {
      children: computed(() => {
        if (!settings.value) return ''
        let css = ':root {\n'
        if (settings.value['theme.primary_color']) {
          const c = settings.value['theme.primary_color']
          css += `  --sirius-red: ${c};\n`
          css += `  --ui-primary: ${c};\n`
        }
        if (settings.value['theme.border_radius']) {
          const r = settings.value['theme.border_radius']
          css += `  --ui-radius: ${r}px;\n`
          css += `  --radius: ${r}px;\n`
        }
        css += '}'
        return css
      })
    }
  ]
})
</script>

