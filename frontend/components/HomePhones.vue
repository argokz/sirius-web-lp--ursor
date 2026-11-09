<template>
  <div class="phones-box" aria-hidden="true">
    <div class="phones">
      <!-- Экран наряда (/field/<id>): карта сети вокруг места, обход, фото, очередь без связи. -->
      <div class="phone phone-back">
        <div class="phone-screen">
          <div class="ph-bar">
            <svg class="ph-icon" viewBox="0 0 24 24"><path :d="ICONS.back" /></svg>
            <div class="ph-bar-title">
              <strong>Н-2026-00031</strong>
              <small>Алматы</small>
            </div>
          </div>
          <div class="ph-body">
            <div class="ph-chips">
              <span class="chip flat progress">В работе</span>
              <span class="ph-muted">Ремонт · Срочный</span>
            </div>
            <strong class="ph-title">Устранить течь в камере 2КД-11</strong>
            <small class="ph-muted">участок 1494 · фр. 2</small>
            <div class="ph-map">
              <svg viewBox="0 0 220 104">
                <rect width="220" height="104" fill="#efede8" />
                <path d="M0 34H220M0 80H220M70 0V104M168 0V104" stroke="#d6d2c8" stroke-width="11" />
                <path d="M0 34H220M0 80H220M70 0V104M168 0V104" stroke="#fff" stroke-width="9" />
                <g fill="#dcd8cf" stroke="#d2cabd" stroke-width="0.6"><rect x="10" y="44" width="48" height="26" rx="2" /><rect x="84" y="6" width="70" height="20" rx="2" /><rect x="180" y="44" width="34" height="28" rx="2" /><rect x="84" y="88" width="60" height="16" rx="2" /></g>
                <path d="M0 58H220M70 58V0M168 58V104" stroke="#1565c0" stroke-width="2.2" fill="none" />
                <circle v-for="n in [[70, 58], [168, 58]]" :key="n[0]" :cx="n[0]" :cy="n[1]" r="3.4" fill="#fff" stroke="#1565c0" stroke-width="1.6" />
                <path class="ph-track" d="M8 96 L70 86 L70 58 L118 58" fill="none" stroke="#00a7d6" stroke-width="2.4" stroke-dasharray="4 4" />
                <circle cx="118" cy="58" r="5.5" fill="#e53935" stroke="#fff" stroke-width="1.8" class="ph-pin" />
              </svg>
              <span class="ph-map-tag">Сеть в радиусе 300 м, сохранена 09.11 08:40</span>
            </div>
            <div class="ph-actions">
              <span class="btn tonal"><svg viewBox="0 0 24 24"><path :d="ICONS.navigation" /></svg>Маршрут</span>
              <span class="btn text"><svg viewBox="0 0 24 24"><path :d="ICONS.marker" /></svg>На карте сети</span>
            </div>
            <div class="ph-walk">
              <div class="ph-walk-head"><b>Обход</b><span class="ph-muted"><span class="walk-n" /> из 8</span></div>
              <div class="ph-progress"><i /></div>
              <div class="ph-dots">
                <i v-for="(dot, i) in WALK" :key="i" :class="dot" :style="{ '--i': i }" />
              </div>
            </div>
            <b class="ph-label">Фото</b>
            <div class="ph-photos">
              <span v-for="(photo, i) in PHOTOS" :key="i" class="ph-photo" :class="{ unsent: photo.unsent }">
                <svg viewBox="0 0 60 44">
                  <rect width="60" height="44" :fill="photo.bg" />
                  <rect x="6" y="20" width="48" height="8" rx="4" fill="#8b7d63" />
                  <circle v-if="photo.leak" cx="40" cy="24" r="5" fill="#c0392b" opacity="0.75" />
                </svg>
              </span>
            </div>
            <p class="ph-queue">Ждут отправки: 3. Уйдут сами, когда появится связь.</p>
          </div>
        </div>
      </div>

      <!-- Список нарядов (/field): бригада, «Дефект на обходе», местоположение, наряды со статусами. -->
      <div class="phone phone-front">
        <div class="phone-screen">
          <div class="ph-bar">
            <svg class="ph-icon" viewBox="0 0 24 24"><path :d="ICONS.hardHat" /></svg>
            <div class="ph-bar-title">
              <strong>Наряды бригады</strong>
              <small>Алматы · бригада 4</small>
            </div>
            <span class="chip tonal warning ph-offline"><svg viewBox="0 0 24 24"><path :d="ICONS.cloudOff" /></svg>Нет связи</span>
            <span class="ph-sync">
              <svg class="ph-icon" viewBox="0 0 24 24"><path :d="ICONS.sync" /></svg>
              <i class="ph-badge">3</i>
            </span>
          </div>
          <div class="ph-body">
            <div class="ph-select">
              <span class="ph-select-label">Бригада</span>
              Бригада 4
              <svg viewBox="0 0 24 24"><path d="M7 10l5 5 5-5z" /></svg>
            </div>
            <span class="btn tonal error block"><svg viewBox="0 0 24 24"><path :d="ICONS.alert" /></svg>Дефект на обходе</span>
            <div class="ph-card ph-switch-card">
              <div class="ph-switch-row"><i class="ph-switch" /> Передавать местоположение</div>
              <small class="ph-muted">Диспетчер увидит бригаду на карте</small>
            </div>
            <div v-for="order in ORDERS" :key="order.num" class="ph-card ph-order">
              <div class="ph-chips">
                <small class="ph-muted">{{ order.num }}</small>
                <span class="chip flat" :class="order.tone">{{ order.status }}</span>
                <span v-if="order.urgent" class="chip tonal warning">Срочный</span>
              </div>
              <strong>{{ order.title }}</strong>
              <small class="ph-muted">{{ order.place }}</small>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * Полевое приложение /field в двух экранах — как в ТГИД (Vuetify, Roboto, те же подписи и статусы).
 * По кругу: без связи действия копятся в очереди, связь появилась — очередь ушла, фото отправлены.
 * Номера и адреса — условные (демо-сеть).
 */
const ICONS = {
  back: 'M20 11V13H8L13.5 18.5L12.08 19.92L4.16 12L12.08 4.08L13.5 5.5L8 11H20Z',
  hardHat: 'M12 15C7.58 15 4 16.79 4 19V21H20V19C20 16.79 16.42 15 12 15M8 9A4 4 0 0 0 12 13A4 4 0 0 0 16 9M11.5 2C11.2 2 11 2.21 11 2.5V5.5H10V3S7.75 3.86 7.75 6.75C7.75 6.75 7 6.89 7 8H17C16.95 6.89 16.25 6.75 16.25 6.75C16.25 3.86 14 3 14 3V5.5H13V2.5C13 2.21 12.81 2 12.5 2H11.5Z',
  cloudOff: 'M7.73 10L15.73 18H6A4 4 0 0 1 2 14A4 4 0 0 1 6 10M3 5.27L5.75 8C2.56 8.15 0 10.77 0 14A6 6 0 0 0 6 20H17.73L19.73 22L21 20.73L4.27 4M19.35 10.03C18.67 6.59 15.64 4 12 4C10.5 4 9.15 4.43 8 5.17L9.45 6.63C10.21 6.23 11.08 6 12 6A5.5 5.5 0 0 1 17.5 11.5V12H19A3 3 0 0 1 22 15C22 16.13 21.36 17.11 20.44 17.62L21.89 19.07C23.16 18.16 24 16.68 24 15C24 12.36 21.95 10.22 19.35 10.03Z',
  sync: 'M12 18A6 6 0 0 1 6 12C6 11 6.25 10.03 6.7 9.2L5.24 7.74C4.46 8.97 4 10.43 4 12A8 8 0 0 0 12 20V23L16 19L12 15M12 4V1L8 5L12 9V6A6 6 0 0 1 18 12C18 13 17.75 13.97 17.3 14.8L18.76 16.26C19.54 15.03 20 13.57 20 12A8 8 0 0 0 12 4Z',
  alert: 'M12 2L1 21H23M12 6L19.53 19H4.47M11 10V14H13V10M11 16V18H13V16',
  navigation: 'M12 2L4.5 20.29L5.21 21L12 18L18.79 21L19.5 20.29L12 2Z',
  marker: 'M12 11.5A2.5 2.5 0 0 1 9.5 9A2.5 2.5 0 0 1 12 6.5A2.5 2.5 0 0 1 14.5 9A2.5 2.5 0 0 1 12 11.5M12 2A7 7 0 0 0 5 9C5 14.25 12 22 12 22S19 14.25 19 9A7 7 0 0 0 12 2Z'
}

// Статусы и их цвета — как в /field: «Назначен» indigo, «В работе» orange-darken-2, «Выполнен» teal.
const ORDERS = [
  { num: 'Н-2026-00031', status: 'В работе', tone: 'progress', urgent: true, title: 'Устранить течь в камере 2КД-11', place: 'участок 1494 · фр. 2 · на месте с 08:40' },
  { num: 'Н-2026-00028', status: 'Назначен', tone: 'assigned', urgent: false, title: 'Осмотреть камеру после замены задвижки', place: 'участок 133 · фр. 1 · до 10.11' },
  { num: 'Н-2026-00024', status: 'Выполнен', tone: 'done', urgent: false, title: 'Опрессовка после ремонта', place: 'участок 1488 · фр. 2' }
]

// Точки обхода: зелёная — в норме, красная — замечание, серая — ещё не пройдена; четвёртая отмечается на глазах.
const WALK = ['ok', 'ok', 'bad', 'next', 'todo', 'todo', 'todo', 'todo']

const PHOTOS = [
  { bg: '#5b5446', leak: true, unsent: false },
  { bg: '#4f4a3e', leak: false, unsent: true },
  { bg: '#655d4c', leak: true, unsent: true }
]
</script>

<style scoped>
/* Телефоны масштабируются по ширине колонки, а не окна. */
.phones-box {
  container-type: inline-size;
}

.phones {
  --cycle: 10s;
  position: relative;
  height: 540px;
  max-width: 540px;
  margin-inline: auto;
}

.phone {
  position: absolute;
  width: 260px;
  height: 520px;
  padding: 9px;
  border-radius: 36px;
  background: var(--ink);
  box-shadow: 0 40px 60px -40px rgba(28, 27, 24, 0.6), inset 0 0 0 1px rgba(255, 255, 255, 0.08);
}

.phone-back {
  top: 0;
  right: 0;
  transform: rotate(4deg);
}

.phone-front {
  bottom: 0;
  left: 0;
  transform: rotate(-3deg);
}

.phone-screen {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
  border-radius: 28px;
  color: var(--app-text);
  background: var(--app-bg);
  font-family: var(--app-font);
  font-size: 11px;
  line-height: 1.35;
}

.ph-bar {
  display: flex;
  flex: none;
  align-items: center;
  gap: 6px;
  height: 52px;
  padding: 10px 12px 0;
  background: #fff;
  box-shadow: 0 1px 0 rgba(0, 0, 0, 0.1);
}

.ph-bar-title {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-width: 0;
}

.ph-bar-title strong {
  overflow: hidden;
  font-size: 11.5px;
  font-weight: 500;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ph-bar-title small {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.ph-offline {
  padding: 0 4px;
  font-size: 8px;
}

.ph-bar-title small,
.ph-muted {
  color: var(--app-muted);
  font-size: 10px;
}

svg {
  fill: currentColor;
}

.ph-icon {
  flex: none;
  width: 18px;
  height: 18px;
}

.ph-sync {
  position: relative;
  display: inline-flex;
}

.ph-badge {
  position: absolute;
  top: -5px;
  right: -6px;
  display: grid;
  place-items: center;
  min-width: 13px;
  height: 13px;
  padding: 0 3px;
  border-radius: 7px;
  color: #fff;
  background: var(--app-error);
  font-size: 8px;
  font-style: normal;
  font-weight: 500;
}

.ph-body {
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 7px;
  min-height: 0;
  padding: 10px 10px 0;
}

/* --- элементы Vuetify в миниатюре --- */
.chip {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  height: 16px;
  padding: 0 6px;
  border-radius: 8px;
  font-size: 8.5px;
  font-weight: 500;
  white-space: nowrap;
}

.chip svg {
  width: 10px;
  height: 10px;
}

.chip.flat {
  color: #fff;
}

.chip.progress { background: #f57c00; }
.chip.assigned { background: #3f51b5; }
.chip.done { background: #00796b; }

.chip.tonal.warning {
  color: #b45309;
  background: rgba(251, 140, 0, 0.14);
}

.ph-chips {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 5px;
}

.ph-title {
  font-size: 12.5px;
  font-weight: 500;
  line-height: 1.3;
}

.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  height: 26px;
  padding: 0 10px;
  border-radius: 6px;
  font-size: 10.5px;
  font-weight: 500;
}

.btn svg {
  width: 13px;
  height: 13px;
}

.btn.tonal {
  background: rgba(0, 0, 0, 0.08);
}

.btn.tonal.error {
  color: var(--app-error);
  background: rgba(176, 0, 32, 0.12);
}

.btn.block {
  width: 100%;
}

.ph-card {
  display: flex;
  flex-direction: column;
  gap: 3px;
  padding: 8px 9px;
  border: 1px solid rgba(0, 0, 0, 0.12);
  border-radius: 12px;
  background: #fff;
}

.ph-order strong {
  font-size: 11px;
  font-weight: 500;
}

.ph-select {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 34px;
  padding: 0 8px 0 10px;
  border: 1px solid rgba(0, 0, 0, 0.38);
  border-radius: 4px;
  font-size: 11.5px;
}

.ph-select svg {
  width: 16px;
  height: 16px;
  color: var(--app-muted);
}

.ph-select-label {
  position: absolute;
  top: -7px;
  left: 8px;
  padding: 0 3px;
  color: var(--app-muted);
  background: var(--app-bg);
  font-size: 8.5px;
}

.ph-switch-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11.5px;
}

.ph-switch {
  position: relative;
  flex: none;
  width: 28px;
  height: 16px;
  border-radius: 8px;
  background: var(--app-primary);
}

.ph-switch::after {
  content: "";
  position: absolute;
  top: 2px;
  right: 2px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: #fff;
}

.ph-map {
  position: relative;
  flex: none;
  overflow: hidden;
  border-radius: 12px;
}

.ph-map svg {
  display: block;
  width: 100%;
  height: auto;
}

.ph-map-tag {
  position: absolute;
  top: 5px;
  left: 5px;
  padding: 1px 5px;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.92);
  font-size: 7.5px;
}

.ph-actions {
  display: flex;
  gap: 4px;
}

.btn.text {
  padding: 0 6px;
}

.ph-walk {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 7px 9px;
  border: 1px solid rgba(0, 0, 0, 0.12);
  border-radius: 12px;
  background: #fff;
}

.ph-walk-head {
  display: flex;
  justify-content: space-between;
}

.ph-walk-head b,
.ph-label {
  font-size: 11px;
  font-weight: 500;
}

.walk-n::before {
  content: "4";
}

.ph-progress {
  height: 4px;
  overflow: hidden;
  border-radius: 2px;
  background: rgba(21, 101, 192, 0.18);
}

.ph-progress i {
  display: block;
  width: 50%;
  height: 100%;
  background: var(--app-primary);
}

.ph-dots {
  display: flex;
  gap: 5px;
}

.ph-dots i {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: #78909c;
}

.ph-dots .ok,
.ph-dots .next { background: #2e7d32; }
.ph-dots .bad { background: #c62828; }
.ph-dots .todo { opacity: 0.45; }

.ph-photos {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 5px;
}

.ph-photo {
  overflow: hidden;
  border-radius: 6px;
  outline: 1.5px solid transparent;
  outline-offset: 1px;
}

.ph-photo svg {
  display: block;
  width: 100%;
  height: auto;
}

/* Неотправленное фото — пунктир цвета warning, как в /field. */
.ph-photo.unsent {
  outline: 1.5px dashed #fb8c00;
}

.ph-queue {
  margin: 0;
  padding: 6px 8px;
  border-radius: 6px;
  color: #8a4b00;
  background: rgba(251, 140, 0, 0.12);
  font-size: 9.5px;
}

/*
 * Оживление (только когда движение разрешено): телефоны плавают, трек бежит, точка обхода
 * отмечается, а через 60 % круга появляется связь — «Нет связи» и счётчик гаснут, фото уходят.
 */
@media (prefers-reduced-motion: no-preference) {
  .phone-back {
    animation: phone-float 7s ease-in-out infinite;
  }

  .phone-front {
    animation: phone-float-2 8s ease-in-out infinite;
  }

  .ph-track {
    animation: track-march 1.6s linear infinite;
  }

  .ph-pin {
    transform-box: fill-box;
    transform-origin: center;
    animation: pin-pulse 2s ease-in-out infinite;
  }

  .walk-n::before {
    animation: walk-count var(--cycle) steps(1) infinite;
  }

  .ph-progress i {
    animation: walk-progress var(--cycle) cubic-bezier(0.4, 0, 0.2, 1) infinite;
  }

  .ph-dots .next {
    animation: walk-dot var(--cycle) ease infinite;
  }

  .ph-offline,
  .ph-badge,
  .ph-queue {
    animation: go-online var(--cycle) ease infinite;
  }

  .ph-photo.unsent {
    animation: photo-sent var(--cycle) ease infinite;
  }
}

@keyframes phone-float {
  50% { transform: rotate(4deg) translateY(-10px); }
}

@keyframes phone-float-2 {
  50% { transform: rotate(-3deg) translateY(8px); }
}

@keyframes track-march {
  to { stroke-dashoffset: -16; }
}

@keyframes pin-pulse {
  50% { transform: scale(1.25); }
}

@keyframes walk-count {
  0% { content: "3"; }
  30% { content: "4"; }
}

@keyframes walk-progress {
  0%, 25% { width: 37.5%; }
  35%, 100% { width: 50%; }
}

@keyframes walk-dot {
  0%, 25% { background: #78909c; opacity: 0.45; transform: scale(1); }
  30% { background: #2e7d32; opacity: 1; transform: scale(1.5); }
  38%, 100% { background: #2e7d32; opacity: 1; transform: scale(1); }
}

@keyframes go-online {
  0%, 58% { opacity: 1; transform: none; }
  64%, 94% { opacity: 0; transform: scale(0.9); }
  100% { opacity: 1; transform: none; }
}

@keyframes photo-sent {
  0%, 58% { outline-color: #fb8c00; outline-style: dashed; }
  64%, 94% { outline-color: transparent; outline-style: solid; }
  100% { outline-color: #fb8c00; outline-style: dashed; }
}

@container (max-width: 539px) {
  .phones {
    zoom: 0.84;
  }
}

@container (max-width: 420px) {
  .phones {
    zoom: 0.7;
  }
}
</style>
