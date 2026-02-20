<template>
  <div>
    <!-- Hero Section -->
    <section class="product-hero py-16">
      <v-container>
        <v-row justify="center">
          <v-col cols="12" md="10" class="text-center">
            <div class="section-badge mb-4">
              <v-chip color="primary" variant="outlined" size="large">
                О продукте
              </v-chip>
            </div>
            <h1 class="product-title mb-4">
              ТГИД-07 SQL
            </h1>
            <p class="product-subtitle text-grey-darken-1">
              Комплексная автоматизированная система для цифрового моделирования, 
              пространственно-технологического анализа и управления режимами теплоснабжения. 
              Объединяет функции расчета, инвентаризации оборудования (ПТС), 
              мониторинга технического состояния и учета связанной инфраструктуры (электросети)
            </p>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Main Features -->
    <section class="py-16 bg-grey-lighten-5">
      <v-container>
        <v-row>
          <v-col cols="12" class="text-center mb-8">
            <h2 class="section-title mb-4">Основные возможности</h2>
            <p class="section-subtitle text-grey-darken-1">
              Все необходимые инструменты для эффективного управления теплоснабжением
            </p>
          </v-col>
        </v-row>
        <v-row>
          <v-col
            v-for="(feature, index) in productFeatures"
            :key="index"
            cols="12"
            md="6"
            class="scroll-reveal"
          >
            <v-card
              elevation="0"
              class="feature-card-modern"
              :class="`feature-modern-${index + 1}`"
            >
              <div class="feature-modern-icon">
                <v-icon :icon="feature.icon" size="40" />
              </div>
              <v-card-title class="text-h5 mb-2">
                {{ feature.title }}
              </v-card-title>
              <v-card-text class="text-body-1">
                {{ feature.description }}
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Modules Section -->
    <section class="py-16">
      <v-container>
        <v-row>
          <v-col cols="12" class="text-center mb-8">
            <h2 class="section-title mb-4">Основные модули системы</h2>
            <p class="section-subtitle text-grey-darken-1">
              Детальное описание функционала каждого модуля
            </p>
          </v-col>
        </v-row>
        <v-row>
          <v-col
            v-for="(module, index) in modules"
            :key="index"
            cols="12"
            class="mb-4 scroll-reveal"
          >
            <v-card
              elevation="2"
              class="module-card"
              rounded="xl"
            >
              <v-card-title class="module-title">
                <v-icon :icon="module.icon" color="primary" class="mr-3" size="32" />
                {{ module.title }}
              </v-card-title>
              <v-card-text>
                <p class="text-body-1 mb-4">{{ module.description }}</p>
                <v-row>
                  <v-col
                    v-for="(item, idx) in module.items"
                    :key="idx"
                    cols="12"
                    md="6"
                  >
                    <div class="module-item">
                      <v-icon icon="mdi-check-circle" color="success" size="20" class="mr-2" />
                      <span>{{ item }}</span>
                    </div>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Technical Details -->
    <section class="py-16 bg-grey-lighten-5">
      <v-container>
        <v-row>
          <v-col cols="12" md="6" class="scroll-reveal">
            <h2 class="section-title mb-6">Технические характеристики</h2>
            <v-list class="bg-transparent">
              <v-list-item
                v-for="(spec, index) in specifications"
                :key="index"
                class="spec-item"
              >
                <template v-slot:prepend>
                  <v-avatar color="primary" size="32" class="mr-4">
                    <v-icon :icon="spec.icon" color="white" size="20" />
                  </v-avatar>
                </template>
                <v-list-item-title class="text-h6">
                  {{ spec.title }}
                </v-list-item-title>
                <v-list-item-subtitle>
                  {{ spec.description }}
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-col>
          <v-col cols="12" md="6" class="scroll-reveal">
            <h2 class="section-title mb-6">Преимущества использования</h2>
            <v-timeline side="end" align="start" density="compact">
              <v-timeline-item
                v-for="(advantage, index) in advantages"
                :key="index"
                :dot-color="advantage.color"
                size="small"
              >
                <div class="advantage-content">
                  <div class="text-h6 mb-1">{{ advantage.title }}</div>
                  <div class="text-body-2 text-grey-darken-1">
                    {{ advantage.description }}
                  </div>
                </div>
              </v-timeline-item>
            </v-timeline>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- CTA Section -->
    <section class="py-16">
      <v-container>
        <v-card
          elevation="8"
          class="cta-card-modern"
          rounded="xl"
        >
          <v-card-text class="text-center pa-12">
            <h2 class="text-h3 mb-4">
              Готовы внедрить ТГИД-07?
            </h2>
            <p class="text-h6 text-grey-darken-1 mb-8">
              Получите демо-версию и консультацию наших специалистов
            </p>
            <v-btn
              size="x-large"
              color="primary"
              variant="elevated"
              to="/demo"
              rounded="xl"
              class="mr-4 mb-2"
            >
              <v-icon start icon="mdi-rocket-launch" />
              Запросить демо
            </v-btn>
            <v-btn
              size="x-large"
              color="primary"
              variant="outlined"
              to="/contacts"
              rounded="xl"
            >
              <v-icon start icon="mdi-phone" />
              Связаться с нами
            </v-btn>
          </v-card-text>
        </v-card>
      </v-container>
    </section>
  </div>
</template>

<script setup lang="ts">
useSEO({
  title: 'Продукт ТГИД-07 - Сириус',
  description: 'ТГИД-07 - автоматизированная система управления теплоснабжением с полным функционалом расчета, мониторинга и анализа'
})
useStructuredData()

const productFeatures = [
  {
    icon: 'mdi-calculator-variant',
    title: 'Расчет режимов работы',
    description: 'Моделирование установившихся режимов работы системы теплоснабжения с расчетом дросселирующих устройств или анализом текущего состояния сети. Система поддерживает плановые режимы для наладки и расчета нагрузок, фактические режимы для анализа текущего состояния и летние режимы для работы в межотопительный период. Автоматический расчет гидравлических параметров, давлений и расходов на всех участках сети.'
  },
  {
    icon: 'mdi-thermometer-lines',
    title: 'Контроль потерь',
    description: 'Автоматическое определение нормативных потерь через теплопередачу и утечки сетевой воды. Система рассчитывает тепловые потери на каждом участке сети, учитывая характеристики изоляции, температуру окружающей среды и режим работы. Визуализация результатов в виде графиков и отчетов, позволяющая выявить проблемные участки и оптимизировать энергопотребление.'
  },
  {
    icon: 'mdi-map-marker-radius',
    title: 'ГИС-интеграция',
    description: 'Привязка расчетных схем к картам местности (Google Maps, OpenStreetMap, ZGNC) с графическими наложениями и пространственным анализом'
  },
  {
    icon: 'mdi-web',
    title: 'Web-доступ',
    description: 'Удаленный доступ с любого устройства через современный веб-интерфейс для просмотра структуры сети и результатов расчетов'
  },
  {
    icon: 'mdi-file-document-multiple',
    title: 'Паспортизация объектов',
    description: 'Ведение электронных паспортов для магистральных и распределительных сетей с детализацией оборудования (ПТС)'
  },
  {
    icon: 'mdi-chart-timeline-variant',
    title: 'Аналитика и отчетность',
    description: 'Визуализация данных, пьезометрические графики, анализ тепловых потерь и жизненный цикл нарушений'
  }
]

const modules = [
  {
    icon: 'mdi-calculator',
    title: 'Моделирование и расчет режимов',
    description: 'Моделирование установившихся режимов с расчетом дросселирующих устройств или анализом текущего состояния сети. Система позволяет работать с различными сценариями работы теплоснабжения, включая расчет оптимальных параметров работы насосов и регулирующих устройств.',
    items: [
      'Плановые режимы для наладки и расчета нагрузок',
      'Фактические режимы для анализа текущего состояния',
      'Летние режимы для работы в межотопительный период',
      'Расчет дросселирующих устройств и регулирующих клапанов',
      'Анализ гидравлических режимов и балансировка сети',
      'Оптимизация работы насосных станций',
      'Расчет параметров подпитки системы'
    ]
  },
  {
    icon: 'mdi-monitor-dashboard',
    title: 'Эксплуатация и мониторинг',
    description: 'Комплексный мониторинг и управление системой теплоснабжения с автоматическим контролем параметров и выявлением нарушений. Система обеспечивает непрерывный контроль работы всех элементов сети с формированием оперативных и аналитических отчетов.',
    items: [
      'Расчет тепловых потерь через теплопередачу и утечки',
      'Пьезометрические графики для контроля давления в заданных направлениях',
      'Жизненный цикл нарушений: от фиксации повреждения до завершения ремонта',
      'Паспортизация объектов (ПТС) с детализацией оборудования',
      'Контроль коррозии и износа оборудования с прогнозированием сроков службы',
      'Планирование ремонтов на основе данных об износе и техническом состоянии',
      'Мониторинг температуры теплоносителя на всех участках сети',
      'Учет и контроль расхода сетевой воды'
    ]
  },
  {
    icon: 'mdi-transmission-tower',
    title: 'Управление инфраструктурой',
    description: 'Отдельный модуль для учета объектов электросети и связанной инфраструктуры, обеспечивающий комплексный учет всех систем. Позволяет вести единую базу данных по всей инфраструктуре теплоснабжения и энергоснабжения.',
    items: [
      'Учет объектов электросети (ЛЭП, трансформаторы, распределительные устройства)',
      'Учет электрооборудования насосных станций и котельных',
      'Связь с тепловыми сетями и привязка к картам',
      'Комплексный анализ инфраструктуры с визуализацией на карте',
      'Учет резервного и аварийного оборудования',
      'Планирование работ по обслуживанию электрооборудования'
    ]
  },
  {
    icon: 'mdi-earth',
    title: 'Цифровая среда и доступ',
    description: 'Современные технологии для удобного доступа к системе с поддержкой различных платформ и устройств. Обеспечивает работу с системой из любой точки мира через веб-интерфейс.',
    items: [
      'ГИС-интеграция с картографическими сервисами (Google Maps, OpenStreetMap, ZGNC)',
      'Web-приложение для удаленного доступа с любого устройства',
      'Мобильная адаптация интерфейса для работы на планшетах и смартфонах',
      'Кроссплатформенная совместимость (Windows, Linux, macOS)',
      'Привязка расчетных схем к картам местности с графическими наложениями',
      'Визуализация структуры сети и результатов расчетов на карте',
      'Экспорт данных в различные форматы (PDF, Excel, изображения)'
    ]
  }
]

const specifications = [
  {
    icon: 'mdi-database',
    title: 'База данных',
    description: 'SQL-сервер для надежного хранения данных'
  },
  {
    icon: 'mdi-cloud',
    title: 'Облачный доступ',
    description: 'Web-интерфейс для работы из любой точки мира'
  },
  {
    icon: 'mdi-map',
    title: 'Картографические сервисы',
    description: 'Интеграция с Google Maps, OSM, ZGNC'
  },
  {
    icon: 'mdi-security',
    title: 'Безопасность',
    description: 'Многоуровневая система защиты данных'
  },
  {
    icon: 'mdi-update',
    title: 'Обновления',
    description: 'Регулярные обновления и техническая поддержка'
  }
]

const advantages = [
  {
    title: 'Экономия времени',
    description: 'Автоматизация расчетов и мониторинга значительно сокращает время на обработку данных',
    color: 'primary'
  },
  {
    title: 'Точность расчетов',
    description: 'Использование современных алгоритмов обеспечивает высокую точность расчетов режимов',
    color: 'success'
  },
  {
    title: 'Удобство использования',
    description: 'Интуитивно понятный интерфейс и доступ с любого устройства',
    color: 'info'
  },
  {
    title: 'Масштабируемость',
    description: 'Система легко масштабируется под любые объемы данных и количество пользователей',
    color: 'secondary'
  }
]

const { observeElements } = useScrollAnimation()

onMounted(() => {
  observeElements()
})
</script>

<style scoped>
.product-hero {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.product-title {
  font-size: 3.5rem;
  font-weight: 700;
  color: #1a1a1a;
}

.product-subtitle {
  font-size: 1.25rem;
  line-height: 1.6;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1a1a1a;
}

.section-subtitle {
  font-size: 1.25rem;
}

.feature-card-modern {
  height: 100%;
  padding: 2rem;
  border-radius: 16px;
  transition: all 0.3s ease;
  background: white;
  border: 2px solid transparent;
}

.feature-card-modern:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
  border-color: #6A1B9A;
}

.feature-modern-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  border-radius: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  margin-bottom: 1.5rem;
}

.feature-modern-1 .feature-modern-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.feature-modern-2 .feature-modern-icon {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.feature-modern-3 .feature-modern-icon {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.feature-modern-4 .feature-modern-icon {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

.feature-modern-5 .feature-modern-icon {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
}

.feature-modern-6 .feature-modern-icon {
  background: linear-gradient(135deg, #30cfd0 0%, #330867 100%);
}

.module-card {
  transition: all 0.3s ease;
}

.module-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15) !important;
}

.module-title {
  font-size: 1.75rem;
  font-weight: 600;
  color: #1a1a1a;
}

.module-item {
  display: flex;
  align-items: center;
  padding: 0.5rem 0;
  font-size: 1rem;
}

.spec-item {
  margin-bottom: 1rem;
  padding: 1rem;
  border-radius: 12px;
  background: white;
  transition: all 0.3s ease;
}

.spec-item:hover {
  background: #f8f9fa;
  transform: translateX(8px);
}

.advantage-content {
  padding-left: 1rem;
}

.cta-card-modern {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  border: none;
}

@media (max-width: 960px) {
  .product-title {
    font-size: 2.5rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
}
</style>
