// Обучающий курс — данные собирает scripts/sync-course.mjs из docs/course репозитория web-itwin.

export type CourseLevel = 'user' | 'admin' | 'dev'

export interface CourseQuestion {
  id: string
  /** Вопрос, варианты и пояснение — готовый HTML (строчная разметка, ссылки на /docs и /learn) */
  q: string
  options: string[]
  answer: number
  explain: string
}

export interface CourseLink {
  title: string
  url: string
}

export interface CourseLessonCard {
  id: string
  kind: 'lesson' | 'practice'
  module: number
  title: string
  summary: string
  level: CourseLevel[]
  minutes: number
  url: string
  /** Вопросы теста урока — по ним считается прогресс */
  questionIds: string[]
  tasks: number
  /** Разделы инструкции («05-analysis»), о которых урок */
  sections: string[]
}

export interface CourseLesson extends Omit<CourseLessonCard, 'questionIds'> {
  html: string
  toc: Array<{ id: string; text: string }>
  manual: CourseLink[]
  related: Array<CourseLink & { id: string }>
  quiz: CourseQuestion[]
  keywords: string[]
  updated: string | null
}

export interface CourseExamRule {
  questions: number
  passPercent: number
  pool: number
}

export interface CourseTrack {
  id: string
  title: string
  summary: string
  level: CourseLevel
  start: string
  lessons: string[]
  practice: string | null
  exam: CourseExamRule
  minutes: number
  /** Вопросов в банке трека (уроки + практика) */
  questions: number
}

export interface CourseData {
  generatedAt: string
  source: string
  tracks: CourseTrack[]
  lessons: Record<string, CourseLesson>
}

export interface CourseCatalog {
  generatedAt: string
  tracks: CourseTrack[]
  lessons: Record<string, CourseLessonCard>
}

export interface CourseLessonResponse {
  lesson: CourseLesson
  track: CourseTrack
  /** Соседи по треку — для «Назад / Далее» */
  prev: CourseLessonCard | null
  next: CourseLessonCard | null
}

export interface CourseExamQuestion extends CourseQuestion {
  lessonId: string
  lessonTitle: string
}

export interface CourseExamResponse {
  track: CourseTrack
  pool: CourseExamQuestion[]
}
