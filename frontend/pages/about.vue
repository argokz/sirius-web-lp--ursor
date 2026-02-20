<template>
  <div>
    <!-- Hero Section -->
    <section class="about-hero py-16">
      <v-container>
        <v-row justify="center">
          <v-col cols="12" md="10" class="text-center">
            <div class="section-badge mb-4">
              <v-chip color="primary" variant="outlined" size="large">
                О компании
              </v-chip>
            </div>
            <h1 class="about-title mb-4">
              ПКФ «Сириус»
            </h1>
            <p class="about-subtitle text-grey-darken-1">
              Ведущий разработчик автоматизированных систем управления для теплоснабжения и промышленности
            </p>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- About Company -->
    <section class="py-16">
      <v-container>
        <v-row>
          <v-col cols="12" md="6" class="scroll-reveal-left">
            <h2 class="section-title mb-6">
              О системе ТГИД-07
            </h2>
            <p class="text-body-1 mb-4">
              <strong>АСУП ТГИД-07 SQL</strong> — это мощная платформа на базе Microsoft SQL Server, 
              объединяющая задачи производственно-технических служб, диспетчерских и инженеров-расчетчиков. 
              Мы предлагаем не просто программу для расчета гидравлики, а полноценный инструмент управления 
              жизненным циклом теплосети: от создания цифровой модели до планирования ремонтных кампаний и анализа аварийности.
            </p>
            <p class="text-body-1 mb-4">
              Программа развития комплекса, охватывающая период 2017–2021 годов, трансформировала графический 
              калькулятор в полноценную систему управления активами предприятия (EAM) и корпоративную информационную среду.
            </p>
            <v-list class="bg-transparent">
              <v-list-item
                v-for="(point, index) in keyPoints"
                :key="index"
                :prepend-icon="'mdi-check-circle'"
                color="success"
              >
                <v-list-item-title>{{ point }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-col>
          <v-col cols="12" md="6" class="scroll-reveal-right">
            <v-card
              elevation="4"
              class="info-card"
              rounded="xl"
            >
              <v-card-text class="pa-8">
                <h3 class="text-h5 mb-4">Почему ТГИД-07 SQL?</h3>
                <v-list class="bg-transparent">
                  <v-list-item class="mb-3">
                    <template v-slot:prepend>
                      <v-icon icon="mdi-arrow-expand" color="primary" />
                    </template>
                    <v-list-item-title class="text-h6">Масштабируемость</v-list-item-title>
                    <v-list-item-subtitle>
                      Работа с крупными сетями мегаполисов с разделением на магистральные и распределительные уровни
                    </v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item class="mb-3">
                    <template v-slot:prepend>
                      <v-icon icon="mdi-ruler" color="primary" />
                    </template>
                    <v-list-item-title class="text-h6">Точность</v-list-item-title>
                    <v-list-item-subtitle>
                      Расчеты на основе реальной геодезии и физических свойств трубопроводов
                    </v-list-item-subtitle>
                  </v-list-item>
                  <v-list-item class="mb-3">
                    <template v-slot:prepend>
                      <v-icon icon="mdi-link-variant" color="primary" />
                    </template>
                    <v-list-item-title class="text-h6">Интеграция</v-list-item-title>
                    <v-list-item-subtitle>
                      Поддержка онлайн-карт (Google, OpenStreetMap) и экспорт данных в Excel/AutoCAD
                    </v-list-item-subtitle>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Scientific Base -->
    <section class="py-16 bg-grey-lighten-5">
      <v-container>
        <v-row>
          <v-col cols="12" class="text-center mb-8 scroll-reveal-scale">
            <div class="section-badge mb-4">
              <v-chip color="info" variant="outlined" size="large">
                Научная база
              </v-chip>
            </div>
            <h2 class="section-title mb-4">
              Научно-методологический базис
            </h2>
            <p class="section-subtitle text-grey-darken-1">
              Эффективность программных продуктов ТГИД обеспечивается их глубокой интеграцией с фундаментальной наукой
            </p>
          </v-col>
        </v-row>
        <v-row>
          <v-col
            v-for="(research, index) in researchAreas"
            :key="index"
            cols="12"
            md="6"
            lg="4"
            class="scroll-reveal"
          >
            <v-card
              elevation="0"
              class="research-card"
              rounded="xl"
            >
              <v-icon :icon="research.icon" size="48" :color="research.color" class="mb-4" />
              <v-card-title class="text-h6 mb-2">
                {{ research.title }}
              </v-card-title>
              <v-card-text>
                {{ research.description }}
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Education -->
    <section class="py-16">
      <v-container>
        <v-row align="center">
          <v-col cols="12" md="6" class="scroll-reveal-left">
            <h2 class="section-title mb-6">
              Методология обучения
            </h2>
            <p class="text-body-1 mb-4">
              Сложность программных продуктов EAM-класса требует высокой квалификации линейного персонала. 
              ПКФ «Сириус» не просто поставляет лицензии, но и выступает провайдером специализированного инженерного образования.
            </p>
            <v-card
              elevation="2"
              class="education-card"
              rounded="xl"
            >
              <v-card-text class="pa-6">
                <div class="text-h5 mb-2">Учебная программа</div>
                <div class="text-h6 mb-4 text-primary">72 академических часа</div>
                <p class="text-body-1">
                  «Оператор информационных технологий ТГИД-05 по разработке эксплуатационных и перспективных 
                  термогидравлических режимов централизованных систем теплоснабжения»
                </p>
                <p class="text-body-2 mt-4 text-grey-darken-1">
                  Программа эквивалентна полноценному курсу повышения квалификации при технических университетах 
                  и построена по принципу последовательного погружения в технологию инжиниринга.
                </p>
              </v-card-text>
            </v-card>
          </v-col>
          <v-col cols="12" md="6" class="scroll-reveal-right">
            <v-card
              elevation="2"
              class="training-card"
              rounded="xl"
            >
              <v-card-text class="pa-6">
                <div class="text-h5 mb-4">Эвристические системы обучения</div>
                <p class="text-body-1 mb-4">
                  Интерактивные тренажеры предназначены для тестирования инженерного состава на способность 
                  оперативно и безошибочно принимать решения в экстремальных и аварийных ситуациях.
                </p>
                <v-list class="bg-transparent">
                  <v-list-item
                    v-for="(item, index) in trainingFeatures"
                    :key="index"
                    :prepend-icon="'mdi-check-circle'"
                    color="success"
                  >
                    <v-list-item-title>{{ item }}</v-list-item-title>
                  </v-list-item>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Partnership -->
    <section class="py-16 bg-grey-lighten-5">
      <v-container>
        <v-row>
          <v-col cols="12" class="text-center mb-8">
            <h2 class="section-title mb-4">Партнерство и сотрудничество</h2>
            <p class="section-subtitle text-grey-darken-1">
              Деятельность ПКФ «Сириус» неразрывно связана с ведущими техническими университетами
            </p>
          </v-col>
        </v-row>
        <v-row>
          <v-col
            v-for="(partner, index) in partners"
            :key="index"
            cols="12"
            md="4"
            class="scroll-reveal"
          >
            <v-card
              elevation="0"
              class="partner-card text-center"
              rounded="xl"
            >
              <v-card-text class="pa-6">
                <v-icon :icon="partner.icon" size="64" :color="partner.color" class="mb-4" />
                <div class="text-h6 mb-2">{{ partner.name }}</div>
                <div class="text-body-2 text-grey-darken-1">{{ partner.description }}</div>
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
  title: 'О компании - Сириус ТГИД-07',
  description: 'ПКФ Сириус - разработчик автоматизированных систем управления для теплоснабжения'
})
useStructuredData()

const keyPoints = [
  'Единое информационное пространство предприятия',
  'Разрушение ведомственных барьеров между подразделениями',
  'Переход к парадигме предиктивного обслуживания',
  'Интеграция с системами SCADA и АСУ ТП',
  'Глубокий научно-методологический базис'
]

const researchAreas = [
  {
    icon: 'mdi-calculator-variant',
    title: 'Математическое моделирование',
    description: 'Математические модели узловых напоров для решения задач потокораспределения в системах мегаполисов',
    color: 'primary'
  },
  {
    icon: 'mdi-cog',
    title: 'Архитектура систем управления',
    description: 'Формирование архитектуры верхнего уровня АСУ ТП с интеграцией расчетных модулей и систем SCADA',
    color: 'secondary'
  },
  {
    icon: 'mdi-lightning-bolt',
    title: 'Энергоэффективность',
    description: 'Исследования по энергосбережению в мегаполисах с достижением снижения затрат на 5-20%',
    color: 'success'
  },
  {
    icon: 'mdi-map',
    title: 'Урбанистика и кадастр',
    description: 'Информационные модели городских территорий для пространственного планирования и градостроительства',
    color: 'info'
  },
  {
    icon: 'mdi-truck',
    title: 'Транспортная логистика',
    description: 'Имитационное моделирование в транспортных системах мегаполисов и оптимизация грузопотоков',
    color: 'warning'
  },
  {
    icon: 'mdi-gavel',
    title: 'Законодательная деятельность',
    description: 'Разработка предложений к концепции Закона РК «О теплоснабжении» и отраслевых стандартов',
    color: 'error'
  }
]

const trainingFeatures = [
  'Тестирование в экстремальных ситуациях',
  'Обучение принятию решений в аварийных условиях',
  'Снижение влияния "человеческого фактора"',
  'Повышение квалификации инженерного состава',
  'Практические навыки работы с системой'
]

const partners = [
  {
    name: 'КарГТУ',
    description: 'Карагандинский государственный технический университет - научный партнер компании',
    icon: 'mdi-school',
    color: 'primary'
  },
  {
    name: 'Государственные гранты',
    description: 'Поддержка исследований государственными грантами по приоритетным направлениям',
    icon: 'mdi-certificate',
    color: 'success'
  },
  {
    name: 'Отраслевые стандарты',
    description: 'Участие в формировании нормативно-правовой базы Республики Казахстан',
    icon: 'mdi-file-document',
    color: 'info'
  }
]

useScrollAnimation()
</script>

<style scoped>
.about-hero {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.about-title {
  font-size: 3.5rem;
  font-weight: 700;
  color: #1a1a1a;
}

.about-subtitle {
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

.info-card {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

.research-card {
  height: 100%;
  padding: 2rem;
  background: white;
  border: 1px solid #e0e0e0;
  transition: all 0.3s ease;
}

.research-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

.education-card,
.training-card {
  height: 100%;
  background: white;
}

.partner-card {
  height: 100%;
  background: white;
  border: 1px solid #e0e0e0;
  transition: all 0.3s ease;
}

.partner-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

@media (max-width: 960px) {
  .about-title {
    font-size: 2.5rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
}
</style>
