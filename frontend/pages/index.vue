<template>
  <div class="home">
    <!-- 1. Первый экран: обещание, кнопки, окно веб-ТГИД, которое рисуется само. -->
    <section class="hero">
      <div class="container">
        <div class="hero-copy">
          <span v-reveal class="eyebrow">ТГИД-07 · электронная модель тепловой сети</span>
          <h1 v-reveal="80" class="display-title hero-title">
            Вся тепловая сеть города — <span class="marker">на одной живой карте</span>
          </h1>
          <div v-reveal="160" class="hero-row">
            <p class="lead hero-lead">
              Расчёт режима, аварии и отключения, наряды бригадам, износ и прогноз повреждений, помощник ИИ.
              В браузере, на вашем сервере и в одной базе с десктопом ТГИД.
            </p>
            <div class="hero-actions">
              <UButton to="/demo" size="xl" color="primary" trailing-icon="i-lucide-arrow-right">
                Запросить демо
              </UButton>
              <UButton to="#how" size="xl" variant="outline" color="neutral">
                Как это работает
              </UButton>
            </div>
          </div>
        </div>

        <div v-reveal="240" class="hero-visual">
          <ProductMapDemo />
          <span class="float-tag float-tag-a"><i class="tag-dot ok" />Расчёт фрагмента 74 · готов</span>
          <span class="float-tag float-tag-b">
            <span class="avatars"><i>АК</i><i>ДС</i><i>МЖ</i></span>
            На карте сейчас · 3
          </span>
        </div>
      </div>
    </section>

    <!-- 2. Города: бегущая строка. -->
    <section class="cities" aria-label="Города, сети которых ведутся в ТГИД">
      <div class="container cities-inner">
        <span class="cities-label">Электронные модели сетей в ТГИД</span>
        <div class="marquee">
          <div class="marquee-track">
            <span v-for="(city, i) in [...CITIES, ...CITIES]" :key="i" class="city" :aria-hidden="i >= CITIES.length">
              {{ city }}
            </span>
          </div>
        </div>
      </div>
    </section>

    <!-- 3. Расчёт режима: пьезометр рисуется, бегунок показывает напоры. -->
    <section id="how" class="section">
      <div class="container split-how">
        <div v-reveal>
          <span class="eyebrow">01 · Расчёт режима</span>
          <h2 class="section-title">Посчитать режим — и сразу <em>понять</em>, что он значит</h2>
          <p class="lead">
            Движок heatnet считает гидравлику и тепло фрагмента сети: плановый режим, аварийный или по показаниям
            телеметрии. Результат — на карте: стрелки потоков, цвет труб по потерям, пьезометр по любому маршруту.
          </p>
          <ul class="link-list">
            <li v-for="item in CALC_LINKS" :key="item.to">
              <NuxtLink :to="item.to">
                <span>{{ item.title }}</span>
                <small>{{ item.text }}</small>
                <UIcon name="i-lucide-arrow-right" />
              </NuxtLink>
            </li>
          </ul>
        </div>
        <div v-reveal="120">
          <HomePiezo />
        </div>
      </div>
    </section>

    <!-- 4. Помощник ИИ: вкладки сценариев на тёмном фоне. -->
    <section class="section dark-panel ai-section">
      <div class="container">
        <div v-reveal class="section-head">
          <div>
            <span class="eyebrow">02 · Помощник ИИ</span>
            <h2 class="section-title">Спросите сеть обычными словами</h2>
          </div>
          <p class="lead">
            Помощник сам ищет объекты, трассирует, локализует аварию и сравнивает сценарии — и показывает ответ на
            карте. Он работает с вашими правами, а функции ИИ включаются флагом и вашим ключом.
          </p>
        </div>
        <HomeAiDemo v-reveal="100" />
      </div>
    </section>

    <!-- 5. Возможности 01–08. -->
    <section class="section">
      <div class="container">
        <div v-reveal class="section-head">
          <div>
            <span class="eyebrow">03 · Возможности</span>
            <h2 class="section-title">От паспорта трубы до плана перекладок</h2>
          </div>
          <p class="lead">
            Восемь направлений в одном окне. У каждого — страница справки с примерами, роликами и тем,
            что делать, если что-то не получается.
          </p>
        </div>
        <div v-reveal.stagger class="cap-grid">
          <NuxtLink v-for="(cap, i) in CAPABILITIES" :key="cap.title" :to="cap.to" class="cap">
            <span class="cap-num">{{ String(i + 1).padStart(2, '0') }}</span>
            <UIcon :name="cap.icon" class="cap-icon" />
            <h3>{{ cap.title }}</h3>
            <p>{{ cap.text }}</p>
            <span class="cap-more">В справке <UIcon name="i-lucide-arrow-right" /></span>
          </NuxtLink>
        </div>
      </div>
    </section>

    <!-- 6. Полевое приложение. -->
    <section class="section field-section">
      <div class="container split-how">
        <div v-reveal>
          <span class="eyebrow">04 · Полевое приложение</span>
          <h2 class="section-title">Бригада работает и там, где нет связи</h2>
          <p class="lead">
            Наряды, обходы по формам, дефекты с фото и трек — в телефоне. Без связи всё копится в очереди
            и уходит на сервер, как только сеть появится. Диспетчер видит, что бригада на месте.
          </p>
          <ol class="steps">
            <li v-for="(step, i) in FIELD_STEPS" :key="step">
              <span>{{ String(i + 1).padStart(2, '0') }}</span>{{ step }}
            </li>
          </ol>
          <NuxtLink to="/docs/field-public/field-app" class="text-link">
            Приложение бригады в справке <UIcon name="i-lucide-arrow-right" />
          </NuxtLink>
        </div>
        <div v-reveal="120">
          <HomePhones />
        </div>
      </div>
    </section>

    <!-- 7. Данные и связи: тонкий список в две колонки. -->
    <section class="section rule-top">
      <div class="container">
        <div v-reveal class="section-head">
          <div>
            <span class="eyebrow">05 · Данные и связи</span>
            <h2 class="section-title">Встаёт в то, что у вас уже есть</h2>
          </div>
          <p class="lead">
            Одна база с десктопом ТГИД, импорт из ZuluGIS и файлов, стандартные протоколы ГИС
            и телеметрии. Данные не нужно переписывать вручную.
          </p>
        </div>
        <ul v-reveal.stagger class="int-list">
          <li v-for="item in INTEGRATIONS" :key="item.title">
            <component :is="item.to ? NuxtLinkComponent : 'div'" :to="item.to || undefined" class="int-item">
              <UIcon :name="item.icon" class="int-icon" />
              <span class="int-text">
                <strong>{{ item.title }}</strong>
                <small>{{ item.text }}</small>
              </span>
              <span class="int-tag">{{ item.tag }}</span>
            </component>
          </li>
        </ul>
      </div>
    </section>

    <!-- 8. Разработчикам. -->
    <section class="section dark-panel">
      <div class="container">
        <div v-reveal class="section-head">
          <div>
            <span class="eyebrow">06 · Разработчикам</span>
            <h2 class="section-title">Открытый API вместо выгрузок по почте</h2>
          </div>
          <p class="lead">
            API v2 для 1С, ERP и SCADA, вебхуки с подписью, OGC API и ArcGIS FeatureServer для ГИС,
            MCP для ИИ-клиентов и встраиваемая карта для сайта города.
          </p>
        </div>
        <HomeDevPanel v-reveal="100" />
      </div>
    </section>

    <!-- 9. Справка и обучение: числа из справки и курса. -->
    <section class="section">
      <div class="container">
        <div v-reveal class="section-head">
          <div>
            <span class="eyebrow">07 · Справка и обучение</span>
            <h2 class="section-title">Каждая функция описана, показана и проверена</h2>
          </div>
          <p class="lead">
            Справка написана по живой системе: у страниц есть снимки, ролики и раздел «если не работает».
            Курс ведёт каждую роль от первого входа до итогового теста.
          </p>
        </div>

        <div ref="statsEl" v-reveal.stagger class="stats">
          <div v-for="stat in statItems" :key="stat.label" class="stat">
            <span class="stat-value">{{ shown[stat.key] ?? stat.value }}</span>
            <span class="stat-label">{{ stat.label }}</span>
          </div>
        </div>

        <div class="learn-grid">
          <div v-reveal class="learn-col">
            <div class="learn-col-head">
              <h3>Курс по ролям</h3>
              <NuxtLink to="/learn" class="text-link">Все треки <UIcon name="i-lucide-arrow-right" /></NuxtLink>
            </div>
            <NuxtLink v-for="track in stats?.trackList || []" :key="track.id" :to="`/learn/${track.id}`" class="track-row">
              <strong>{{ track.title }}</strong>
              <small>{{ track.lessons }} уроков · {{ hours(track.minutes) }}</small>
              <UIcon name="i-lucide-arrow-right" />
            </NuxtLink>
          </div>
          <div v-reveal="100" class="learn-col">
            <div class="learn-col-head">
              <h3>Справка по разделам</h3>
              <NuxtLink to="/docs" class="text-link">Вся справка <UIcon name="i-lucide-arrow-right" /></NuxtLink>
            </div>
            <button type="button" class="search-pill" @click="searchOpen = true">
              <UIcon name="i-lucide-search" />
              Найти в справке и курсе…
              <kbd>Ctrl K</kbd>
            </button>
            <div class="section-chips">
              <NuxtLink v-for="section in stats?.sectionList || []" :key="section.slug" :to="`/docs/${section.slug}`" class="section-chip">
                <span>{{ section.num }}</span>{{ section.title }}
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 10. Безопасность 01–03. -->
    <section class="section rule-top">
      <div class="container">
        <div v-reveal class="section-head">
          <div>
            <span class="eyebrow">08 · Безопасность</span>
            <h2 class="section-title">Данные сети остаются вашими</h2>
          </div>
        </div>
        <div v-reveal.stagger class="sec-grid">
          <NuxtLink v-for="(item, i) in SECURITY" :key="item.title" :to="item.to" class="sec-item">
            <span class="index-label">{{ String(i + 1).padStart(2, '0') }}</span>
            <h3>{{ item.title }}</h3>
            <p>{{ item.text }}</p>
          </NuxtLink>
        </div>
      </div>
    </section>

    <!-- 11. Вопросы. -->
    <section class="section rule-top">
      <div class="container faq-wrap">
        <div v-reveal>
          <span class="eyebrow">Вопросы</span>
          <h2 class="section-title">Что обычно спрашивают</h2>
          <p class="lead">Не нашли ответа — нажмите <kbd>Ctrl K</kbd> и поищите в справке или напишите нам.</p>
        </div>
        <div v-reveal="100" class="faq">
          <details v-for="(item, i) in FAQ" :key="item.q" class="faq-item">
            <summary>
              <span class="faq-num">{{ String(i + 1).padStart(2, '0') }}</span>
              {{ item.q }}
              <UIcon name="i-lucide-plus" class="faq-icon" />
            </summary>
            <p>{{ item.a }}</p>
          </details>
        </div>
      </div>
    </section>

    <!-- 12. Призыв. -->
    <section class="section-tight">
      <div class="container">
        <div v-reveal class="cta">
          <div class="cta-grid" aria-hidden="true" />
          <span class="eyebrow">Демонстрация</span>
          <h2 class="section-title">Покажем ТГИД на сети вашего города</h2>
          <p class="lead">
            Расчёт режима, локализация аварии, наряд бригаде и помощник ИИ — за одну встречу.
            Расскажем, что понадобится для запуска.
          </p>
          <div class="hero-actions">
            <UButton to="/demo" size="xl" color="neutral" variant="solid" class="cta-primary" trailing-icon="i-lucide-arrow-right">
              Запросить демо
            </UButton>
            <UButton to="/contacts" size="xl" variant="outline" color="neutral" class="cta-secondary">
              Связаться
            </UButton>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { resolveComponent } from 'vue'

interface SiteStats {
  sections: number
  pages: number
  videos: number
  journeys: number
  tracks: number
  lessons: number
  practice: number
  questions: number
  hours: number
  sectionList: Array<{ num: string; title: string; slug: string; pages: number }>
  trackList: Array<{ id: string; title: string; summary: string; lessons: number; minutes: number; level: string }>
}

useSEO({
  title: 'ТГИД-07 — электронная модель тепловой сети города | ПКФ «Сириус»',
  description: 'Веб-ТГИД: карта и паспорт тепловой сети, теплогидравлический расчёт, аварии и отключения, наряды, износ и прогноз аварийности, телеметрия, помощник ИИ, API. Справка и курс обучения.'
})
useStructuredData()

const NuxtLinkComponent = resolveComponent('NuxtLink')
const searchOpen = useState('site-search-open', () => false)

const CITIES = ['Алматы', 'Астана', 'Шымкент', 'Тараз', 'Актобе', 'Семей', 'Шахтинск', 'Шатура']

const CALC_LINKS = [
  { title: 'Расчёт режима', text: 'Плановый, аварийный, по факту', to: '/docs/analysis/calculation' },
  { title: 'Протокол расчёта', text: 'Ошибки с переходом к объекту', to: '/docs/analysis/protocol' },
  { title: 'Пьезометрический график', text: 'Напоры по маршруту на карте', to: '/docs/analysis/piezometer' },
  { title: 'Сценарий «что если»', text: 'Копия, правка, сравнение', to: '/docs/journeys/scenario' }
]

const CAPABILITIES = [
  { icon: 'i-lucide-map', title: 'Карта и паспорт сети', text: 'Участки, узлы, камеры и потребители поверх подложки, карточка объекта как в десктопе, сеть под землёй в 3D.', to: '/docs/start/map-overview' },
  { icon: 'i-lucide-gauge', title: 'Расчёт и анализ режима', text: 'Гидравлика и тепло, анализ режима, наладка шайбами и элеваторами, температурные графики и тепловые потери.', to: '/docs/analysis/regime-analysis' },
  { icon: 'i-lucide-pen-tool', title: 'Редактор сети', text: 'Новый участок трассой, врезка узла, проверка топологии после каждой правки, история и откат.', to: '/docs/journeys/network-edit' },
  { icon: 'i-lucide-siren', title: 'Аварии и отключения', text: 'Какие задвижки закрыть и кто останется без тепла, объявление отключения, публичная карта для жителей.', to: '/docs/operations/outage-simulation' },
  { icon: 'i-lucide-clipboard-list', title: 'Наряды и обходы', text: 'От заявки или дефекта до закрытия: бригада, сроки, формы осмотра, журналы шурфовок, опрессовок и ремонтов.', to: '/docs/operations/work-orders' },
  { icon: 'i-lucide-trending-up', title: 'Износ и прогноз аварийности', text: 'Индекс износа по методике ТГИД, вероятность повреждения на два года, план перекладок с запиской ИИ.', to: '/docs/analysis/failure-forecast' },
  { icon: 'i-lucide-radio-tower', title: 'Телеметрия', text: 'Датчики и ОДПУ против расчёта, тревоги, баланс расхода, прогноз нагрузки на сутки по погоде.', to: '/docs/other-networks/telemetry' },
  { icon: 'i-lucide-droplets', title: 'Водопровод и другие сети', text: 'Модели EPANET, зоны водоучёта и утечки, электросеть, сближения коммуникаций и раскопки.', to: '/docs/water/water' }
]

const FIELD_STEPS = [
  'Наряды бригады и маршрут на карте',
  'Обход по форме с фото и отметками',
  'Дефект на месте — сразу в журнал нарушений',
  'Без связи всё ждёт в очереди и уходит само'
]

const INTEGRATIONS = [
  { icon: 'i-lucide-monitor', title: 'Десктоп ТГИД', text: 'Одна база города, правки видны в обоих', tag: 'Одна база', to: '/docs/administration/architecture' },
  { icon: 'i-lucide-import', title: 'ZuluGIS', text: 'Перенос сети с пересчётом координат', tag: 'Импорт', to: '' },
  { icon: 'i-lucide-database', title: 'PostgreSQL · PostGIS', text: 'База города на вашем сервере', tag: 'База', to: '/docs/administration/backups' },
  { icon: 'i-lucide-sheet', title: 'Excel', text: 'Ведомости по шаблонам, импорт с подбором колонок', tag: 'Отчёты', to: '/docs/journeys/reports' },
  { icon: 'i-lucide-layers', title: 'GeoPackage · Shapefile · FlatGeobuf', text: 'Обмен слоями с ГИС', tag: 'ГИС', to: '/docs/source-data/network-import' },
  { icon: 'i-lucide-globe', title: 'OGC API — Features и Processes', text: 'Слои сети по стандарту, GeoJSON в WGS 84', tag: 'Стандарт', to: '/docs/developers/ogc' },
  { icon: 'i-lucide-map-pinned', title: 'ArcGIS FeatureServer', text: 'Слои для ArcGIS и QGIS по GeoServices REST', tag: 'GeoServices', to: '/docs/developers/arcgis' },
  { icon: 'i-lucide-cpu', title: 'OPC UA · SCADA · ОДПУ', text: 'Показания датчиков против модели', tag: 'Телеметрия', to: '/docs/other-networks/telemetry' },
  { icon: 'i-lucide-waves', title: 'EPANET', text: 'Расчёт водопровода по часам', tag: 'Водопровод', to: '/docs/water/water' },
  { icon: 'i-lucide-cloud-sun', title: 'Open-Meteo', text: 'Прогноз нагрузки источников на сутки', tag: 'Погода', to: '/docs/other-networks/telemetry-forecast' },
  { icon: 'i-lucide-code', title: 'Встраиваемая карта', text: 'Карта сети на сайте города по ключу', tag: 'SDK', to: '/docs/developers/embed' },
  { icon: 'i-lucide-bot', title: 'MCP', text: 'Claude и другие ИИ-клиенты с вашими правами', tag: 'ИИ', to: '/docs/ai/mcp-server' }
]

const SECURITY = [
  { title: 'Права по ролям', text: 'Матрица видов и действий, роли-шаблоны, правка «только своих» объектов и журнал действий каждого пользователя.', to: '/docs/administration/roles-rights' },
  { title: 'Персональные данные под маской', text: 'ФИО и адреса абонентов видят только те, кому выдано право. Остальным API отдаёт их скрытыми.', to: '/docs/administration/personal-data' },
  { title: 'Ваш сервер', text: 'Система ставится в вашей сети, резервные копии — по расписанию. Функции ИИ необязательны: без ключа всё остальное работает.', to: '/docs/administration/architecture' }
]

const FAQ = [
  { q: 'Нужно ли отказываться от десктопа ТГИД?', a: 'Нет. Веб и десктоп работают в одной базе города: правка в одном видна в другом, номера объектов не меняются. Переходить можно постепенно, по службам.' },
  { q: 'Можно ли перенести сеть из ZuluGIS?', a: 'Да. Конвертер переносит сеть ZuluGIS в базу ТГИД с пересчётом координат, ход переноса виден в приложении. Слои SHP, Excel и координаты загружаются импортом.' },
  { q: 'Насколько можно доверять расчёту?', a: 'Движок heatnet сверяется с эталонными расчётами прежнего движка на сетях Алматы и Астаны. Протокол показывает каждую ошибку и предупреждение с переходом к объекту, а помощник ИИ объясняет их словами.' },
  { q: 'Сколько времени займёт обучение?', a: 'Трек «Новичок» — 8 уроков, около четырёх часов. У режимщика, редактора сети, диспетчера, администратора и разработчика свои треки с практикой на стенде и итоговым тестом.' },
  { q: 'Можно ли вести несколько городов?', a: 'Да. Один сервер обслуживает несколько городов: у каждого своя база, свой адрес и свои пользователи, переход между городами — из меню пользователя.' },
  { q: 'Обязателен ли ИИ?', a: 'Нет. Функции ИИ включаются отдельно и работают с вашим ключом. Без них доступны все расчёты, журналы, карта и отчёты.' },
  { q: 'Как устроен доступ для внешних систем?', a: 'API v2 с ключом для 1С, ERP и SCADA, вебхуки с подписью Standard Webhooks, OGC API и ArcGIS FeatureServer для ГИС, MCP для ИИ-клиентов. Всё описано в разделе справки «Разработчикам».' }
]

const { data: stats } = await useFetch<SiteStats>('/docs-data/stats', { key: 'site-stats' })

const hours = (minutes: number) => `≈ ${Math.max(1, Math.round(minutes / 60))} ч`

const statItems = computed(() => {
  const s = stats.value
  if (!s) return []
  return [
    { key: 'sections', value: s.sections, label: 'разделов справки' },
    { key: 'pages', value: s.pages, label: 'страниц с примерами' },
    { key: 'videos', value: s.videos, label: 'роликов' },
    { key: 'journeys', value: s.journeys, label: 'сквозных сценариев' },
    { key: 'tracks', value: s.tracks, label: 'треков курса' },
    { key: 'lessons', value: s.lessons, label: 'уроков и практик' },
    { key: 'questions', value: s.questions, label: 'вопросов в тестах' },
    { key: 'hours', value: s.hours, label: 'часов обучения' }
  ]
})

// Числа «досчитываются» до значения, когда блок дошёл до экрана.
const COUNT_MS = 1400
const statsEl = ref<HTMLElement | null>(null)
const shown = reactive<Record<string, number>>({})
let statsObserver: IntersectionObserver | null = null

const countUp = () => {
  const items = statItems.value
  const startAt = performance.now()
  const tick = (now: number) => {
    const t = Math.min(1, (now - startAt) / COUNT_MS)
    const eased = 1 - (1 - t) ** 3
    for (const item of items) shown[item.key] = Math.round(item.value * eased)
    if (t < 1) requestAnimationFrame(tick)
  }
  requestAnimationFrame(tick)
}

onMounted(() => {
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches || !statsEl.value) return
  statsObserver = new IntersectionObserver(([entry]) => {
    if (!entry?.isIntersecting) return
    statsObserver?.disconnect()
    countUp()
  }, { threshold: 0.4 })
  statsObserver.observe(statsEl.value)
})

onBeforeUnmount(() => statsObserver?.disconnect())
</script>

<style scoped>
.home {
  overflow-x: clip;
}

/* Первый экран */
.hero {
  padding: 148px 0 72px;
  background:
    radial-gradient(circle at 1px 1px, rgba(28, 27, 24, 0.09) 1px, transparent 0) 0 0 / 22px 22px,
    var(--paper);
}

.hero-title {
  max-width: 980px;
  font-size: clamp(2.6rem, 6vw, 5rem);
}

.hero-row {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 32px;
}

.hero-lead {
  max-width: 620px;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  flex-shrink: 0;
}

.hero-visual {
  position: relative;
  margin-top: 56px;
}

.float-tag {
  position: absolute;
  z-index: 2;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border: 1px solid var(--ink);
  border-radius: 6px;
  color: var(--ink);
  background: var(--surface);
  box-shadow: 0 14px 30px -18px rgba(28, 27, 24, 0.5);
  font-family: var(--mono);
  font-size: 0.7rem;
  letter-spacing: 0.04em;
  white-space: nowrap;
  animation: tag-float 6s ease-in-out infinite;
}

.float-tag-a {
  top: -18px;
  right: 6%;
}

.float-tag-b {
  bottom: -18px;
  left: 4%;
  animation-delay: -3s;
}

@keyframes tag-float {
  50% { transform: translateY(-6px); }
}

.tag-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.tag-dot.ok {
  background: #2f9e44;
  box-shadow: 0 0 0 3px rgba(47, 158, 68, 0.2);
}

.avatars {
  display: inline-flex;
}

.avatars i {
  width: 22px;
  height: 22px;
  display: grid;
  place-items: center;
  margin-left: -6px;
  border: 2px solid var(--surface);
  border-radius: 50%;
  color: #fff;
  font-size: 0.56rem;
  font-style: normal;
}

.avatars i:first-child { margin-left: 0; background: #0a7af2; }
.avatars i:nth-child(2) { background: #e30613; }
.avatars i:nth-child(3) { background: #2f9e44; }

/* Города */
.cities {
  border-top: 1px solid var(--line);
  border-bottom: 1px solid var(--line);
  background: var(--paper);
}

.cities-inner {
  display: flex;
  align-items: center;
  gap: 32px;
  height: 64px;
}

.cities-label {
  flex: 0 0 auto;
  color: var(--muted);
  font-family: var(--mono);
  font-size: 0.68rem;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.marquee {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  mask-image: linear-gradient(90deg, transparent, #000 8%, #000 92%, transparent);
}

.marquee-track {
  display: flex;
  width: max-content;
  animation: marquee 36s linear infinite;
}

.marquee:hover .marquee-track {
  animation-play-state: paused;
}

.city {
  padding: 0 28px;
  color: var(--ink-2);
  font-family: var(--serif);
  font-size: 1.3rem;
}

.city::after {
  content: "·";
  margin-left: 56px;
  color: var(--line-strong);
}

@keyframes marquee {
  to { transform: translateX(-50%); }
}

/* Общие заголовки секций: слева заголовок, справа пояснение. */
.section-head {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 0.8fr);
  gap: 40px;
  align-items: end;
  margin-bottom: 48px;
}

.section-head .lead {
  margin: 0;
}

.section-title em {
  font-style: italic;
  color: var(--accent);
}

.dark-panel .section-title em {
  color: #ff6b5e;
}

.split-how {
  display: grid;
  grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr);
  gap: 56px;
  align-items: center;
}

.link-list {
  margin: 32px 0 0;
  padding: 0;
  list-style: none;
  border-top: 1px solid var(--line);
}

.link-list a {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto 18px;
  gap: 16px;
  align-items: center;
  padding: 14px 0;
  border-bottom: 1px solid var(--line);
  color: var(--ink);
  transition: padding 0.25s ease, color 0.2s ease;
}

.link-list a:hover {
  padding-left: 8px;
  color: var(--accent);
}

.link-list small {
  color: var(--muted);
  font-family: var(--mono);
  font-size: 0.7rem;
}

.text-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-top: 24px;
  color: var(--ink);
  font-weight: 500;
  text-decoration: underline;
  text-decoration-color: var(--line-strong);
  text-underline-offset: 5px;
  transition: text-decoration-color 0.2s ease;
}

.text-link:hover {
  text-decoration-color: var(--sirius-red);
}

/* Возможности 01–08 */
.cap-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  border-top: 1px solid var(--ink);
  border-left: 1px solid var(--line);
}

.cap {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-height: 280px;
  padding: 24px 22px;
  border-right: 1px solid var(--line);
  border-bottom: 1px solid var(--line);
  color: var(--ink);
  transition: background-color 0.25s ease;
}

.cap::before {
  content: "";
  position: absolute;
  top: -1px;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--sirius-red);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.35s ease;
}

.cap:hover {
  background: var(--surface);
}

.cap:hover::before {
  transform: scaleX(1);
}

.cap-num {
  color: var(--accent);
  font-family: var(--mono);
  font-size: 0.74rem;
}

.cap-icon {
  width: 26px;
  height: 26px;
  margin: 18px 0 6px;
  color: var(--ink);
}

.cap h3 {
  margin: 0;
  font-family: var(--serif);
  font-size: 1.3rem;
  font-weight: 400;
  line-height: 1.2;
}

.cap p {
  margin: 0;
  color: var(--ink-2);
  font-size: 0.92rem;
  line-height: 1.55;
}

.cap-more {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-top: auto;
  padding-top: 10px;
  color: var(--muted);
  font-size: 0.82rem;
  transition: color 0.2s ease, gap 0.2s ease;
}

.cap:hover .cap-more {
  gap: 10px;
  color: var(--accent);
}

/* Полевое приложение */
.field-section {
  background: var(--paper-2);
}

.steps {
  margin: 28px 0 0;
  padding: 0;
  list-style: none;
}

.steps li {
  display: flex;
  gap: 16px;
  padding: 12px 0;
  border-bottom: 1px solid var(--line-strong);
  color: var(--ink);
}

.steps span {
  color: var(--accent);
  font-family: var(--mono);
  font-size: 0.78rem;
  line-height: 1.6;
}

/* Данные и связи */
.int-list {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  column-gap: 48px;
  margin: 0;
  padding: 0;
  list-style: none;
  border-top: 1px solid var(--ink);
}

.int-item {
  display: grid;
  grid-template-columns: 22px minmax(0, 1fr) auto;
  gap: 16px;
  align-items: center;
  padding: 16px 0;
  border-bottom: 1px solid var(--line);
  color: var(--ink);
}

a.int-item:hover .int-text strong {
  color: var(--accent);
}

.int-icon {
  width: 20px;
  height: 20px;
  color: var(--ink-2);
}

.int-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.int-text strong {
  font-weight: 500;
  transition: color 0.2s ease;
}

.int-text small {
  color: var(--muted);
  font-size: 0.84rem;
}

.int-tag {
  padding: 3px 8px;
  border: 1px solid var(--line-strong);
  border-radius: 999px;
  color: var(--muted);
  font-family: var(--mono);
  font-size: 0.64rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  white-space: nowrap;
}

/* Справка и обучение */
.stats {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  border-top: 1px solid var(--ink);
}

.stat {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 22px 0 26px;
  border-bottom: 1px solid var(--line);
}

.stat-value {
  color: var(--ink);
  font-family: var(--serif);
  font-size: clamp(2.4rem, 4.5vw, 3.6rem);
  line-height: 1;
  font-variant-numeric: tabular-nums;
}

.stat-label {
  color: var(--muted);
  font-family: var(--mono);
  font-size: 0.72rem;
  letter-spacing: 0.04em;
}

.learn-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 48px;
  margin-top: 56px;
}

.learn-col-head {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 16px;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--ink);
}

.learn-col-head h3 {
  margin: 0;
  font-family: var(--serif);
  font-size: 1.5rem;
  font-weight: 400;
}

.learn-col-head .text-link {
  margin: 0;
  font-size: 0.9rem;
}

.track-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto 18px;
  gap: 16px;
  align-items: center;
  padding: 14px 0;
  border-bottom: 1px solid var(--line);
  color: var(--ink);
  transition: padding 0.25s ease, color 0.2s ease;
}

.track-row:hover {
  padding-left: 8px;
  color: var(--accent);
}

.track-row strong {
  font-weight: 500;
}

.track-row small {
  color: var(--muted);
  font-family: var(--mono);
  font-size: 0.72rem;
}

.search-pill {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 18px 0;
  padding: 12px 14px;
  border: 1px solid var(--line-strong);
  border-radius: 6px;
  color: var(--muted);
  background: var(--surface);
  font-size: 0.95rem;
  text-align: left;
  cursor: pointer;
  transition: border-color 0.2s ease;
}

.search-pill:hover {
  border-color: var(--ink);
}

.search-pill kbd {
  margin-left: auto;
}

kbd {
  padding: 2px 6px;
  border: 1px solid var(--line-strong);
  border-bottom-width: 2px;
  border-radius: 4px;
  background: var(--paper);
  font-family: var(--mono);
  font-size: 0.7em;
}

.section-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.section-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 10px;
  border: 1px solid var(--line);
  border-radius: 4px;
  color: var(--ink-2);
  font-size: 0.86rem;
  transition: border-color 0.2s ease, color 0.2s ease;
}

.section-chip span {
  color: var(--accent);
  font-family: var(--mono);
  font-size: 0.7rem;
}

.section-chip:hover {
  border-color: var(--ink);
  color: var(--ink);
}

/* Безопасность */
.sec-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 40px;
}

.sec-item {
  display: block;
  color: var(--ink);
}

.sec-item h3 {
  margin: 18px 0 10px;
  font-family: var(--serif);
  font-size: 1.5rem;
  font-weight: 400;
  transition: color 0.2s ease;
}

.sec-item:hover h3 {
  color: var(--accent);
}

.sec-item p {
  margin: 0;
  color: var(--ink-2);
  line-height: 1.6;
}

/* Вопросы */
.faq-wrap {
  display: grid;
  grid-template-columns: minmax(0, 0.8fr) minmax(0, 1.2fr);
  gap: 56px;
  align-items: start;
}

.faq {
  border-top: 1px solid var(--ink);
}

.faq-item {
  border-bottom: 1px solid var(--line);
}

.faq-item summary {
  display: grid;
  grid-template-columns: 36px minmax(0, 1fr) 20px;
  gap: 12px;
  align-items: center;
  padding: 20px 0;
  color: var(--ink);
  font-family: var(--serif);
  font-size: 1.2rem;
  cursor: pointer;
  list-style: none;
}

.faq-item summary::-webkit-details-marker {
  display: none;
}

.faq-num {
  color: var(--accent);
  font-family: var(--mono);
  font-size: 0.74rem;
}

.faq-icon {
  width: 18px;
  height: 18px;
  transition: transform 0.25s ease;
}

.faq-item[open] .faq-icon {
  transform: rotate(45deg);
}

.faq-item p {
  margin: 0;
  padding: 0 32px 22px 48px;
  color: var(--ink-2);
  line-height: 1.65;
  animation: faq-open 0.3s ease;
}

@keyframes faq-open {
  from { opacity: 0; transform: translateY(-6px); }
}

/* Призыв */
.cta {
  position: relative;
  overflow: hidden;
  padding: 72px 56px;
  border-radius: 10px;
  color: var(--on-dark);
  background: var(--dark);
}

.cta-grid {
  position: absolute;
  inset: 0;
  background:
    linear-gradient(rgba(246, 244, 238, 0.06) 1px, transparent 1px) 0 0 / 48px 48px,
    linear-gradient(90deg, rgba(246, 244, 238, 0.06) 1px, transparent 1px) 0 0 / 48px 48px;
  mask-image: radial-gradient(circle at 80% 30%, #000, transparent 70%);
  animation: grid-pan 30s linear infinite;
}

@keyframes grid-pan {
  to { background-position: 48px 48px, 48px 48px; }
}

.cta > *:not(.cta-grid) {
  position: relative;
}

.cta .eyebrow {
  color: #ff6b5e;
}

.cta .section-title {
  color: var(--on-dark);
}

.cta .lead {
  color: var(--on-dark-muted);
}

.cta .hero-actions {
  margin-top: 32px;
}

.cta-primary {
  color: var(--ink);
  background: var(--on-dark);
}

.cta-primary:hover {
  background: #fff;
}

.cta-secondary {
  color: var(--on-dark);
  background: transparent;
  box-shadow: inset 0 0 0 1px rgba(246, 244, 238, 0.4);
}

.cta-secondary:hover {
  background: rgba(246, 244, 238, 0.08);
}

@media (max-width: 1100px) {
  .cap-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .cap {
    min-height: 0;
  }
}

@media (max-width: 900px) {
  .hero-row,
  .section-head,
  .split-how,
  .learn-grid,
  .faq-wrap {
    display: grid;
    grid-template-columns: 1fr;
    gap: 28px;
  }

  .hero-row {
    align-items: start;
  }

  .int-list {
    grid-template-columns: 1fr;
  }

  .sec-grid {
    grid-template-columns: 1fr;
    gap: 32px;
  }

  .stats {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 640px) {
  .hero {
    padding: 104px 0 56px;
  }

  .hero-visual {
    margin-top: 40px;
  }

  .float-tag {
    display: none;
  }

  .cities-inner {
    height: 56px;
    gap: 16px;
  }

  .cities-label {
    display: none;
  }

  .cap-grid {
    grid-template-columns: 1fr;
  }

  .cta {
    padding: 48px 24px;
  }

  .faq-item p {
    padding: 0 0 20px 48px;
  }

  .link-list small {
    display: none;
  }
}

@media (prefers-reduced-motion: reduce) {
  .float-tag,
  .marquee-track,
  .cta-grid {
    animation: none;
  }
}
</style>
