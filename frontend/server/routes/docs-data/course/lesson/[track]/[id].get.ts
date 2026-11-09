export default defineEventHandler((event) => {
  const lesson = getCourseLesson(getRouterParam(event, 'track') || '', getRouterParam(event, 'id') || '')
  if (!lesson) throw createError({ statusCode: 404, statusMessage: 'Урок не найден' })
  return lesson
})
