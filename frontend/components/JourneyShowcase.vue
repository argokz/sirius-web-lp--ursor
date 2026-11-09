<template>
  <section v-if="data?.featured" class="section journeys">
    <div class="container">
      <div class="journeys-head">
        <div>
          <span class="eyebrow">Посмотрите в работе</span>
          <h2 class="section-title">{{ heading }}</h2>
          <p class="lead">
            Сквозные сценарии одним роликом: от сообщения о нарушении до наряда, от правки сети до расчёта и отчёта.
            С субтитрами — можно смотреть без звука.
          </p>
        </div>
        <UButton to="/learn" color="neutral" variant="outline" size="lg" icon="i-lucide-graduation-cap">
          Пройти обучение
        </UButton>
      </div>

      <div class="journeys-grid">
        <figure class="journey-player">
          <video
            controls
            muted
            playsinline
            preload="metadata"
            :src="data.featured.video.src"
            :aria-label="`Ролик: ${data.featured.title}`"
          >
            <track v-if="data.featured.video.track" kind="subtitles" srclang="ru" label="Русский" :src="data.featured.video.track" default>
          </video>
          <figcaption>
            <strong>{{ data.featured.title }}</strong>
            <NuxtLink :to="data.featured.url">Пошагово со снимками</NuxtLink>
          </figcaption>
        </figure>

        <ol class="journey-list">
          <li v-for="item in others" :key="item.key">
            <NuxtLink :to="item.url">
              <UIcon name="i-lucide-play-circle" class="journey-play" />
              <span>
                <strong>{{ item.title }}</strong>
                <small>{{ item.summary }}</small>
              </span>
            </NuxtLink>
          </li>
        </ol>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import type { ManualJourneys } from '~~/types/manual'

withDefaults(defineProps<{ heading?: string }>(), {
  heading: 'Как ТГИД работает на реальной задаче'
})

const { data } = await useFetch<ManualJourneys>('/docs-data/journeys', { key: 'docs-journeys' })
const others = computed(() => (data.value?.items || []).filter((item) => item.key !== data.value?.featured?.key))
</script>

<style scoped>
.journeys {
  border-top: 1px solid var(--line);
}

.journeys-head {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
  margin-bottom: 32px;
}

.journeys-head .lead {
  max-width: 720px;
}

.journeys-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.5fr) minmax(0, 1fr);
  gap: 28px;
  align-items: start;
}

.journey-player {
  margin: 0;
}

.journey-player video {
  display: block;
  width: 100%;
  aspect-ratio: 16 / 10;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--dark);
}

.journey-player figcaption {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  gap: 8px 16px;
  margin-top: 12px;
  font-size: 0.95rem;
}

.journey-player figcaption a {
  color: var(--ink);
  text-decoration: underline;
  text-underline-offset: 3px;
}

.journey-list {
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 4px;
}

.journey-list a {
  display: flex;
  gap: 12px;
  padding: 12px 14px;
  border-radius: var(--radius-sm);
  transition: background 0.15s ease;
}

.journey-list a:hover {
  background: var(--panel-soft);
}

.journey-play {
  flex: none;
  width: 20px;
  height: 20px;
  margin-top: 2px;
  color: var(--sirius-red);
}

.journey-list span {
  display: grid;
  gap: 2px;
}

.journey-list strong {
  color: var(--ink);
  font-size: 0.98rem;
}

.journey-list small {
  color: var(--muted);
  font-size: 0.85rem;
  line-height: 1.45;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

@media (max-width: 960px) {
  .journeys-grid {
    grid-template-columns: 1fr;
  }

  .journeys-head {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
