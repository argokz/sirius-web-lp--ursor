<template>
  <div v-if="data" class="page learn-lesson">
    <div class="container lesson-layout">
      <article class="lesson">
        <nav class="crumbs" aria-label="Навигация">
          <NuxtLink to="/learn">Обучение</NuxtLink>
          <span aria-hidden="true">/</span>
          <NuxtLink :to="`/learn/${data.track.id}`">{{ data.track.title }}</NuxtLink>
        </nav>

        <span class="lesson-kind">
          {{ data.lesson.kind === 'practice' ? 'Практика' : `Урок ${position} из ${order.length}` }} · {{ data.lesson.minutes }} мин
          <UIcon v-if="done" name="i-lucide-circle-check" class="done-icon" aria-label="пройден" />
        </span>
        <h1>{{ data.lesson.title }}</h1>
        <p class="lesson-lead">{{ data.lesson.summary }}</p>

        <div v-if="data.lesson.manual.length" class="lesson-howto">
          <span>Как сделать в ТГИД:</span>
          <NuxtLink v-for="link in data.lesson.manual" :key="link.url" :to="link.url">{{ link.title }}</NuxtLink>
        </div>

        <!-- HTML урока собирает scripts/sync-course.mjs из курса в репозитории web-itwin -->
        <div class="doc-body lesson-body" v-html="data.lesson.html" />

        <QuizBlock v-if="data.lesson.quiz.length" :questions="data.lesson.quiz" />
        <div v-else class="lesson-mark card">
          <div>
            <strong>{{ done ? 'Практика отмечена пройденной' : 'Разобрали задания?' }}</strong>
            <span>Ответы — под «Ответ» у каждого задания. Отметка хранится только в вашем браузере.</span>
          </div>
          <UButton :color="done ? 'neutral' : 'primary'" :variant="done ? 'outline' : 'solid'" @click="setDone(data.lesson.id, !done)">
            {{ done ? 'Снять отметку' : 'Отметить пройденной' }}
          </UButton>
        </div>

        <section v-if="data.lesson.related.length" class="lesson-related">
          <h2>Связанные уроки</h2>
          <div class="related-links">
            <NuxtLink v-for="item in data.lesson.related" :key="item.id" :to="item.url">{{ item.title }}</NuxtLink>
          </div>
        </section>

        <nav class="lesson-pager" aria-label="Уроки трека">
          <NuxtLink v-if="data.prev" :to="`/learn/${data.track.id}/${data.prev.id}`" class="pager-link">
            <small>Назад</small>
            <strong>{{ data.prev.title }}</strong>
          </NuxtLink>
          <span v-else />
          <NuxtLink :to="data.next ? `/learn/${data.track.id}/${data.next.id}` : `/learn/${data.track.id}/exam`" class="pager-link next">
            <small>{{ data.next ? 'Далее' : 'Итоговый тест' }}</small>
            <strong>{{ data.next ? data.next.title : `${data.track.title}: ${data.track.exam.questions} вопросов` }}</strong>
          </NuxtLink>
        </nav>
      </article>

      <aside v-if="data.lesson.toc.length" class="lesson-toc" aria-label="Содержание урока">
        <span>В уроке</span>
        <a v-for="item in data.lesson.toc" :key="item.id" :href="`#${item.id}`">{{ item.text }}</a>
        <a v-if="data.lesson.quiz.length" href="#quiz-title">Проверьте себя</a>
      </aside>
    </div>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const trackId = computed(() => String(route.params.track))
const lessonId = computed(() => String(route.params.lesson))

const { data, error } = await useCourseLesson(trackId, lessonId)
if (error.value || !data.value) {
  throw createError({ statusCode: 404, statusMessage: 'Урок не найден', fatal: true })
}

const { lessonDone, setDone } = useCourseProgress()

const order = computed(() => (data.value ? [...data.value.track.lessons, ...(data.value.track.practice ? [data.value.track.practice] : [])] : []))
const position = computed(() => order.value.indexOf(lessonId.value) + 1)
const done = computed(() => (data.value ? lessonDone(data.value.lesson.id, data.value.lesson.quiz.map((question) => question.id)) : false))

useSeoMeta({
  title: () => `${data.value?.lesson.title} — курс по веб-ТГИД`,
  description: () => data.value?.lesson.summary
})
</script>

<style scoped>
.learn-lesson {
  padding: 120px 0 72px;
}

.lesson-layout {
  display: grid;
  grid-template-columns: minmax(0, 780px) 240px;
  gap: 56px;
  justify-content: center;
  align-items: start;
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

.lesson-kind {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-family: var(--font-mono);
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--muted);
}

.done-icon {
  color: #15803d;
}

.lesson h1 {
  margin: 10px 0 0;
  font-family: var(--font-serif);
  font-size: clamp(2rem, 4vw, 2.8rem);
  font-weight: 600;
  line-height: 1.12;
  color: var(--ink);
}

.lesson-lead {
  margin: 18px 0 0;
  font-size: 1.12rem;
  line-height: 1.6;
  color: var(--ink-2);
}

.lesson-howto {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 14px;
  align-items: baseline;
  margin-top: 22px;
  padding: 14px 16px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--panel-soft);
  font-size: 0.95rem;
}

.lesson-howto span {
  color: var(--muted);
}

.lesson-howto a {
  color: var(--ink);
  text-decoration: underline;
  text-underline-offset: 3px;
}

.lesson-body {
  margin-top: 28px;
}

.lesson-body :deep(blockquote) {
  margin: 20px 0;
  padding: 12px 18px;
  border-left: 3px solid var(--ink);
  background: var(--panel-soft);
  color: var(--ink-2);
}

.lesson-body :deep(blockquote p) {
  margin: 0;
}

.lesson-body :deep(details) {
  margin: 10px 0 22px;
  padding: 10px 16px;
  border: 1px dashed var(--line-strong);
  border-radius: var(--radius-sm);
}

.lesson-body :deep(details > summary) {
  cursor: pointer;
  font-weight: 650;
  color: var(--ink);
}

.lesson-body :deep(details[open] > summary) {
  margin-bottom: 8px;
}

.lesson-body :deep(pre) {
  overflow-x: auto;
  padding: 14px 16px;
  border-radius: var(--radius-sm);
  background: var(--panel-soft);
  font-size: 0.88rem;
}

.lesson-mark {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  margin-top: 44px;
  padding: 20px 22px;
}

.lesson-mark div {
  display: grid;
  gap: 4px;
}

.lesson-mark span {
  color: var(--ink-2);
  font-size: 0.92rem;
}

.lesson-related {
  margin-top: 44px;
}

.lesson-related h2 {
  margin: 0 0 12px;
  font-family: var(--font-serif);
  font-size: 1.35rem;
  font-weight: 600;
  color: var(--ink);
}

.related-links {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.related-links a {
  padding: 6px 12px;
  border: 1px solid var(--line);
  border-radius: 999px;
  font-size: 0.9rem;
  color: var(--ink-2);
  transition: border-color 0.15s ease, color 0.15s ease;
}

.related-links a:hover {
  border-color: var(--ink);
  color: var(--ink);
}

.lesson-pager {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
  margin-top: 44px;
}

.pager-link {
  display: grid;
  gap: 4px;
  padding: 16px 18px;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  transition: border-color 0.15s ease;
}

.pager-link:hover {
  border-color: var(--ink);
}

.pager-link.next {
  text-align: right;
}

.pager-link small {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  text-transform: uppercase;
  color: var(--muted);
}

.pager-link strong {
  color: var(--ink);
}

.lesson-toc {
  position: sticky;
  top: 104px;
  display: grid;
  gap: 8px;
  font-size: 0.88rem;
}

.lesson-toc span {
  font-family: var(--font-mono);
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--muted);
}

.lesson-toc a {
  color: var(--ink-2);
  line-height: 1.4;
}

.lesson-toc a:hover {
  color: var(--ink);
}

@media (max-width: 1100px) {
  .lesson-layout {
    grid-template-columns: minmax(0, 1fr);
  }

  .lesson-toc {
    display: none;
  }
}

@media (max-width: 640px) {
  .learn-lesson {
    padding-top: 96px;
  }

  .lesson-pager {
    grid-template-columns: 1fr;
  }

  .lesson-mark {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
