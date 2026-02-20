<template>
  <div>
    <!-- Hero Section -->
    <section class="features-hero py-16">
      <v-container>
        <v-row justify="center">
          <v-col cols="12" md="10" class="text-center">
            <div class="section-badge mb-4">
              <v-chip color="primary" variant="outlined" size="large">
                Функционал
              </v-chip>
            </div>
            <h1 class="features-title mb-4">
              Возможности системы ТГИД-07
            </h1>
            <p class="features-subtitle text-grey-darken-1">
              Полный функционал для эффективного управления теплоснабжением
            </p>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Features Grid -->
    <section class="py-16">
      <v-container>
        <v-row>
          <v-col
            cols="12"
            md="6"
            v-for="(feature, index) in features"
            :key="index"
            class="mb-4 scroll-reveal"
          >
            <v-card
              elevation="0"
              class="feature-card-detailed"
              :class="`feature-detailed-${index + 1}`"
              rounded="xl"
            >
              <div class="feature-header">
                <div class="feature-icon-detailed">
                  <v-icon :icon="feature.icon" size="40" />
                </div>
                <v-card-title class="feature-title-detailed">
                  {{ feature.title }}
                </v-card-title>
              </div>
              <v-card-text class="feature-text-detailed">
                <p class="mb-4">{{ feature.description }}</p>
                <div class="feature-tags">
                  <v-chip
                    v-for="(tag, idx) in feature.tags"
                    :key="idx"
                    size="small"
                    class="mr-2 mb-2"
                    :color="getTagColor(idx)"
                    variant="flat"
                  >
                    {{ tag }}
                  </v-chip>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Additional Info -->
    <section class="py-16 bg-grey-lighten-5">
      <v-container>
        <v-row>
          <v-col cols="12" class="text-center mb-8">
            <h2 class="section-title mb-4">Дополнительные возможности</h2>
            <p class="section-subtitle text-grey-darken-1">
              Расширенный функционал для профессиональной работы
            </p>
          </v-col>
        </v-row>
        <v-row>
          <v-col
            v-for="(item, index) in additionalFeatures"
            :key="index"
            cols="12"
            md="4"
            class="scroll-reveal"
          >
            <v-card
              elevation="0"
              class="additional-feature-card"
              rounded="xl"
            >
              <v-icon :icon="item.icon" size="48" :color="item.color" class="mb-4" />
              <v-card-title class="text-h6 mb-2">
                {{ item.title }}
              </v-card-title>
              <v-card-text>
                {{ item.description }}
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>
  </div>
</template>

<script setup lang="ts">
useSEO({
  title: 'Возможности - ТГИД-07',
  description: 'Возможности системы ТГИД-07 для управления теплоснабжением'
})
useStructuredData()

const features = [
  {
    icon: 'mdi-calculator',
    title: 'Плановые и фактические режимы',
    description: 'Моделирование установившихся режимов с расчетом дросселирующих устройств или анализом текущего состояния сети. Система поддерживает работу с плановыми режимами для наладки и расчета нагрузок, фактическими режимами для анализа текущего состояния и летними режимами для работы в межотопительный период.',
    tags: ['Расчет', 'Моделирование', 'Анализ', 'Режимы']
  },
  {
    icon: 'mdi-thermometer-lines',
    title: 'Расчет тепловых потерь',
    description: 'Автоматическое определение нормативных потерь через теплопередачу и утечки сетевой воды. Система автоматически рассчитывает потери на основе нормативных данных и предоставляет детальную аналитику по каждому участку сети.',
    tags: ['Автоматизация', 'Нормативы', 'Потери', 'Аналитика']
  },
  {
    icon: 'mdi-chart-line',
    title: 'Пьезометрические графики',
    description: 'Визуализация и анализ давлений в заданных направлениях для контроля надежности системы. Графики позволяют быстро выявить проблемные участки и спланировать необходимые мероприятия.',
    tags: ['Визуализация', 'Давление', 'Графики', 'Контроль']
  },
  {
    icon: 'mdi-alert-circle',
    title: 'Жизненный цикл нарушений',
    description: 'Сквозной мониторинг дефектов: от фиксации повреждения до завершения ремонта и ввода в эксплуатацию. Система отслеживает все этапы работы с нарушениями и обеспечивает полную прозрачность процесса.',
    tags: ['Мониторинг', 'Дефекты', 'Ремонт', 'Учет']
  },
  {
    icon: 'mdi-file-document',
    title: 'Паспортизация объектов (ПТС)',
    description: 'Ведение электронных паспортов для магистральных и распределительных сетей с детализацией оборудования. Система обеспечивает полный учет всех объектов теплоснабжения с привязкой к картам и расчетным схемам.',
    tags: ['Документация', 'ПТС', 'Учет', 'Паспорта']
  },
  {
    icon: 'mdi-shield-alert',
    title: 'Контроль коррозии и износа',
    description: 'Учет показателей коррозии и планирование ремонтов на основе данных об износе оборудования. Система помогает прогнозировать необходимость ремонтных работ и оптимизировать затраты на обслуживание.',
    tags: ['Коррозия', 'Износ', 'Планирование', 'Прогнозирование']
  },
  {
    icon: 'mdi-transmission-tower',
    title: 'Управление инфраструктурой',
    description: 'Отдельный модуль для учета объектов электросети (ЛЭП, трансформаторы, электрооборудование). Обеспечивает комплексный учет всей инфраструктуры, связанной с теплоснабжением.',
    tags: ['Инфраструктура', 'Электросеть', 'Учет', 'Комплексность']
  },
  {
    icon: 'mdi-map',
    title: 'ГИС-интеграция',
    description: 'Привязка расчетных схем к картам местности (Google, OSM, ZGNC) и графические наложения. Система поддерживает работу с различными картографическими сервисами и обеспечивает визуализацию данных на карте.',
    tags: ['ГИС', 'Карты', 'Интеграция', 'Визуализация']
  },
  {
    icon: 'mdi-web',
    title: 'Web-приложение',
    description: 'Удаленный доступ с любого устройства для просмотра структуры сети и результатов расчетов. Современный веб-интерфейс обеспечивает удобную работу как на десктопе, так и на мобильных устройствах.',
    tags: ['Web', 'Доступ', 'Мобильность', 'Удобство']
  }
]

const additionalFeatures = [
  {
    icon: 'mdi-database',
    title: 'Надежное хранение данных',
    description: 'SQL-сервер обеспечивает надежное хранение и быстрый доступ к данным',
    color: 'primary'
  },
  {
    icon: 'mdi-security',
    title: 'Безопасность',
    description: 'Многоуровневая система защиты данных и разграничение доступа',
    color: 'success'
  },
  {
    icon: 'mdi-update',
    title: 'Регулярные обновления',
    description: 'Постоянное развитие системы с добавлением новых функций',
    color: 'info'
  }
]

const getTagColor = (index: number) => {
  const colors = ['primary', 'secondary', 'success', 'info', 'warning', 'error']
  return colors[index % colors.length]
}

const { observeElements } = useScrollAnimation()

onMounted(() => {
  observeElements()
})
</script>

<style scoped>
.features-hero {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.features-title {
  font-size: 3rem;
  font-weight: 700;
  color: #1a1a1a;
}

.features-subtitle {
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

.feature-card-detailed {
  height: 100%;
  padding: 2rem;
  background: white;
  border: 2px solid #e0e0e0;
  transition: all 0.3s ease;
}

.feature-card-detailed:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
  border-color: transparent;
}

.feature-header {
  display: flex;
  align-items: center;
  margin-bottom: 1.5rem;
}

.feature-icon-detailed {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  border-radius: 12px;
  margin-right: 1rem;
  flex-shrink: 0;
}

.feature-detailed-1 .feature-icon-detailed {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.feature-detailed-2 .feature-icon-detailed {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.feature-detailed-3 .feature-icon-detailed {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
}

.feature-detailed-4 .feature-icon-detailed {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  color: white;
}

.feature-detailed-5 .feature-icon-detailed {
  background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
  color: white;
}

.feature-detailed-6 .feature-icon-detailed {
  background: linear-gradient(135deg, #30cfd0 0%, #330867 100%);
  color: white;
}

.feature-detailed-7 .feature-icon-detailed {
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  color: #1a1a1a;
}

.feature-detailed-8 .feature-icon-detailed {
  background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
  color: #1a1a1a;
}

.feature-detailed-9 .feature-icon-detailed {
  background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
  color: #1a1a1a;
}

.feature-title-detailed {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1a1a1a;
  padding: 0;
}

.feature-text-detailed {
  color: #666;
  line-height: 1.6;
  padding: 0;
}

.feature-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.additional-feature-card {
  height: 100%;
  padding: 2rem;
  text-align: center;
  background: white;
  border: 1px solid #e0e0e0;
  transition: all 0.3s ease;
}

.additional-feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

@media (max-width: 960px) {
  .features-title {
    font-size: 2.5rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .feature-header {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .feature-icon-detailed {
    margin-bottom: 1rem;
    margin-right: 0;
  }
}
</style>
