<template>
  <img
    class="sirius-logo"
    :class="{ 'sirius-logo-mark': markOnly }"
    :src="markOnly ? '/android-chrome-192x192.png' : '/logo.png'"
    alt="Sirius"
    :style="style"
    decoding="async"
    loading="eager"
  >
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  size?: number | string
  width?: number | string
  markOnly?: boolean
}>(), {
  size: 44,
  width: undefined,
  markOnly: false
})

const addUnit = (value?: number | string) => {
  if (value === undefined) return undefined
  return typeof value === 'number' ? `${value}px` : value
}

const style = computed(() => {
  if (props.markOnly) {
    const size = addUnit(props.size)
    return { width: size, height: size }
  }

  return {
    width: addUnit(props.width || 184),
    height: 'auto'
  }
})
</script>

<style scoped>
.sirius-logo {
  display: block;
  object-fit: contain;
}

.sirius-logo-mark {
  aspect-ratio: 1;
}
</style>
