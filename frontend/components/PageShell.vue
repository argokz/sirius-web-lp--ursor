<template>
  <div class="page">
    <section class="page-hero">
      <div class="container page-hero-grid">
        <div class="reveal">
          <UBadge color="primary" variant="subtle" size="lg">{{ eyebrow }}</UBadge>
          <h1 class="display-title">{{ title }}</h1>
          <p class="lead">{{ description }}</p>
          <div class="page-actions">
            <UButton to="/demo" color="primary" size="xl" trailing-icon="i-lucide-arrow-right">
              Запросить демо
            </UButton>
            <UButton to="/contacts" color="neutral" variant="outline" size="xl">
              Связаться
            </UButton>
          </div>
        </div>

        <div class="hero-card card scan-line reveal delay-2">
          <img v-if="image" :src="image" :alt="title" loading="eager" fetchpriority="high" decoding="async">
          <div v-else class="hero-symbol">
            <SiriusLogo mark-only :size="126" />
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <span class="eyebrow">{{ sectionEyebrow }}</span>
        <h2 class="section-title">{{ sectionTitle }}</h2>
        <div class="grid grid-3 cards">
          <article v-for="item in items" :key="item.title" class="card card-pad accent-card">
            <div class="icon-box">
              <UIcon :name="item.icon" />
            </div>
            <h3>{{ item.title }}</h3>
            <p>{{ item.text }}</p>
          </article>
        </div>
      </div>
    </section>

    <slot />

    <section class="section-tight">
      <div class="container">
        <div class="cta card">
          <div>
            <span class="eyebrow">Следующий шаг</span>
            <h2 class="section-title">{{ ctaTitle }}</h2>
            <p class="lead">{{ ctaText }}</p>
          </div>
          <UButton to="/demo" color="primary" size="xl" trailing-icon="i-lucide-calendar-check">
            Назначить демонстрацию
          </UButton>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{
  eyebrow: string
  title: string
  description: string
  image?: string
  sectionEyebrow: string
  sectionTitle: string
  items: Array<{ icon: string; title: string; text: string }>
  ctaTitle?: string
  ctaText?: string
}>(), {
  ctaTitle: 'Покажем ТГИД-07 на ваших данных',
  ctaText: 'Подготовим сценарий демонстрации под вашу структуру сети и управленческие задачи.'
})
</script>

<style scoped>
.page-hero {
  padding: 136px 0 80px;
  border-bottom: 1px solid var(--line);
}

.page-hero-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(320px, 0.8fr);
  gap: 44px;
  align-items: center;
}

.page-hero-grid > * {
  min-width: 0;
}

.page-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 32px;
}

.hero-card {
  max-width: 100%;
  min-width: 0;
  overflow: hidden;
  padding: 8px;
  border: 0;
  border-radius: var(--radius);
  background: var(--dark);
}

.hero-card img {
  width: 100%;
  height: auto;
  object-fit: contain;
  border-radius: 3px;
}

.hero-symbol {
  width: 260px;
  height: 260px;
  display: grid;
  place-items: center;
  border-radius: 999px;
  background: var(--paper);
}

.cards {
  margin-top: 34px;
}

.cards h3 {
  margin: 22px 0 8px;
  color: var(--ink);
  font-family: var(--serif);
  font-size: 1.4rem;
  font-weight: 400;
  line-height: 1.2;
}

.cards p {
  margin: 0;
  color: var(--muted);
  line-height: 1.7;
}

.cta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  padding: 40px;
}

@media (max-width: 900px) {
  .page-hero-grid {
    grid-template-columns: 1fr;
  }

  .hero-card {
    min-height: 300px;
  }
}

@media (max-width: 640px) {
  .page-hero {
    padding-top: 104px;
  }

  .cta {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
