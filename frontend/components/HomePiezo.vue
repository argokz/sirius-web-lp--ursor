<template>
  <figure ref="rootEl" class="piezo" :class="{ drawn }" aria-label="Пьезометрический график по маршруту от источника до потребителя">
    <header class="piezo-head">
      <span class="piezo-title">Пьезометрический график</span>
      <span class="piezo-route">ТЭЦ-2 → 2КД-14 · 3,2 км · −25 °C</span>
    </header>
    <svg
      ref="svgEl"
      :viewBox="`0 0 ${W} ${H}`"
      class="piezo-svg"
      @pointermove="onPointer"
      @pointerleave="hovering = false"
    >
      <g class="piezo-grid">
        <line v-for="tick in yTicks" :key="`y${tick}`" :x1="PAD.l" :x2="W - PAD.r" :y1="y(tick)" :y2="y(tick)" />
        <text v-for="tick in yTicks" :key="`yt${tick}`" :x="PAD.l - 8" :y="y(tick) + 3" text-anchor="end">{{ tick }}</text>
        <text v-for="tick in xTicks" :key="`xt${tick}`" :x="x(tick)" :y="H - 8" text-anchor="middle">{{ tick }} км</text>
      </g>
      <path :d="groundArea" class="piezo-ground" />
      <path :d="line(STATIC)" class="piezo-static" />
      <path :d="line(SUPPLY)" class="piezo-line piezo-supply" pathLength="1" />
      <path :d="line(RETURN)" class="piezo-line piezo-return" pathLength="1" />
      <g v-for="(node, i) in NODES" :key="node.name" class="piezo-node" :style="{ animationDelay: `${1.2 + i * 0.12}s` }">
        <line :x1="x(node.km)" :x2="x(node.km)" :y1="y(at(SUPPLY, node.km))" :y2="y(at(RETURN, node.km))" />
        <circle :cx="x(node.km)" :cy="y(at(SUPPLY, node.km))" r="3" />
        <circle :cx="x(node.km)" :cy="y(at(RETURN, node.km))" r="3" />
        <text :x="x(node.km)" :y="PAD.t - 6" text-anchor="middle">{{ node.name }}</text>
      </g>
      <g class="piezo-scrub" :transform="`translate(${x(scrubKm)} 0)`">
        <line :y1="PAD.t" :y2="H - PAD.b" />
        <circle :cy="y(at(SUPPLY, scrubKm))" r="4.5" class="dot-supply" />
        <circle :cy="y(at(RETURN, scrubKm))" r="4.5" class="dot-return" />
      </g>
    </svg>
    <figcaption class="piezo-readout">
      <span><i class="sw sw-supply" />H₁ <b>{{ fmt(at(SUPPLY, scrubKm)) }} м</b></span>
      <span><i class="sw sw-return" />H₂ <b>{{ fmt(at(RETURN, scrubKm)) }} м</b></span>
      <span>ΔH <b :class="{ low: dh < MIN_DH }">{{ fmt(dh) }} м</b></span>
      <span class="piezo-km">{{ fmt(scrubKm, 2) }} км</span>
    </figcaption>
  </figure>
</template>

<script setup lang="ts">
/**
 * Пьезометрический график «как в программе»: подающий и обратный напор по маршруту, рельеф,
 * статический напор. Линии прорисовываются при появлении, бегунок ходит сам, пока не наведёшь мышь.
 * Числа условные, но правдоподобные для магистрали Ду 800 при −25 °C.
 */
type Point = [km: number, head: number]

const W = 640
const H = 300
const PAD = { l: 44, r: 16, t: 30, b: 28 }
const KM_MAX = 3.2
const HEAD_MIN = 0
const HEAD_MAX = 120
const MIN_DH = 15
const SWEEP_MS = 9000

const SUPPLY: Point[] = [[0, 112], [0.6, 106], [1.1, 101.5], [1.6, 96], [2.1, 90.5], [2.6, 84], [3.2, 76]]
const RETURN: Point[] = [[0, 28], [0.6, 33], [1.1, 37], [1.6, 41.5], [2.1, 47], [2.6, 54], [3.2, 61.5]]
const GROUND: Point[] = [[0, 8], [0.5, 10], [1, 14], [1.4, 12], [1.9, 18], [2.4, 22], [2.8, 20], [3.2, 26]]
const STATIC: Point[] = [[0, 62], [3.2, 62]]
const NODES = [
  { name: 'ТЭЦ-2', km: 0 }, { name: '2ВВ-5', km: 1.1 }, { name: '2КД-10', km: 2.1 }, { name: '2КД-14', km: 3.2 }
]

const yTicks = [0, 40, 80, 120]
const xTicks = [0, 1, 2, 3]

const x = (km: number) => PAD.l + (km / KM_MAX) * (W - PAD.l - PAD.r)
const y = (head: number) => H - PAD.b - ((head - HEAD_MIN) / (HEAD_MAX - HEAD_MIN)) * (H - PAD.t - PAD.b)

/** Напор в точке маршрута — линейно между соседними точками. */
const at = (points: Point[], km: number) => {
  for (let i = 1; i < points.length; i++) {
    const [k0, h0] = points[i - 1]!
    const [k1, h1] = points[i]!
    if (km <= k1) return h0 + ((km - k0) / (k1 - k0 || 1)) * (h1 - h0)
  }
  return points[points.length - 1]![1]
}

const line = (points: Point[]) => points.map(([km, head], i) => `${i ? 'L' : 'M'}${x(km).toFixed(1)} ${y(head).toFixed(1)}`).join('')
const groundArea = computed(() => `${line(GROUND)}L${x(KM_MAX)} ${y(HEAD_MIN)}L${x(0)} ${y(HEAD_MIN)}Z`)

const fmt = (value: number, digits = 1) => value.toFixed(digits).replace('.', ',')

const rootEl = ref<HTMLElement | null>(null)
const svgEl = ref<SVGSVGElement | null>(null)
const drawn = ref(false)
const hovering = ref(false)
const scrubKm = ref(2.1)
const dh = computed(() => at(SUPPLY, scrubKm.value) - at(RETURN, scrubKm.value))

let frame = 0
let start = 0
let observer: IntersectionObserver | null = null
let onScreen = false

const sweep = (time: number) => {
  frame = 0
  if (!onScreen) return
  if (!start) start = time
  if (!hovering.value) {
    // Туда и обратно по маршруту, плавно у концов.
    const phase = ((time - start) % SWEEP_MS) / SWEEP_MS
    const eased = (1 - Math.cos(phase * Math.PI * 2)) / 2
    scrubKm.value = 0.15 + eased * (KM_MAX - 0.3)
  }
  frame = requestAnimationFrame(sweep)
}

const onPointer = (event: PointerEvent) => {
  const svg = svgEl.value
  if (!svg) return
  const box = svg.getBoundingClientRect()
  const px = ((event.clientX - box.left) / box.width) * W
  hovering.value = true
  scrubKm.value = Math.min(KM_MAX, Math.max(0, ((px - PAD.l) / (W - PAD.l - PAD.r)) * KM_MAX))
}

onMounted(() => {
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  observer = new IntersectionObserver(([entry]) => {
    onScreen = Boolean(entry?.isIntersecting)
    if (onScreen) drawn.value = true
    if (onScreen && !reduced && !frame) frame = requestAnimationFrame(sweep)
  }, { threshold: 0.3 })
  if (rootEl.value) observer.observe(rootEl.value)
})

onBeforeUnmount(() => {
  if (frame) cancelAnimationFrame(frame)
  observer?.disconnect()
})
</script>

<style scoped>
.piezo {
  margin: 0;
  overflow: hidden;
  border: 1px solid var(--ink);
  border-radius: 8px;
  background: var(--surface);
  box-shadow: 0 30px 60px -40px rgba(28, 27, 24, 0.45);
}

.piezo-head {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 10px 14px;
  border-bottom: 1px solid var(--line);
  font-size: 0.85rem;
}

.piezo-title {
  font-weight: 500;
}

.piezo-route {
  color: var(--muted);
  font-family: var(--mono);
  font-size: 0.7rem;
}

.piezo-svg {
  display: block;
  width: 100%;
  height: auto;
  touch-action: pan-y;
  cursor: crosshair;
}

.piezo-grid line {
  stroke: var(--line);
  stroke-dasharray: 2 4;
}

.piezo-grid text,
.piezo-node text {
  fill: var(--muted);
  font-family: var(--mono);
  font-size: 10px;
}

.piezo-ground {
  fill: #e7dfcc;
  stroke: #a8977a;
  stroke-width: 1;
}

.piezo-static {
  fill: none;
  stroke: #6b675c;
  stroke-dasharray: 6 5;
}

.piezo-line {
  fill: none;
  stroke-width: 2.6;
  stroke-linecap: round;
  stroke-dasharray: 1;
  stroke-dashoffset: 1;
}

.piezo-supply { stroke: #b00510; }
.piezo-return { stroke: #1f4fbf; }

.drawn .piezo-line {
  animation: piezo-draw 1.6s cubic-bezier(0.6, 0, 0.2, 1) 0.2s forwards;
}

.drawn .piezo-return {
  animation-delay: 0.45s;
}

.piezo-node {
  opacity: 0;
}

.drawn .piezo-node {
  animation: piezo-fade 0.4s ease forwards;
}

.piezo-node line {
  stroke: var(--line-strong);
}

.piezo-node circle {
  fill: var(--surface);
  stroke: var(--ink);
  stroke-width: 1.4;
}

.piezo-scrub {
  opacity: 0;
  transition: opacity 0.3s ease;
}

.drawn .piezo-scrub {
  opacity: 1;
  transition-delay: 1.8s;
}

.piezo-scrub line {
  stroke: var(--ink);
  stroke-width: 1;
}

.dot-supply,
.dot-return {
  stroke: var(--surface);
  stroke-width: 2;
}

.dot-supply { fill: #b00510; }
.dot-return { fill: #1f4fbf; }

.piezo-readout {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 22px;
  padding: 10px 14px;
  border-top: 1px solid var(--line);
  color: var(--muted);
  font-family: var(--mono);
  font-size: 0.74rem;
  font-variant-numeric: tabular-nums;
}

.piezo-readout b {
  color: var(--ink);
  font-weight: 500;
}

.piezo-readout b.low {
  color: var(--accent);
}

.piezo-km {
  margin-left: auto;
}

.sw {
  display: inline-block;
  width: 14px;
  height: 3px;
  margin-right: 6px;
  vertical-align: middle;
}

.sw-supply { background: #b00510; }
.sw-return { background: #1f4fbf; }

@keyframes piezo-draw {
  to { stroke-dashoffset: 0; }
}

@keyframes piezo-fade {
  to { opacity: 1; }
}

@media (prefers-reduced-motion: reduce) {
  .piezo-line { stroke-dashoffset: 0; }
  .piezo-node { opacity: 1; }
  .drawn .piezo-line,
  .drawn .piezo-node { animation: none; }
}
</style>
