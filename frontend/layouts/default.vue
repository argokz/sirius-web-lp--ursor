<template>
  <div class="default-layout">
    <AppHeader />
    <main>
      <slot />
    </main>
    <AppFooter />
  </div>
</template>

<script setup lang="ts">
useAnalytics()
</script>

<style scoped>
.default-layout {
  min-height: 100vh;
}

main {
  min-height: 70vh;
}
</style>
