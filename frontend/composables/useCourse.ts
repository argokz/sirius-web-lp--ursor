import type { CourseCatalog, CourseExamResponse, CourseLessonResponse } from '~~/types/course'

export const useCourseCatalog = () => useFetch<CourseCatalog>('/docs-data/course/catalog', {
  key: 'course-catalog'
})

export const useCourseLesson = (track: Ref<string>, id: Ref<string>) => useFetch<CourseLessonResponse>(
  () => `/docs-data/course/lesson/${track.value}/${id.value}`,
  { key: computed(() => `course-lesson-${track.value}-${id.value}`) }
)

export const useCourseExam = (track: Ref<string>) => useFetch<CourseExamResponse>(
  () => `/docs-data/course/exam/${track.value}`,
  { key: computed(() => `course-exam-${track.value}`) }
)
