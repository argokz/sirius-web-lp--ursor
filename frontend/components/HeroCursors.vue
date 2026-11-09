<template>
  <div class="cursors" aria-hidden="true">
    <div v-for="cursor in CURSORS" :key="cursor.name" class="cursor" :class="cursor.id">
      <svg viewBox="0 0 16 20" width="16" height="20">
        <path d="M1 1 L1 16 L5 12 L8 19 L11 17.6 L8 11 L14 11 Z" :fill="cursor.color" stroke="#fff" stroke-width="1.4" stroke-linejoin="round" />
      </svg>
      <span class="cursor-name" :style="{ background: cursor.color }">{{ cursor.name }}</span>
      <i class="cursor-ping" :style="{ borderColor: cursor.color }" />
    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * «Кто на карте» как у felt.com: курсоры коллег с подписями ходят по окну программы.
 * Подписи — роли, не люди. Появляются после того, как карта дорисовалась (ProductMapDemo ~8 с).
 * Положение задаётся в cqw/cqh — доли ширины и высоты окна, поэтому путь не зависит от размера.
 */
const CURSORS = [
  { id: 'c1', name: 'Диспетчер', color: '#e30613' },
  { id: 'c2', name: 'Режимщик', color: '#0a7af2' }
]
</script>

<style scoped>
.cursors {
  position: absolute;
  inset: 0;
  z-index: 3;
  container-type: size;
  overflow: hidden;
  border-radius: 8px;
  pointer-events: none;
}

.cursor {
  position: absolute;
  top: 0;
  left: 0;
  opacity: 0;
  filter: drop-shadow(0 2px 3px rgba(0, 0, 0, 0.25));
}

.cursor-name {
  position: absolute;
  top: 16px;
  left: 12px;
  padding: 2px 7px;
  border-radius: 4px 999px 999px 999px;
  color: #fff;
  font-family: var(--font-sans);
  font-size: 11px;
  font-weight: 500;
  white-space: nowrap;
}

.cursor-ping {
  position: absolute;
  top: -9px;
  left: -9px;
  width: 20px;
  height: 20px;
  border: 2px solid;
  border-radius: 50%;
  opacity: 0;
}

@media (prefers-reduced-motion: no-preference) {
  .c1 {
    animation: c1-path 16s cubic-bezier(0.45, 0, 0.25, 1) 8.5s infinite;
  }

  .c2 {
    animation: c2-path 19s cubic-bezier(0.45, 0, 0.25, 1) 10s infinite;
  }

  .c1 .cursor-ping {
    animation: ping 16s ease-out 8.5s infinite;
  }

  .c2 .cursor-ping {
    animation: ping-2 19s ease-out 10s infinite;
  }
}

/* Диспетчер: от панели слоёв к магистрали, «щелчок» на участке, к правым кнопкам. */
@keyframes c1-path {
  0% { opacity: 0; transform: translate(30cqw, 70cqh); }
  4% { opacity: 1; }
  22% { transform: translate(44cqw, 52cqh); }
  30% { transform: translate(44cqw, 52cqh); }
  52% { transform: translate(62cqw, 38cqh); }
  62% { transform: translate(62cqw, 38cqh); }
  84% { transform: translate(52cqw, 78cqh); opacity: 1; }
  92%, 100% { transform: translate(52cqw, 78cqh); opacity: 0; }
}

@keyframes ping {
  0%, 26% { opacity: 0; transform: scale(0.4); }
  27% { opacity: 1; transform: scale(0.4); }
  33% { opacity: 0; transform: scale(1.8); }
  100% { opacity: 0; }
}

/* Режимщик: сверху справа к расчёту, к подписи Qсум, обратно. */
@keyframes c2-path {
  0% { opacity: 0; transform: translate(86cqw, 22cqh); }
  5% { opacity: 1; }
  24% { transform: translate(72cqw, 30cqh); }
  34% { transform: translate(72cqw, 30cqh); }
  58% { transform: translate(80cqw, 60cqh); }
  70% { transform: translate(80cqw, 60cqh); }
  88% { transform: translate(90cqw, 44cqh); opacity: 1; }
  95%, 100% { transform: translate(90cqw, 44cqh); opacity: 0; }
}

@keyframes ping-2 {
  0%, 64% { opacity: 0; transform: scale(0.4); }
  65% { opacity: 1; transform: scale(0.4); }
  71% { opacity: 0; transform: scale(1.8); }
  100% { opacity: 0; }
}

@media (max-width: 640px) {
  .cursor-name {
    font-size: 10px;
  }
}
</style>
