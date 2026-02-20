<template>
  <div>
    <!-- Hero Section -->
    <section class="solutions-hero py-16">
      <v-container>
        <v-row justify="center">
          <v-col cols="12" md="10" class="text-center">
            <div class="section-badge mb-4">
              <v-chip color="primary" variant="outlined" size="large">
                Решения
              </v-chip>
            </div>
            <h1 class="solutions-title mb-4">
              Автоматизированные рабочие места (АРМ)
            </h1>
            <p class="solutions-subtitle text-grey-darken-1">
              Система структурно разделена на АРМ для конкретных департаментов, 
              обеспечивая эффективную работу каждого подразделения
            </p>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- ARM Solutions -->
    <section class="py-16">
      <v-container>
        <v-row>
          <v-col
            v-for="(arm, index) in armSolutions"
            :key="index"
            cols="12"
            md="6"
            class="mb-4 scroll-reveal"
          >
            <v-card
              elevation="2"
              class="arm-card"
              rounded="xl"
            >
              <v-card-title class="arm-title">
                <v-icon :icon="arm.icon" color="primary" class="mr-3" size="32" />
                {{ arm.title }}
              </v-card-title>
              <v-card-text>
                <p class="text-body-1 mb-4">{{ arm.description }}</p>
                <v-list class="bg-transparent">
                  <v-list-item
                    v-for="(feature, idx) in arm.features"
                    :key="idx"
                    :prepend-icon="'mdi-check-circle'"
                    color="success"
                  >
                    <v-list-item-title>{{ feature }}</v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- EAM System -->
    <section class="py-16 bg-grey-lighten-5">
      <v-container>
        <v-row>
          <v-col cols="12" class="text-center mb-8 scroll-reveal-scale">
            <div class="section-badge mb-4">
              <v-chip color="secondary" variant="outlined" size="large">
                ИСУПА
              </v-chip>
            </div>
            <h2 class="section-title mb-4">
              Информационная система управления производственными активами
            </h2>
            <p class="section-subtitle text-grey-darken-1">
              Переход от реактивного устранения аварий к предиктивному (предупредительному) обслуживанию
            </p>
          </v-col>
        </v-row>
        <v-row>
          <v-col
            v-for="(module, index) in eamModules"
            :key="index"
            cols="12"
            md="4"
            class="scroll-reveal"
          >
            <v-card
              elevation="0"
              class="eam-module-card"
              rounded="xl"
            >
              <div class="eam-icon-wrapper">
                <v-icon :icon="module.icon" size="48" :color="module.color" />
              </div>
              <v-card-title class="text-h6 mb-2">
                {{ module.title }}
              </v-card-title>
              <v-card-text>
                {{ module.description }}
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Economic Value -->
    <section class="py-16">
      <v-container>
        <v-row align="center">
          <v-col cols="12" md="6" class="scroll-reveal-left">
            <h2 class="section-title mb-6">
              Экономическая ценность внедрения
            </h2>
            <v-list class="bg-transparent">
              <v-list-item
                v-for="(benefit, index) in economicBenefits"
                :key="index"
                class="mb-4"
              >
                <template v-slot:prepend>
                  <v-avatar color="success" size="40" class="mr-4">
                    <v-icon :icon="benefit.icon" color="white" />
                  </v-avatar>
                </template>
                <v-list-item-title class="text-h6 mb-1">
                  {{ benefit.title }}
                </v-list-item-title>
                <v-list-item-subtitle>
                  {{ benefit.description }}
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-col>
          <v-col cols="12" md="6" class="scroll-reveal-right">
            <v-card
              elevation="8"
              class="stats-card"
              rounded="xl"
            >
              <v-card-text class="pa-8">
                <div class="text-center">
                  <div class="stat-number mb-2">15-20%</div>
                  <div class="text-h6 mb-6">Снижение аварийности</div>
                  <div class="stat-number mb-2">5-20%</div>
                  <div class="text-h6 mb-6">Экономия затрат на генерацию</div>
                  <div class="stat-number mb-2">20%</div>
                  <div class="text-h6">Экономия электроэнергии на насосных станциях</div>
                </div>
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
  title: 'Решения - ТГИД-07',
  description: 'Автоматизированные рабочие места и решения для управления теплоснабжением'
})
useStructuredData()

const armSolutions = [
  {
    icon: 'mdi-calculator',
    title: 'АРМ "Служба режимов"',
    description: 'Математическое моделирование и расчет термогидравлических режимов для наладки системы теплоснабжения',
    features: [
      'Расчет плановых режимов для наладки',
      'Анализ фактических режимов',
      'Расчет летних режимов и ГВС',
      'Построение пьезометрических графиков',
      'Расчет дросселирующих устройств'
    ]
  },
  {
    icon: 'mdi-chart-timeline',
    title: 'АРМ "Перспективного развития"',
    description: 'Модуль "Технические условия" для координации выдачи мощностей застройщикам и планирования развития сети',
    features: [
      'Выдача технических условий',
      'Координация присоединений',
      'Планирование развития сети',
      'Анализ перспективных нагрузок'
    ]
  },
  {
    icon: 'mdi-file-document',
    title: 'АРМ "Производственная служба"',
    description: 'Модуль "Инвентаризация и паспортизация" для ведения цифрового реестра тепловых сетей',
    features: [
      'Ведение реестра тепловых камер',
      'Учет магистралей и вводов',
      'Паспортизация оборудования',
      'Инвентаризация объектов'
    ]
  },
  {
    icon: 'mdi-tools',
    title: 'АРМ "Диспетчер"',
    description: 'Автоматизированное рабочее место для служб эксплуатации с полной историей жизни теплосети',
    features: [
      'Учет нарушений и дефектов',
      'Планирование ремонтов',
      'Гидравлические испытания',
      'Мониторинг коррозии'
    ]
  }
]

const eamModules = [
  {
    icon: 'mdi-map-marker',
    title: 'Учет оборудования',
    description: 'Геопозиционирование активов, привязка технической документации к каждому инвентарному объекту на карте',
    color: 'primary'
  },
  {
    icon: 'mdi-alert-circle',
    title: 'Управление дефектами',
    description: 'Журналирование дефектов с точной привязкой к участкам трубопровода, формирование заявок на устранение аварий',
    color: 'error'
  },
  {
    icon: 'mdi-calendar-clock',
    title: 'Планирование эксплуатации',
    description: 'Модули "Опрессовки", "Шурфовки" и мониторинг "Коррозии" с автоматическим сигнализированием о необходимости замены',
    color: 'warning'
  },
  {
    icon: 'mdi-chart-bar',
    title: 'Аналитика',
    description: 'Графическая визуализация зон риска, статистическая обработка повреждаемости тепловых сетей',
    color: 'info'
  },
  {
    icon: 'mdi-shield-check',
    title: 'Предиктивное обслуживание',
    description: 'Оценка скорости коррозионного износа на основе статистики отказов и результатов шурфовок',
    color: 'success'
  },
  {
    icon: 'mdi-cog',
    title: 'Планирование ресурсов',
    description: 'Оптимизация бюджета на капитальный ремонт и продление жизненного цикла критически важных активов',
    color: 'secondary'
  }
]

const economicBenefits = [
  {
    icon: 'mdi-chart-line',
    title: 'Балансировка сети',
    description: 'Виртуальная балансировка сети с расчетом точных диаметров дроссельных диафрагм устраняет "перетопы" и "недогревы"'
  },
  {
    icon: 'mdi-shield-alert',
    title: 'Снижение аварийности',
    description: 'Применение систем поддержки принятия решений обеспечивает прозрачность функционирования сети и снижает аварийность на 15-20%'
  },
  {
    icon: 'mdi-lightning-bolt',
    title: 'Энергосбережение',
    description: 'Снижение затрат на генерацию тепла и перекачку теплоносителя на 5-20%, экономия до 20% электрической энергии на насосных станциях'
  },
  {
    icon: 'mdi-eye',
    title: 'Выявление скрытых проблем',
    description: 'Идентификация скрытых порывов труб или несанкционированного отбора горячей воды через анализ отклонений'
  }
]

useScrollAnimation()
</script>

<style scoped>
.solutions-hero {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.solutions-title {
  font-size: 3rem;
  font-weight: 700;
  color: #1a1a1a;
}

.solutions-subtitle {
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

.arm-card {
  height: 100%;
  transition: all 0.3s ease;
}

.arm-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15) !important;
}

.arm-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1a1a1a;
}

.eam-module-card {
  height: 100%;
  padding: 2rem;
  background: white;
  border: 1px solid #e0e0e0;
  transition: all 0.3s ease;
}

.eam-module-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.eam-icon-wrapper {
  margin-bottom: 1.5rem;
}

.stats-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.stat-number {
  font-size: 3rem;
  font-weight: 700;
  color: white;
}

@media (max-width: 960px) {
  .solutions-title {
    font-size: 2.5rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .stat-number {
    font-size: 2.5rem;
  }
}
</style>
