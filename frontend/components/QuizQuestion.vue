<template>
  <fieldset class="quiz-question" :class="{ revealed, correct: revealed && isCorrect, wrong: revealed && !isCorrect }">
    <legend>
      <span class="quiz-num">{{ index + 1 }}</span>
      <!-- HTML вопроса собирает scripts/sync-course.mjs из курса в репозитории -->
      <span v-html="question.q" />
    </legend>

    <div class="quiz-options" role="radiogroup">
      <label
        v-for="(option, i) in question.options"
        :key="i"
        class="quiz-option"
        :class="{
          chosen: selected === i,
          right: revealed && i === question.answer,
          miss: revealed && selected === i && i !== question.answer
        }"
      >
        <input
          type="radio"
          :name="`q-${question.id}`"
          :value="i"
          :checked="selected === i"
          :disabled="revealed"
          @change="emit('update:selected', i)"
        >
        <span class="quiz-letter">{{ LETTERS[i] }}</span>
        <span class="quiz-option-text" v-html="option" />
        <UIcon v-if="revealed && i === question.answer" name="i-lucide-check" class="quiz-mark" />
        <UIcon v-else-if="revealed && selected === i" name="i-lucide-x" class="quiz-mark" />
      </label>
    </div>

    <div v-if="revealed" class="quiz-explain" role="status">
      <strong>{{ isCorrect ? 'Верно.' : 'Неверно.' }}</strong>
      <span v-html="question.explain" />
    </div>
    <slot />
  </fieldset>
</template>

<script setup lang="ts">
import type { CourseQuestion } from '~~/types/course'

const LETTERS = ['А', 'Б', 'В', 'Г', 'Д', 'Е']

const props = defineProps<{
  question: CourseQuestion
  index: number
  selected: number | null
  revealed: boolean
}>()
const emit = defineEmits<{ 'update:selected': [value: number] }>()

const isCorrect = computed(() => props.selected === props.question.answer)
</script>

<style scoped>
.quiz-question {
  margin: 0 0 18px;
  padding: 18px 20px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--surface);
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.quiz-question.correct {
  border-color: #15803d;
}

.quiz-question.wrong {
  border-color: var(--sirius-red);
}

legend {
  display: flex;
  gap: 10px;
  padding: 0;
  font-weight: 650;
  line-height: 1.45;
  color: var(--ink);
}

.quiz-num {
  flex: none;
  min-width: 1.6em;
  font-family: var(--font-mono);
  color: var(--muted);
}

.quiz-options {
  display: grid;
  gap: 8px;
  margin-top: 14px;
}

.quiz-option {
  position: relative;
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 10px 12px;
  border: 1px solid var(--line);
  border-radius: var(--radius-sm);
  cursor: pointer;
  line-height: 1.45;
  transition: border-color 0.15s ease, background 0.15s ease;
}

.quiz-option:hover {
  border-color: var(--line-strong);
}

.quiz-option input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}

.quiz-option:has(input:focus-visible) {
  outline: 2px solid var(--ink);
  outline-offset: 2px;
}

.quiz-option.chosen {
  border-color: var(--ink);
  background: var(--panel-soft);
}

.quiz-option.right {
  border-color: #15803d;
  background: #f0fdf4;
}

.quiz-option.miss {
  border-color: var(--sirius-red);
  background: var(--sirius-red-soft);
}

.revealed .quiz-option {
  cursor: default;
}

.quiz-letter {
  flex: none;
  font-family: var(--font-mono);
  font-size: 0.85rem;
  color: var(--muted);
  padding-top: 1px;
}

.quiz-option-text {
  flex: 1;
}

.quiz-mark {
  flex: none;
  margin-top: 3px;
}

.quiz-option.right .quiz-mark {
  color: #15803d;
}

.quiz-option.miss .quiz-mark {
  color: var(--sirius-red);
}

.quiz-explain {
  margin-top: 12px;
  color: var(--ink-2);
  line-height: 1.55;
}

.quiz-explain strong {
  margin-right: 6px;
}

.quiz-explain :deep(a),
legend :deep(a),
.quiz-option-text :deep(a) {
  color: var(--ink);
  text-decoration: underline;
  text-underline-offset: 3px;
}

.quiz-explain :deep(code),
legend :deep(code),
.quiz-option-text :deep(code) {
  font-family: var(--font-mono);
  font-size: 0.9em;
}
</style>
