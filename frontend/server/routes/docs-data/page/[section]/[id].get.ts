export default defineEventHandler((event) => {
  const result = getManualPage(getRouterParam(event, 'section') || '', getRouterParam(event, 'id') || '')
  if (!result) {
    throw createError({ statusCode: 404, statusMessage: 'Страница справки не найдена' })
  }
  return result
})
