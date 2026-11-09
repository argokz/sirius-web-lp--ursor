<template>
  <div class="phones-box" aria-hidden="true">
  <div class="phones">
    <div class="phone phone-back">
      <div class="phone-screen">
        <div class="ph-bar ph-bar-stack">
          <span>Обход · форма «Камера»</span>
          <span class="ph-sync">
            <i class="ph-sync-dot" />
            <span class="ph-sync-text">
              <span class="ph-sync-off">Нет связи · 3 в очереди</span>
              <span class="ph-sync-on">Отправлено</span>
            </span>
          </span>
        </div>
        <div class="ph-photo">
          <svg viewBox="0 0 200 110">
            <rect width="200" height="110" fill="#5b5446" />
            <rect x="20" y="58" width="160" height="16" rx="8" fill="#8b7d63" />
            <rect x="20" y="58" width="160" height="5" rx="2.5" fill="#a89878" />
            <circle cx="140" cy="66" r="9" fill="#c0392b" opacity="0.75" />
            <path d="M0 96 Q 60 84 120 92 T 200 88 V110 H0Z" fill="#3f3a30" />
          </svg>
          <span class="ph-photo-tag">ФОТО 2 из 3</span>
        </div>
        <div class="ph-field">
          <span>Состояние изоляции</span>
          <div class="ph-options">
            <b>Норма</b><b class="on">Повреждена</b><b>Нет</b>
          </div>
        </div>
        <div class="ph-field">
          <span>Затопление камеры</span>
          <div class="ph-check"><i class="on" /> Есть, до 30 см</div>
        </div>
        <div class="ph-cta">Сохранить и дальше</div>
      </div>
    </div>

    <div class="phone phone-front">
      <div class="phone-screen">
        <div class="ph-bar">
          <span>Бригада 4 · наряды</span>
          <span class="ph-count">3</span>
        </div>
        <div class="ph-map">
          <svg viewBox="0 0 200 120">
            <rect width="200" height="120" fill="#efece4" />
            <path d="M0 40H200M0 92H200M60 0V120M150 0V120" stroke="#fff" stroke-width="8" />
            <path d="M10 66H190M60 66V10M150 66V115" stroke="#7f0000" stroke-width="2.4" fill="none" />
            <path class="ph-track" d="M20 100 L60 92 L60 66 L110 66 L150 66 L150 40" fill="none" stroke="#00a7d6" stroke-width="2.4" stroke-dasharray="4 4" />
            <circle cx="150" cy="40" r="6" fill="#e30613" stroke="#fff" stroke-width="2" class="ph-pin" />
          </svg>
          <span class="ph-map-tag">ТРЕК 2,4 КМ</span>
        </div>
        <div v-for="order in ORDERS" :key="order.num" class="ph-order">
          <div>
            <strong>{{ order.title }}</strong>
            <small>№{{ order.num }} · {{ order.place }}</small>
          </div>
          <span class="ph-status" :class="order.tone">{{ order.status }}</span>
        </div>
      </div>
    </div>
  </div>
  </div>
</template>

<script setup lang="ts">
// Полевое приложение /field в двух экранах: наряды бригады с треком и форма обхода с фото без связи.
const ORDERS = [
  { title: 'Устранить течь', num: '1207', place: '2КД-11', status: 'На месте', tone: 'warn' },
  { title: 'Осмотр камеры', num: '1211', place: '2ВВ-5', status: 'В работе', tone: 'info' },
  { title: 'Опрессовка', num: '1198', place: 'М2', status: 'Выполнен', tone: 'ok' }
]
</script>

<style scoped>
/* Телефоны масштабируются по ширине колонки, а не окна. */
.phones-box {
  container-type: inline-size;
}

.phones {
  position: relative;
  height: 520px;
  max-width: 520px;
  margin-inline: auto;
}

.phone {
  position: absolute;
  width: 250px;
  height: 500px;
  padding: 10px;
  border: 1px solid var(--ink);
  border-radius: 34px;
  background: var(--ink);
  box-shadow: 0 40px 60px -40px rgba(28, 27, 24, 0.6);
}

.phone-back {
  top: 0;
  right: 0;
  transform: rotate(4deg);
  animation: phone-float 7s ease-in-out infinite;
}

.phone-front {
  bottom: 0;
  left: 0;
  transform: rotate(-3deg);
  animation: phone-float-2 8s ease-in-out infinite;
}

@keyframes phone-float {
  50% { transform: rotate(4deg) translateY(-10px); }
}

@keyframes phone-float-2 {
  50% { transform: rotate(-3deg) translateY(8px); }
}

.phone-screen {
  height: 100%;
  display: flex;
  flex-direction: column;
  gap: 10px;
  overflow: hidden;
  padding: 14px 12px;
  border-radius: 25px;
  color: #18181b;
  background: #f4f4f5;
  font-family: Roboto, var(--font-sans), sans-serif;
  font-size: 11px;
}

.ph-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 6px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e4e4e7;
  font-weight: 600;
}

.ph-bar-stack {
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
}

.ph-count {
  display: grid;
  place-items: center;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  color: #fff;
  background: #e30613;
  font-size: 10px;
}

.ph-sync {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: #a16207;
  font-size: 9px;
  font-weight: 500;
}

.ph-sync-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}

/* Очередь без связи уходит на сервер, когда связь появилась: подпись и цвет меняются по кругу. */
.ph-sync {
  animation: sync-color 8s steps(1) infinite;
}

.ph-sync-text {
  display: inline-grid;
  justify-items: end;
}

.ph-sync-off,
.ph-sync-on {
  grid-area: 1 / 1;
  white-space: nowrap;
}

.ph-sync-off {
  animation: sync-off 8s steps(1) infinite;
}

.ph-sync-on {
  opacity: 0;
  animation: sync-on 8s steps(1) infinite;
}

@keyframes sync-color {
  0% { color: #a16207; }
  60% { color: #15803d; }
}

@keyframes sync-off {
  0% { opacity: 1; }
  60% { opacity: 0; }
}

@keyframes sync-on {
  0% { opacity: 0; }
  60% { opacity: 1; }
}

.ph-photo,
.ph-map {
  position: relative;
  overflow: hidden;
  border-radius: 10px;
}

.ph-photo svg,
.ph-map svg {
  display: block;
  width: 100%;
  height: auto;
}

.ph-photo-tag,
.ph-map-tag {
  position: absolute;
  left: 8px;
  bottom: 8px;
  padding: 2px 6px;
  border-radius: 4px;
  color: #fff;
  background: rgba(0, 0, 0, 0.55);
  font-family: var(--mono);
  font-size: 8px;
  letter-spacing: 0.06em;
}

.ph-map-tag {
  color: #18181b;
  background: rgba(255, 255, 255, 0.9);
}

.ph-track {
  animation: track-march 1.6s linear infinite;
}

@keyframes track-march {
  to { stroke-dashoffset: -16; }
}

.ph-pin {
  transform-box: fill-box;
  transform-origin: center;
  animation: pin-pulse 2s ease-in-out infinite;
}

@keyframes pin-pulse {
  50% { transform: scale(1.25); }
}

.ph-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 8px;
  border-radius: 8px;
  background: #fff;
}

.ph-field > span {
  color: #52525b;
}

.ph-options {
  display: flex;
  gap: 4px;
}

.ph-options b {
  flex: 1;
  padding: 5px 0;
  border: 1px solid #d4d4d8;
  border-radius: 6px;
  font-weight: 500;
  text-align: center;
}

.ph-options b.on {
  border-color: #0a7af2;
  color: #fff;
  background: #0a7af2;
}

.ph-check {
  display: flex;
  align-items: center;
  gap: 6px;
}

.ph-check i {
  width: 14px;
  height: 14px;
  border: 2px solid #0a7af2;
  border-radius: 3px;
  background: #0a7af2;
}

.ph-cta {
  margin-top: auto;
  padding: 10px;
  border-radius: 8px;
  color: #fff;
  background: #18181b;
  font-weight: 600;
  text-align: center;
}

.ph-order {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 8px;
  border-radius: 8px;
  background: #fff;
}

.ph-order div {
  display: flex;
  flex-direction: column;
}

.ph-order small {
  color: #71717a;
  font-size: 9.5px;
}

.ph-status {
  padding: 2px 6px;
  border-radius: 999px;
  font-size: 9px;
  font-weight: 600;
}

.ph-status.warn { color: #a16207; background: #fef3c7; }
.ph-status.info { color: #1d4ed8; background: #dbeafe; }
.ph-status.ok { color: #15803d; background: #dcfce7; }

@container (max-width: 519px) {
  .phones {
    zoom: 0.84;
  }
}

@container (max-width: 400px) {
  .phones {
    zoom: 0.7;
  }
}

@media (prefers-reduced-motion: reduce) {
  .phone,
  .ph-track,
  .ph-pin {
    animation: none;
  }
}
</style>
