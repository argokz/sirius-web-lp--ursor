<template>
  <section class="quiz-block" aria-labelledby="quiz-title">
    <header class="quiz-head">
      <h2 id="quiz-title">Проверьте себя</h2>
      <span class="quiz-score" aria-live="polite">Решено {{ solvedCount }} из {{ questions.length }}</span>
    </header>

    <QuizQuestion
      v-for="(question, i) in questions"
      :key="question.id"
      v-model:selected="state[question.id].selected"
      :question="question"
      :index="i"
      :revealed="state[question.id].revealed"
    >
      <div class="quiz-actions">
        <UButton
          v-if="!state[question.id].revealed"
          size="sm"
          :disabled="state[question.id].selected === null"
          @click="check(question)"
        >
          Проверить
        </UButton>
        <UButton
          v-else-if="state[question.id].selected !== question.answer"
          size="sm"
          color="neutral"
          variant="outline"
          @click="retry(question)"
        >
          Ещё раз
        </UButton>
      </div>
    </QuizQuestion>
  </section>
</template>

<script setup lang="ts">
import type { CourseQuestion } from '~~/types/course'

const props = defineProps<{ questions: CourseQuestion[] }>()

const { progress, recordAnswer } = useCourseProgress()

const state = reactive<Record<string, { selected: number | null; revealed: boolean }>>({})
watch(() => props.questions, (questions) => {
  for (const question of questions) state[question.id] ??= { selected: null, revealed: false }
}, { immediate: true })

const solvedCount = computed(() => props.questions.filter((question) => progress.value.questions[question.id]?.solved).length)

const check = (question: CourseQuestion) => {
  const answer = state[question.id]
  if (!answer || answer.selected === null) return
  answer.revealed = true
  recordAnswer(question.id, answer.selected === question.answer)
}

const retry = (question: CourseQuestion) => {
  state[question.id] = { selected: null, revealed: false }
}
</script>

<style scoped>
.quiz-block {
  margin-top: 48px;
}

.quiz-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 18px;
}

.quiz-head h2 {
  margin: 0;
  font-family: var(--font-serif);
  font-size: 1.6rem;
  font-weight: 600;
  color: var(--ink);
}

.quiz-score {
  font-family: var(--font-mono);
  font-size: 0.85rem;
  color: var(--muted);
}

.quiz-actions {
  display: flex;
  gap: 8px;
  margin-top: 12px;
}

.quiz-actions:empty {
  display: none;
}
</style>
