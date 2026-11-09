// Курс: треки и карточки уроков. Не под /api: на itwin.kz этот префикс nginx отдаёт другому сервису.
export default defineEventHandler(() => getCourseCatalog())
