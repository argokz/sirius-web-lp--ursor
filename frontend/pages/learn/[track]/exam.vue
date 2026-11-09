<template>
  <div v-if="data" class="page learn-exam">
    <div class="container exam">
      <nav class="crumbs" aria-label="Навигация">
        <NuxtLink to="/learn">Обучение</NuxtLink>
        <span aria-hidden="true">/</span>
        <NuxtLink :to="`/learn/${data.track.id}`">{{ data.track.title }}</NuxtLink>
      </nav>
      <span class="exam-kind">Итоговый тест трека</span>
      <h1>{{ data.track.title }}</h1>
      <p class="exam-lead">
        {{ rule.questions }} случайных вопросов из {{ data.pool.length }}. Зачёт — от {{ rule.passPercent }} %.
        Ответьте на все вопросы и нажмите «Проверить»; к каждому вопросу будет пояснение и ссылка на урок.
      </p>

      <div v-if="result" class="exam-result card" :class="{ passed: result.passed }" role="status">
        <strong>{{ result.passed ? 'Тест сдан' : 'Тест не сдан' }}: {{ result.correct }} из {{ questions.length }} ({{ result.percent }} %)</strong>
        <span v-if="!result.passed">Повторите уроки по вопросам с ошибками — ссылки под каждым вопросом.</span>
        <div class="exam-actions">
          <UButton @click="start">Новый вариант</UButton>
          <NuxtLink :to="`/learn/${data.track.id}`" class="btn-link">К урокам трека</NuxtLink>
        </div>
      </div>

      <!-- Вопросы выбираются в браузере: на сервере список пуст, чтобы не было расхождения гидратации -->
      <p v-if="!questions.length" class="exam-loading">Готовим вопросы…</p>
      <form v-else @submit.prevent="submit">
        <QuizQuestion
          v-for="(question, i) in questions"
          :key="question.id"
          v-model:selected="answers[question.id]"
          :question="question"
          :index="i"
          :revealed="Boolean(result)"
        >
          <NuxtLink v-if="result" :to="`/learn/${data.track.id}/${question.lessonId}`" class="exam-lesson">
            Урок: {{ question.lessonTitle }}
          </NuxtLink>
        </QuizQuestion>

        <div v-if="!result" class="exam-submit">
          <span>Отвечено {{ answeredCount }} из {{ questions.length }}</span>
          <UButton type="submit" size="lg" :disabled="answeredCount < questions.length">Проверить</UButton>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { CourseExamQuestion } from '~~/types/course'

const route = useRoute()
const trackId = computed(() => String(route.params.track))

const { data, error } = await useCourseExam(trackId)
if (error.value || !data.value) {
  throw createError({ statusCode: 404, statusMessage: 'Трек курса не найден', fatal: true })
}

const { recordExam } = useCourseProgress()

const rule = computed(() => data.value!.track.exam)
const questions = ref<CourseExamQuestion[]>([])
const answers = reactive<Record<string, number | null>>({})
const result = ref<{ correct: number; percent: number; passed: boolean } | null>(null)

/** Случайная выборка без повторов (Фишер — Йейтс по копии банка) */
const pick = (pool: CourseExamQuestion[], count: number) => {
  const copy = [...pool]
  for (let i = copy.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[copy[i], copy[j]] = [copy[j]!, copy[i]!]
  }
  return copy.slice(0, Math.min(count, copy.length))
}

const start = () => {
  if (!data.value) return
  result.value = null
  questions.value = pick(data.value.pool, rule.value.questions)
  for (const key of Object.keys(answers)) delete answers[key]
  for (const question of questions.value) answers[question.id] = null
  if (import.meta.client) window.scrollTo({ top: 0, behavior: 'smooth' })
}
onMounted(start)

const answeredCount = computed(() => questions.value.filter((question) => answers[question.id] !== null && answers[question.id] !== undefined).length)

const submit = () => {
  if (answeredCount.value < questions.value.length) return
  const correct = questions.value.filter((question) => answers[question.id] === question.answer).length
  const percent = Math.round((correct / questions.value.length) * 100)
  result.value = { correct, percent, passed: percent >= rule.value.passPercent }
  recordExam(trackId.value, percent, rule.value.passPercent)
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

useSeoMeta({
  title: () => `Итоговый тест: ${data.value?.track.title} — курс по веб-ТГИД`,
  description: () => data.value?.track.summary,
  robots: 'noindex'
})
</script>

<style scoped>
.learn-exam {
  padding: 120px 0 72px;
}

.exam {
  max-width: 820px;
}

.crumbs {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 22px;
  font-size: 0.9rem;
  color: var(--muted);
}

.crumbs a:hover {
  color: var(--ink);
}

.exam-kind {
  font-family: var(--font-mono);
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--muted);
}

.exam h1 {
  margin: 10px 0 0;
  font-family: var(--font-serif);
  font-size: clamp(2rem, 4vw, 2.8rem);
  font-weight: 600;
  color: var(--ink);
}

.exam-lead {
  margin: 16px 0 32px;
  font-size: 1.08rem;
  line-height: 1.6;
  color: var(--ink-2);
}

.exam-result {
  display: grid;
  gap: 8px;
  margin-bottom: 28px;
  padding: 20px 22px;
  border-color: var(--sirius-red);
}

.exam-result.passed {
  border-color: #15803d;
}

.exam-result strong {
  font-size: 1.15rem;
  color: var(--ink);
}

.exam-result span {
  color: var(--ink-2);
}

.exam-actions {
  display: flex;
  align-items: center;
  gap: 18px;
  margin-top: 6px;
}

.exam-loading {
  color: var(--muted);
}

.exam-lesson {
  display: inline-block;
  margin-top: 10px;
  font-size: 0.9rem;
  color: var(--ink);
  text-decoration: underline;
  text-underline-offset: 3px;
}

.exam-submit {
  position: sticky;
  bottom: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 14px 18px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--surface);
  box-shadow: 0 8px 24px rgb(0 0 0 / 0.06);
}

.exam-submit span {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  color: var(--muted);
}

@media (max-width: 640px) {
  .learn-exam {
    padding-top: 96px;
  }
}
</style>
