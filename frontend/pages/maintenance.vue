<template>
  <div class="maintenance-page">
    <!-- Hero Section -->
    <section class="hero-section glass-effect">
      <v-container>
        <v-row align="center" justify="center" class="text-center">
          <v-col cols="12" md="10">
            <div class="badge fade-in-up">Раздел 4. Эксплуатация и Ремонты</div>
            <h1 class="display-1 fade-in-up delay-1">Управление надежностью: Ремонты и Дефекты</h1>
            <p class="subtitle fade-in-up delay-2">
              Автоматизированное рабочее место (АРМ) для служб эксплуатации: 
              мониторинг всей истории жизни теплосети и планирование работ.
            </p>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Modules Timeline -->
    <section class="modules-timeline py-16">
      <v-container>
        <v-row>
          <v-col v-for="(module, index) in modules" :key="index" cols="12" md="6" lg="3" class="scroll-reveal">
            <v-card class="module-card elevation-0">
              <div class="module-number">{{ index + 1 }}</div>
              <h3>{{ module.title }}</h3>
              <p>{{ module.description }}</p>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Specific Highlights -->
    <section class="highlights py-16 bg-dark text-white">
      <v-container>
        <v-row align="center">
          <v-col cols="12" md="6" class="scroll-reveal-left">
            <h2 class="section-title text-white">Мониторинг коррозии</h2>
            <p class="opacity-80">Уникальный модуль для анализа скорости внутренней коррозии. Оценка агрессивности сетевой воды и прогноз ресурса труб для предотвращения аварий.</p>
            <div class="stats-box mt-8">
              <div class="stat-item">
                <span class="stat-val">15-20%</span>
                <span class="stat-label">Снижение аварийности</span>
              </div>
            </div>
          </v-col>
          <v-col cols="12" md="6" class="scroll-reveal-right">
             <div class="image-showcase premium-border apple-shadow rounded-xl overflow-hidden">
                <v-img src="/maintenance_tablet.png" alt="Планшет мастера с дефектами" cover class="rounded-xl transition-transform glow-hover" />
             </div>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Download CTA -->
    <section class="download-section py-16 text-center">
      <v-container>
        <v-btn size="x-large" color="secondary" dark rounded="pill" class="cta-btn shadow-premium" to="/demo">
          Скачать презентацию модуля Ремонты
          <v-icon end icon="mdi-download" />
        </v-btn>
      </v-container>
    </section>
  </div>
</template>

<script setup lang="ts">
const modules = [
  { title: 'Учет нарушений', description: 'Фиксация порывов, свищей и дефектов на интерактивной карте с классификацией.' },
  { title: 'Опрессовка', description: 'Планирование кампаний испытаний и создание фиксация повреждений в реальном времени.' },
  { title: 'Планирование ТОиР', description: 'Управление капитальными и текущими ремонтами на основе данных диагностики.' },
  { title: 'Индикаторы', description: 'Учет установки индикаторов коррозии и анализ наработки на отказ.' }
]

const { observeElements } = useScrollAnimation()

onMounted(() => {
  observeElements()
})

useSEO({
  title: 'Управление эксплуатацией и ремонтами (ТОиР) ТГИД-07',
  description: 'АРМ службы эксплуатации: учет повреждений, планирование ремонтов, мониторинг коррозии и опрессовка. Продлите срок службы вашей сети с ТГИД-07.'
})
</script>

<style scoped>
.maintenance-page { background: #ffffff; }

.hero-section {
  padding: 100px 0;
  background: radial-gradient(circle at left bottom, rgba(239, 68, 68, 0.05), transparent);
}

.badge {
  display: inline-block;
  padding: 6px 16px;
  background: rgba(239, 68, 68, 0.1);
  color: #ef4444;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 24px;
}

.display-1 {
  font-size: 3rem;
  font-weight: 800;
  color: #1a1a1a;
  margin-bottom: 24px;
}

.module-card {
  padding: 30px;
  border-radius: 24px;
  background: #fdf2f2;
  height: 100%;
  position: relative;
  overflow: hidden;
}

.module-number {
  font-size: 5rem;
  font-weight: 900;
  position: absolute;
  right: -10px;
  top: -20px;
  color: rgba(239, 68, 68, 0.05);
}

.bg-dark { background: #0f172a; }

.stat-val {
  display: block;
  font-size: 3rem;
  font-weight: 800;
  color: #ef4444;
}

.cta-btn {
  box-shadow: 0 10px 20px rgba(239, 68, 68, 0.2);
}

@media (max-width: 960px) {
  .display-1 { font-size: 2rem; }
}
</style>
