<template>
  <v-app>
    <!-- Truly Global Background Animation Layer -->
    <div class="global-animation-layer">
      <div class="global-vertical-pipe main-left">
        <WaterFlowAnimation mode="vertical" />
      </div>
      <div class="global-vertical-pipe main-right">
        <WaterFlowAnimation mode="vertical" />
      </div>
    </div>

    <AppHeader />
    <v-main>
      <slot />
    </v-main>
    <AppFooter />
  </v-app>
</template>

<script setup lang="ts">
import WaterFlowAnimation from '~/components/WaterFlowAnimation.vue'
</script>

<style>
.global-animation-layer {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: none;
  opacity: 0.12;
  background: #0f172a; /* Base site background */
}

.global-vertical-pipe {
  position: absolute;
  top: 0;
  height: 100%;
  width: 120px;
}

.main-left {
  left: 2%;
}

.main-right {
  right: 5%;
  opacity: 0.5;
}

@media (max-width: 960px) {
  .global-animation-layer {
    opacity: 0.08;
  }
  .main-right {
    display: none;
  }
}
</style>

