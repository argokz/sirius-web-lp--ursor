<template>
  <figure ref="rootEl" class="flow" :class="{ on: inView }" aria-label="Схема: какие данные приходят в ТГИД и куда уходят">
    <!-- Провода между колонками считаются по положению карточек, поэтому не зависят от ширины. -->
    <svg v-if="wires.length" class="flow-wires" :viewBox="`0 0 ${box.w} ${box.h}`" aria-hidden="true">
      <path v-for="(wire, i) in wires" :key="wire.id" :d="wire.d" class="wire" :class="wire.side" pathLength="1" :style="{ '--i': i }" />
      <template v-if="inView && motion">
        <circle v-for="(wire, i) in wires" :key="`p${wire.id}`" r="3.2" class="packet" :class="wire.side">
          <animateMotion :path="wire.d" :dur="`${2.6 + (i % 3) * 0.5}s`" :begin="`${1.4 + i * 0.37}s`" repeatCount="indefinite" />
        </circle>
      </template>
    </svg>

    <div class="flow-col">
      <span class="flow-label">Что приходит</span>
      <div v-for="item in SOURCES" :key="item.title" ref="srcEls" class="flow-item">
        <UIcon :name="item.icon" class="flow-icon" />
        <span><b>{{ item.title }}</b><small>{{ item.text }}</small></span>
      </div>
    </div>

    <div ref="coreEl" class="flow-core">
      <span class="flow-label">ТГИД</span>
      <div class="core-box">
        <div v-for="layer in CORE" :key="layer.title" class="core-layer">
          <b>{{ layer.title }}</b>
          <small>{{ layer.text }}</small>
        </div>
        <i class="core-pulse" />
      </div>
    </div>

    <div class="flow-col">
      <span class="flow-label">Что уходит</span>
      <div v-for="item in OUTPUTS" :key="item.title" ref="outEls" class="flow-item">
        <UIcon :name="item.icon" class="flow-icon" />
        <span><b>{{ item.title }}</b><small>{{ item.text }}</small></span>
      </div>
    </div>
  </figure>
</template>

<script setup lang="ts">
/**
 * Инфографика «откуда данные и куда»: источники → база города и расчёт → потребители данных.
 * Все пункты — существующие функции (справка: 07-source-data, 05-analysis, 14-developers).
 * На узком экране колонки встают друг под друга, провода заменяются стрелками.
 */
const SOURCES = [
  { icon: 'i-lucide-monitor', title: 'Десктоп ТГИД', text: 'та же база города' },
  { icon: 'i-lucide-import', title: 'ZuluGIS', text: 'перенос с пересчётом координат' },
  { icon: 'i-lucide-file-spreadsheet', title: 'SHP · GPKG · Excel', text: 'импорт слоёв и таблиц' },
  { icon: 'i-lucide-gauge', title: 'SCADA · ОДПУ', text: 'OPC UA, показания датчиков' },
  { icon: 'i-lucide-cloud-sun', title: 'Open-Meteo', text: 'прогноз погоды для режима' },
  { icon: 'i-lucide-hard-hat', title: 'Бригады', text: 'обходы, дефекты и фото' }
]

const CORE = [
  { title: 'База города', text: 'PostgreSQL · PostGIS' },
  { title: 'Расчёт heatnet', text: 'гидравлика и тепло' },
  { title: 'Права и журнал', text: 'кто что видел и менял' }
]

const OUTPUTS = [
  { icon: 'i-lucide-map', title: 'Карта и окна', text: 'браузер, 3D, печать' },
  { icon: 'i-lucide-sparkles', title: 'Помощник ИИ · MCP', text: 'вопросы словами' },
  { icon: 'i-lucide-webhook', title: 'API v2 · вебхуки', text: '1С, ERP, диспетчерская' },
  { icon: 'i-lucide-layers', title: 'OGC API · ArcGIS', text: 'слои для ГИС, только чтение' },
  { icon: 'i-lucide-megaphone', title: 'Лента отключений', text: 'для жителей города' },
  { icon: 'i-lucide-file-text', title: 'Excel · Word', text: 'отчёты и глава «Электронная модель»' }
]

const rootEl = ref<HTMLElement | null>(null)
const coreEl = ref<HTMLElement | null>(null)
const srcEls = ref<HTMLElement[]>([])
const outEls = ref<HTMLElement[]>([])
const inView = useInView(rootEl, 0.25)
const motion = useMotionAllowed()

const box = reactive({ w: 0, h: 0 })
const wires = ref<Array<{ id: string; d: string; side: 'in' | 'out' }>>([])

/** Кривая от правого края источника к ядру и от ядра к левому краю получателя. */
const layout = () => {
  const root = rootEl.value
  const core = coreEl.value?.querySelector('.core-box') as HTMLElement | null
  if (!root || !core) return
  const r = root.getBoundingClientRect()
  // Колонки друг под другом — проводов нет.
  if (getComputedStyle(root).gridTemplateColumns.split(' ').length < 3) {
    wires.value = []
    return
  }
  const c = core.getBoundingClientRect()
  box.w = r.width
  box.h = r.height
  const coreY = (i: number, n: number) => c.top - r.top + c.height / 2 + (i - (n - 1) / 2) * 14
  const curve = (x1: number, y1: number, x2: number, y2: number) => {
    const dx = (x2 - x1) * 0.5
    return `M${x1.toFixed(1)} ${y1.toFixed(1)}C${(x1 + dx).toFixed(1)} ${y1.toFixed(1)} ${(x2 - dx).toFixed(1)} ${y2.toFixed(1)} ${x2.toFixed(1)} ${y2.toFixed(1)}`
  }
  const next: typeof wires.value = []
  srcEls.value.forEach((el, i) => {
    const e = el.getBoundingClientRect()
    next.push({ id: `in${i}`, side: 'in', d: curve(e.right - r.left + 4, e.top - r.top + e.height / 2, c.left - r.left - 4, coreY(i, srcEls.value.length)) })
  })
  outEls.value.forEach((el, i) => {
    const e = el.getBoundingClientRect()
    next.push({ id: `out${i}`, side: 'out', d: curve(c.right - r.left + 4, coreY(i, outEls.value.length), e.left - r.left - 4, e.top - r.top + e.height / 2) })
  })
  wires.value = next
}

let resizeObserver: ResizeObserver | null = null
onMounted(() => {
  nextTick(layout)
  if (typeof ResizeObserver === 'undefined' || !rootEl.value) return
  resizeObserver = new ResizeObserver(() => layout())
  resizeObserver.observe(rootEl.value)
})
onBeforeUnmount(() => resizeObserver?.disconnect())
</script>

<style scoped>
.flow {
  position: relative;
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(220px, 0.8fr) minmax(0, 1fr);
  gap: 0 clamp(48px, 9vw, 140px);
  align-items: center;
  margin: 0;
  padding: 28px 0 8px;
}

.flow-wires {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  overflow: visible;
  pointer-events: none;
}

.wire {
  fill: none;
  stroke: var(--line-strong);
  stroke-width: 1.2;
}

.on .wire {
  animation: wire-draw 1.1s cubic-bezier(0.55, 0.1, 0.35, 1) calc(var(--i) * 60ms) forwards;
}

.packet.in { fill: #7f0000; }
.packet.out { fill: #00007f; }

.flow-col {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.flow-label {
  margin-bottom: 4px;
  color: var(--accent);
  font-family: var(--mono);
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.flow-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--surface);
  transition: opacity 0.5s ease, transform 0.5s ease, border-color 0.2s ease;
}

/* Спрятано до появления только при работающем JS и разрешённом движении. */
@media (scripting: enabled) and (prefers-reduced-motion: no-preference) {
  .flow-item {
    opacity: 0;
    transform: translateY(8px);
  }

  .wire {
    stroke-dasharray: 1;
    stroke-dashoffset: 1;
  }
}

.flow-item:hover {
  border-color: var(--ink);
}

.on .flow-item {
  opacity: 1;
  transform: none;
}

.flow-col:first-child .flow-item:nth-child(2) { transition-delay: 0ms; }
.flow-col .flow-item:nth-child(3) { transition-delay: 60ms; }
.flow-col .flow-item:nth-child(4) { transition-delay: 120ms; }
.flow-col .flow-item:nth-child(5) { transition-delay: 180ms; }
.flow-col .flow-item:nth-child(6) { transition-delay: 240ms; }
.flow-col .flow-item:nth-child(7) { transition-delay: 300ms; }

.flow-icon {
  flex: none;
  width: 18px;
  height: 18px;
  color: var(--ink-2);
}

.flow-item b {
  display: block;
  font-size: 0.92rem;
  font-weight: 600;
  letter-spacing: -0.005em;
}

.flow-item small {
  display: block;
  color: var(--muted);
  font-size: 0.8rem;
  line-height: 1.35;
}

.flow-core {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.core-box {
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 8px;
  border-radius: 10px;
  color: var(--on-dark);
  background: var(--dark);
  box-shadow: 0 30px 50px -30px rgba(28, 27, 24, 0.6);
}

.core-layer {
  padding: 14px 14px 12px;
  border-radius: 6px;
}

.core-layer + .core-layer {
  border-top: 1px solid rgba(246, 244, 238, 0.12);
}

.core-layer b {
  display: block;
  font-family: var(--serif);
  font-size: 1.2rem;
  font-weight: 400;
}

.core-layer small {
  color: var(--on-dark-subtle);
  font-family: var(--mono);
  font-size: 0.7rem;
  letter-spacing: 0.04em;
}

/* Ядро «дышит»: волна идёт от центра, пока по проводам бегут данные. */
.core-pulse {
  position: absolute;
  inset: 0;
  border: 1px solid rgba(192, 4, 15, 0.5);
  border-radius: 10px;
  opacity: 0;
  pointer-events: none;
}

@media (prefers-reduced-motion: no-preference) {
  .on .core-pulse {
    animation: core-pulse 2.8s ease-out 1.2s infinite;
  }
}

@media (prefers-reduced-motion: reduce) {
  .on .wire {
    animation: none;
  }
}

@keyframes wire-draw {
  to { stroke-dashoffset: 0; }
}

@keyframes core-pulse {
  0% { opacity: 0.9; transform: scale(1); }
  100% { opacity: 0; transform: scale(1.08, 1.12); }
}

/* Узко: колонки друг под другом, между ними — стрелки вниз. */
@media (max-width: 899px) {
  .flow {
    grid-template-columns: 1fr;
    gap: 0;
  }

  .flow-col {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .flow-label {
    grid-column: 1 / -1;
  }

  .flow-core {
    margin: 22px 0;
    padding: 30px 0;
    background: linear-gradient(var(--line-strong), var(--line-strong)) center / 1px 100% no-repeat;
  }

  .core-box {
    flex-direction: row;
    flex-wrap: wrap;
  }

  .core-layer {
    flex: 1 1 140px;
  }

  .core-layer + .core-layer {
    border-top: 0;
    border-left: 1px solid rgba(246, 244, 238, 0.12);
  }
}

@media (max-width: 520px) {
  .flow-col {
    grid-template-columns: 1fr;
  }

  .core-box {
    flex-direction: column;
  }

  .core-layer {
    flex: none;
  }

  .core-layer + .core-layer {
    border-top: 1px solid rgba(246, 244, 238, 0.12);
    border-left: 0;
  }
}
</style>
