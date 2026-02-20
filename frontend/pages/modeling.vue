<template>
  <div class="modeling-page">
    <!-- Hero Section -->
    <section class="hero-section glass-effect">
      <v-container>
        <div class="blob-bg" style="top: 0; right: 0;"></div>
        <v-row align="center" justify="center">
          <v-col cols="12" md="10" lg="8" class="text-center">
            <div class="badge fade-in-up">Раздел 2. Моделирование</div>
            <h1 class="display-1 fade-in-up delay-1 primary-gradient-text">Высокоточные теплогидравлические расчеты</h1>
            <p class="subtitle fade-in-up delay-2">
              Сердце системы — модуль создания математической модели тепловой сети, 
              позволяющий моделировать поведение системы в любых условиях.
            </p>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Interactive Zest: Calculation Demo -->
    <section class="calculation-zest py-16 bg-pattern-dots">
      <v-container>
        <v-card class="glass-card pa-8 apple-shadow scroll-reveal">
          <v-row align="center">
            <v-col cols="12" md="6">
              <h2 class="mb-4">Мгновенный подбор оборудования</h2>
              <p>Попробуйте наш калькулятор "интеллектуального сопла". Система автоматически подберет диаметр сужающего устройства на основе ваших параметров.</p>
              <div class="mt-6">
                <v-btn color="primary" variant="outlined" rounded="pill">Инструменты инженера</v-btn>
              </div>
            </v-col>
            <v-col cols="12" md="6">
              <div class="interactive-diagram glass-effect pa-6 rounded-xl border">
                 <div class="diagram-line primary"></div>
                 <div class="diagram-node"></div>
                 <div class="diagram-label">Узел 12-Б</div>
              </div>
            </v-col>
          </v-row>
        </v-card>
      </v-container>
    </section>

    <!-- Technical Scheme (main-func.png) -->
    <section class="technical-scheme py-16 bg-white">
      <v-container>
        <v-card class="glass-card pa-8 apple-shadow scroll-reveal">
          <v-row align="center">
            <v-col cols="12" md="5">
              <h2 class="mb-4 primary-gradient-text">Функциональная схема</h2>
              <p>Наглядное представление взаимосвязи модулей системы ТГИД-07. Обеспечение бесшовного обмена данными между расчетным ядром и базой ГИС.</p>
              <v-list class="bg-transparent mt-4">
                <v-list-item prepend-icon="mdi-check-all" title="Целостность данных" />
                <v-list-item prepend-icon="mdi-check-all" title="Высокая скорость обработки" />
              </v-list>
            </v-col>
            <v-col cols="12" md="7">
              <div class="scheme-wrapper glass-effect pa-4 rounded-xl border">
                <v-img src="/main-func.png" alt="Функциональная схема ТГИД-07" class="rounded-lg" />
              </div>
            </v-col>
          </v-row>
        </v-card>
      </v-container>
    </section>

    <!-- Key Features Grid -->
    <section class="features-grid py-16 bg-pattern-grid">
      <v-container>
        <v-row>
          <v-col cols="12" md="6" class="scroll-reveal">
            <v-card class="feature-card elevation-0">
              <div class="icon-box primary-gradient">
                <v-icon icon="mdi-calculator" size="40" color="white" />
              </div>
              <h3>Плановый режим</h3>
              <p>Определение идеального состояния сети для подбора дросселирующих устройств (сопел, шайб). Расчет с учетом нормативных тепловых потерь.</p>
            </v-card>
          </v-col>
          <v-col cols="12" md="6" class="scroll-reveal" data-delay="100">
            <v-card class="feature-card elevation-0">
              <div class="icon-box secondary-gradient">
                <v-icon icon="mdi-alert-decagram" size="40" color="white" />
              </div>
              <h3>Фактический режим</h3>
              <p>Моделирование реальной ситуации в трубах с учетом текущего состояния оборудования, дефектов и отключений.</p>
            </v-card>
          </v-col>
          <v-col cols="12" md="6" class="scroll-reveal">
            <v-card class="feature-card elevation-0">
              <div class="icon-box accent-gradient">
                <v-icon icon="mdi-water-sync" size="40" color="white" />
              </div>
              <h3>Летний режим и ГВС</h3>
              <p>Специализированные алгоритмы для расчета гидравлики в межотопительный период с оптимизацией насосных станций.</p>
            </v-card>
          </v-col>
          <v-col cols="12" md="6" class="scroll-reveal" data-delay="100">
            <v-card class="feature-card elevation-0">
              <div class="icon-box info-gradient">
                <v-icon icon="mdi-chart-areaspline" size="40" color="white" />
              </div>
              <h3>Пьезометрические графики</h3>
              <p>Автоматическое построение графиков давлений по любому пути. Визуальный анализ напоров, вскипания и кавитации.</p>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Detailed Section: Thermal Losses -->
    <section class="detail-section py-16 bg-light">
      <v-container>
        <v-row align="center">
          <v-col cols="12" md="6" class="scroll-reveal-left">
            <h2 class="section-title">Расчет тепловых потерь</h2>
            <p>Модуль рассчитывает нормативные и фактические потери тепла через изоляцию и с утечками. Это база для экономического обоснования тарифов.</p>
            <v-list class="bg-transparent">
              <v-list-item prepend-icon="mdi-check-circle" title="Учет видов прокладки (надземная, канальная)" />
              <v-list-item prepend-icon="mdi-check-circle" title="Анализ состояния изоляции" />
              <v-list-item prepend-icon="mdi-check-circle" title="Учет температуры грунта" />
            </v-list>
          </v-col>
          <v-col cols="12" md="6" class="scroll-reveal-right">
            <div class="illustration-box interactive-hover">
               <v-icon icon="mdi-thermometer-lines" size="120" color="primary" class="opacity-20" />
               <div class="animated-pulse"></div>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- CTA -->
    <section class="cta-section py-16 text-center">
      <v-container>
        <v-btn size="x-large" color="primary" dark rounded="pill" class="cta-btn" to="/demo">
          Заказать расчет модели
          <v-icon end icon="mdi-chevron-right" />
        </v-btn>
      </v-container>
    </section>
  </div>
</template>

<script setup lang="ts">
const { observeElements } = useScrollAnimation()

onMounted(() => {
  observeElements()
})

useSEO({
  title: 'Моделирование и расчеты - ТГИД-07',
  description: 'Высокоточные теплогидравлические расчеты и наладка режимов тепловых сетей.'
})
</script>

<style scoped>
.modeling-page {
  background: #ffffff;
}

.hero-section {
  padding: 100px 0;
  background: radial-gradient(circle at top right, rgba(102, 126, 234, 0.05), transparent);
}

.badge {
  display: inline-block;
  padding: 6px 16px;
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 24px;
}

.display-1 {
  font-size: 3.5rem;
  font-weight: 800;
  line-height: 1.1;
  color: #1a1a1a;
  margin-bottom: 24px;
}

.subtitle {
  font-size: 1.25rem;
  color: #666;
  max-width: 600px;
  margin: 0 auto;
}

.feature-card {
  padding: 40px;
  border-radius: 24px;
  background: #f8fafc;
  height: 100%;
  transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.feature-card:hover {
  transform: translateY(-10px);
  background: #ffffff;
  box-shadow: 0 20px 40px rgba(0,0,0,0.05) !important;
}

.icon-box {
  width: 80px;
  height: 80px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 24px;
}

.primary-gradient { background: linear-gradient(135deg, #667eea, #764ba2); }
.secondary-gradient { background: linear-gradient(135deg, #fb923c, #f97316); }
.accent-gradient { background: linear-gradient(135deg, #38bdf8, #0ea5e9); }
.info-gradient { background: linear-gradient(135deg, #4ade80, #22c55e); }

h3 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 16px;
  color: #1a1a1a;
}

.bg-light { background: #fbfcfe; }

.illustration-box {
  height: 300px;
  background: #ffffff;
  border-radius: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  box-shadow: inset 0 0 40px rgba(0,0,0,0.02);
}

.animated-pulse {
  position: absolute;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle, rgba(102, 126, 234, 0.05) 0%, transparent 70%);
  animation: pulse 4s infinite;
}

@keyframes pulse {
  0% { transform: scale(0.8); opacity: 0.5; }
  50% { transform: scale(1.2); opacity: 0.8; }
  100% { transform: scale(0.8); opacity: 0.5; }
}

.cta-btn {
  padding: 0 40px;
  font-weight: 700;
  letter-spacing: 0.5px;
  box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
}

/* Animations from useAdvancedAnimations will trigger via IntersectionObserver */
.scroll-reveal {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.8s ease-out;
}

.scroll-reveal.animate-in {
  opacity: 1;
  transform: translateY(0);
}

@media (max-width: 960px) {
  .display-1 { font-size: 2.5rem; }
}
</style>
