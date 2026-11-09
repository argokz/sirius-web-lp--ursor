<template>
  <svg class="topo" :class="tone" viewBox="0 0 1200 700" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
    <g class="topo-drift">
      <path
        v-for="(line, i) in LINES"
        :key="i"
        :d="line.d"
        :class="{ index: line.index }"
        pathLength="1"
        :style="{ '--d': `${i * 90}ms` }"
      />
    </g>
  </svg>
</template>

<script setup lang="ts">
/**
 * Фон «как на карте»: горизонтали рельефа вокруг двух вершин. Каждая пятая — утолщённая,
 * как на топографической карте. Линии прорисовываются пером при загрузке, потом медленно плывут.
 * Форма считается детерминированно (без случайных чисел), поэтому сервер и браузер рисуют одно и то же.
 */
withDefaults(defineProps<{ tone?: 'light' | 'dark' }>(), { tone: 'light' })

interface Peak { cx: number; cy: number; levels: number; step: number; seed: number }

const PEAKS: Peak[] = [
  { cx: 930, cy: 210, levels: 11, step: 34, seed: 0.7 },
  { cx: 180, cy: 620, levels: 8, step: 38, seed: 2.1 }
]
const SAMPLES = 72

/** Замкнутая горизонталь: окружность, искажённая гармониками, сглаженная кривыми Катмулла — Рома. */
const contour = (peak: Peak, level: number) => {
  const radius = 26 + level * peak.step
  const points = Array.from({ length: SAMPLES }, (_, i) => {
    const a = (i / SAMPLES) * Math.PI * 2
    const wobble = 1
      + 0.16 * Math.sin(2 * a + peak.seed + level * 0.11)
      + 0.08 * Math.sin(3 * a - peak.seed * 1.7 + level * 0.23)
      + 0.04 * Math.sin(5 * a + level * 0.41)
    return [peak.cx + Math.cos(a) * radius * wobble * 1.25, peak.cy + Math.sin(a) * radius * wobble] as const
  })
  const at = (i: number) => points[(i + SAMPLES) % SAMPLES]!
  let d = `M${at(0)[0].toFixed(1)} ${at(0)[1].toFixed(1)}`
  for (let i = 0; i < SAMPLES; i++) {
    const [p0, p1, p2, p3] = [at(i - 1), at(i), at(i + 1), at(i + 2)]
    const c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6]
    const c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6]
    d += `C${c1[0]!.toFixed(1)} ${c1[1]!.toFixed(1)} ${c2[0]!.toFixed(1)} ${c2[1]!.toFixed(1)} ${p2[0].toFixed(1)} ${p2[1].toFixed(1)}`
  }
  return `${d}Z`
}

const LINES = PEAKS.flatMap((peak) =>
  Array.from({ length: peak.levels }, (_, level) => ({ d: contour(peak, level), index: level % 5 === 4 }))
)
</script>

<style scoped>
.topo {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.topo path {
  fill: none;
  stroke-width: 1;
  vector-effect: non-scaling-stroke;
}

.light path { stroke: rgba(28, 27, 24, 0.14); }
.light path.index { stroke: rgba(192, 4, 15, 0.2); stroke-width: 1.4; }
.dark path { stroke: rgba(246, 244, 238, 0.1); }
.dark path.index { stroke: rgba(255, 107, 94, 0.2); stroke-width: 1.4; }

@media (scripting: enabled) and (prefers-reduced-motion: no-preference) {
  .topo path {
    stroke-dasharray: 1;
    stroke-dashoffset: 1;
    animation: topo-draw 2.6s cubic-bezier(0.55, 0.1, 0.35, 1) var(--d) forwards;
  }

  .topo-drift {
    animation: topo-drift 40s ease-in-out infinite alternate;
  }
}

@keyframes topo-draw {
  to { stroke-dashoffset: 0; }
}

@keyframes topo-drift {
  to { transform: translate(-24px, 14px); }
}
</style>
