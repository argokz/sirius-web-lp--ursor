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
        // значения из настроек CMS попадают в <style> — только цвет #rgb…#rrggbbaa и число, иначе CSS-инъекция
        const color = String(settings.value['theme.primary_color'] ?? '')
        if (/^#[0-9a-f]{3,8}$/i.test(color)) {
          const c = color
          css += `  --sirius-red: ${c};\n`
          css += `  --ui-primary: ${c};\n`
        }
        const radius = Number(settings.value['theme.border_radius'])
        if (settings.value['theme.border_radius'] && Number.isFinite(radius) && radius >= 0 && radius <= 64) {
          const r = radius
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

