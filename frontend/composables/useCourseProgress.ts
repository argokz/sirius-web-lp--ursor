/**
 * Прогресс курса — только в браузере (localStorage), без входа на сайт.
 * Без хранилища (приватный режим, запрет cookie) курс работает, просто ничего не запоминает.
 */
const STORAGE_KEY = 'course-progress'

interface QuestionProgress {
  /** Ответ с первой попытки верный */
  first: boolean
  /** Верный ответ найден (с любой попытки) */
  solved: boolean
}

interface ExamResult {
  best: number
  last: number
  passed: boolean
  at: string
}

export interface CourseProgress {
  questions: Record<string, QuestionProgress>
  /** Уроки, отмеченные пройденными вручную (практика без теста) */
  done: Record<string, string>
  exams: Record<string, ExamResult>
}

const emptyProgress = (): CourseProgress => ({ questions: {}, done: {}, exams: {} })

const readStored = (): CourseProgress => {
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY)
    if (!raw) return emptyProgress()
    const parsed = JSON.parse(raw) as Partial<CourseProgress>
    return {
      questions: parsed.questions && typeof parsed.questions === 'object' ? parsed.questions : {},
      done: parsed.done && typeof parsed.done === 'object' ? parsed.done : {},
      exams: parsed.exams && typeof parsed.exams === 'object' ? parsed.exams : {}
    }
  } catch {
    return emptyProgress()
  }
}

export const useCourseProgress = () => {
  const progress = useState<CourseProgress>('course-progress', emptyProgress)
  // Сохранённое читается после монтирования — сервер всегда рисует «ничего не пройдено», без расхождения гидратации.
  const loaded = useState('course-progress-loaded', () => false)

  onMounted(() => {
    if (loaded.value) return
    progress.value = readStored()
    loaded.value = true
  })

  const save = () => {
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(progress.value))
    } catch {
      // не запомнили — прогресс живёт до перезагрузки страницы
    }
  }

  /** Ответ на вопрос урока: первая попытка запоминается, дальнейшие только отмечают «решён» */
  const recordAnswer = (questionId: string, correct: boolean) => {
    const previous = progress.value.questions[questionId]
    progress.value.questions[questionId] = {
      first: previous ? previous.first : correct,
      solved: Boolean(previous?.solved) || correct
    }
    save()
  }

  const setDone = (lessonId: string, done: boolean) => {
    if (done) progress.value.done[lessonId] = new Date().toISOString()
    else delete progress.value.done[lessonId]
    save()
  }

  const recordExam = (trackId: string, percent: number, passPercent: number) => {
    const previous = progress.value.exams[trackId]
    progress.value.exams[trackId] = {
      best: Math.max(previous?.best ?? 0, percent),
      last: percent,
      passed: Boolean(previous?.passed) || percent >= passPercent,
      at: new Date().toISOString()
    }
    save()
  }

  /** Урок пройден: все вопросы теста решены, а урок без теста — отмечен вручную */
  const lessonDone = (lessonId: string, questionIds: string[]) =>
    questionIds.length
      ? questionIds.every((id) => progress.value.questions[id]?.solved)
      : Boolean(progress.value.done[lessonId])

  const reset = () => {
    progress.value = emptyProgress()
    save()
  }

  return { progress, loaded, recordAnswer, setDone, recordExam, lessonDone, reset }
}
