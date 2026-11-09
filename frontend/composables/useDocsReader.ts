import type { ManualLevel } from '~~/types/manual'

const STORAGE_KEY = 'docs-reader'
const READER_OPTIONS: Array<{ value: ManualLevel; label: string }> = [
  { value: 'user', label: 'Пользователь' },
  { value: 'admin', label: 'Администратор' },
  { value: 'dev', label: 'Разработчик' }
]
const isLevel = (value: unknown): value is ManualLevel => READER_OPTIONS.some((option) => option.value === value)

/**
 * «Читаю как»: пользователю разделы «Для администратора» и «Для разработчика» свёрнуты,
 * администратору открыт свой, разработчику — оба. Выбор помнит браузер; без хранилища — «Пользователь».
 */
export const useDocsReader = () => {
  const reader = useState<ManualLevel>('docs-reader', () => 'user')

  onMounted(() => {
    try {
      const saved = window.localStorage.getItem(STORAGE_KEY)
      if (isLevel(saved)) reader.value = saved
    } catch {
      // хранилище недоступно (приватный режим) — остаётся «Пользователь»
    }
  })

  watch(reader, (value) => {
    try {
      window.localStorage.setItem(STORAGE_KEY, value)
    } catch {
      // не запомнили — выбор действует до перезагрузки
    }
  })

  const levelOpen = (level: string | undefined) =>
    reader.value === 'dev' || (reader.value === 'admin' && level === 'admin')

  return { reader, READER_OPTIONS, levelOpen }
}
