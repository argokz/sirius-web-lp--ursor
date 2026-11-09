<template>
  <CmsPageRenderer slug="home">
    <div class="page">
    <section class="hero">
      <div class="container hero-grid">
        <div class="hero-copy reveal">
          <UBadge color="primary" variant="subtle" size="lg">
            АСУП ТГИД-07 / цифровой контур теплоснабжения
          </UBadge>
          <h1 class="display-title">
            ТГИД-07: единая платформа управления тепловыми сетями
          </h1>
          <p class="lead">
            Профессиональный комплекс ПКФ «Сириус» для теплогидравлического моделирования, ГИС-паспортизации, диспетчеризации, ТОиР и предиктивной аналитики в корпоративной SQL-среде.
          </p>
          <div class="hero-actions">
            <UButton to="/demo" size="xl" color="primary" trailing-icon="i-lucide-arrow-right">
              Запросить демо
            </UButton>
            <UButton to="/product" size="xl" variant="outline" color="neutral">
              Смотреть продукт
            </UButton>
          </div>
          <div class="hero-tags" aria-label="Ключевые характеристики">
            <span class="pill">Расчетные схемы</span>
            <span class="pill">Паспорта объектов</span>
            <span class="pill">Опрессовки и ТОиР</span>
            <span class="pill">SCADA-ready</span>
          </div>
        </div>

        <ProductMapDemo class="hero-demo reveal delay-2" />
      </div>
    </section>

    <section class="section">
      <div class="container">
        <span class="eyebrow">Ключевые возможности</span>
        <h2 class="section-title">Вся инженерная картина в одном продукте</h2>
        <div class="grid grid-4 feature-grid">
          <article v-for="feature in features" :key="feature.title" class="card card-pad accent-card reveal">
            <div class="icon-box">
              <UIcon :name="feature.icon" />
            </div>
            <h3>{{ feature.title }}</h3>
            <p>{{ feature.text }}</p>
          </article>
        </div>
      </div>
    </section>

    <section class="section-tight">
      <div class="container">
        <span class="eyebrow">Результат внедрения</span>
        <h2 class="section-title">Предприятие получает управляемую цифровую модель сети</h2>
        <div class="detail-grid home-outcomes">
          <article v-for="outcome in outcomes" :key="outcome.title" class="detail-card">
            <h3>{{ outcome.title }}</h3>
            <p>{{ outcome.text }}</p>
          </article>
        </div>
      </div>
    </section>

    <section class="section-tight">
      <div class="container">
        <div class="content-band split-panel">
          <div>
            <span class="eyebrow">Единое пространство</span>
            <h2 class="section-title">Данные перестают жить в разных отделах</h2>
            <p class="lead">
              ТГИД-07 связывает расчетчиков, диспетчеров, ПТС, ремонтные службы и развитие сети. В одном контуре видны режимы, карта, договорные нагрузки, технические условия, паспорта и история событий.
            </p>
            <div class="tag-row">
              <span class="pill">Плановые режимы</span>
              <span class="pill">Аварийные сценарии</span>
              <span class="pill">Перспективное развитие</span>
            </div>
          </div>
          <div class="detail-grid">
            <article v-for="space in informationSpace" :key="space.title" class="detail-card">
              <h3>{{ space.title }}</h3>
              <p>{{ space.text }}</p>
            </article>
          </div>
        </div>
      </div>
    </section>

    <section class="section dark-panel">
      <div class="container split">
        <div>
          <span class="eyebrow">Живая визуализация</span>
          <h2 class="section-title">Потоки, режимы и риски видны без перегруза интерфейса</h2>
          <p class="lead">
            Анимации построены на SVG и CSS, работают плавно, отключаются при reduced motion и не требуют тяжелых 3D-библиотек. Эффект есть, а производительность остается рабочей.
          </p>
        </div>
        <div class="flow-card">
          <WaterFlowAnimation mode="horizontal" show-badge label="FLOW_STABLE" />
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <span class="eyebrow">АРМ по ролям</span>
        <h2 class="section-title">Каждая служба работает в своем сценарии, но с одной базой</h2>
        <div class="grid grid-4 feature-grid">
          <article v-for="role in roles" :key="role.title" class="card card-pad accent-card">
            <div class="icon-box">
              <UIcon :name="role.icon" />
            </div>
            <h3>{{ role.title }}</h3>
            <p>{{ role.text }}</p>
          </article>
        </div>
      </div>
    </section>

    <section class="section-tight">
      <div class="container">
        <div class="metric-grid">
          <article v-for="metric in impact" :key="metric.title" class="metric-card">
            <span class="metric-value">{{ metric.value }}</span>
            <strong>{{ metric.title }}</strong>
            <p>{{ metric.text }}</p>
          </article>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="cta card">
          <div>
            <span class="eyebrow">Готовность к запуску</span>
            <h2 class="section-title">Готовы увидеть ТГИД-07 в работе?</h2>
            <p class="lead">Подготовим демонстрацию под вашу структуру сети: режимы, карту, паспорта, дефекты, ремонты и web-доступ для выездных служб.</p>
          </div>
          <UButton to="/demo" size="xl" color="primary" trailing-icon="i-lucide-calendar-check">
            Назначить демо
          </UButton>
        </div>
      </div>
    </section>
    </div>
    <template #append>
      <ProductCapabilities />
    </template>
  </CmsPageRenderer>
</template>

<script setup lang="ts">
import WaterFlowAnimation from '~/components/WaterFlowAnimation.vue'

useSEO({
  title: 'ТГИД-07 — ПКФ «Сириус»',
  description: 'АСУП ТГИД-07: моделирование, ГИС, паспортизация, диспетчеризация, ремонты и эксплуатационная аналитика тепловых сетей от ПКФ «Сириус».'
})
useStructuredData()

const metrics = [
  { label: 'Давление', value: '4.2 МПа' },
  { label: 'Температура', value: '95.4 C' },
  { label: 'Потери', value: '1.8%' },
  { label: 'Дефекты', value: '12' }
]

const features = [
  { icon: 'i-lucide-calculator', title: 'Теплогидравлические расчеты', text: 'Плановые, фактические, летние и аварийные режимы с учетом геодезии, температурных графиков и состояния оборудования.' },
  { icon: 'i-lucide-map', title: 'ГИС и паспорта', text: 'Карта сети, тепловые камеры, трубопроводы, арматура, потребители, документы и история изменений в единой базе.' },
  { icon: 'i-lucide-activity', title: 'Эксплуатация и ИСУПА', text: 'Дефекты, опрессовки, шурфовки, коррозия, заявки, ремонтные контуры и аналитика повреждаемости по участкам.' },
  { icon: 'i-lucide-radio-tower', title: 'Диспетчерский контур', text: 'Сравнение телеметрии с расчетной моделью, поиск отклонений, контроль насосных станций и критичных зон.' }
]

const informationSpace = [
  { title: 'Расчетные схемы', text: 'Плановые, аварийные и перспективные режимы хранятся как управляемые сценарии, а не как разрозненные файлы.' },
  { title: 'Карты и мнемосхемы', text: 'Онлайн-подложки, городские планы и детальные схемы оборудования помогают быстро найти нужный объект.' },
  { title: 'Паспорта и справочники', text: 'Трубопроводы, камеры, арматура, насосы, изоляция, материалы и заводские данные доступны из карточек объектов.' },
  { title: 'Нагрузки и ТУ', text: 'Договорные нагрузки абонентов и технические условия на подключение новых объектов связаны с развитием сети.' }
]

const outcomes = [
  { title: 'Единая достоверная схема', text: 'Расчетная модель, карта, паспорта и события эксплуатации опираются на один набор данных, поэтому решения не расходятся между отделами.' },
  { title: 'Быстрее диагностика режима', text: 'Инженер видит давление, теплопотери, узкие места и последствия переключений до физического вмешательства в сеть.' },
  { title: 'Планирование ремонтов по фактам', text: 'Дефекты, опрессовки, шурфовки и коррозия превращаются в ремонтные контуры, приоритеты и отчетность.' },
  { title: 'Прозрачность для руководства', text: 'Риски, аварийность, эффект регулировки и состояние активов собираются в понятную управленческую картину.' }
]

const roles = [
  { icon: 'i-lucide-gauge', title: 'Служба режимов', text: 'Математическая модель, пьезометрические графики, дросселирующие устройства и анализ отклонений.' },
  { icon: 'i-lucide-building-2', title: 'Перспективное развитие', text: 'Оценка подключений, технические условия, резерв мощности и сценарии роста городской нагрузки.' },
  { icon: 'i-lucide-hard-hat', title: 'Производственная служба', text: 'Инвентаризация, паспортизация камер, магистралей, вводов зданий и оборудования на карте.' },
  { icon: 'i-lucide-wrench', title: 'Ремонтные службы', text: 'Планы ТОиР, дефекты, опрессовки, заявки на устранение аварий и контроль статусов работ.' }
]

const impact = [
  { value: '15-20%', title: 'меньше аварийности', text: 'По оценкам разработчиков, СППР и предиктивная аналитика помогают снизить аварийность за счет раннего выявления зон риска.' },
  { value: '5-20%', title: 'снижение затрат', text: 'Иерархические расчетные технологии поддерживают оптимизацию генерации тепла и перекачки теплоносителя.' },
  { value: '0.1 мм', title: 'точность настройки', text: 'Расчет сопел и дроссельных диафрагм позволяет балансировать сопротивление сети до физической установки устройств.' }
]
</script>

<style scoped>
.hero {
  position: relative;
  padding: 136px 0 80px;
  border-bottom: 1px solid var(--line);
}

.hero-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr);
  gap: 48px;
}

.hero-grid .display-title {
  max-width: 1040px;
  font-size: clamp(2.6rem, 6vw, 5rem);
}

.hero-actions,
.hero-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 34px;
}

.hero-tags {
  margin-top: 24px;
}

.hero-demo {
  min-width: 0;
}

.feature-grid {
  margin-top: 34px;
}

.home-outcomes {
  margin-top: 30px;
}

.feature-grid h3 {
  margin: 22px 0 8px;
  color: var(--ink);
  font-family: var(--serif);
  font-size: 1.4rem;
  font-weight: 400;
  line-height: 1.2;
}

.feature-grid p {
  margin: 0;
  color: var(--muted);
  line-height: 1.65;
}

.split {
  display: grid;
  grid-template-columns: 0.9fr 1.1fr;
  gap: 48px;
  align-items: center;
}

.flow-card {
  height: 360px;
  overflow: hidden;
  border: 1px solid var(--line-dark);
  border-radius: var(--radius);
  background: var(--dark-2);
}

.cta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 40px;
}

@media (max-width: 980px) {
  .split {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 640px) {
  .hero {
    padding: 104px 0 56px;
  }

  .cta {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
