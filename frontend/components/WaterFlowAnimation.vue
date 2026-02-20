<template>
  <div class="water-flow-container" :class="{'mode-vertical': mode === 'vertical'}" ref="containerRef">
    <svg
      :viewBox="mode === 'vertical' ? '0 0 200 1200' : '0 0 800 400'"
      preserveAspectRatio="xMidYMid slice"
      class="water-flow-svg"
    >
      <defs>
        <linearGradient id="pipeGradient" x1="0%" y1="0%" x2="100%" y2="0%" v-if="mode !== 'vertical'">
          <stop offset="0%" style="stop-color:#334155" />
          <stop offset="40%" style="stop-color:#475569" />
          <stop offset="60%" style="stop-color:#475569" />
          <stop offset="100%" style="stop-color:#1e293b" />
        </linearGradient>
        <linearGradient id="pipeGradientVert" x1="0%" y1="0%" x2="100%" y2="0%" v-else>
          <stop offset="0%" style="stop-color:#334155" />
          <stop offset="50%" style="stop-color:#94a3b8" />
          <stop offset="100%" style="stop-color:#1e293b" />
        </linearGradient>

        <filter id="glow">
          <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
          <feMerge>
            <feMergeNode in="coloredBlur"/>
            <feMergeNode in="SourceGraphic"/>
          </feMerge>
        </filter>

        <mask id="pipeMask">
           <path :d="pathD1" fill="none" stroke="white" stroke-width="26" />
           <path :d="pathD2" v-if="pathD2" fill="none" stroke="white" stroke-width="26" />
        </mask>
      </defs>

      <!-- Background Pipe -->
      <g :stroke="mode === 'vertical' ? 'url(#pipeGradientVert)' : 'url(#pipeGradient)'" stroke-width="30" fill="none" stroke-linecap="round">
        <path :d="pathD1" />
        <path :d="pathD2" v-if="pathD2" />
      </g>

      <!-- Water Content -->
      <g mask="url(#pipeMask)">
        <path :d="pathD1" fill="none" stroke="#3b82f6" stroke-width="20" opacity="0.2" />
        <path :d="pathD2" v-if="pathD2" fill="none" stroke="#3b82f6" stroke-width="20" opacity="0.2" />

        <!-- Animated Water Bits -->
        <path 
          :d="pathD1" 
          fill="none" 
          stroke="#60a5fa" 
          stroke-width="14" 
          stroke-dasharray="30, 150"
          filter="url(#glow)"
        >
          <animate attributeName="stroke-dashoffset" :from="dashOffsetFrom" :to="dashOffsetTo" dur="3s" repeatCount="indefinite" />
        </path>

        <path 
          v-if="pathD2"
          :d="pathD2" 
          fill="none" 
          stroke="#60a5fa" 
          stroke-width="14" 
          stroke-dasharray="30, 150"
          filter="url(#glow)"
        >
          <animate attributeName="stroke-dashoffset" :from="dashOffsetFrom" :to="dashOffsetTo" dur="3s" repeatCount="indefinite" />
        </path>
      </g>

      <!-- Decorative Gauges (only in horizontal mode) -->
      <g v-if="mode !== 'vertical'" transform="translate(150, 175)">
        <circle r="12" fill="white" stroke="#1e293b" stroke-width="2" />
        <path d="M0 0 L0 -8" stroke="#ef4444" stroke-width="2">
          <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="4s" repeatCount="indefinite" />
        </path>
      </g>
    </svg>
    
    <div class="overlay-text" v-if="mode !== 'vertical'">
        <span class="pulse-dot"></span>
        System Active
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  mode?: 'horizontal' | 'vertical'
}>()

const pathD1 = computed(() => {
  if (props.mode === 'vertical') {
    return 'M100 0 L100 1200'
  }
  return 'M50 200 L300 200 Q350 200 350 150 L350 50'
})

const pathD2 = computed(() => {
  if (props.mode === 'vertical') return null
  return 'M350 150 Q350 200 400 200 L750 200'
})

const dashOffsetFrom = computed(() => props.mode === 'vertical' ? '180' : '180')
const dashOffsetTo = computed(() => props.mode === 'vertical' ? '0' : '0')
</script>

<style scoped>
.water-flow-container {
  width: 100%;
  height: 100%;
  background: transparent;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.mode-vertical {
  width: 100px;
  height: 100%;
}

.water-flow-svg {
  width: 100%;
  height: 100%;
}

.overlay-text {
  position: absolute;
  top: 15px;
  right: 15px;
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(8px);
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.7rem;
  color: white;
  display: flex;
  align-items: center;
  border: 1px solid rgba(255,255,255,0.1);
}

.pulse-dot {
  width: 6px;
  height: 6px;
  background: #3b82f6;
  border-radius: 50%;
  margin-right: 6px;
  box-shadow: 0 0 10px #3b82f6;
}
</style>

