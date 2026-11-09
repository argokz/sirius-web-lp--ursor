<template>
  <figure ref="rootEl" class="piezo" :class="{ drawn }" aria-label="Пьезометрический график по маршруту от источника до потребителя">
    <!-- Панель графиков ТГИД (ChartDock): заголовок, кнопки, вкладки — как в приложении. -->
    <header class="piezo-head">
      <svg class="piezo-icon" viewBox="0 0 24 24" aria-hidden="true"><path :d="ICON_CHART" /></svg>
      <span class="piezo-title">Пьезометрический график</span>
      <span class="piezo-route">Длина маршрута 3.2 км · узлов 12</span>
      <span class="piezo-tools" aria-hidden="true">
        <svg v-for="icon in TOOLS" :key="icon" viewBox="0 0 24 24"><path :d="icon" /></svg>
      </span>
    </header>
    <div class="piezo-tabs" aria-hidden="true">
      <span class="active">График</span><span>Таблица узлов</span><span>Время прохождения</span>
    </div>
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
        <text v-for="tick in xTicks" :key="`xt${tick}`" :x="x(tick)" :y="H - 12" text-anchor="middle">{{ tick * 1000 }}</text>
        <text :x="PAD.l - 8" :y="PAD.t - 12" text-anchor="end" class="piezo-axis">H, м</text>
        <text :x="W - PAD.r" :y="H - 12" text-anchor="end" class="piezo-axis">L, м</text>
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
    <div class="piezo-zoom" aria-hidden="true"><i /></div>
    <figcaption class="piezo-readout">
      <span><i class="sw sw-supply" />Подающий <b>{{ fmt(at(SUPPLY, scrubKm)) }} м</b></span>
      <span><i class="sw sw-return" />Обратный <b>{{ fmt(at(RETURN, scrubKm)) }} м</b></span>
      <span>Располагаемый <b :class="{ low: dh < MIN_DH }">{{ fmt(dh) }} м</b></span>
      <span><i class="sw sw-ground" />Рельеф</span>
      <span><i class="sw sw-static" />Статический</span>
      <span class="piezo-km">L = {{ Math.round(scrubKm * 1000) }} м</span>
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
const PAD = { l: 44, r: 16, t: 34, b: 30 }
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

// Значки Material Design Icons, как в панели ТГИД: график, выгрузка, свернуть, закрыть.
const ICON_CHART = 'M3.5 18.5L9.5 12.5L13.5 16.5L22 6.92L20.59 5.5L13.5 13.5L9.5 9.5L2 17L3.5 18.5Z'
const TOOLS = [
  'M5 20H19V18H5M19 9H15V3H9V9H5L12 16L19 9Z',
  'M7.41 8.58L12 13.17L16.59 8.58L18 10L12 16L6 10L7.41 8.58Z',
  'M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z'
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
/* Панель графиков ТГИД: белая, радиус 8, Roboto; цвета линий — как в PiezometerModal. */
.piezo {
  --supply: #e53935;
  --return: #1e88e5;
  --ground: #8d6e63;
  --ground-fill: #d7ccc8;
  --static: #1a237e;
  margin: 0;
  overflow: hidden;
  border-radius: 8px;
  color: var(--app-text);
  background: #fff;
  box-shadow: 0 30px 60px -36px rgba(28, 27, 24, 0.5), 0 0 0 1px rgba(0, 0, 0, 0.08);
  font-family: var(--app-font);
}

.piezo-head {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 4px 10px;
  padding: 10px 12px 8px 14px;
  font-size: 14px;
}

.piezo-icon {
  width: 20px;
  height: 20px;
  fill: var(--app-primary);
}

.piezo-title {
  font-weight: 500;
}

.piezo-route {
  color: var(--app-muted);
  font-size: 12px;
}

.piezo-tools {
  display: flex;
  gap: 10px;
  margin-left: auto;
}

.piezo-tools svg {
  width: 18px;
  height: 18px;
  fill: var(--app-muted);
}

.piezo-tabs {
  display: flex;
  gap: 4px;
  padding: 0 8px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
  font-size: 13px;
  font-weight: 500;
}

.piezo-tabs span {
  padding: 8px 10px;
  color: var(--app-muted);
}

.piezo-tabs .active {
  color: var(--app-primary);
  box-shadow: inset 0 -2px 0 var(--app-primary);
}

.piezo-axis {
  font-weight: 500;
}

.piezo-zoom {
  position: relative;
  height: 6px;
  margin: 0 16px 0 44px;
  border-radius: 3px;
  background: rgba(0, 0, 0, 0.08);
}

.piezo-zoom i {
  position: absolute;
  inset: 0;
  border-radius: 3px;
  background: rgba(21, 101, 192, 0.3);
}

.piezo-zoom i::before,
.piezo-zoom i::after {
  content: "";
  position: absolute;
  top: -4px;
  width: 6px;
  height: 14px;
  border-radius: 2px;
  background: #fff;
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.3);
}

.piezo-zoom i::before { left: -3px; }
.piezo-zoom i::after { right: -3px; }

.piezo-svg {
  display: block;
  width: 100%;
  height: auto;
  touch-action: pan-y;
  cursor: crosshair;
}

.piezo-grid line {
  stroke: rgba(0, 0, 0, 0.08);
}

.piezo-grid text,
.piezo-node text {
  fill: var(--app-muted);
  font-size: 10px;
}

.piezo-ground {
  fill: var(--ground-fill);
  stroke: var(--ground);
  stroke-width: 1.2;
}

.piezo-static {
  fill: none;
  stroke: var(--static);
  stroke-width: 1.4;
}

.piezo-line {
  fill: none;
  stroke-width: 2.6;
  stroke-linecap: round;
  stroke-dasharray: 1;
  stroke-dashoffset: 1;
}

.piezo-supply { stroke: var(--supply); }
.piezo-return { stroke: var(--return); }

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
  stroke: rgba(0, 0, 0, 0.18);
}

.piezo-node circle {
  fill: #fff;
  stroke: var(--app-text);
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
  stroke: rgba(0, 0, 0, 0.5);
  stroke-width: 1;
  stroke-dasharray: 3 3;
}

.dot-supply,
.dot-return {
  stroke: #fff;
  stroke-width: 2;
}

.dot-supply { fill: var(--supply); }
.dot-return { fill: var(--return); }

.piezo-readout {
  display: flex;
  flex-wrap: wrap;
  gap: 6px 18px;
  padding: 10px 14px 12px;
  color: var(--app-muted);
  font-size: 12px;
  font-variant-numeric: tabular-nums;
}

.piezo-readout b {
  color: var(--app-text);
  font-weight: 500;
}

.piezo-readout b.low {
  color: var(--app-error);
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

.sw-supply { background: var(--supply); }
.sw-return { background: var(--return); }
.sw-ground { height: 8px; background: var(--ground-fill); box-shadow: inset 0 2px 0 var(--ground); }
.sw-static { background: var(--static); }

@media (max-width: 480px) {
  .piezo-tools {
    display: none;
  }

  .piezo-tabs span:last-child {
    display: none;
  }
}

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
