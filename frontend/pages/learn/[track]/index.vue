<template>
  <div v-if="track && catalog" class="page learn-track">
    <section class="track-hero">
      <div class="container">
        <nav class="crumbs" aria-label="Навигация">
          <NuxtLink to="/learn">Обучение</NuxtLink>
          <span aria-hidden="true">/</span>
          <span>{{ track.title }}</span>
        </nav>
        <h1 class="display-title">{{ track.title }}</h1>
        <p class="lead">{{ track.summary }}</p>
        <div class="track-progress">
          <div class="track-bar"><span :style="{ width: `${percentDone}%` }" /></div>
          <small>Пройдено {{ doneCount }} из {{ order.length }} · ≈ {{ track.minutes }} мин</small>
        </div>
      </div>
    </section>

    <section class="section-tight">
      <div class="container track-layout">
        <ol class="lesson-list">
          <li v-for="(id, i) in order" :key="id">
            <NuxtLink :to="`/learn/${track.id}/${id}`" class="lesson-row card" :class="{ done: isDone(id) }">
              <span class="lesson-num">
                <UIcon v-if="isDone(id)" name="i-lucide-check" />
                <template v-else>{{ i + 1 }}</template>
              </span>
              <span class="lesson-text">
                <span class="lesson-kind">{{ lessonOf(id).kind === 'practice' ? 'Практика' : 'Урок' }} · {{ lessonOf(id).minutes }} мин</span>
                <strong>{{ lessonOf(id).title }}</strong>
                <span class="lesson-summary">{{ lessonOf(id).summary }}</span>
              </span>
              <span class="lesson-quiz">
                <template v-if="lessonOf(id).questionIds.length">{{ solvedIn(id) }}/{{ lessonOf(id).questionIds.length }} вопросов</template>
                <template v-else>{{ lessonOf(id).tasks }} заданий</template>
              </span>
            </NuxtLink>
          </li>
        </ol>

        <aside class="exam-card card">
          <span class="eyebrow">Итоговый тест</span>
          <h2>{{ track.exam.questions }} вопросов из {{ track.questions }}</h2>
          <p>
            Случайные вопросы из уроков трека. Зачёт — от {{ track.exam.passPercent }} % верных ответов.
            Пересдавать можно сколько угодно.
          </p>
          <p v-if="exam" class="exam-result" :class="{ passed: exam.passed }">
            {{ exam.passed ? 'Сдан' : 'Пока не сдан' }} · лучший результат {{ exam.best }} %
          </p>
          <NuxtLink :to="`/learn/${track.id}/exam`" class="btn-primary">{{ exam ? 'Пройти ещё раз' : 'Пройти тест' }}</NuxtLink>
        </aside>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const trackId = computed(() => String(route.params.track))

const { data: catalog } = await useCourseCatalog()
const track = computed(() => catalog.value?.tracks.find((item) => item.id === trackId.value))
if (!track.value) {
  throw createError({ statusCode: 404, statusMessage: 'Трек курса не найден', fatal: true })
}

const { progress, lessonDone } = useCourseProgress()

const order = computed(() => (track.value ? [...track.value.lessons, ...(track.value.practice ? [track.value.practice] : [])] : []))
const lessonOf = (id: string) => catalog.value!.lessons[id]!
const isDone = (id: string) => lessonDone(id, lessonOf(id).questionIds)
const solvedIn = (id: string) => lessonOf(id).questionIds.filter((qid) => progress.value.questions[qid]?.solved).length
const doneCount = computed(() => order.value.filter(isDone).length)
const percentDone = computed(() => Math.round((doneCount.value / Math.max(1, order.value.length)) * 100))
const exam = computed(() => progress.value.exams[trackId.value])

useSeoMeta({
  title: () => `${track.value?.title} — курс по веб-ТГИД`,
  description: () => track.value?.summary
})
</script>

<style scoped>
.track-hero {
  padding: 136px 0 48px;
  border-bottom: 1px solid var(--line);
}

.crumbs {
  display: flex;
  gap: 8px;
  margin-bottom: 18px;
  font-size: 0.9rem;
  color: var(--muted);
}

.crumbs a:hover {
  color: var(--ink);
}

.track-progress {
  max-width: 520px;
  margin-top: 28px;
}

.track-progress small {
  display: block;
  margin-top: 8px;
  font-size: 0.85rem;
  color: var(--muted);
}

.track-bar {
  height: 6px;
  border-radius: 999px;
  background: var(--panel-soft);
  overflow: hidden;
}

.track-bar span {
  display: block;
  height: 100%;
  background: var(--ink);
  transition: width 0.5s ease;
}

.track-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 320px;
  gap: 28px;
  align-items: start;
}

.lesson-list {
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 10px;
}

.lesson-row {
  display: grid;
  grid-template-columns: 40px minmax(0, 1fr) auto;
  gap: 16px;
  align-items: start;
  padding: 18px 20px;
  transition: transform 0.15s ease, border-color 0.15s ease;
}

.lesson-row:hover {
  transform: translateX(2px);
  border-color: var(--line-strong);
}

.lesson-num {
  display: grid;
  place-items: center;
  width: 32px;
  height: 32px;
  border: 1px solid var(--line-strong);
  border-radius: 50%;
  font-family: var(--font-mono);
  font-size: 0.85rem;
  color: var(--ink-2);
}

.lesson-row.done .lesson-num {
  border-color: var(--ink);
  background: var(--ink);
  color: var(--paper);
}

.lesson-text {
  display: grid;
  gap: 4px;
}

.lesson-kind {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--muted);
}

.lesson-text strong {
  font-size: 1.05rem;
  color: var(--ink);
}

.lesson-summary {
  color: var(--ink-2);
  font-size: 0.92rem;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.lesson-quiz {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  color: var(--muted);
  white-space: nowrap;
}

.exam-card {
  position: sticky;
  top: 96px;
  display: grid;
  gap: 12px;
  padding: 24px;
}

.exam-card h2 {
  margin: 0;
  font-family: var(--font-serif);
  font-size: 1.35rem;
  font-weight: 600;
  color: var(--ink);
}

.exam-card p {
  margin: 0;
  color: var(--ink-2);
  line-height: 1.55;
}

.exam-result {
  font-weight: 650;
}

.exam-result.passed {
  color: #15803d;
}

@media (max-width: 960px) {
  .track-layout {
    grid-template-columns: 1fr;
  }

  .exam-card {
    position: static;
  }
}

@media (max-width: 640px) {
  .track-hero {
    padding: 112px 0 36px;
  }

  .lesson-row {
    grid-template-columns: 36px minmax(0, 1fr);
  }

  .lesson-quiz {
    grid-column: 2;
  }
}
</style>
