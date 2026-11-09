export default defineEventHandler((event) => {
  const exam = getCourseExam(getRouterParam(event, 'track') || '')
  if (!exam) throw createError({ statusCode: 404, statusMessage: 'Трек не найден' })
  return exam
})
