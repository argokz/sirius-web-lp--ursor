<template>
  <div ref="rootEl" class="ai-demo" :class="{ paused: !visible }">
    <div class="ai-tabs" role="tablist" aria-label="Сценарии помощника ИИ">
      <button
        v-for="(item, index) in SCENARIOS"
        :key="item.id"
        type="button"
        role="tab"
        class="ai-tab"
        :class="{ active: index === current }"
        :aria-selected="index === current"
        @click="select(index)"
      >
        <span class="ai-tab-title">{{ item.tab }}</span>
        <span class="ai-tab-place">{{ item.place }}</span>
        <span class="ai-tab-progress" :style="index === current ? { animationDuration: `${CYCLE_MS}ms` } : undefined" />
      </button>
    </div>

    <div :key="`${scenario.id}-${round}`" class="ai-stage">
      <!-- Карта демонстрационной сети: подложка общая, поверх — то, что нашёл помощник. -->
      <div class="ai-map" aria-hidden="true">
        <svg viewBox="0 0 480 360" preserveAspectRatio="xMidYMid slice">
          <rect width="480" height="360" fill="#efece4" />
          <path d="M0 120H480M0 250H480M120 0V360M300 0V360M410 0V360" stroke="#fff" stroke-width="14" />
          <path d="M0 120H480M0 250H480M120 0V360M300 0V360M410 0V360" stroke="#d9d4c6" stroke-width="1" fill="none" />
          <path d="M430 300 C 440 250 470 230 480 220 V360 H420 Z" fill="#dfe8d5" />
          <g fill="#e3ded1" stroke="#c9c2b1" stroke-width="0.8">
            <rect v-for="b in BUILDINGS" :key="b.id" :x="b.x" :y="b.y" :width="b.w" :height="b.h" rx="1.5"
              :class="{ hit: scenario.buildings.includes(b.id) }" />
          </g>
          <g fill="none" stroke-linecap="round">
            <path v-for="pipe in PIPES" :key="pipe.id" :d="pipe.d" stroke="#7f0000" :stroke-width="pipe.main ? 3.2 : 1.8" />
            <path v-for="pipe in PIPES" :key="`${pipe.id}-r`" :d="pipe.d" stroke="#00007f" :stroke-width="pipe.main ? 1.4 : 0.8" transform="translate(2.5 2.5)" opacity="0.8" />
          </g>
          <g v-if="scenario.zone" class="ai-zone">
            <path :d="scenario.zone" fill="rgba(227, 6, 19, 0.08)" stroke="#e30613" stroke-width="1.6" stroke-dasharray="6 5" />
          </g>
          <g v-for="ring in scenario.rings" :key="`${ring.x}-${ring.y}`" class="ai-ring">
            <circle :cx="ring.x" :cy="ring.y" r="46" fill="rgba(0, 200, 255, 0.08)" stroke="#00a7d6" stroke-dasharray="3 4" />
            <rect :x="ring.x - 7" :y="ring.y - 7" width="14" height="14" rx="3" fill="#1c1b18" />
            <path :d="`M${ring.x - 3.5} ${ring.y + 2.5}V${ring.y - 1}L${ring.x} ${ring.y - 4}L${ring.x + 3.5} ${ring.y - 1}V${ring.y + 2.5}Z`" fill="#fff" />
          </g>
          <g class="ai-selected" fill="none" stroke-linecap="round">
            <path v-for="(d, i) in scenario.selected" :key="d" :d="d" stroke="#00c8ff" stroke-width="7" opacity="0.85"
              pathLength="1" :style="{ animationDelay: `${SHOW_MAP_MS + i * 120}ms` }" />
          </g>
          <g v-for="(valve, i) in scenario.valves" :key="`${valve.x}-${valve.y}`" class="ai-valve" :style="{ animationDelay: `${SHOW_MAP_MS + 300 + i * 140}ms` }">
            <path :d="`M${valve.x - 7} ${valve.y - 5}L${valve.x + 7} ${valve.y + 5}V${valve.y - 5}L${valve.x - 7} ${valve.y + 5}Z`" fill="#1c1b18" stroke="#fff" stroke-width="1.2" />
          </g>
          <g v-for="(flag, i) in scenario.flags" :key="`${flag.x}-${flag.y}`" class="ai-flag" :style="{ animationDelay: `${SHOW_MAP_MS + i * 160}ms` }">
            <circle :cx="flag.x" :cy="flag.y" r="11" :fill="flag.error ? 'rgba(227, 6, 19, 0.18)' : 'rgba(224, 160, 0, 0.2)'" class="ai-flag-pulse" />
            <circle :cx="flag.x" :cy="flag.y" r="5" :fill="flag.error ? '#e30613' : '#e0a000'" stroke="#fff" stroke-width="1.5" />
          </g>
          <circle v-for="node in NODES" :key="`${node.x}-${node.y}`" :cx="node.x" :cy="node.y" r="3.2" fill="#fff" stroke="#7f0000" stroke-width="1.4" />
        </svg>

        <div class="ai-map-card" :style="{ animationDelay: `${SHOW_CARD_MS}ms` }">
          <span class="ai-map-card-label">{{ scenario.card.label }}</span>
          <strong>{{ scenario.card.value }}</strong>
          <span>{{ scenario.card.note }}</span>
        </div>
        <span class="ai-map-crs">ДЕМО-СЕТЬ · WGS 84</span>
      </div>

      <!-- Окно помощника: шаги появляются по очереди, как ответ идёт в приложении. -->
      <div class="ai-chat">
        <header class="ai-chat-head">
          <span class="ai-chat-dot" />
          Помощник ИИ
          <span class="ai-chat-model">Claude</span>
        </header>
        <div class="ai-chat-body">
          <p class="ai-msg ai-user" :style="{ animationDelay: '150ms' }">{{ scenario.question }}</p>
          <div
            v-for="(step, i) in scenario.steps"
            :key="step.tool"
            class="ai-step"
            :style="{ animationDelay: `${STEP_START_MS + i * STEP_GAP_MS}ms` }"
          >
            <span class="ai-step-tool">{{ step.tool }}</span>
            <span class="ai-step-result">{{ step.result }}</span>
          </div>
          <p class="ai-msg ai-answer" :style="{ animationDelay: `${answerDelay}ms` }">{{ scenario.answer }}</p>
          <div class="ai-actions" :style="{ animationDelay: `${answerDelay + 300}ms` }">
            <span v-for="action in scenario.actions" :key="action" class="ai-action">{{ action }}</span>
          </div>
        </div>
      </div>
    </div>
    <p class="ai-note">Пример на демонстрационной сети. Помощник работает с вашими правами и только с данными вашего сервера.</p>
  </div>
</template>

<script setup lang="ts">
/**
 * Витрина помощника ИИ «как у felt.com»: вкладки сценариев, карта и окно ответа, шаги по очереди.
 * Сценарии взяты из справки (10-ai, 03-operations), числа — примерные, на условной сети.
 */
interface Scenario {
  id: string
  tab: string
  place: string
  question: string
  steps: Array<{ tool: string; result: string }>
  answer: string
  actions: string[]
  card: { label: string; value: string; note: string }
  zone?: string
  selected: string[]
  valves: Array<{ x: number; y: number }>
  flags: Array<{ x: number; y: number; error?: boolean }>
  rings: Array<{ x: number; y: number }>
  buildings: string[]
}

const CYCLE_MS = 11000
const STEP_START_MS = 900
const STEP_GAP_MS = 900
const SHOW_MAP_MS = 1200
const SHOW_CARD_MS = 2600

const PIPES = [
  { id: 'm1', d: 'M20 186H460', main: true },
  { id: 'b1', d: 'M120 186V40', main: false },
  { id: 'b2', d: 'M120 186V330', main: false },
  { id: 'b3', d: 'M300 186V60', main: false },
  { id: 'b4', d: 'M300 186V320', main: false },
  { id: 's1', d: 'M120 90H170', main: false },
  { id: 's2', d: 'M120 280H70', main: false },
  { id: 's3', d: 'M300 100H350', main: false },
  { id: 's4', d: 'M300 290H360', main: false },
  { id: 's5', d: 'M300 140H250', main: false }
]

const NODES = [
  { x: 120, y: 186 }, { x: 300, y: 186 }, { x: 120, y: 90 }, { x: 120, y: 280 },
  { x: 300, y: 100 }, { x: 300, y: 290 }, { x: 300, y: 140 }, { x: 410, y: 186 }
]

const BUILDINGS = [
  { id: 'a', x: 150, y: 60, w: 46, h: 22 }, { id: 'b', x: 150, y: 96, w: 30, h: 16 },
  { id: 'c', x: 40, y: 262, w: 40, h: 36 }, { id: 'd', x: 140, y: 296, w: 34, h: 26 },
  { id: 'e', x: 330, y: 70, w: 52, h: 24 }, { id: 'f', x: 334, y: 112, w: 30, h: 22 },
  { id: 'g', x: 330, y: 272, w: 48, h: 30 }, { id: 'h', x: 220, y: 128, w: 34, h: 26 },
  { id: 'i', x: 30, y: 40, w: 50, h: 28 }, { id: 'j', x: 200, y: 270, w: 50, h: 34 },
  { id: 'k', x: 430, y: 60, w: 36, h: 40 }, { id: 'l', x: 340, y: 210, w: 38, h: 22 }
]

const SCENARIOS: Scenario[] = [
  {
    id: 'outage',
    tab: 'Авария на участке',
    place: 'М2 2КД-10 → 2КД-11',
    question: 'Порыв на участке 1494. Какие задвижки закрыть и кто останется без тепла?',
    steps: [
      { tool: 'locate_outage · участок 1494', result: 'Закрыть 4 задвижки' },
      { tool: 'consumers_off', result: '37 зданий · 4,2 Гкал/ч' },
      { tool: 'near_poi · социальные', result: 'Школа-гимназия, детский сад' }
    ],
    answer: 'Закройте 2КД-9 и 2КД-12 на подающем и обратном. Без тепла останутся 37 зданий, среди них школа-гимназия — её стоит предупредить первой.',
    actions: ['Создать отключение', 'Наряд бригаде'],
    card: { label: 'ЛОКАЛИЗАЦИЯ', value: '37 зданий', note: '4 задвижки · 1 школа · 1 детсад' },
    zone: 'M230 40 H400 V330 H230 Z',
    selected: ['M300 186V60', 'M300 186V320'],
    valves: [{ x: 300, y: 50 }, { x: 300, y: 330 }, { x: 250, y: 186 }, { x: 355, y: 186 }],
    flags: [],
    rings: [],
    buildings: ['e', 'f', 'g', 'h', 'l']
  },
  {
    id: 'select',
    tab: 'Выборка вопросом',
    place: 'Ду 500 · до 1980 г.',
    question: 'Участки Ду 500 старше 1980 года в 300 м от школ',
    steps: [
      { tool: 'network_select · Ду = 500', result: 'Условие по паспорту' },
      { tool: 'year < 1980', result: 'Год прокладки' },
      { tool: 'near_poi · школы · 300 м', result: '12 участков · 3,8 км' }
    ],
    answer: 'Нашёл 12 участков общей длиной 3,8 км рядом с двумя школами. Средний износ — 71 %, три участка уже в плане ремонтов.',
    actions: ['Показать списком', 'В Excel'],
    card: { label: 'ВЫБОРКА', value: '12 участков', note: '3,8 км · износ 71 %' },
    selected: ['M20 186H120', 'M120 186V40', 'M120 90H170', 'M120 186V330'],
    valves: [],
    flags: [],
    rings: [{ x: 75, y: 70 }, { x: 175, y: 300 }],
    buildings: ['a', 'c', 'd', 'i']
  },
  {
    id: 'protocol',
    tab: 'Разбор протокола',
    place: 'Фрагмент 74 · −25 °C',
    question: 'Почему в расчёте фрагмента 74 столько предупреждений?',
    steps: [
      { tool: 'calc_protocol · фрагмент 74', result: '3 ошибки · 11 предупреждений' },
      { tool: 'trace_network · 2ВВ-5', result: 'Задвижка закрыта' },
      { tool: 'regime_analysis', result: '4 узла: напор < 5 м' }
    ],
    answer: 'Главная причина — закрытая задвижка у 2ВВ-5: она отрезала 6 потребителей, отсюда три ошибки. Остальное — низкий располагаемый напор в концевых узлах.',
    actions: ['Перейти к узлу', 'Пьезометр'],
    card: { label: 'ПРОТОКОЛ', value: '3 причины', note: 'вместо 14 строк протокола' },
    selected: ['M300 186H460'],
    valves: [{ x: 410, y: 186 }],
    flags: [{ x: 410, y: 186, error: true }, { x: 350, y: 100 }, { x: 360, y: 290 }, { x: 70, y: 280 }, { x: 250, y: 140 }],
    rings: [],
    buildings: ['k']
  }
]

const current = ref(0)
const round = ref(0)
const visible = ref(false)
const rootEl = ref<HTMLElement | null>(null)
const scenario = computed(() => SCENARIOS[current.value]!)
const answerDelay = computed(() => STEP_START_MS + scenario.value.steps.length * STEP_GAP_MS + 200)

let timer: ReturnType<typeof setTimeout> | null = null
let observer: IntersectionObserver | null = null

const schedule = () => {
  if (timer) clearTimeout(timer)
  if (!visible.value) return
  timer = setTimeout(() => {
    current.value = (current.value + 1) % SCENARIOS.length
    round.value += 1
    schedule()
  }, CYCLE_MS)
}

const select = (index: number) => {
  current.value = index
  round.value += 1
  schedule()
}

onMounted(() => {
  observer = new IntersectionObserver(([entry]) => {
    const was = visible.value
    visible.value = Boolean(entry?.isIntersecting)
    // Сценарий начинается заново, когда блок снова на экране, — иначе шаги отыграли бы за кадром.
    if (visible.value && !was) round.value += 1
    schedule()
  }, { threshold: 0.35 })
  if (rootEl.value) observer.observe(rootEl.value)
})

onBeforeUnmount(() => {
  if (timer) clearTimeout(timer)
  observer?.disconnect()
})
</script>

<style scoped>
.ai-demo {
  --ai-line: rgba(246, 244, 238, 0.14);
}

.ai-tabs {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  border-top: 1px solid var(--ai-line);
}

.ai-tab {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 18px 18px 20px 0;
  border: 0;
  color: var(--on-dark-muted);
  background: transparent;
  text-align: left;
  cursor: pointer;
  transition: color 0.2s ease;
}

.ai-tab + .ai-tab {
  padding-left: 18px;
  border-left: 1px solid var(--ai-line);
}

.ai-tab:hover,
.ai-tab.active {
  color: var(--on-dark);
}

.ai-tab-title {
  font-family: var(--serif);
  font-size: 1.2rem;
}

.ai-tab-place {
  color: #8b867a;
  font-family: var(--mono);
  font-size: 0.7rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

.ai-tab-progress {
  position: absolute;
  top: -1px;
  left: 0;
  right: 0;
  height: 2px;
  background: #ff6b5e;
  transform: scaleX(0);
  transform-origin: left;
}

.ai-tab.active .ai-tab-progress {
  animation: ai-progress linear forwards;
}

.paused .ai-tab.active .ai-tab-progress {
  animation-play-state: paused;
}

@keyframes ai-progress {
  to { transform: scaleX(1); }
}

.ai-stage {
  display: grid;
  grid-template-columns: minmax(0, 1.35fr) minmax(300px, 1fr);
  gap: 0;
  margin-top: 8px;
  overflow: hidden;
  border: 1px solid var(--ai-line);
  border-radius: 8px;
  background: #23221e;
}

.ai-map {
  position: relative;
  min-height: 420px;
  overflow: hidden;
}

.ai-map svg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

.ai-map-crs {
  position: absolute;
  left: 12px;
  bottom: 10px;
  padding: 3px 8px;
  border-radius: 999px;
  color: #3a382f;
  background: rgba(255, 255, 255, 0.85);
  font-family: var(--mono);
  font-size: 0.62rem;
  letter-spacing: 0.06em;
}

/* Всё, что «нашёл» помощник, появляется после соответствующего шага в чате. */
.hit {
  fill: #f6d5cf;
  stroke: #e30613;
  animation: ai-hit 0.5s ease 1.6s both;
}

.ai-zone path {
  animation: ai-fade 0.6s ease 1.1s both, ai-march 1.2s linear 1.1s infinite;
}

.ai-selected path {
  stroke-dasharray: 1;
  stroke-dashoffset: 1;
  animation: ai-draw 0.9s cubic-bezier(0.6, 0, 0.2, 1) both;
}

.ai-valve,
.ai-flag,
.ai-ring {
  transform-box: fill-box;
  transform-origin: center;
  animation: ai-pop 0.45s cubic-bezier(0.3, 1.6, 0.5, 1) both;
}

.ai-ring {
  animation-delay: 2.4s;
}

.ai-flag-pulse {
  transform-box: fill-box;
  transform-origin: center;
  animation: ai-pulse 1.8s ease-out 2s infinite;
}

.ai-map-card {
  position: absolute;
  top: 16px;
  right: 16px;
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 170px;
  padding: 12px 14px;
  border: 1px solid var(--ink);
  border-radius: 6px;
  color: var(--ink);
  background: var(--surface);
  box-shadow: 0 14px 30px -18px rgba(0, 0, 0, 0.5);
  animation: ai-rise 0.5s cubic-bezier(0.2, 0.8, 0.2, 1) both;
}

.ai-map-card-label {
  color: var(--accent);
  font-family: var(--mono);
  font-size: 0.62rem;
  letter-spacing: 0.08em;
}

.ai-map-card strong {
  font-family: var(--serif);
  font-size: 1.5rem;
  font-weight: 400;
}

.ai-map-card span:last-child {
  color: var(--muted);
  font-size: 0.78rem;
}

.ai-chat {
  display: flex;
  flex-direction: column;
  border-left: 1px solid var(--ai-line);
  color: var(--ink);
  background: var(--surface);
}

.ai-chat-head {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 16px;
  border-bottom: 1px solid var(--line);
  font-size: 0.86rem;
  font-weight: 500;
}

.ai-chat-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #2f9e44;
}

.ai-chat-model {
  margin-left: auto;
  padding: 2px 8px;
  border: 1px solid var(--line);
  border-radius: 999px;
  color: var(--muted);
  font-family: var(--mono);
  font-size: 0.64rem;
}

.ai-chat-body {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 16px;
}

.ai-msg,
.ai-step,
.ai-actions {
  margin: 0;
  animation: ai-rise 0.45s cubic-bezier(0.2, 0.8, 0.2, 1) both;
}

.ai-msg {
  padding: 10px 12px;
  border-radius: 8px;
  font-size: 0.9rem;
  line-height: 1.45;
}

.ai-user {
  align-self: flex-end;
  max-width: 88%;
  color: var(--on-dark);
  background: var(--ink);
}

.ai-answer {
  border: 1px solid var(--line);
  background: var(--paper);
}

.ai-step {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  padding: 7px 10px;
  border-left: 2px solid var(--line-strong);
  font-size: 0.78rem;
}

.ai-step-tool {
  color: var(--muted);
  font-family: var(--mono);
  font-size: 0.7rem;
}

.ai-step-result {
  color: var(--ink);
  text-align: right;
}

.ai-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.ai-action {
  padding: 6px 10px;
  border: 1px solid var(--ink);
  border-radius: 4px;
  font-size: 0.8rem;
}

.ai-action:first-child {
  color: var(--on-dark);
  background: var(--ink);
}

.ai-note {
  margin: 14px 0 0;
  color: #8b867a;
  font-size: 0.8rem;
}

.paused .ai-stage * {
  animation-play-state: paused !important;
}

@keyframes ai-rise {
  from { opacity: 0; transform: translateY(10px); }
}

@keyframes ai-hit {
  from { fill: #e3ded1; stroke: #c9c2b1; }
}

@keyframes ai-march {
  to { stroke-dashoffset: -11; }
}

@keyframes ai-fade {
  from { opacity: 0; }
}

@keyframes ai-draw {
  to { stroke-dashoffset: 0; }
}

@keyframes ai-pop {
  from { opacity: 0; transform: scale(0.2); }
}

@keyframes ai-pulse {
  0% { transform: scale(1); opacity: 1; }
  100% { transform: scale(2.4); opacity: 0; }
}

@media (max-width: 900px) {
  .ai-stage {
    grid-template-columns: 1fr;
  }

  .ai-map {
    min-height: 300px;
  }

  .ai-chat {
    border-top: 1px solid var(--ai-line);
    border-left: 0;
  }
}

@media (max-width: 640px) {
  .ai-tabs {
    grid-template-columns: 1fr;
  }

  .ai-tab,
  .ai-tab + .ai-tab {
    padding: 12px 0;
    border-left: 0;
    border-bottom: 1px solid var(--ai-line);
  }

  .ai-tab:not(.active) .ai-tab-place {
    display: none;
  }

  /* На телефоне карточка не должна закрывать карту. */
  .ai-map-card {
    top: 10px;
    right: 10px;
    min-width: 0;
    padding: 8px 10px;
  }

  .ai-map-card strong {
    font-size: 1.1rem;
  }

  .ai-map-card span:last-child {
    display: none;
  }
}

@media (prefers-reduced-motion: reduce) {
  .ai-stage *,
  .ai-tab-progress {
    animation: none !important;
  }
}
</style>
