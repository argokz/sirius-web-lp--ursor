<template>
  <div class="homepage-wrapper">
    <!-- Full-page vertical pipe ornamental line -->
    <div class="global-vertical-pipe">
       <WaterFlowAnimation mode="vertical" />
    </div>
    <div class="global-vertical-pipe-2">
       <WaterFlowAnimation mode="vertical" />
    </div>
    <!-- Modern Hero Section -->
    <section class="hero-section">
      <!-- Premium Mesh Background -->
      <div class="mesh-background">
        <div class="mesh-blob mesh-blob-1"></div>
        <div class="mesh-blob mesh-blob-2"></div>
        <div class="mesh-blob mesh-blob-3"></div>
        <div class="mesh-blob mesh-blob-4"></div>
      </div>

      <!-- Vertical Pipe Animation Background (Subtle) -->
      <div class="vertical-pipe-container">
        <WaterFlowAnimation mode="vertical" />
      </div>

      <v-container class="hero-content">
        <v-row justify="center" align="center" class="min-height-screen">
          <v-col cols="12" md="10" lg="8" class="text-center relative-box">
            <div class="hero-badge-premium mb-6 fade-in-up">
              <span class="glass-pill">
                <v-icon start icon="mdi-shield-check" class="pulse-primary" />
                {{ contentMap.hero_badge || 'Инновационная система управления ТГИД-07' }}
              </span>
            </div>
            
            <h1 class="hero-title-premium fade-in-up">
              Будущее <span class="text-gradient">тепловой</span> энергетики
            </h1>
            
            <p class="hero-subtitle-premium fade-in-up delay-1">
              {{ contentMap.hero_subtitle || 'Единая цифровая экосистема для моделирования, паспортизации и оперативного управления городскими тепловыми сетями. Мощь SQL и точность инженерных расчетов.' }}
            </p>

            <div class="hero-actions-premium mt-10 fade-in-up delay-2">
              <v-btn
                size="x-large"
                class="btn-premium primary-btn mr-md-6 mb-4"
                to="/demo"
                rounded="pill"
              >
                <span>Начать внедрение</span>
                <v-icon end icon="mdi-chevron-right" class="btn-arrow" />
              </v-btn>
              
              <v-btn
                size="x-large"
                variant="outlined"
                class="btn-premium ghost-btn mb-4"
                to="/product"
                rounded="pill"
              >
                Технические характеристики
              </v-btn>
            </div>

            <!-- Premium Stats -->
            <div class="hero-stats-premium fade-in-up delay-3">
              <v-row justify="center">
                <v-col cols="6" sm="3" v-for="(stat, index) in stats" :key="index">
                  <div class="stat-item-premium">
                    <span class="stat-value-premium">{{ stat.value }}</span>
                    <span class="stat-label-premium">{{ stat.label }}</span>
                  </div>
                </v-col>
              </v-row>
            </div>
          </v-col>
        </v-row>
      </v-container>

      <!-- Scroll Indicator -->
      <div class="scroll-down-indicator">
        <div class="mouse">
          <div class="wheel"></div>
        </div>
      </div>
    </section>

    <!-- Water Flow Animation Section -->
    <section class="water-animation-section py-16 bg-pattern-grid">
      <div class="blob-bg" style="top: -100px; left: -100px;"></div>
      <v-container>
        <v-row align="center">
          <v-col cols="12" md="6" class="scroll-reveal-left">
            <div class="section-badge mb-4">
              <v-chip color="info" variant="outlined" size="large" class="glass-effect">
                Визуализация
              </v-chip>
            </div>
            <h2 class="section-title mb-4 primary-gradient-text">
              Управление потоками теплоснабжения
            </h2>
            <p class="section-subtitle text-grey-darken-2 mb-6 font-weight-medium">
              ТГИД-07 обеспечивает полный контроль и мониторинг потоков теплоносителя 
              в системе теплоснабжения. Система отслеживает движение воды по трубам, 
              контролирует давление и температуру на каждом участке сети.
            </p>
            <v-list class="bg-transparent">
              <v-list-item
                v-for="(item, index) in flowFeatures"
                :key="index"
                class="mb-2 glass-card interactive-hover"
              >
                <template v-slot:prepend>
                  <v-icon :icon="item.icon" color="primary" />
                </template>
                <v-list-item-title class="font-weight-bold">{{ item.title }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-col>
          <v-col cols="12" md="6" class="scroll-reveal-right">
            <div class="water-animation-wrapper glass-card apple-shadow">
              <WaterFlowAnimation />
            </div>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <div class="section-divider"></div>

    <!-- Features Section -->
    <section class="features-section py-16 bg-pattern-dots">
      <v-container>
        <v-row>
          <v-col cols="12" class="text-center mb-12 scroll-reveal-scale">
            <div class="section-badge mb-4">
              <v-chip color="primary" variant="outlined" size="large" class="glass-effect">
                Возможности системы
              </v-chip>
            </div>
            <h2 class="section-title mb-4">
              Комплексное решение для управления теплоснабжением
            </h2>
            <p class="section-subtitle text-grey-darken-1">
              Все необходимые инструменты в одной системе
            </p>
          </v-col>
        </v-row>
        <v-row class="stagger-children">
          <v-col
            v-for="(feature, index) in features"
            :key="index"
            cols="12"
            md="6"
            lg="4"
            :data-delay="index * 100"
          >
            <v-card
              elevation="0"
              class="feature-card glass-card apple-shadow interactive-hover"
              :class="`feature-${index + 1}`"
            >
              <div class="feature-icon-wrapper">
                <div class="feature-icon">
                  <v-icon :icon="feature.icon" size="48" />
                </div>
              </div>
              <v-card-title class="feature-title">
                {{ feature.title }}
              </v-card-title>
              <v-card-text class="feature-description">
                {{ feature.description }}
              </v-card-text>
              <v-spacer />
              <v-card-actions>
                <v-btn
                  variant="text"
                  color="primary"
                  :to="feature.link"
                  append-icon="mdi-arrow-right"
                  class="font-weight-bold"
                >
                  Подробнее
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Benefits Section -->
    <section class="benefits-section py-16 bg-white">
      <div class="blob-bg" style="bottom: 0; right: 0;"></div>
      <v-container>
        <v-row align="center">
          <v-col cols="12" md="6" class="scroll-reveal-left">
            <div class="section-badge mb-4">
              <v-chip color="secondary" variant="outlined" size="large" class="glass-effect">
                Преимущества
              </v-chip>
            </div>
            <h2 class="section-title mb-6 primary-gradient-text">
              Почему выбирают ТГИД-07?
            </h2>
            <v-list class="benefits-list bg-transparent">
              <v-list-item
                v-for="(benefit, index) in benefits"
                :key="index"
                class="benefit-item glass-card mb-4 interactive-hover"
              >
                <template v-slot:prepend>
                  <v-avatar color="primary" size="44" class="mr-4 shadow-sm">
                    <v-icon :icon="benefit.icon" color="white" />
                  </v-avatar>
                </template>
                <v-list-item-title class="text-h6 mb-1 font-weight-bold">
                  {{ benefit.title }}
                </v-list-item-title>
                <v-list-item-subtitle class="opacity-80">
                  {{ benefit.description }}
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-col>
          <v-col cols="12" md="6" class="scroll-reveal-right">
            <div class="benefits-visual">
              <div class="visual-card card-1 floating" data-duration="3" data-distance="15">
                <v-icon icon="mdi-chart-line" size="64" color="primary" />
                <p class="mt-4">Аналитика в реальном времени</p>
              </div>
              <div class="visual-card card-2 floating" data-duration="3.5" data-distance="20">
                <v-icon icon="mdi-shield-check" size="64" color="secondary" />
                <p class="mt-4">Надежность и безопасность</p>
              </div>
              <div class="visual-card card-3 floating" data-duration="2.5" data-distance="12">
                <v-icon icon="mdi-speedometer" size="64" color="accent" />
                <p class="mt-4">Высокая производительность</p>
              </div>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- CTA Section -->
    <section class="cta-section py-16">
      <v-container>
        <v-card
          elevation="8"
          class="cta-card"
          rounded="xl"
        >
          <v-card-text class="text-center pa-12">
            <h2 class="text-h3 mb-4 text-white">
              Готовы начать работу с ТГИД-07?
            </h2>
            <p class="text-h6 text-white mb-8 opacity-90">
              Свяжитесь с нами для получения демо-версии системы и консультации
            </p>
            <div class="cta-actions">
              <v-btn
                size="x-large"
                color="white"
                variant="elevated"
                to="/demo"
                class="mr-4 mb-2"
                rounded="xl"
              >
                <v-icon start icon="mdi-email" />
                Оставить заявку
              </v-btn>
              <v-btn
                size="x-large"
                color="white"
                variant="outlined"
                to="/contacts"
                rounded="xl"
              >
                <v-icon start icon="mdi-phone" />
                Связаться с нами
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-container>
    </section>
  </div>
</template>

<script setup lang="ts">
import { onMounted, nextTick, ref, computed } from 'vue'
import { useAdvancedAnimations } from '~/composables/useAdvancedAnimations'
import WaterFlowAnimation from '~/components/WaterFlowAnimation.vue'
const config = useRuntimeConfig()
const { data: pageContent } = await useFetch('/api/public/pages/home/content', {
  baseURL: config.public.apiBase
})

const contentMap = computed(() => {
  const map: Record<string, string> = {}
  if (pageContent.value) {
    (pageContent.value as any[]).forEach(item => {
      map[item.content_key] = item.content_value
    })
  }
  return map
})

useSEO({
  title: 'Главная - Сириус ТГИД-07',
  description: 'Многофункциональная автоматизированная система для управления теплоснабжением ТГИД-07'
})
useStructuredData()

const stats = [
  { value: '100%', label: 'Автоматизация' },
  { value: '24/7', label: 'Мониторинг' },
  { value: '10+', label: 'Лет опыта' },
  { value: '50+', label: 'Проектов' }
]

const features = [
  {
    icon: 'mdi-calculator-variant',
    title: 'Моделирование и расчеты',
    description: 'Высокоточные теплогидравлические расчеты и наладка режимов. Плановые, фактические и летние режимы с расчетом дросселирующих устройств',
    link: '/modeling'
  },
  {
    icon: 'mdi-file-document-multiple',
    title: 'Паспортизация и ГИС',
    description: 'Электронная паспортизация и карта тепловых сетей. Привязка к Google Maps, OpenStreetMap, ZGNC с автоматическим формированием паспортов',
    link: '/gis'
  },
  {
    icon: 'mdi-tools',
    title: 'Эксплуатация и ремонты',
    description: 'АРМ для служб эксплуатации: учет нарушений, опрессовка, планирование ремонтов, мониторинг коррозии',
    link: '/maintenance'
  },
  {
    icon: 'mdi-web',
    title: 'Web-версия',
    description: 'Мобильность и доступность данных. Работа в браузере на любом устройстве с разграничением прав доступа',
    link: '/web-version'
  },
  {
    icon: 'mdi-chart-line',
    title: 'Пьезометрические графики',
    description: 'Автоматическое построение графиков давлений по любому выбранному пути для визуального анализа напоров',
    link: '/features'
  },
  {
    icon: 'mdi-thermometer-lines',
    title: 'Расчет тепловых потерь',
    description: 'Модуль рассчитывает нормативные и фактические потери через изоляцию и утечки. База для экономического обоснования тарифов',
    link: '/features'
  }
]

const benefits = [
  {
    icon: 'mdi-check-circle',
    title: 'Масштабируемость',
    description: 'Работа с крупными сетями мегаполисов с разделением на магистральные и распределительные уровни'
  },
  {
    icon: 'mdi-ruler',
    title: 'Точность',
    description: 'Расчеты на основе реальной геодезии и физических свойств трубопроводов'
  },
  {
    icon: 'mdi-link-variant',
    title: 'Интеграция',
    description: 'Поддержка онлайн-карт (Google, OpenStreetMap) и экспорт данных в Excel/AutoCAD'
  },
  {
    icon: 'mdi-shield-check',
    title: 'Единое информационное пространство',
    description: 'Объединяет задачи производственно-технических служб, диспетчерских и инженеров-расчетчиков'
  }
]

const flowFeatures = [
  {
    icon: 'mdi-water',
    title: 'Мониторинг потоков в реальном времени'
  },
  {
    icon: 'mdi-thermometer',
    title: 'Контроль температуры и давления'
  },
  {
    icon: 'mdi-chart-line',
    title: 'Анализ гидравлических режимов'
  },
  {
    icon: 'mdi-alert',
    title: 'Автоматическое обнаружение утечек'
  }
]

const { observeElements } = useScrollAnimation()
const { initFloatingAnimation } = useAdvancedAnimations()

onMounted(() => {
  observeElements()
  // Инициализация floating анимаций
  if (process.client) {
    nextTick(() => {
      document.querySelectorAll('.floating').forEach((el) => {
        initFloatingAnimation(el as HTMLElement)
      })
    })
  }
})
</script>


/* Global Page Wrapper & Elements */
.homepage-wrapper {
  position: relative;
  overflow: hidden;
  background: #0f172a; /* Consistent dark theme start */
}

.global-vertical-pipe {
  position: absolute;
  top: 0;
  right: 8%;
  height: 100%;
  width: 120px;
  z-index: 1;
  opacity: 0.25; /* Increased visibility */
  pointer-events: none;
}

.global-vertical-pipe-2 {
  position: absolute;
  top: 0;
  left: 5%;
  height: 100%;
  width: 80px;
  z-index: 1;
  opacity: 0.1;
  pointer-events: none;
}

/* Hero Section Premium Redesign */
.hero-section {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  overflow: hidden;
  background: #0f172a;
}

.mesh-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  filter: blur(100px);
  opacity: 0.6;
}

.mesh-blob {
  position: absolute;
  border-radius: 50%;
  mix-blend-mode: screen;
  animation: mesh-float 20s infinite alternate ease-in-out;
}

.mesh-blob-1 { width: 600px; height: 600px; background: #3b82f6; top: -10%; left: -10%; }
.mesh-blob-2 { width: 500px; height: 500px; background: #8b5cf6; bottom: -10%; right: -10%; animation-delay: -5s; }
.mesh-blob-3 { width: 400px; height: 400px; background: #ef4444; top: 40%; left: 30%; animation-delay: -10s; }
.mesh-blob-4 { width: 450px; height: 450px; background: #0ea5e9; bottom: 20%; left: 10%; animation-delay: -15s; }

@keyframes mesh-float {
  0% { transform: translate(0, 0) rotate(0deg) scale(1); }
  100% { transform: translate(100px, 50px) rotate(90deg) scale(1.1); }
}

.hero-content {
  position: relative;
  z-index: 2;
}

.min-height-screen {
  min-height: 100vh;
}

.hero-badge-premium {
  display: inline-block;
}

.glass-pill {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 8px 20px;
  border-radius: 100px;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 600;
  font-size: 0.9rem;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.hero-title-premium {
  font-size: clamp(3rem, 8vw, 6rem);
  font-weight: 950;
  line-height: 1.05;
  color: white;
  margin-bottom: 2rem;
  letter-spacing: -3px;
}

.text-gradient {
  background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.hero-subtitle-premium {
  font-size: clamp(1rem, 2vw, 1.4rem);
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.7);
  max-width: 800px;
  margin: 0 auto;
  font-weight: 500;
}

.hero-stats-premium {
  margin-top: 5rem;
  padding-top: 3rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
}

.stat-item-premium {
  text-align: center;
}

.stat-value-premium {
  font-size: clamp(2rem, 5vw, 3.5rem);
  font-weight: 900;
  color: white;
  margin-bottom: 0.25rem;
  display: block;
}

.stat-label-premium {
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: rgba(255, 255, 255, 0.5);
  font-weight: 700;
}

.btn-premium {
  font-weight: 800 !important;
  letter-spacing: 0.8px !important;
  text-transform: none !important;
  padding: 0 45px !important;
  height: 64px !important;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
}

.primary-btn {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
  color: white !important;
  box-shadow: 0 20px 40px rgba(37, 99, 235, 0.3) !important;
}

.primary-btn:hover {
  transform: translateY(-5px);
  box-shadow: 0 25px 50px rgba(37, 99, 235, 0.4) !important;
}

.ghost-btn {
  border: 1px solid rgba(255, 255, 255, 0.2) !important;
  color: white !important;
  backdrop-filter: blur(8px);
}

.ghost-btn:hover {
  background: rgba(255, 255, 255, 0.1) !important;
  border-color: rgba(255, 255, 255, 0.5) !important;
}

/* Restored Section Styles */
.water-animation-section, .features-section, .benefits-section {
  position: relative;
  z-index: 2;
}

.water-animation-section {
  background: #f8fafc;
}

.section-title {
  font-size: clamp(2rem, 5vw, 3rem);
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -1px;
}

.water-animation-wrapper {
  height: 450px;
  border-radius: 32px;
  overflow: hidden;
  box-shadow: 0 40px 80px rgba(0,0,0,0.08);
}

/* Features restored */
.features-section {
  background: #ffffff;
}

.feature-card {
  height: 100%;
  padding: 3rem;
  border-radius: 24px;
  transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
  background: white;
  border: 1px solid #f1f5f9;
}

.feature-card:hover {
  transform: translateY(-12px);
  box-shadow: 0 30px 60px rgba(0,0,0,0.05);
  border-color: #3b82f6;
}

.feature-icon {
  width: 70px;
  height: 70px;
  border-radius: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 2rem;
  color: white;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
}

/* Benefits restored */
.benefit-item {
  padding: 1.5rem;
  border-radius: 20px;
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.benefit-item:hover {
  background: white;
  border-color: #f1f5f9;
  box-shadow: 0 10px 30px rgba(0,0,0,0.03);
  transform: translateX(10px);
}

/* Visual components */
.visual-card {
  background: white;
  border-radius: 24px;
  padding: 2rem;
  box-shadow: 0 20px 40px rgba(0,0,0,0.05);
  text-align: center;
}

/* CTA restored */
.cta-card {
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  overflow: hidden;
}

/* Scroll indicator */
.scroll-down-indicator {
  position: absolute;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 2;
}

.mouse {
  width: 26px;
  height: 44px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 20px;
  position: relative;
}

.wheel {
  width: 4px;
  height: 8px;
  background: #3b82f6;
  border-radius: 2px;
  position: absolute;
  top: 8px;
  left: 50%;
  margin-left: -2px;
  animation: scroll-wheel 2.s infinite;
}

@keyframes scroll-wheel {
  0% { transform: translateY(0); opacity: 1; }
  100% { transform: translateY(15px); opacity: 0; }
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(40px); }
  to { opacity: 1; transform: translateY(0); }
}

.fade-in-up {
  animation: fadeInUp 1s cubic-bezier(0.2, 0.8, 0.2, 1) forwards;
}

/* Responsive */
.primary-btn:hover .btn-arrow {
  transform: translateX(5px);
}

.btn-arrow {
  transition: transform 0.3s ease;
}

.glass-pill:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-2px);
  transition: all 0.3s ease;
}

.text-gradient {
  background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #60a5fa 100%);
  background-size: 200% auto;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: shine 3s linear infinite;
}

@keyframes shine {
  to { background-position: 200% center; }
}

.stat-item-premium:hover {
  transform: scale(1.05);
  transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}
</style>
