import courseJson from '../data/course.json'
import type { CourseCatalog, CourseData, CourseExamResponse, CourseLesson, CourseLessonCard, CourseLessonResponse } from '~~/types/course'

// Данные собирает scripts/sync-course.mjs из docs/course репозитория web-itwin.
const course = courseJson as unknown as CourseData

const toCard = (lesson: CourseLesson): CourseLessonCard => ({
  id: lesson.id,
  kind: lesson.kind,
  module: lesson.module,
  title: lesson.title,
  summary: lesson.summary,
  level: lesson.level,
  minutes: lesson.minutes,
  url: lesson.url,
  questionIds: lesson.quiz.map((question) => question.id),
  tasks: lesson.tasks,
  sections: lesson.sections
})

const catalog: CourseCatalog = {
  generatedAt: course.generatedAt,
  tracks: course.tracks,
  lessons: Object.fromEntries(Object.values(course.lessons).map((lesson) => [lesson.id, toCard(lesson)]))
}

export const getCourseCatalog = () => catalog

export const getCourseTrack = (trackId: string) => course.tracks.find((track) => track.id === trackId)

/** Порядок трека: уроки, затем практика */
const trackOrder = (trackId: string) => {
  const track = getCourseTrack(trackId)
  return track ? [...track.lessons, ...(track.practice ? [track.practice] : [])] : []
}

export const getCourseLesson = (trackId: string, lessonId: string): CourseLessonResponse | null => {
  const track = getCourseTrack(trackId)
  const order = trackOrder(trackId)
  const position = order.indexOf(lessonId)
  const lesson = course.lessons[lessonId]
  if (!track || !lesson || position < 0) return null
  const card = (id: string | undefined) => (id ? catalog.lessons[id] ?? null : null)
  return { lesson, track, prev: card(order[position - 1]), next: card(order[position + 1]) }
}

/** Банк вопросов итогового теста: все вопросы уроков и практики трека; выборку делает браузер */
export const getCourseExam = (trackId: string): CourseExamResponse | null => {
  const track = getCourseTrack(trackId)
  if (!track) return null
  const pool = trackOrder(trackId).flatMap((id) => {
    const lesson = course.lessons[id]
    return lesson ? lesson.quiz.map((question) => ({ ...question, lessonId: id, lessonTitle: lesson.title })) : []
  })
  return { track, pool }
}
