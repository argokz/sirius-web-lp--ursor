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

    <div :key="`${scenario.id}-${round}`" class="ai-stage" :style="timeline.vars">
      <!-- Карта демонстрационной сети: найденное помощником появляется, когда ответ готов («Показано»). -->
      <div class="ai-map" aria-hidden="true">
        <svg viewBox="0 0 480 360" preserveAspectRatio="xMidYMid slice">
          <defs>
            <filter id="ai-halo-blur" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="1.6" /></filter>
          </defs>
          <rect width="480" height="360" fill="#efede8" />
          <path d="M424 300 C 436 250 466 228 480 220 V360 H414 Z" class="park" />
          <g class="roads">
            <path v-for="road in ROADS" :key="`e${road.d}`" :d="road.d" class="road-edge" :stroke-width="road.w + 2" />
            <path v-for="road in ROADS" :key="road.d" :d="road.d" class="road" :stroke-width="road.w" />
          </g>
          <g class="buildings">
            <rect v-for="b in BUILDINGS" :key="b.id" :x="b.x" :y="b.y" :width="b.w" :height="b.h"
              :class="{ consumer: b.q, hit: scenario.buildings.includes(b.id) }" />
          </g>
          <g class="map-text">
            <text v-for="street in STREETS" :key="street.name" :x="street.x" :y="street.y" class="street">{{ street.name }}</text>
            <text v-for="b in CONSUMERS" :key="`q${b.id}`" :x="b.x + b.w / 2" :y="b.y + b.h / 2 + 2.5" text-anchor="middle" class="load">Qсум={{ b.q }}</text>
          </g>
          <g v-for="(ring, i) in scenario.rings" :key="`${ring.x}-${ring.y}`" class="ai-ring" :style="{ '--i': i }">
            <circle :cx="ring.x" :cy="ring.y" r="46" fill="rgba(0, 200, 255, 0.08)" stroke="#00a7d6" stroke-dasharray="3 4" />
            <rect :x="ring.x - 7" :y="ring.y - 7" width="14" height="14" rx="3" fill="#1c1b18" />
            <path :d="`M${ring.x - 3.5} ${ring.y + 2.5}V${ring.y - 1}L${ring.x} ${ring.y - 4}L${ring.x + 3.5} ${ring.y - 1}V${ring.y + 2.5}Z`" fill="#fff" />
          </g>
          <!-- Трубы: белая обводка, подача #7f0000 и обратка #00007f рядом, закрытые — #808000 (как в десктопе). -->
          <g class="pipes">
            <path v-for="pipe in PIPES" :key="`c${pipe.id}`" :d="pipe.d" class="casing" :stroke-width="(pipe.main ? 2.2 : 1.5) + 4.4" transform="translate(1.1 1.1)" />
            <path v-for="pipe in PIPES" :key="`s${pipe.id}`" :d="pipe.d" class="supply" :stroke-width="pipe.main ? 2.2 : 1.5" />
            <path v-for="pipe in PIPES" :key="`r${pipe.id}`" :d="pipe.d" class="return" :stroke-width="pipe.main ? 2.2 : 1.5" transform="translate(2.2 2.2)" />
            <g v-for="(d, i) in scenario.closed" :key="`x${d}`" class="ai-closed" :style="{ '--i': i }">
              <path :d="d" class="closed" stroke-width="1.5" />
              <path :d="d" class="closed" stroke-width="1.5" transform="translate(2.2 2.2)" />
            </g>
          </g>
          <!-- Выделение — как utils/selectionHighlight.ts: размытый ореол #00c8ff и тонкая линия поверх. -->
          <g class="ai-selected">
            <path v-for="(d, i) in scenario.selected" :key="`h${d}`" :d="d" class="halo" filter="url(#ai-halo-blur)" :style="{ '--i': i }" />
            <path v-for="(d, i) in scenario.selected" :key="`l${d}`" :d="d" class="line" pathLength="1" :style="{ '--i': i }" />
          </g>
          <g v-for="(valve, i) in scenario.valves" :key="`${valve.x}-${valve.y}`" class="ai-valve" :style="{ '--i': i }">
            <path :d="`M${valve.x - 6} ${valve.y - 4.5}L${valve.x + 6} ${valve.y + 4.5}V${valve.y - 4.5}L${valve.x - 6} ${valve.y + 4.5}Z`" fill="#111" stroke="#fff" stroke-width="1.2" />
          </g>
          <g class="nodes">
            <template v-for="node in NODES" :key="`${node.x}-${node.y}`">
              <circle :cx="node.x + 1.1" :cy="node.y + 1.1" :r="node.chamber ? 4.2 : 3" class="node" />
              <circle v-if="node.chamber" :cx="node.x + 1.1" :cy="node.y + 1.1" r="1.5" class="node-dot" />
            </template>
          </g>
          <g class="net-text">
            <text v-for="node in NAMED_NODES" :key="node.name" :x="node.x + 7" :y="node.y - 7">{{ node.name }}</text>
            <text x="196" y="181" class="dn">Ду 500</text>
          </g>
        </svg>
        <span class="ai-map-crs">ДЕМО-СЕТЬ · WGS 84</span>
      </div>

      <!-- Окно «Помощник ИИ» как в ТГИД (AssistantDialog): тот же заголовок, шаги, подвал и поле вопроса. -->
      <div class="ai-dialog" role="img" :aria-label="`Окно «Помощник ИИ»: ${scenario.question}`">
        <header class="ai-head">
          <svg class="ai-head-icon" viewBox="0 0 24 24" aria-hidden="true"><path :d="ICON_ROBOT" /></svg>
          <span class="ai-head-title">Помощник ИИ</span>
          <span class="ai-head-new">+ Новая беседа</span>
          <svg class="ai-head-close" viewBox="0 0 24 24" aria-hidden="true"><path :d="ICON_CLOSE" /></svg>
        </header>

        <div ref="bodyEl" class="ai-body" aria-hidden="true">
          <div class="grow" style="--at: var(--t-ask)"><div><p class="ai-user">{{ scenario.question }}</p></div></div>
          <div class="wait" style="--at: var(--t-wait1)"><div><p class="ai-wait">Разбираю вопрос…</p></div></div>

          <div class="grow" style="--at: var(--t-steps)">
            <div>
              <div class="ai-steps">
                <div v-for="(step, i) in scenario.steps" :key="step.title" class="grow" :style="{ '--at': `var(--t-step-${i})` }">
                  <div>
                    <p class="ai-step">
                      <span class="ai-step-state" :style="{ '--at': `var(--t-done-${i})` }">
                        <svg class="spin" viewBox="0 0 16 16"><circle cx="8" cy="8" r="6" /></svg>
                        <svg class="check" viewBox="0 0 24 24"><path :d="ICON_CHECK" /></svg>
                      </span>
                      <span><b>{{ step.title }}</b><span class="ai-step-params"> — {{ step.params }}</span><span class="ai-step-time" :style="{ '--at': `var(--t-done-${i})` }"> · {{ step.time }}</span></span>
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="wait" style="--at: var(--t-wait2)"><div><p class="ai-wait">Собираю ответ…</p></div></div>

          <div v-for="(line, i) in scenario.answer" :key="line" class="grow" :style="{ '--at': `calc(var(--t-answer) + ${i * LINE_GAP_MS}ms)` }">
            <div>
              <p class="ai-answer" :class="{ bullet: line.startsWith('• ') }">
                <template v-for="(seg, s) in segments(line)" :key="s"><b v-if="seg.bold">{{ seg.text }}</b><template v-else>{{ seg.text }}</template></template>
              </p>
            </div>
          </div>

          <div class="grow" style="--at: var(--t-footer)">
            <div>
              <div class="ai-found">
                <span>{{ scenario.found }}</span>
                <span class="ai-chip">
                  <svg viewBox="0 0 24 24" aria-hidden="true"><path :d="ICON_MARKER" /></svg>
                  <span class="chip-text"><span class="chip-a">Показать на карте</span><span class="chip-b">Показано</span></span>
                </span>
              </div>
              <p class="ai-meta">{{ scenario.meta }}</p>
            </div>
          </div>
        </div>

        <footer class="ai-foot" aria-hidden="true">
          <div class="ai-input" :class="{ typing: typed }">
            <span v-if="typed" class="ai-typed">{{ typed }}<i class="ai-caret" /></span>
            <span v-else class="ai-placeholder">Например: какие задвижки закрыть при порыве у ТК-12 и кто останется без тепла?</span>
          </div>
          <p class="ai-hint">Enter — отправить, Shift+Enter — новая строка. Ответ опирается на данные ТГИД; проверяйте важные решения.</p>
          <div class="ai-buttons">
            <span class="ai-btn-text">Оставить на карте</span>
            <span class="ai-btn-primary">
              <svg viewBox="0 0 24 24"><path :d="ICON_SEND" /></svg>
              Спросить
              <i class="ai-press" />
            </span>
            <svg class="ai-cursor" viewBox="0 0 16 20" width="16" height="20">
              <path d="M1 1 L1 16 L5 12 L8 19 L11 17.6 L8 11 L14 11 Z" fill="#1c1b18" stroke="#fff" stroke-width="1.4" stroke-linejoin="round" />
            </svg>
          </div>
        </footer>
      </div>
    </div>
    <p class="ai-note">Пример на демонстрационной сети: окно то же, что в ТГИД, числа условные. Помощник работает с вашими правами и только с данными вашего сервера.</p>
  </div>
</template>

<script setup lang="ts">
/**
 * Витрина помощника ИИ: окно повторяет AssistantDialog веб-ТГИД (заголовок, шаги-инструменты
 * с параметрами вызова, «Найдено на карте», «N с · вызовов инструментов», поле вопроса).
 * Названия и параметры инструментов — настоящие (tgid_mcp/tools.py), числа — условные.
 * Ход сценария задан CSS-переменными времени (--t-ask, --t-step-0…), JS только набирает вопрос.
 */
interface Step { title: string; params: string; time: string }
interface Scenario {
  id: string
  tab: string
  place: string
  question: string
  steps: Step[]
  answer: string[]
  found: string
  meta: string
  selected: string[]
  closed: string[]
  valves: Array<{ x: number; y: number }>
  rings: Array<{ x: number; y: number }>
  buildings: string[]
}

const CYCLE_MS = 15000
const TYPE_START_MS = 500
const TYPE_CHAR_MS = 26
const SEND_PAUSE_MS = 350
const STEP_GAP_MS = 1100
const STEP_RUN_MS = 750
const LINE_GAP_MS = 160

// Значки Material Design Icons — те же, что в окне ТГИД.
const ICON_ROBOT = 'M17.5 15.5C17.5 16.61 16.61 17.5 15.5 17.5S13.5 16.61 13.5 15.5 14.4 13.5 15.5 13.5 17.5 14.4 17.5 15.5M8.5 13.5C7.4 13.5 6.5 14.4 6.5 15.5S7.4 17.5 8.5 17.5 10.5 16.61 10.5 15.5 9.61 13.5 8.5 13.5M23 15V18C23 18.55 22.55 19 22 19H21V20C21 21.11 20.11 22 19 22H5C3.89 22 3 21.1 3 20V19H2C1.45 19 1 18.55 1 18V15C1 14.45 1.45 14 2 14H3C3 10.13 6.13 7 10 7H11V5.73C10.4 5.39 10 4.74 10 4C10 2.9 10.9 2 12 2S14 2.9 14 4C14 4.74 13.6 5.39 13 5.73V7H14C17.87 7 21 10.13 21 14H22C22.55 14 23 14.45 23 15M21 16H19V14C19 11.24 16.76 9 14 9H10C7.24 9 5 11.24 5 14V16H3V17H5V20H19V17H21V16Z'
const ICON_CLOSE = 'M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z'
const ICON_CHECK = 'M12 2C6.5 2 2 6.5 2 12S6.5 22 12 22 22 17.5 22 12 17.5 2 12 2M12 20C7.59 20 4 16.41 4 12S7.59 4 12 4 20 7.59 20 12 16.41 20 12 20M16.59 7.58L10 14.17L7.41 11.59L6 13L10 17L18 9L16.59 7.58Z'
const ICON_MARKER = 'M12 6.5A2.5 2.5 0 0 1 14.5 9A2.5 2.5 0 0 1 12 11.5A2.5 2.5 0 0 1 9.5 9A2.5 2.5 0 0 1 12 6.5M12 2A7 7 0 0 1 19 9C19 14.25 12 22 12 22S5 14.25 5 9A7 7 0 0 1 12 2M12 4A5 5 0 0 0 7 9C7 10 7 12 12 18.71C17 12 17 10 17 9A5 5 0 0 0 12 4Z'
const ICON_SEND = 'M2 21L23 12L2 3V10L17 12L2 14V21Z'

// Улицы подложки (ширина — как у MapTiler на крупном масштабе) и подписи улиц.
const ROADS = [
  { d: 'M0 120H480', w: 12 }, { d: 'M0 250H480', w: 9 },
  { d: 'M140 0V360', w: 9 }, { d: 'M322 0V360', w: 12 }, { d: 'M440 0V360', w: 7 }
]

const STREETS = [
  { name: 'ул. Курмангазы', x: 186, y: 123 },
  { name: 'ул. Жамбыла', x: 30, y: 253 }
]

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

// Узлы: камеры — кольцо с точкой, простые узлы — кружок с чёрным ободком (как значки сети в ТГИД).
const NODES = [
  { x: 120, y: 186, name: '2КД-8', chamber: true }, { x: 300, y: 186, name: '2КД-10', chamber: true },
  { x: 410, y: 186, name: '2КД-11', chamber: true }, { x: 120, y: 90, name: '2ВВ-5', chamber: true },
  { x: 120, y: 280, name: '' }, { x: 300, y: 100, name: '' }, { x: 300, y: 290, name: '' }, { x: 300, y: 140, name: '' }
]
const NAMED_NODES = NODES.filter((node) => node.name)

// Здания; у потребителей (q) — оранжевый контур и подпись «Qсум» в Гкал/ч, как на карте ТГИД.
const BUILDINGS: Array<{ id: string; x: number; y: number; w: number; h: number; q?: string }> = [
  { id: 'a', x: 150, y: 56, w: 50, h: 26, q: '0.152' }, { id: 'b', x: 152, y: 94, w: 30, h: 16 },
  { id: 'c', x: 34, y: 262, w: 48, h: 36, q: '0.087' }, { id: 'd', x: 152, y: 292, w: 40, h: 28, q: '0.121' },
  { id: 'e', x: 334, y: 66, w: 56, h: 28, q: '0.248' }, { id: 'f', x: 336, y: 132, w: 32, h: 22 },
  { id: 'g', x: 334, y: 270, w: 52, h: 32, q: '0.298' }, { id: 'h', x: 210, y: 130, w: 48, h: 28, q: '0.264' },
  { id: 'i', x: 26, y: 36, w: 56, h: 30, q: '0.205' }, { id: 'j', x: 204, y: 266, w: 50, h: 34 },
  { id: 'k', x: 448, y: 58, w: 30, h: 44 }, { id: 'l', x: 342, y: 204, w: 40, h: 24, q: '0.113' }
]
const CONSUMERS = BUILDINGS.filter((b) => b.q)

const SCENARIOS: Scenario[] = [
  {
    id: 'outage',
    tab: 'Авария на участке',
    place: 'М2 2КД-10 → 2КД-11',
    question: 'Порыв на участке 2КД-10 — 2КД-11. Какие задвижки закрыть и кто останется без тепла?',
    steps: [
      { title: 'Поиск объектов сети', params: 'kind: line · text: 2КД-10 · text2: 2КД-11', time: '0,4 с' },
      { title: 'Локализация аварии', params: 'line_id: 1494', time: '2,6 с' }
    ],
    answer: [
      'Чтобы отсечь участок 1494, закройте **4 задвижки** — 2КД-9 и 2КД-12 на подающем и обратном.',
      '• Без тепла останутся **37 зданий**, недоотпуск — **4,2 Гкал/ч**.',
      '• Список зданий с нагрузкой — во вкладке «Отключенные потребители».'
    ],
    found: 'Найдено на карте: 9 участков и 4 узла',
    meta: '11 с · вызовов инструментов: 2',
    selected: ['M300 186H460', 'M300 186V60', 'M300 186V320', 'M300 100H350', 'M300 290H360', 'M300 140H250'],
    closed: [],
    valves: [{ x: 262, y: 187 }, { x: 448, y: 187 }],
    rings: [],
    buildings: ['e', 'f', 'g', 'h', 'l']
  },
  {
    id: 'select',
    tab: 'Выборка вопросом',
    place: 'Ду 500 · до 1980 г.',
    question: 'Участки Ду 500, проложенные до 1980 года, в 300 м от школ',
    steps: [
      {
        title: 'Выборка объектов по условиям',
        params: 'target: lines · conditions: {"field":"diameter","op":"eq","value":500}, {"field":"year","op":"lt","value":1980} · near_poi: {"categories":["school"],"meters":300}',
        time: '1,8 с'
      }
    ],
    answer: [
      'Нашёл **12 участков** Ду 500 до 1980 года общей длиной **3,8 км**.',
      '• Все они в 300 м от двух школ — подсвечены на карте.',
      '• Самый старый проложен в 1968 году.'
    ],
    found: 'Найдено на карте: 12 участков',
    meta: '7,4 с · вызовов инструментов: 1',
    selected: ['M20 186H120', 'M120 186V330', 'M120 280H70'],
    closed: [],
    valves: [],
    rings: [{ x: 58, y: 280 }, { x: 172, y: 306 }],
    buildings: ['c', 'd']
  },
  {
    id: 'regime',
    tab: 'Разбор режима',
    place: 'Фрагмент 74 · −25 °C',
    question: 'Почему в последнем расчёте фрагмента 74 у части потребителей нет расхода?',
    steps: [
      { title: 'Расчёты фрагментов', params: 'fragment_ids: 74 · limit: 5', time: '0,3 с' },
      { title: 'Анализ режима', params: 'fragment_id: 74 · kind: closed_sections', time: '1,1 с' },
      { title: 'Трассировка сети', params: 'trace_type: downstream · start_node_ids: 2208', time: '0,9 с' }
    ],
    answer: [
      'В расчёте при −25 °C закрыта задвижка у **2ВВ-5**.',
      '• Она отрезала **6 потребителей** — у них нулевой расход.',
      '• Откройте её в сценарии «что если», пересчитайте и сравните режим с основой.'
    ],
    found: 'Найдено на карте: 6 участков и 7 узлов',
    meta: '14 с · вызовов инструментов: 3',
    selected: ['M120 90V40', 'M120 90H170'],
    closed: ['M120 90V40', 'M120 90H170'],
    valves: [{ x: 121, y: 104 }],
    rings: [],
    buildings: ['a', 'i']
  }
]

const current = ref(0)
const round = ref(0)
const visible = ref(false)
const typed = ref('')
const rootEl = ref<HTMLElement | null>(null)
const bodyEl = ref<HTMLElement | null>(null)
const scenario = computed(() => SCENARIOS[current.value]!)

/** Расписание сценария: когда задан вопрос, когда идёт и заканчивается каждый шаг, ответ, подвал, карта. */
const timeline = computed(() => {
  const s = scenario.value
  const ask = TYPE_START_MS + s.question.length * TYPE_CHAR_MS + SEND_PAUSE_MS
  const steps = ask + 900
  const stepAt = s.steps.map((_, i) => steps + i * STEP_GAP_MS)
  const stepsEnd = stepAt[stepAt.length - 1]! + STEP_RUN_MS
  const answer = stepsEnd + 900
  const footer = answer + s.answer.length * LINE_GAP_MS + 300
  const map = footer + 450
  const vars: Record<string, string> = {
    '--t-ask': `${ask}ms`,
    '--t-wait1': `${ask + 150}ms`,
    '--t-steps': `${steps}ms`,
    '--t-wait2': `${stepsEnd + 50}ms`,
    '--t-answer': `${answer}ms`,
    '--t-footer': `${footer}ms`,
    '--t-map': `${map}ms`
  }
  stepAt.forEach((at, i) => {
    vars[`--t-step-${i}`] = `${at}ms`
    vars[`--t-done-${i}`] = `${at + STEP_RUN_MS}ms`
  })
  return { ask, vars }
})

const segments = (line: string) => line.replace(/^• /, '').split('**').map((text, i) => ({ text, bold: i % 2 === 1 }))

let cycleTimer: ReturnType<typeof setTimeout> | null = null
let typeTimer: ReturnType<typeof setInterval> | null = null
let sendTimer: ReturnType<typeof setTimeout> | null = null
let followFrame = 0
let observer: IntersectionObserver | null = null

const stopTyping = () => {
  if (typeTimer) clearInterval(typeTimer)
  if (sendTimer) clearTimeout(sendTimer)
  typeTimer = null
  sendTimer = null
  typed.value = ''
}

const motionAllowed = () => !window.matchMedia('(prefers-reduced-motion: reduce)').matches

/** Вопрос набирается в поле, потом «отправляется» — в тот момент, когда в окне появляется пузырь. */
const startTyping = () => {
  stopTyping()
  if (!visible.value || !motionAllowed()) return
  const text = scenario.value.question
  let count = 0
  sendTimer = setTimeout(() => {
    typeTimer = setInterval(() => {
      count += 1
      typed.value = text.slice(0, count)
      if (count >= text.length && typeTimer) clearInterval(typeTimer)
    }, TYPE_CHAR_MS)
    sendTimer = setTimeout(() => { typed.value = '' }, timeline.value.ask - TYPE_START_MS)
  }, TYPE_START_MS)
}

/** Окно ответа держит низ в виду, как чат в приложении: новые шаги не уходят за край. */
const follow = () => {
  cancelAnimationFrame(followFrame)
  const started = performance.now()
  const tick = () => {
    const body = bodyEl.value
    if (body) body.scrollTop = body.scrollHeight
    if (visible.value && performance.now() - started < CYCLE_MS) followFrame = requestAnimationFrame(tick)
  }
  followFrame = requestAnimationFrame(tick)
}

const restart = () => {
  startTyping()
  follow()
}

const schedule = () => {
  if (cycleTimer) clearTimeout(cycleTimer)
  if (!visible.value) return
  cycleTimer = setTimeout(() => {
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

watch(round, () => nextTick(restart))

onMounted(() => {
  observer = new IntersectionObserver(([entry]) => {
    const was = visible.value
    visible.value = Boolean(entry?.isIntersecting)
    // Сценарий начинается заново, когда блок снова на экране, — иначе шаги отыграли бы за кадром.
    if (visible.value && !was) round.value += 1
    if (!visible.value) stopTyping()
    schedule()
  }, { threshold: 0.35 })
  if (rootEl.value) observer.observe(rootEl.value)
})

onBeforeUnmount(() => {
  if (cycleTimer) clearTimeout(cycleTimer)
  stopTyping()
  cancelAnimationFrame(followFrame)
  observer?.disconnect()
})
</script>

<style scoped>
.ai-demo {
  --ai-line: rgba(246, 244, 238, 0.14);
  --dialog-w: min(470px, 50%);
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

.ai-tab:focus-visible {
  outline: 2px solid #ff6b5e;
  outline-offset: -2px;
}

.ai-tab-title {
  font-family: var(--serif);
  font-size: 1.2rem;
}

.ai-tab-place {
  color: var(--on-dark-subtle);
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

/* --- сцена: карта на всю ширину, окно помощника поверх справа, как в приложении --- */
.ai-stage {
  position: relative;
  height: 560px;
  margin-top: 8px;
  overflow: hidden;
  border: 1px solid var(--ai-line);
  border-radius: 8px;
  background: #efece4;
}

.ai-map {
  position: absolute;
  inset: 0;
}

.ai-map svg {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  width: calc(100% - var(--dialog-w) - 24px);
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

/* Подложка и сеть — цвета веб-ТГИД (buildingStyle.ts, networkStyleTuning.ts, selectionHighlight.ts). */
.park {
  fill: #d6e8cb;
}

.road-edge,
.road {
  fill: none;
}

.road-edge {
  stroke: #d6d2c8;
}

.road {
  stroke: #fff;
}

.buildings rect {
  fill: #dcd8cf;
  stroke: #d2cabd;
  stroke-width: 0.8;
}

.buildings rect.consumer {
  fill: #e6cdb6;
  stroke: #e99a52;
  stroke-width: 1;
}

.map-text text,
.net-text text {
  paint-order: stroke;
  stroke: #fff;
  stroke-width: 2.4px;
  stroke-linejoin: round;
  font-family: var(--app-font);
}

.map-text .street {
  fill: #8c8a84;
  font-size: 7.5px;
}

.map-text .load {
  fill: #555;
  font-size: 6.4px;
}

.net-text text {
  fill: #333;
  font-size: 7.5px;
  font-weight: 500;
}

.net-text .dn {
  font-size: 6.8px;
  font-weight: 400;
}

.pipes path {
  fill: none;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.pipes .casing { stroke: #fff; stroke-opacity: 0.85; }
.pipes .supply { stroke: #7f0000; }
.pipes .return { stroke: #00007f; }
.pipes .closed { stroke: #808000; }

.node {
  fill: #fff;
  stroke: #111;
  stroke-width: 1.2;
}

.node-dot {
  fill: #111;
}

.ai-selected path {
  fill: none;
  stroke: #00c8ff;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.ai-selected .halo {
  stroke-opacity: 0.35;
  stroke-width: 11;
}

.ai-selected .line {
  stroke-width: 2.4;
}

/* Найденное появляется на карте вместе с «Показано» в подвале ответа. */
.buildings rect.hit {
  animation: ai-hit 0.5s ease var(--t-map) both;
}

.ai-selected .line {
  stroke-dasharray: 1;
  stroke-dashoffset: 1;
  animation: ai-draw 0.9s cubic-bezier(0.6, 0, 0.2, 1) calc(var(--t-map) + var(--i) * 110ms) both;
}

.ai-selected .halo,
.ai-closed {
  animation: ai-fade 0.6s ease calc(var(--t-map) + var(--i) * 110ms) both;
}

.ai-valve,
.ai-ring {
  transform-box: fill-box;
  transform-origin: center;
  animation: ai-pop 0.45s cubic-bezier(0.3, 1.6, 0.5, 1) calc(var(--t-map) + 300ms + var(--i) * 140ms) both;
}

/* --- окно «Помощник ИИ»: Vuetify-тема ТГИД (Roboto, primary #1565C0, радиус 12) --- */
.ai-dialog {
  position: absolute;
  top: 20px;
  right: 20px;
  bottom: 20px;
  display: flex;
  flex-direction: column;
  width: var(--dialog-w);
  overflow: hidden;
  border-radius: 12px;
  color: var(--app-text);
  background: #fff;
  box-shadow: 0 11px 15px -7px rgba(0, 0, 0, 0.2), 0 24px 38px 3px rgba(0, 0, 0, 0.14), 0 9px 46px 8px rgba(0, 0, 0, 0.12);
  font-family: var(--app-font);
  font-size: 14px;
  line-height: 1.45;
  animation: ai-window 0.6s cubic-bezier(0.2, 0.8, 0.2, 1) both;
}

.ai-head {
  display: flex;
  flex: none;
  align-items: center;
  gap: 8px;
  padding: 12px 12px 12px 16px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}

.ai-head svg {
  width: 22px;
  height: 22px;
  fill: currentColor;
}

.ai-head-icon {
  color: var(--app-primary);
}

.ai-head-title {
  font-size: 18px;
  font-weight: 500;
}

.ai-head-new {
  margin-left: auto;
  padding: 4px 8px;
  border-radius: 6px;
  color: var(--app-primary);
  font-size: 13px;
  font-weight: 500;
}

.ai-head-close {
  color: var(--app-muted);
}

.ai-body {
  flex: 1;
  min-height: 0;
  padding: 4px 16px 12px;
  overflow: hidden;
}

/* Каждый новый кусок ответа «раздвигает» окно, а не появляется в заранее занятом месте. */
.grow,
.wait {
  display: grid;
  grid-template-rows: 1fr;
}

.grow > div,
.wait > div {
  min-height: 0;
  overflow: hidden;
}

.ai-user {
  max-width: 88%;
  margin: 12px 0 0 auto;
  padding: 8px 12px;
  border-radius: 12px 12px 4px 12px;
  background: rgba(21, 101, 192, 0.1);
  width: fit-content;
}

.ai-wait {
  margin: 10px 0 0;
  color: var(--app-muted);
  font-size: 12px;
}

.ai-steps {
  margin-top: 12px;
  padding: 6px 10px;
  border-left: 3px solid rgba(21, 101, 192, 0.35);
  border-radius: 4px;
  background: rgba(21, 101, 192, 0.03);
}

.ai-step {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin: 2px 0;
  font-size: 12px;
  line-height: 1.5;
  overflow-wrap: anywhere;
}

.ai-step b {
  font-weight: 500;
}

.ai-step-params,
.ai-step-time {
  color: var(--app-muted);
}

.ai-step-state {
  position: relative;
  flex: none;
  width: 16px;
  height: 16px;
  margin-top: 1px;
}

.ai-step-state svg {
  position: absolute;
  inset: 0;
  width: 16px;
  height: 16px;
}

.spin {
  opacity: 0;
}

.spin circle {
  fill: none;
  stroke: var(--app-primary);
  stroke-width: 2;
  stroke-dasharray: 26 12;
  stroke-linecap: round;
}

.check {
  fill: var(--app-success);
}

.ai-answer {
  margin: 10px 0 0;
}

.ai-answer.bullet {
  position: relative;
  margin-top: 4px;
  padding-left: 16px;
}

.ai-answer.bullet::before {
  content: "•";
  position: absolute;
  left: 4px;
}

.ai-answer b {
  font-weight: 500;
}

.ai-found {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  margin-top: 12px;
  color: var(--app-muted);
  font-size: 12px;
}

.ai-chip {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  height: 24px;
  padding: 0 10px 0 8px;
  border: 1px solid rgba(21, 101, 192, 0.5);
  border-radius: 6px;
  color: var(--app-primary);
  font-size: 12px;
  font-weight: 500;
}

.ai-chip svg {
  width: 15px;
  height: 15px;
  fill: currentColor;
}

/* Обе надписи в одной ячейке: смена «Показать на карте» → «Показано» без скачка ширины. */
.chip-text {
  display: grid;
}

.chip-a,
.chip-b {
  grid-area: 1 / 1;
}

.chip-b {
  opacity: 0;
}

.ai-meta {
  margin: 6px 0 0;
  color: var(--app-muted);
  font-size: 12px;
  text-align: right;
}

.ai-foot {
  flex: none;
  padding: 10px 16px 14px;
  border-top: 1px solid rgba(0, 0, 0, 0.12);
}

.ai-input {
  min-height: 52px;
  padding: 8px 12px;
  border: 1px solid rgba(0, 0, 0, 0.38);
  border-radius: 4px;
  font-size: 14px;
  line-height: 1.4;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.ai-input.typing {
  border-color: var(--app-primary);
  box-shadow: inset 0 0 0 1px var(--app-primary);
}

.ai-placeholder {
  color: rgba(0, 0, 0, 0.5);
}

.ai-caret {
  display: inline-block;
  width: 1.5px;
  height: 1.1em;
  margin-left: 1px;
  vertical-align: -0.2em;
  background: var(--app-primary);
  animation: ai-blink 1s steps(1) infinite;
}

.ai-hint {
  margin: 6px 0 0;
  color: var(--app-muted);
  font-size: 11px;
  line-height: 1.35;
}

.ai-buttons {
  position: relative;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
}

.ai-btn-text {
  padding: 6px 10px;
  color: var(--app-primary);
  font-size: 13px;
  font-weight: 500;
}

.ai-btn-primary {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 14px;
  overflow: hidden;
  border-radius: 6px;
  color: #fff;
  background: var(--app-primary);
  box-shadow: 0 3px 1px -2px rgba(0, 0, 0, 0.2), 0 2px 2px rgba(0, 0, 0, 0.14);
  font-size: 13px;
  font-weight: 500;
}

.ai-btn-primary svg {
  width: 16px;
  height: 16px;
  fill: currentColor;
}

.ai-press {
  position: absolute;
  top: 50%;
  left: 70%;
  width: 90px;
  height: 90px;
  margin: -45px 0 0 -45px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.35);
  opacity: 0;
  transform: scale(0);
}

.ai-cursor {
  position: absolute;
  right: 18px;
  bottom: -6px;
  opacity: 0;
  filter: drop-shadow(0 2px 3px rgba(0, 0, 0, 0.3));
  pointer-events: none;
}

/* --- ход сценария: только когда движение разрешено; без него окно показано целиком --- */
@media (prefers-reduced-motion: no-preference) {
  .grow {
    animation: ai-grow 0.45s cubic-bezier(0.2, 0.8, 0.2, 1) var(--at) both;
  }

  .wait {
    grid-template-rows: 0fr;
    opacity: 0;
    animation: ai-wait 0.75s ease var(--at) both;
  }

  .spin {
    animation: ai-show-hide var(--run) linear var(--at-start) both, ai-rotate 0.8s linear infinite;
  }

  .ai-step-state {
    --run: 750ms;
    --at-start: calc(var(--at) - var(--run));
  }

  .check {
    animation: ai-pop 0.35s cubic-bezier(0.3, 1.6, 0.5, 1) var(--at) both;
  }

  .ai-step-time {
    animation: ai-fade 0.3s ease var(--at) both;
  }

  .chip-a {
    animation: ai-fade-out 0.25s ease var(--t-map) both;
  }

  .chip-b {
    animation: ai-fade-in 0.25s ease var(--t-map) both;
  }

  .ai-chip {
    animation: ai-chip-fill 0.3s ease var(--t-map) both;
  }

  .ai-cursor {
    animation: ai-cursor 1.3s cubic-bezier(0.45, 0, 0.25, 1) calc(var(--t-ask) - 900ms) both;
  }

  .ai-press {
    animation: ai-press 0.5s ease-out calc(var(--t-ask) - 120ms) both;
  }

  .ai-btn-primary {
    animation: ai-btn 0.25s ease calc(var(--t-ask) - 120ms) both;
  }
}

/* Без анимации подвал сразу в конечном виде: «Показано». */
@media (prefers-reduced-motion: reduce) {
  .ai-stage *,
  .ai-dialog,
  .ai-tab-progress {
    animation: none !important;
  }

  .spin,
  .wait {
    display: none;
  }

  .chip-a {
    opacity: 0;
  }

  .chip-b {
    opacity: 1;
  }

  .ai-chip {
    color: #fff;
    background: var(--app-primary);
  }
}

.ai-note {
  margin: 14px 0 0;
  color: var(--on-dark-subtle);
  font-size: 0.8rem;
}

.paused .ai-stage,
.paused .ai-stage * {
  animation-play-state: paused !important;
}

@keyframes ai-window {
  from { opacity: 0; transform: translateY(18px) scale(0.98); }
}

@keyframes ai-grow {
  from { grid-template-rows: 0fr; opacity: 0; transform: translateY(6px); }
}

@keyframes ai-wait {
  0% { grid-template-rows: 0fr; opacity: 0; }
  20%, 80% { grid-template-rows: 1fr; opacity: 1; }
  100% { grid-template-rows: 0fr; opacity: 0; }
}

@keyframes ai-show-hide {
  0%, 99% { opacity: 1; }
  100% { opacity: 0; }
}

@keyframes ai-rotate {
  to { transform: rotate(360deg); }
}

@keyframes ai-fade-out {
  to { opacity: 0; }
}

@keyframes ai-fade-in {
  to { opacity: 1; }
}

@keyframes ai-chip-fill {
  to { color: #fff; background: var(--app-primary); border-color: var(--app-primary); }
}

@keyframes ai-cursor {
  0% { opacity: 0; transform: translate(-90px, 46px); }
  20% { opacity: 1; }
  60% { transform: translate(0, 0); }
  70% { transform: translate(0, 0) scale(0.86); }
  78% { opacity: 1; transform: translate(0, 0); }
  100% { opacity: 0; transform: translate(8px, 12px); }
}

@keyframes ai-press {
  0% { opacity: 1; transform: scale(0); }
  100% { opacity: 0; transform: scale(1); }
}

@keyframes ai-btn {
  50% { transform: scale(0.95); }
}

@keyframes ai-blink {
  50% { opacity: 0; }
}

@keyframes ai-hit {
  to { fill: rgba(0, 200, 255, 0.22); stroke: #00c8ff; }
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


/* Планшет и телефон: карта сверху, окно помощника ниже, «листом» поверх края карты. */
@media (max-width: 900px) {
  .ai-demo {
    --dialog-w: 100%;
  }

  .ai-stage {
    display: flex;
    flex-direction: column;
    height: auto;
  }

  .ai-map {
    position: relative;
    height: 240px;
    flex: none;
  }

  .ai-map svg {
    width: 100%;
  }

  .ai-dialog {
    position: relative;
    inset: auto;
    width: auto;
    height: 540px;
    margin: -24px 8px 8px;
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

  .ai-map {
    height: 200px;
  }

  .ai-dialog {
    height: 520px;
    margin: -20px 0 0;
    border-radius: 12px 12px 0 0;
  }

  .ai-head-new {
    display: none;
  }

  .ai-hint {
    display: none;
  }
}
</style>
