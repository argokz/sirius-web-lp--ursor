// Сводные числа справки и курса для витрины: главная показывает их, не загружая каталоги целиком.
export default defineEventHandler(() => {
  const manual = getManualCatalog()
  const course = getCourseCatalog()
  const pages = Object.values(manual.pages)
  const lessons = Object.values(course.lessons)
  const sections = manual.sections.filter((section) => section.id !== 'journeys')

  return {
    sections: sections.length,
    pages: pages.length,
    videos: pages.filter((page) => page.video).length,
    journeys: manual.sections.find((section) => section.id === 'journeys')?.pageIds.length || 0,
    tracks: course.tracks.length,
    lessons: lessons.length,
    practice: lessons.filter((lesson) => lesson.kind === 'practice').length,
    questions: lessons.reduce((sum, lesson) => sum + lesson.questionIds.length, 0),
    hours: Math.round(course.tracks.reduce((sum, track) => sum + track.minutes, 0) / 60),
    sectionList: sections.map((section) => ({ num: section.num, title: section.title, slug: section.slug, pages: section.pageIds.length })),
    trackList: course.tracks.map((track) => ({ id: track.id, title: track.title, summary: track.summary, lessons: track.lessons.length, minutes: track.minutes, level: track.level }))
  }
})
