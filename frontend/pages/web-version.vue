<template>
  <CmsPageRenderer slug="web-version">
    <PageShell
    eyebrow="Web-версия"
    title="Доступ к актуальной схеме теплоснабжения из браузера"
    description="Руководители, мастера участков и выездные бригады получают карту, параметры объектов, поиск, режимы и отчеты без тяжелых локальных установок."
    image="/web_access.webp"
    section-eyebrow="Доступ"
    section-title="Быстро, безопасно, адаптивно"
    :items="items"
    cta-title="Запросите web-демо"
    cta-text="Покажем работу с картой, поиском, карточками объектов, режимами и правами доступа на desktop и мобильном экране."
  >
    <section class="section-tight">
      <div class="container">
        <div class="content-band split-panel">
          <div>
            <span class="eyebrow">Работа в поле</span>
            <h2 class="section-title">Инженер получает данные там, где находится объект</h2>
            <p class="lead">
              Web-версия открывается в Chrome, Safari и других современных браузерах на ПК, планшете или смартфоне. Сотруднику не нужно искать бумажный паспорт или звонить диспетчеру, чтобы уточнить параметры камеры или потребителя.
            </p>
          </div>
          <div class="module-list">
            <article v-for="workflow in workflows" :key="workflow.title" class="module-row">
              <div class="icon-box">
                <UIcon :name="workflow.icon" />
              </div>
              <div>
                <h3>{{ workflow.title }}</h3>
                <p>{{ workflow.text }}</p>
              </div>
            </article>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <span class="eyebrow">Контроль доступа</span>
        <h2 class="section-title">Данные открываются по ролям, а не всем подряд</h2>
        <div class="detail-grid">
          <article v-for="security in securityBlocks" :key="security.title" class="detail-card">
            <h3>{{ security.title }}</h3>
            <p>{{ security.text }}</p>
          </article>
        </div>
      </div>
    </section>
    </PageShell>
    <template #append>
      <ProductCapabilities
        :sections="['10-ai', '08-admin', '09-field-public']"
        eyebrow="Возможности web-версии"
        title="ИИ, интеграции и доступ из браузера"
        description="Помощник ИИ, права и аудит, вебхуки и встраиваемые карты, полевое приложение — всё в браузере без установки."
      />
    </template>
  </CmsPageRenderer>
</template>

<script setup lang="ts">
useSEO({
  title: 'Web-версия ТГИД-07',
  description: 'Web-интерфейс ТГИД-07 для карты теплосети, поиска объектов, просмотра режимов и безопасного доступа из браузера от ПКФ «Сириус».'
})

const items = [
  { icon: 'i-lucide-laptop', title: 'Работа из браузера', text: 'Доступ через Chrome, Safari и другие браузеры без установки тяжелого рабочего места.' },
  { icon: 'i-lucide-tablet-smartphone', title: 'Адаптивность', text: 'Интерфейс сохраняет читаемость и рабочие сценарии на desktop, планшете и мобильном экране.' },
  { icon: 'i-lucide-map-pinned', title: 'Карта и карточки', text: 'Параметры узла, трубы, камеры или потребителя открываются кликом по карте.' },
  { icon: 'i-lucide-search', title: 'Поиск в поле', text: 'Быстрый поиск абонентов, тепловых камер, адресов и объектов сети во время выезда.' },
  { icon: 'i-lucide-chart-line', title: 'Режимы удаленно', text: 'Просмотр пьезометрических графиков, текущих режимов и расчетных результатов без доступа к desktop-клиенту.' },
  { icon: 'i-lucide-lock-keyhole', title: 'Права и SSL', text: 'Разграничение чтения и записи, защищенный обмен данными и администрирование пользователей.' }
]

const workflows = [
  { icon: 'i-lucide-navigation', title: 'Найти объект', text: 'По адресу, инвентарному номеру, названию камеры, абоненту или участку сети.' },
  { icon: 'i-lucide-mouse-pointer-click', title: 'Открыть параметры', text: 'Получить характеристики трубы, камеры, потребителя, оборудования и связанные документы.' },
  { icon: 'i-lucide-chart-spline', title: 'Проверить режим', text: 'Посмотреть расчетные параметры и пьезометрические графики перед принятием решения.' },
  { icon: 'i-lucide-send', title: 'Передать действие', text: 'Сформировать обращение, уточнение или задачу для эксплуатационной команды.' }
]

const securityBlocks = [
  { title: 'Роли пользователей', text: 'Руководитель, диспетчер, инженер, мастер участка и подрядчик могут видеть разные наборы данных.' },
  { title: 'Чтение и запись', text: 'Для полевых сотрудников можно оставить просмотр, а внесение изменений разрешить только ответственным ролям.' },
  { title: 'Защищенное подключение', text: 'SSL-шифрование и серверная авторизация снижают риск доступа к производственным данным вне контура предприятия.' },
  { title: 'Администрирование сайта', text: 'Пользователи, заявки, контент и SEO управляются из отдельной административной зоны.' }
]
</script>
