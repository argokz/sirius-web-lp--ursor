<template>
  <figure class="sirius-image" :style="{ aspectRatio }">
    <img
      :src="src"
      :alt="alt"
      :loading="eager ? 'eager' : 'lazy'"
      :fetchpriority="eager ? 'high' : undefined"
      decoding="async"
    >
  </figure>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  src: string
  alt?: string
  aspectRatio?: string
  /** Картинка первого экрана: грузить сразу и с высоким приоритетом. */
  eager?: boolean
}>(), {
  alt: '',
  aspectRatio: '16 / 10',
  eager: false
})
</script>

<style scoped>
.sirius-image {
  margin: 0;
  overflow: hidden;
  border-radius: 8px;
  background: #f1f5f9;
}

.sirius-image img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
}
</style>
