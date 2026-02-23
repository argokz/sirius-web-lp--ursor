<template>
  <div class="sirius-logo" :style="{ width: size + 'px', height: size + 'px' }">
    <svg viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
      <!-- Outer Ring -->
      <circle cx="50" cy="50" r="45" stroke="url(#logoGradient)" stroke-width="2" stroke-dasharray="10 5" opacity="0.3">
          <animateTransform attributeName="transform" type="rotate" from="0 50 50" to="360 50 50" dur="20s" repeatCount="indefinite" />
      </circle>
      
      <!-- Inner Star/Nodes -->
      <path d="M50 15L58 42H85L63 58L72 85L50 68L28 85L37 58L15 42H42L50 15Z" fill="white" class="logo-star">
          <animate attributeName="opacity" values="0.9;1;0.9" dur="2s" repeatCount="indefinite" />
      </path>
      
      <!-- Connections -->
      <circle cx="50" cy="50" r="10" fill="white" />
      <circle cx="50" cy="50" r="5" fill="url(#logoGradient)" />

      <defs>
        <linearGradient id="logoGradient" x1="0" y1="0" x2="100" y2="100" gradientUnits="userSpaceOnUse">
          <stop stop-color="#60a5fa" />
          <stop offset="1" stop-color="#a78bfa" />
        </linearGradient>
      </defs>
    </svg>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  size?: number | string
}>()
</script>

<style scoped>
.sirius-logo {
  display: inline-block;
  transition: transform 0.3s ease;
}
.logo-star {
    filter: drop-shadow(0 0 5px rgba(59, 130, 246, 0.5));
}
</style>
