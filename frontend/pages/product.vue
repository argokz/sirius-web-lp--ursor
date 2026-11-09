<template>
  <CmsPageRenderer slug="product">
    <PageShell
    eyebrow="Продукт"
    title="ТГИД-07 как единая платформа управления теплосетью"
    description="АСУП ТГИД-07 от ПКФ «Сириус» объединяет расчетную модель, ГИС, паспортизацию, диспетчеризацию, эксплуатацию и аналитику активов в едином корпоративном контуре."
    image="/main-func.webp"
    section-eyebrow="Архитектура"
    section-title="Модули, которые работают вместе"
    :items="items"
    cta-title="Разберем архитектуру под вашу теплосеть"
    cta-text="Покажем, как связать расчетные схемы, карту, паспорта, диспетчерские данные и ремонтные процессы в единую систему."
  >
    <section class="section-tight">
      <div class="container">
        <div class="content-band split-panel">
          <div>
            <span class="eyebrow">Что внутри</span>
            <h2 class="section-title">От графического калькулятора к EAM-системе</h2>
            <p class="lead">
              ТГИД-07 развивает расчетное ядро в полноценную автоматизированную систему управления производством. Платформа хранит состояние активов, связывает подразделения и помогает принимать решения до того, как проблема станет аварией.
            </p>
          </div>
          <div class="module-list">
            <article v-for="layer in platformLayers" :key="layer.title" class="module-row">
              <div class="icon-box">
                <UIcon :name="layer.icon" />
              </div>
              <div>
                <h3>{{ layer.title }}</h3>
                <p>{{ layer.text }}</p>
              </div>
            </article>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <span class="eyebrow">Предиктивная эксплуатация</span>
        <h2 class="section-title">ИСУПА помогает перейти от реакции к предупреждению</h2>
        <div class="process-flow">
          <article v-for="(step, index) in eamFlow" :key="step.title" class="process-step">
            <span>{{ index + 1 }}</span>
            <h3>{{ step.title }}</h3>
            <p>{{ step.text }}</p>
          </article>
        </div>
      </div>
    </section>

    <section class="section-tight">
      <div class="container">
        <div class="metric-grid">
          <article v-for="metric in metrics" :key="metric.title" class="metric-card">
            <span class="metric-value">{{ metric.value }}</span>
            <strong>{{ metric.title }}</strong>
            <p>{{ metric.text }}</p>
          </article>
        </div>
      </div>
    </section>
    </PageShell>
    <template #append>
      <JourneyShowcase />
      <ProductCapabilities />
    </template>
  </CmsPageRenderer>
</template>

<script setup lang="ts">
useSEO({
  title: 'О продукте ТГИД-07 — ПКФ «Сириус»',
  description: 'АСУП ТГИД-07: единая платформа для расчетов, ГИС, паспортизации, диспетчеризации, ремонтов и управления активами теплосетей от ПКФ «Сириус».'
})
useStructuredData()

const items = [
  { icon: 'i-lucide-calculator', title: 'Расчетное ядро', text: 'Плановые, фактические, аварийные и перспективные режимы для крупных магистральных и распределительных сетей.' },
  { icon: 'i-lucide-map', title: 'ГИС-контур', text: 'Координатная карта объектов, онлайн-подложки, поиск по адресам и связанная с геометрией техническая база.' },
  { icon: 'i-lucide-file-check-2', title: 'Паспортизация', text: 'Паспорта трубопроводов, камер, павильонов, арматуры, насосов, компенсаторов, опор, воздушников и дренажей.' },
  { icon: 'i-lucide-radio-tower', title: 'Диспетчеризация', text: 'Сопоставление фактических параметров и расчетной модели, поиск отклонений, анализ скрытых порывов и несанкционированных отборов.' },
  { icon: 'i-lucide-wrench', title: 'Эксплуатация и ремонты', text: 'Дефекты, опрессовки, шурфовки, коррозия, ремонтные контуры, заявки и контроль выполнения работ.' },
  { icon: 'i-lucide-monitor-cog', title: 'Web-доступ и администрирование', text: 'Браузерный доступ к данным, роли пользователей, заявки на демонстрацию, контент и SEO через административный интерфейс.' }
]

const platformLayers = [
  { icon: 'i-lucide-database', title: 'Единая корпоративная SQL-база', text: 'Расчетные схемы, паспорта, договорные нагрузки, технические условия, дефекты и ремонты не расходятся по разным файлам.' },
  { icon: 'i-lucide-network', title: 'АСУП / АСУД для подразделений', text: 'Служба режимов, диспетчерская, ПТС, ремонтные службы и развитие сети работают с одной картиной, но через свои задачи.' },
  { icon: 'i-lucide-satellite-dish', title: 'Интеграции с SCADA и картами', text: 'Система готова к связке с телеметрией, насосными станциями, Google Maps, OpenStreetMap, Visicom, Excel и AutoCAD.' },
  { icon: 'i-lucide-graduation-cap', title: 'Методология внедрения', text: 'Продукт поддержан учебной программой для операторов ТГИД-07 и инженерными сценариями принятия решений.' }
]

const eamFlow = [
  { title: 'Описать активы', text: 'Каждый участок, камера и элемент оборудования получают координаты, параметры, документы и историю.' },
  { title: 'Накопить события', text: 'Дефекты, опрессовки, шурфовки, ремонты и коррозионные данные привязываются к конкретному месту сети.' },
  { title: 'Найти риск', text: 'Аналитика повреждаемости и наработка на отказ выделяют зоны, где ресурс подходит к критическому порогу.' },
  { title: 'Запланировать работу', text: 'Система помогает сформировать ремонтный контур, заявку, сроки, ответственных и отчетность.' }
]

const metrics = [
  { value: 'SQL', title: 'корпоративная база', text: 'Подходит для крупных сетей с разделением на магистральные и распределительные уровни.' },
  { value: 'SCADA', title: 'готовность к телеметрии', text: 'Расчетная модель может сравниваться с фактическими параметрами в режиме оперативного контроля.' },
  { value: 'EAM', title: 'управление активами', text: 'Фокус смещается с устранения аварий на прогнозирование, ресурс и планирование обслуживания.' }
]
</script>
