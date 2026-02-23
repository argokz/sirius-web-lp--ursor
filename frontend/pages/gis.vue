<template>
  <div class="gis-page">
    <!-- Hero Section -->
    <section class="hero-section glass-effect bg-pattern-grid">
      <div class="blob-bg" style="top: -100px; right: -100px;"></div>
      <v-container>
        <v-row align="center">
          <v-col cols="12" md="7">
            <div class="badge fade-in-up">Раздел 3. Паспортизация и ГИС</div>
            <h1 class="display-1 fade-in-up delay-1 primary-gradient-text">Цифровая карта и электронные паспорта</h1>
            <p class="subtitle fade-in-up delay-2">
              Переведите бумажные архивы в цифру. Модуль паспортизации связывает технические 
              характеристики оборудования с его точным местоположением на карте местности.
            </p>
          </v-col>
          <v-col cols="12" md="5" class="d-none d-md-block">
            <div class="hero-visual fade-in-right glass-card pa-8 apple-shadow">
              <v-icon icon="mdi-map-search" size="160" color="primary" class="opacity-10" />
            </div>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Map Features -->
    <section class="map-features py-16 bg-pattern-dots">
      <v-container>
        <v-row>
          <v-col cols="12" md="4" class="scroll-reveal">
            <div class="feature-item glass-card interactive-hover h-100">
              <v-icon icon="mdi-layers-outline" color="primary" size="48" class="mb-4" />
              <h4>Интерактивная карта (ГИС)</h4>
              <p>Полная привязка схемы теплоснабжения к координатам местности с использованием Google Maps, OpenStreetMap.</p>
            </div>
          </v-col>
          <v-col cols="12" md="4" class="scroll-reveal" data-delay="100">
            <div class="feature-item glass-card interactive-hover h-100">
              <v-icon icon="mdi-card-text-outline" color="secondary" size="48" class="mb-4" />
              <h4>Детальная паспортизация</h4>
              <p>Диаметры, материалы, годы прокладки, типы изоляции и схемы узлов для каждого элемента сети.</p>
            </div>
          </v-col>
          <v-col cols="12" md="4" class="scroll-reveal" data-delay="200">
            <div class="feature-item glass-card interactive-hover h-100">
              <v-icon icon="mdi-file-export-outline" color="success" size="48" class="mb-4" />
              <h4>Автоматические отчеты</h4>
              <p>Мгновенная генерация паспортов магистральных и распределительных участков на основе данных системы.</p>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Visual Showcase -->
    <section class="showcase py-16 bg-white">
      <div class="blob-bg" style="bottom: 0; left: 0;"></div>
      <v-container>
        <v-row align="center">
          <v-col cols="12" md="6" class="scroll-reveal-left">
            <div class="image-showcase premium-border apple-shadow rounded-xl overflow-hidden p-0 bg-transparent">
              <v-img src="/gis_map.png" alt="Интерактивная ГИС модель" cover class="rounded-xl transition-transform glow-hover h-100" />
            </div>
          </v-col>
          <v-col cols="12" md="6" class="scroll-reveal-right">
            <h2 class="section-title">Объекты ПТС и Электрические сети</h2>
            <p>Система хранит исчерпывающие данные по каждому элементу: трубопроводы, узлы, камеры, павильоны и оборудование.</p>
            <div class="mt-8">
              <v-chip variant="elevated" color="info" class="mr-2 mb-2">Трубопроводы</v-chip>
              <v-chip variant="elevated" color="info" class="mr-2 mb-2">Камеры и задвижки</v-chip>
              <v-chip variant="elevated" color="info" class="mr-2 mb-2">Электросети (ЛЭП)</v-chip>
              <v-chip variant="elevated" color="info" class="mr-2 mb-2">Трансформаторы</v-chip>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Footer CTA -->
    <section class="cta-section py-16 bg-primary white--text text-center">
      <v-container>
        <h2 class="mb-6">Хотите увидеть систему в действии?</h2>
        <v-btn size="x-large" color="white" light rounded="pill" class="cta-btn" to="/demo">
          Посмотреть пример паспорта
          <v-icon end icon="mdi-file-pdf-box" />
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
  title: 'ГИС и Паспортизация тепловых сетей ТГИД-07 — Цифровой двойник',
  description: 'Электронная карта и паспорта оборудования. Объедините технические данные с географической привязкой для мгновенного доступа к информации о любом участке сети.'
})
</script>

<style scoped>
.gis-page {
  background: #ffffff;
}

.hero-section {
  padding: 120px 0;
  background: linear-gradient(135deg, rgba(240, 244, 255, 1) 0%, rgba(255, 255, 255, 1) 100%);
}

.badge {
  display: inline-block;
  padding: 6px 16px;
  background: rgba(30, 64, 175, 0.1);
  color: #1e40af;
  border-radius: 20px;
  font-weight: 600;
  font-size: 0.9rem;
  margin-bottom: 24px;
}

.display-1 {
  font-size: 3.5rem;
  font-weight: 800;
  color: #0f172a;
  margin-bottom: 24px;
}

.subtitle {
  font-size: 1.2rem;
  color: #475569;
}

.bg-light { background: #f8fafc; }

.feature-item {
  padding: 30px;
  text-align: center;
}

.feature-item h4 {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 12px;
}

.image-showcase {
  height: 400px;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  border-radius: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  box-shadow: 0 20px 50px rgba(59, 130, 246, 0.2);
}

.map-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
  100% { transform: translateY(0px); }
}

.bg-primary {
  background: #1d4ed8 !important;
  color: white;
}

.cta-btn {
  color: #1d4ed8 !important;
  font-weight: 700;
}

.glass-card {
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

@media (max-width: 960px) {
  .display-1 { font-size: 2.2rem; }
}
</style>
