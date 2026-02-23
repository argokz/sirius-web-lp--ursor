<template>
  <div class="water-flow-container" :class="{'mode-vertical': mode === 'vertical'}" ref="containerRef">
    <svg
      :viewBox="mode === 'vertical' ? '0 0 100 1200' : '0 0 800 400'"
      preserveAspectRatio="xMidYMid slice"
      class="water-flow-svg"
    >
      <defs>
        <!-- Metallic Pipe Gradients -->
        <linearGradient :id="`pipe-grad-${id}`" x1="0%" y1="0%" :x2="mode === 'vertical' ? '100%' : '0%'" :y2="mode === 'vertical' ? '0%' : '100%'">
          <stop offset="0%" style="stop-color:#0f172a" />
          <stop offset="30%" style="stop-color:#334155" />
          <stop offset="50%" style="stop-color:#64748b" />
          <stop offset="70%" style="stop-color:#334155" />
          <stop offset="100%" style="stop-color:#0f172a" />
        </linearGradient>

        <!-- Water Particle Gradients -->
        <linearGradient :id="`water-grad-${id}`">
          <stop offset="0%" style="stop-color:rgba(59, 130, 246, 0)" />
          <stop offset="50%" style="stop-color:rgba(96, 165, 250, 0.8)" />
          <stop offset="100%" style="stop-color:rgba(59, 130, 246, 0)" />
        </linearGradient>

        <!-- Glow Filter -->
        <filter :id="`glow-${id}`" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="2" result="blur" />
          <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>

        <mask :id="`pipe-mask-${id}`">
          <path :d="pathD1" fill="none" stroke="white" :stroke-width="strokeWidth - 4" stroke-linecap="round" />
          <path v-if="pathD2" :d="pathD2" fill="none" stroke="white" :stroke-width="strokeWidth - 4" stroke-linecap="round" />
        </mask>
      </defs>

      <!-- Main Pipe Structure -->
      <g :stroke="`url(#pipe-grad-${id})`" :stroke-width="strokeWidth" fill="none" stroke-linecap="round" stroke-linejoin="round">
        <path :d="pathD1" />
        <path v-if="pathD2" :d="pathD2" />
      </g>

      <!-- Connection Joint Highlights -->
      <g v-if="mode !== 'vertical'" stroke="white" stroke-width="1" opacity="0.1" fill="none">
         <circle cx="350" cy="150" r="15" />
      </g>

      <!-- Flowing Water Layers -->
      <g :mask="`url(#pipe-mask-${id})`">
        <!-- Layer 1: Base Stream -->
        <path :d="pathD" class="water-stream base-stream" />
        
        <!-- Layer 2: Fast Particles -->
        <path :d="pathD" class="water-stream fast-particles" />
        
        <!-- Layer 3: Glowing Highlights -->
        <path :d="pathD" class="water-stream glowing-stream" :filter="`url(#glow-${id})`" />
      </g>

      <!-- Manometers -->
      <g v-for="(gauge, index) in gauges" :key="index" :transform="`translate(${gauge.x}, ${gauge.y})`" class="manometer">
        <!-- Outer Ring -->
        <circle r="18" fill="#1e293b" stroke="#475569" stroke-width="2" />
        <circle r="15" fill="#f8fafc" />
        <!-- Markings -->
        <g stroke="#94a3b8" stroke-width="1">
          <line v-for="n in 8" :key="n" x1="0" y1="-12" x2="0" y2="-15" :transform="`rotate(${n * 45})`" />
        </g>
        <!-- Needle -->
        <g class="needle-anim">
          <path d="M0 2 L0 -12" stroke="#ef4444" stroke-width="2" stroke-linecap="round" />
          <circle r="2" fill="#ef4444" />
        </g>
        <!-- Glass Highlight -->
        <path d="M-10 -10 A 15 15 0 0 1 10 -10" fill="none" stroke="white" stroke-width="2" opacity="0.3" stroke-linecap="round" />
      </g>
    </svg>
    
    <div class="overlay-badge" v-if="showBadge">
        <span class="pulse-icon"></span>
        <span class="badge-text">{{ label || 'FLOW ACTIVE' }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  mode?: 'horizontal' | 'vertical'
  label?: string
  showBadge?: boolean
}>()

const instanceId = Math.random().toString(36).substring(7)
const id = computed(() => `flow-${instanceId}`)
const strokeWidth = computed(() => props.mode === 'vertical' ? 40 : 30)

const pathD1 = computed(() => {
  if (props.mode === 'vertical') {
    return 'M50 0 L50 1200'
  }
  return 'M50 200 L300 200 Q350 200 350 150 L350 50'
})

const pathD2 = computed(() => {
  if (props.mode === 'vertical') return null
  return 'M350 150 Q350 200 400 200 L750 200'
})

const pathD = computed(() => {
  if (props.mode === 'vertical') return pathD1.value
  return `${pathD1.value} ${pathD2.value}`
})

const gauges = computed(() => {
  if (props.mode === 'vertical') {
    return [
      { x: 50, y: 300 },
      { x: 50, y: 900 }
    ]
  }
  return [
    { x: 175, y: 200 },
    { x: 575, y: 200 }
  ]
})
</script>

<style scoped>
.water-flow-container {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
}

.water-flow-svg {
  width: 100%;
  height: 100%;
  display: block;
}

.water-stream {
  fill: none;
  stroke: #3b82f6;
  stroke-linecap: round;
}

.base-stream {
  stroke-width: 12;
  opacity: 0.3;
  stroke-dasharray: 200, 400;
  animation: flow 4s linear infinite;
}

.fast-particles {
  stroke: #60a5fa;
  stroke-width: 4;
  opacity: 0.6;
  stroke-dasharray: 10, 100;
  animation: flow 2s linear infinite;
}

.glowing-stream {
  stroke: #93c5fd;
  stroke-width: 2;
  opacity: 0.8;
  stroke-dasharray: 40, 300;
  animation: flow 3s linear infinite;
}

@keyframes flow {
  from { stroke-dashoffset: 600; }
  to { stroke-dashoffset: 0; }
}

.needle-anim {
  animation: gauge-wiggle 3s ease-in-out infinite;
  transform-origin: 0px 0px;
}

@keyframes gauge-wiggle {
  0%, 100% { transform: rotate(-30deg); }
  50% { transform: rotate(45deg); }
}

.overlay-badge {
  position: absolute;
  top: 20px;
  right: 20px;
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(8px);
  padding: 8px 16px;
  border-radius: 12px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}

.pulse-icon {
  width: 8px;
  height: 8px;
  background: #3b82f6;
  border-radius: 50%;
  box-shadow: 0 0 10px #3b82f6;
  animation: pulse 2s infinite;
}

.badge-text {
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 1px;
  color: white;
}

@keyframes pulse {
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.5); opacity: 0.5; }
  100% { transform: scale(1); opacity: 1; }
}

.mode-vertical .manometer {
  /* Scale down manometers slightly for vertical pipes */
  transform: scale(0.8);
}
</style>

