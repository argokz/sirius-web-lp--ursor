/**
 * Русская типографика для текстов витрины: короткие предлоги и союзы приклеиваются к следующему
 * слову, тире — к предыдущему (неразрывный пробел), числа — к единицам измерения.
 * Так «в», «на», «—» не повисают в конце или начале строки.
 */
const NBSP = ' '
const SHORT_WORDS = /(^|[\s(«])(а|в|и|к|о|с|у|я|во|до|за|из|ко|на|не|ни|но|об|от|по|со|для|без|при|про)\s+/gi
const DASH = /\s+—\s/g
const NUMBER_UNIT = /(\d)\s+(%|°|мм|см|м|км|ч|мин|с|МПа|Гкал|т|шт|Ду)(?=[\s.,;:)»]|$)/g

export const typo = (text: string) => text
  .replace(SHORT_WORDS, (_, before: string, word: string) => `${before}${word}${NBSP}`)
  // Второй проход: «и в городе» — после замены «и» следующий предлог тоже должен приклеиться.
  .replace(SHORT_WORDS, (_, before: string, word: string) => `${before}${word}${NBSP}`)
  .replace(DASH, `${NBSP}— `)
  .replace(NUMBER_UNIT, `$1${NBSP}$2`)
