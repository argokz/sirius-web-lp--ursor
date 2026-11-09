<template>
  <div ref="rootEl" class="proof" :class="{ on: inView }">
    <!-- 1. Прогноз повреждений: 20 км из 928 — 60 % повреждений. -->
    <figure class="proof-card">
      <span class="proof-tag">Прогноз повреждений · Астана</span>
      <strong class="proof-big num">60&nbsp;%</strong>
      <p class="proof-lead">{{ typo('повреждений 2022–2023 года пришлись на 20 км сети, которые заранее выбрал прогноз.') }}</p>
      <div class="bars" aria-hidden="true">
        <div class="bar-row">
          <span class="bar-label">Сеть, 928 км</span>
          <span class="bar"><i class="bar-fill net" :style="{ '--v': 20 / 928 }" /></span>
          <span class="bar-value num">20 км</span>
        </div>
        <div class="bar-row">
          <span class="bar-label">Повреждения</span>
          <span class="bar"><i class="bar-fill" :style="{ '--v': 0.6 }" /></span>
          <span class="bar-value num">60 %</span>
        </div>
      </div>
      <figcaption>{{ typo('Модель училась на журнале повреждений до 2020 года, проверка — на следующих годах. Случайные 20 км поймали бы около 2 %.') }}</figcaption>
    </figure>

    <!-- 2. Последствия аварии: сверка заранее посчитанного с полной локализацией. -->
    <figure class="proof-card">
      <span class="proof-tag">Кого отключит авария</span>
      <strong class="proof-big num">100 из 100</strong>
      <p class="proof-lead">{{ typo('случаев совпали с полной локализацией аварии: 60 в Астане и 40 в Алматы.') }}</p>
      <div class="dots" aria-hidden="true">
        <i v-for="n in 100" :key="n" :class="n <= 60 ? 'a' : 'b'" :style="{ '--n': n }" />
      </div>
      <div class="legend" aria-hidden="true"><span><i class="a" />Астана</span><span><i class="b" />Алматы</span></div>
      <figcaption>{{ typo('Для каждого участка заранее известно, кто останется без тепла при аварии на нём: 94,7 тыс. участков Астаны считаются примерно за 13 с.') }}</figcaption>
    </figure>

    <!-- 3. heatnet против прежнего движка. -->
    <figure class="proof-card">
      <span class="proof-tag">Расчёт heatnet · Алматы</span>
      <strong class="proof-big num">±0,01&nbsp;%</strong>
      <p class="proof-lead">{{ typo('расхождение по теплу с эталонными расчётами прежнего движка.') }}</p>
      <div class="bars" aria-hidden="true">
        <div class="bar-row">
          <span class="bar-label">Прежний движок</span>
          <span class="bar"><i class="bar-fill ref" :style="{ '--v': 0.86 }" /></span>
          <span class="bar-value num">100 %</span>
        </div>
        <div class="bar-row">
          <span class="bar-label">heatnet</span>
          <span class="bar"><i class="bar-fill" :style="{ '--v': 0.86 }" /></span>
          <span class="bar-value num">±0,01 %</span>
        </div>
      </div>
      <figcaption>{{ typo('Сверка на сетях Алматы, Астаны и Шатуры; найденные ошибки прежнего движка исправлены и описаны в справке.') }}</figcaption>
    </figure>
  </div>
</template>

<script setup lang="ts">
/**
 * Инфографика «проверено на данных»: три числа из проверок на сетях городов.
 * Источники: ретроспектива прогноза Астаны (обучение до 2020, проверка 2022–2023, 20 км — 60 %),
 * сверка tgid_line_consequence с локализацией (60/60 Астана, 40/40 Алматы), сверка heatnet с sety.
 */
const rootEl = ref<HTMLElement | null>(null)
const inView = useInView(rootEl, 0.25)
</script>

<style scoped>
.proof {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 20px;
}

.proof-card {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin: 0;
  padding: 26px 24px 22px;
  border: 1px solid var(--line);
  border-radius: 10px;
  background: var(--surface);
}

.proof-tag {
  color: var(--accent);
  font-family: var(--mono);
  font-size: 0.7rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.proof-big {
  margin-top: 6px;
  font-family: var(--serif);
  font-size: clamp(2.6rem, 4.2vw, 3.6rem);
  font-weight: 400;
  line-height: 1;
  letter-spacing: -0.03em;
}

.proof-lead {
  margin: 0;
  color: var(--ink-2);
  font-size: 0.98rem;
  line-height: 1.5;
}

.proof-card figcaption {
  margin-top: auto;
  padding-top: 14px;
  border-top: 1px solid var(--line);
  color: var(--muted);
  font-size: 0.82rem;
  line-height: 1.5;
}

.bars {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin: 10px 0 4px;
}

.bar-row {
  display: grid;
  grid-template-columns: 112px minmax(0, 1fr) 64px;
  align-items: center;
  gap: 10px;
  font-size: 0.8rem;
}

.bar-label {
  color: var(--muted);
}

.bar-value {
  font-family: var(--mono);
  font-size: 0.74rem;
  text-align: right;
}

.bar {
  position: relative;
  height: 12px;
  overflow: hidden;
  border-radius: 2px;
  background: var(--paper-2);
  box-shadow: inset 0 0 0 1px var(--line);
}

.bar-fill {
  position: absolute;
  inset: 0 auto 0 0;
  width: calc(var(--v) * 100%);
  min-width: 3px;
  background: var(--accent);
}

.bar-fill.net {
  background: var(--accent);
}

.bar-fill.ref {
  background: var(--ink-2);
}

.dots {
  display: grid;
  grid-template-columns: repeat(20, 1fr);
  gap: 4px;
  margin: 10px 0 0;
}

.dots i {
  aspect-ratio: 1;
  border-radius: 50%;
}

.dots .a,
.legend .a { background: var(--accent); }
.dots .b,
.legend .b { background: var(--ink-2); }

.legend {
  display: flex;
  gap: 16px;
  color: var(--muted);
  font-size: 0.78rem;
}

.legend i {
  display: inline-block;
  width: 8px;
  height: 8px;
  margin-right: 6px;
  border-radius: 50%;
}

/* Полосы растут и точки ставятся по одной, когда блок дошёл до экрана. */
@media (scripting: enabled) and (prefers-reduced-motion: no-preference) {
  .bar-fill {
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 1.2s cubic-bezier(0.2, 0.75, 0.15, 1) 0.3s;
  }

  .bar-row + .bar-row .bar-fill {
    transition-delay: 0.7s;
  }

  .on .bar-fill {
    transform: none;
  }

  .dots i {
    opacity: 0;
    transform: scale(0.3);
    transition: opacity 0.3s ease, transform 0.3s cubic-bezier(0.3, 1.6, 0.5, 1);
    transition-delay: calc(0.3s + var(--n) * 14ms);
  }

  .on .dots i {
    opacity: 1;
    transform: none;
  }
}

@media (max-width: 1023px) {
  .proof {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 420px) {
  .bar-row {
    grid-template-columns: 96px minmax(0, 1fr) 56px;
  }
}
</style>
