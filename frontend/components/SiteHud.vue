<template>
  <div class="hud" aria-hidden="true">
    <div class="container hud-inner">
      <span class="hud-city"><i class="hud-dot" />{{ city }}</span>
      <span class="hud-item"><b>LAT</b>{{ latText }}</span>
      <span class="hud-item"><b>LON</b>{{ lonText }}</span>
      <span class="hud-item hud-wide"><b>BRG</b>{{ bearingText }}</span>
      <span class="hud-item hud-wide"><b>ZOOM</b>{{ zoom.toFixed(1) }}</span>
      <span class="hud-item hud-wide"><b>CRS</b>EPSG:4326</span>
      <span class="hud-scale">
        <span class="hud-scale-bar" :style="{ width: `${scale.px}px` }" />
        {{ scale.label }}
      </span>
    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * Полоса координат над шапкой, как у felt.com: курсор «ходит» по карте Алматы.
 * Широта и долгота — от положения курсора на странице, азимут — от центра экрана к курсору,
 * масштаб и линейка — от прокрутки (чем ниже, тем крупнее).
 */
const BBOX = { west: 76.82, east: 77.04, south: 43.18, north: 43.34 }
const ZOOM_TOP = 12
const ZOOM_BOTTOM = 17
const SCALE_TARGET_PX = 72
const EQUATOR_M_PER_PX = 156543.03
const NICE_STEPS = [1, 2, 5]

const city = 'АЛМАТЫ'

const pointer = reactive({ x: 0.5, page: 0.1 })
const bearing = ref(46.2)
const zoom = ref(ZOOM_TOP)

const lat = computed(() => BBOX.north - pointer.page * (BBOX.north - BBOX.south))
const lon = computed(() => BBOX.west + pointer.x * (BBOX.east - BBOX.west))

const latText = computed(() => `${lat.value.toFixed(4)}° N`)
const lonText = computed(() => `${lon.value.toFixed(4)}° E`)
const bearingText = computed(() => `${bearing.value.toFixed(1).padStart(5, '0')}°`)

/** Линейка: «круглое» расстояние (1, 2, 5 × 10ⁿ) около SCALE_TARGET_PX пикселей при текущем масштабе. */
const scale = computed(() => {
  const metersPerPx = EQUATOR_M_PER_PX * Math.cos((lat.value * Math.PI) / 180) / 2 ** zoom.value
  const target = metersPerPx * SCALE_TARGET_PX
  const power = 10 ** Math.floor(Math.log10(target))
  const step = NICE_STEPS.reduce((best, item) => (item * power <= target ? item : best), 1)
  const meters = step * power
  return {
    px: Math.round(meters / metersPerPx),
    label: meters >= 1000 ? `${meters / 1000} km` : `${meters} m`
  }
})

let frame = 0
let lastEvent: { x: number; y: number } | null = null

const update = () => {
  frame = 0
  const doc = document.documentElement
  const scrollable = Math.max(1, doc.scrollHeight - window.innerHeight)
  const progress = Math.min(1, window.scrollY / scrollable)
  zoom.value = ZOOM_TOP + progress * (ZOOM_BOTTOM - ZOOM_TOP)

  const x = lastEvent ? lastEvent.x : window.innerWidth / 2
  const y = lastEvent ? lastEvent.y : window.innerHeight * 0.4
  pointer.x = x / window.innerWidth
  pointer.page = Math.min(1, (window.scrollY + y) / doc.scrollHeight)

  const dx = x - window.innerWidth / 2
  const dy = y - window.innerHeight / 2
  if (lastEvent && Math.hypot(dx, dy) > 4) {
    bearing.value = ((Math.atan2(dx, -dy) * 180) / Math.PI + 360) % 360
  }
}

const schedule = () => {
  if (!frame) frame = requestAnimationFrame(update)
}

const onMove = (event: PointerEvent) => {
  if (event.pointerType === 'touch') return
  lastEvent = { x: event.clientX, y: event.clientY }
  schedule()
}

onMounted(() => {
  update()
  window.addEventListener('pointermove', onMove, { passive: true })
  window.addEventListener('scroll', schedule, { passive: true })
  window.addEventListener('resize', schedule, { passive: true })
})

onBeforeUnmount(() => {
  if (frame) cancelAnimationFrame(frame)
  window.removeEventListener('pointermove', onMove)
  window.removeEventListener('scroll', schedule)
  window.removeEventListener('resize', schedule)
})
</script>

<style scoped>
.hud {
  height: 28px;
  color: var(--on-dark-muted);
  background: var(--dark);
  font-family: var(--mono);
  font-size: 0.68rem;
  letter-spacing: 0.06em;
  font-variant-numeric: tabular-nums;
  user-select: none;
}

.hud-inner {
  height: 100%;
  display: flex;
  align-items: center;
  gap: 22px;
  white-space: nowrap;
  overflow: hidden;
}

.hud-city {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: var(--on-dark);
}

.hud-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #ff6b5e;
  box-shadow: 0 0 0 0 rgba(255, 107, 94, 0.6);
  animation: hud-pulse 2.4s ease-out infinite;
}

@keyframes hud-pulse {
  70% { box-shadow: 0 0 0 6px rgba(255, 107, 94, 0); }
  100% { box-shadow: 0 0 0 0 rgba(255, 107, 94, 0); }
}

.hud-item b {
  margin-right: 8px;
  color: #8b867a;
  font-weight: 500;
}

.hud-scale {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
  color: var(--on-dark);
}

.hud-scale-bar {
  height: 6px;
  border: 1px solid var(--on-dark-muted);
  border-top: 0;
  transition: width 0.25s ease;
}

@media (max-width: 1023px) {
  .hud-wide {
    display: none;
  }
}

@media (prefers-reduced-motion: reduce) {
  .hud-dot { animation: none; }
  .hud-scale-bar { transition: none; }
}
</style>
