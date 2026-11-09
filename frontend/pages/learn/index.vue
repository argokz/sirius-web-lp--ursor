<template>
  <div class="page learn-home">
    <section class="learn-hero">
      <div class="container">
        <UBadge color="primary" variant="subtle" size="lg">Обучение</UBadge>
        <h1 class="display-title">Курс по веб-ТГИД</h1>
        <p class="lead">
          Теория, которая объясняет, почему система считает именно так, задания с ответами и тесты с проверкой.
          Выберите трек по своей работе — уроки идут от простого к сложному, в конце трека — итоговый тест.
          Вход не нужен: пройденное запоминает ваш браузер.
        </p>
        <div v-if="catalog" class="learn-stats">
          <span><strong>{{ catalog.tracks.length }}</strong> треков</span>
          <span><strong>{{ lessonCount }}</strong> уроков</span>
          <span><strong>{{ questionCount }}</strong> вопросов с пояснениями</span>
          <span><strong>{{ taskCount }}</strong> заданий с ответами</span>
        </div>
      </div>
    </section>

    <section class="section-tight">
      <div class="container">
        <span class="eyebrow">Треки</span>
        <h2 class="section-title">Выберите, с чего начать</h2>
        <div v-if="catalog" class="track-grid">
          <article v-for="track in catalog.tracks" :key="track.id" class="track-card card">
            <div class="track-top">
              <UIcon :name="TRACK_ICONS[track.id] || 'i-lucide-book-open'" class="track-icon" />
              <span class="track-level">{{ LEVEL_LABELS[track.level] }}</span>
            </div>
            <h3>{{ track.title }}</h3>
            <p>{{ track.summary }}</p>
            <div class="track-facts">
              <span>{{ trackLessons(track).length }} уроков</span>
              <span>≈ {{ hours(track.minutes) }}</span>
              <span>тест {{ track.exam.questions }} вопросов</span>
            </div>
            <div class="track-progress" :aria-label="`Пройдено ${doneCount(track)} из ${trackLessons(track).length}`">
              <div class="track-bar"><span :style="{ width: `${percentDone(track)}%` }" /></div>
              <small>
                <template v-if="examPassed(track)">Итоговый тест сдан</template>
                <template v-else>Пройдено {{ doneCount(track) }} из {{ trackLessons(track).length }}</template>
              </small>
            </div>
            <div class="track-actions">
              <NuxtLink :to="continueUrl(track)" class="btn-primary">
                {{ doneCount(track) ? 'Продолжить' : 'Начать' }}
              </NuxtLink>
              <NuxtLink :to="`/learn/${track.id}`" class="btn-link">Все уроки</NuxtLink>
            </div>
          </article>
        </div>
      </div>
    </section>

    <section class="section-tight learn-how">
      <div class="container how-grid">
        <div>
          <span class="eyebrow">Как устроен курс</span>
          <h2 class="section-title">Урок — это «почему», справка — «как»</h2>
        </div>
        <ul>
          <li><strong>Теория.</strong> Что считает система и откуда берутся числа — формулы сверены с кодом движка.</li>
          <li><strong>Как сделать в ТГИД.</strong> Порядок действий в окнах — ссылками на <NuxtLink to="/docs">справку</NuxtLink> со снимками и роликами.</li>
          <li><strong>Задания.</strong> Задачи с числами из учебной копии сети; ответ спрятан под «Ответ».</li>
          <li><strong>Тест урока и итоговый тест трека.</strong> Проверка сразу, к каждому вопросу — пояснение.</li>
        </ul>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import type { CourseTrack } from '~~/types/course'

const TRACK_ICONS: Record<string, string> = {
  novice: 'i-lucide-sprout',
  regime: 'i-lucide-gauge',
  editor: 'i-lucide-pen-tool',
  operations: 'i-lucide-hard-hat',
  admin: 'i-lucide-server-cog',
  dev: 'i-lucide-code-xml'
}
const LEVEL_LABELS: Record<string, string> = { user: 'Пользователю', admin: 'Администратору', dev: 'Разработчику' }

const { data: catalog } = await useCourseCatalog()
const { progress, lessonDone } = useCourseProgress()

const lessons = computed(() => Object.values(catalog.value?.lessons || {}))
const lessonCount = computed(() => lessons.value.filter((lesson) => lesson.kind === 'lesson').length)
const questionCount = computed(() => lessons.value.reduce((sum, lesson) => sum + lesson.questionIds.length, 0))
const taskCount = computed(() => lessons.value.reduce((sum, lesson) => sum + lesson.tasks, 0))

const trackLessons = (track: CourseTrack) => [...track.lessons, ...(track.practice ? [track.practice] : [])]
const isDone = (id: string) => lessonDone(id, catalog.value?.lessons[id]?.questionIds || [])
const doneCount = (track: CourseTrack) => trackLessons(track).filter(isDone).length
const percentDone = (track: CourseTrack) => Math.round((doneCount(track) / Math.max(1, trackLessons(track).length)) * 100)
const examPassed = (track: CourseTrack) => Boolean(progress.value.exams[track.id]?.passed)
const continueUrl = (track: CourseTrack) => {
  const next = trackLessons(track).find((id) => !isDone(id))
  return next ? `/learn/${track.id}/${next}` : `/learn/${track.id}/exam`
}
const hours = (minutes: number) => (minutes < 90 ? `${minutes} мин` : `${Math.round(minutes / 6) / 10} ч`.replace('.', ','))

useSeoMeta({
  title: 'Курс по веб-ТГИД — обучение',
  description: 'Бесплатный курс по веб-ТГИД: треки для режимщика, редактора сети, эксплуатации, администратора и разработчика — уроки, задания и тесты.'
})
</script>

<style scoped>
.learn-hero {
  padding: 136px 0 56px;
  border-bottom: 1px solid var(--line);
}

.learn-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 28px;
  margin-top: 28px;
  color: var(--muted);
  font-size: 0.95rem;
}

.learn-stats strong {
  font-family: var(--font-mono);
  color: var(--ink);
  margin-right: 4px;
}

.track-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 18px;
  margin-top: 28px;
}

.track-card {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 24px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.track-card:hover {
  transform: translateY(-2px);
}

.track-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.track-icon {
  width: 28px;
  height: 28px;
  color: var(--sirius-red);
}

.track-level {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--muted);
}

.track-card h3 {
  margin: 0;
  font-family: var(--font-serif);
  font-size: 1.45rem;
  font-weight: 600;
  color: var(--ink);
}

.track-card p {
  margin: 0;
  color: var(--ink-2);
  line-height: 1.55;
  flex: 1;
}

.track-facts {
  display: flex;
  flex-wrap: wrap;
  gap: 6px 14px;
  font-size: 0.85rem;
  color: var(--muted);
}

.track-progress small {
  display: block;
  margin-top: 6px;
  font-size: 0.8rem;
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
  border-radius: inherit;
  transition: width 0.5s ease;
}

.track-actions {
  display: flex;
  align-items: center;
  gap: 18px;
  margin-top: 4px;
}

.learn-how {
  border-top: 1px solid var(--line);
}

.how-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1.4fr);
  gap: 32px;
}

.how-grid ul {
  margin: 0;
  padding: 0;
  list-style: none;
  display: grid;
  gap: 14px;
  color: var(--ink-2);
  line-height: 1.6;
}

.how-grid strong {
  color: var(--ink);
}

.how-grid a {
  text-decoration: underline;
  text-underline-offset: 3px;
}

@media (max-width: 860px) {
  .how-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .learn-hero {
    padding: 112px 0 40px;
  }

  .track-grid {
    grid-template-columns: 1fr;
  }
}
</style>
