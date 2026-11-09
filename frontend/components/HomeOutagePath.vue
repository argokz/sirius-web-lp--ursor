<template>
  <figure ref="rootEl" class="path" :class="{ on: inView }" aria-label="Путь аварии в ТГИД: от сигнала до включения">
    <!-- Пара труб (подача и обратка) с камерами-шагами; голубое выделение идёт по ним, как на карте. -->
    <div class="pipe" aria-hidden="true">
      <i class="pipe-supply" />
      <i class="pipe-return" />
      <i class="pipe-glow" :style="{ '--p': progress }" />
    </div>
    <ol class="steps">
      <li v-for="(step, i) in STEPS" :key="step.title" class="step" :class="{ lit: i <= active, current: i === active, 'seg-lit': i < active }">
        <span class="node" aria-hidden="true"><i /></span>
        <span class="step-num">{{ String(i + 1).padStart(2, '0') }}</span>
        <b class="step-title">{{ step.title }}</b>
        <span class="step-text">{{ typo(step.text) }}</span>
        <code class="step-event">{{ step.event }}</code>
      </li>
    </ol>
  </figure>
</template>

<script setup lang="ts">
/**
 * Инфографика «авария одним процессом»: шесть шагов от сигнала до включения, каждый — функция ТГИД.
 * Подпись снизу — событие вебхука или окно, где шаг живёт (database/api_events.py, справка 03-operations).
 * Шаги загораются по очереди, пока блок на экране; при reduced motion горят все сразу.
 */
const STEPS = [
  { title: 'Сигнал', text: 'Дефект с обхода, звонок в диспетчерскую или тревога датчика.', event: 'defect.created' },
  { title: 'Локализация', text: 'Какие задвижки закрыть, какие здания останутся без тепла, сколько Гкал/ч.', event: 'окно «Локализация аварии»' },
  { title: 'Отключение', text: 'Зона на карте, пересечения с другими отключениями, социальные объекты в зоне.', event: 'outage.created' },
  { title: 'Оповещение', text: 'Лента отключений для жителей и событие во внешние системы.', event: 'вебхук · лента' },
  { title: 'Наряд', text: 'Бригаде в телефон: место, сеть рядом, форма обхода, фото — и без связи.', event: 'work_order.created' },
  { title: 'Включение', text: 'Наряд закрыт, отключение завершено — всё остаётся в журнале и показателях.', event: 'outage.status_changed' }
]

const STEP_MS = 1500
const HOLD_STEPS = 3

const rootEl = ref<HTMLElement | null>(null)
const inView = useInView(rootEl, 0.35)
const motion = useMotionAllowed()
const tick = ref(-1)
const active = computed(() => (motion.value ? Math.min(tick.value, STEPS.length - 1) : STEPS.length - 1))
const progress = computed(() => Math.max(active.value, 0) / (STEPS.length - 1))

let timer: ReturnType<typeof setInterval> | null = null
watch([inView, motion], ([seen, allowed]) => {
  if (!seen || !allowed || timer) return
  tick.value = 0
  // По шагу каждые 1,5 с, на последнем — пауза, потом заново.
  timer = setInterval(() => {
    tick.value = tick.value >= STEPS.length - 1 + HOLD_STEPS ? 0 : tick.value + 1
  }, STEP_MS)
})
onBeforeUnmount(() => {
  if (timer) clearInterval(timer)
})
</script>

<style scoped>
.path {
  --node: 26px;
  position: relative;
  margin: 0;
}

.pipe {
  position: absolute;
  top: calc(var(--node) / 2 - 3px);
  left: calc(100% / 12);
  right: calc(100% / 12);
  height: 8px;
}

.pipe i {
  position: absolute;
  left: 0;
  right: 0;
  height: 2px;
  border-radius: 1px;
}

.pipe-supply { top: 0; background: #7f0000; box-shadow: 0 0 0 1px #fff; }
.pipe-return { top: 5px; background: #00007f; box-shadow: 0 0 0 1px #fff; }

/* Выделение как в ТГИД: голубой ореол поверх пары труб, растёт до текущего шага. */
.pipe-glow {
  top: -3px !important;
  right: auto !important;
  width: calc(var(--p) * 100%);
  height: 14px !important;
  border-radius: 7px !important;
  background: rgba(0, 200, 255, 0.35);
  box-shadow: 0 0 10px rgba(0, 200, 255, 0.45), inset 0 0 0 1px rgba(0, 200, 255, 0.6);
  transition: width 1.2s cubic-bezier(0.45, 0, 0.25, 1);
}

.steps {
  position: relative;
  display: grid;
  grid-template-columns: repeat(6, minmax(0, 1fr));
  gap: 16px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.step {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  text-align: center;
}

/* Камера: кольцо с точкой — значок узла сети в ТГИД. */
.node {
  display: grid;
  place-items: center;
  width: var(--node);
  height: var(--node);
  margin-bottom: 10px;
  border: 2px solid var(--ink);
  border-radius: 50%;
  background: var(--paper);
  transition: border-color 0.4s ease, box-shadow 0.4s ease, transform 0.4s ease;
}

.node i {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--ink);
  transition: background 0.4s ease;
}

.step.lit .node {
  border-color: #00a7d6;
  box-shadow: 0 0 0 4px rgba(0, 200, 255, 0.18);
}

.step.lit .node i {
  background: #00a7d6;
}

.step.current .node {
  transform: scale(1.18);
}

.step-num {
  color: var(--accent);
  font-family: var(--mono);
  font-size: 0.72rem;
  letter-spacing: 0.06em;
}

.step-title {
  font-family: var(--serif);
  font-size: 1.3rem;
  font-weight: 400;
  line-height: 1.15;
}

.step-text {
  color: var(--ink-2);
  font-size: 0.86rem;
  line-height: 1.45;
}

.step-event {
  margin-top: 4px;
  padding: 3px 7px;
  border: 1px solid var(--line);
  border-radius: 4px;
  color: var(--muted);
  background: var(--surface);
  font-family: var(--mono);
  font-size: 0.66rem;
  transition: border-color 0.4s ease, color 0.4s ease;
}

.step.current .step-event {
  border-color: #00a7d6;
  color: var(--ink);
}

@media (prefers-reduced-motion: reduce) {
  .pipe-glow,
  .node,
  .node i,
  .step-event {
    transition: none;
  }
}

/* Узко: шаги строками, между узлами — отрезки пары труб; пройденные подсвечены. */
@media (max-width: 899px) {
  .pipe {
    display: none;
  }

  .steps {
    grid-template-columns: 1fr;
    gap: 22px;
  }

  .step {
    position: relative;
    display: grid;
    grid-template-columns: var(--node) minmax(0, 1fr);
    column-gap: 16px;
    row-gap: 4px;
    align-items: start;
    text-align: left;
  }

  .step:not(:last-child)::before {
    content: "";
    position: absolute;
    top: calc(var(--node) / 2);
    left: calc(var(--node) / 2 - 4px);
    width: 2px;
    height: calc(100% + 22px);
    background: #7f0000;
    box-shadow: 5px 0 0 #00007f;
    transition: box-shadow 0.6s ease;
  }

  .step.seg-lit::before {
    box-shadow: 5px 0 0 #00007f, 0 0 0 4px rgba(0, 200, 255, 0.3), 5px 0 0 4px rgba(0, 200, 255, 0.3);
  }

  .node {
    position: relative;
    z-index: 1;
    grid-row: 1 / span 4;
    margin: 0;
  }

  .step-event {
    justify-self: start;
  }
}
</style>
