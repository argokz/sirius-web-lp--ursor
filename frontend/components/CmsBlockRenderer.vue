<template>
  <section v-if="block.block_type === 'hero'" :class="['dynamic-hero', layoutClasses, { 'hero-wide': heroVisual === 'map' }]">
    <div class="container hero-grid">
      <div class="hero-copy reveal">
        <UBadge v-if="block.eyebrow" color="primary" variant="subtle" size="lg">{{ block.eyebrow }}</UBadge>
        <h1 class="display-title">{{ block.title || 'Страница' }}</h1>
        <div v-if="block.body" class="lead rich-body" v-html="block.body" />
        <div class="hero-actions">
          <UButton :to="payload.button_url || '/demo'" color="primary" size="lg" trailing-icon="i-lucide-arrow-right">
            {{ payload.button_text || 'Запросить демо' }}
          </UButton>
          <UButton :to="payload.button2_url || '/contacts'" variant="outline" color="neutral" size="lg">
            {{ payload.button2_text || 'Связаться' }}
          </UButton>
        </div>
      </div>
      <ProductMapDemo v-if="heroVisual === 'map'" class="hero-demo reveal delay-1" />
      <SiriusImage
        v-else-if="payload.image"
        class="hero-media scan-line reveal delay-1"
        :src="payload.image"
        :alt="block.title || 'Изображение'"
        aspect-ratio="16 / 11"
        eager
      />
    </div>
  </section>

  <section v-else-if="block.block_type === 'cards'" :class="['section', layoutClasses]">
    <div class="container">
      <span v-if="block.eyebrow" class="eyebrow">{{ block.eyebrow }}</span>
      <h2 v-if="block.title" class="section-title">{{ block.title }}</h2>
      <div v-if="block.body" class="lead rich-body" v-html="block.body" />
      <div class="grid grid-3 dynamic-cards">
        <article v-for="(item, index) in items" :key="index" class="card card-pad reveal" :class="`delay-${Math.min(index, 3)}`">
          <div class="icon-box"><UIcon :name="item.icon || 'i-lucide-sparkles'" /></div>
          <h3>{{ item.title }}</h3>
          <p>{{ item.text }}</p>
        </article>
      </div>
    </div>
  </section>

  <section v-else-if="block.block_type === 'metrics'" :class="['section-tight', layoutClasses]">
    <div class="container">
      <span v-if="block.eyebrow" class="eyebrow">{{ block.eyebrow }}</span>
      <h2 v-if="block.title" class="section-title">{{ block.title }}</h2>
      <div v-if="block.body" class="lead rich-body" v-html="block.body" />
      <div class="metric-grid dynamic-metrics">
        <article v-for="(item, index) in items" :key="index" class="metric-card reveal" :class="`delay-${Math.min(index, 3)}`">
          <span class="metric-value">{{ item.value }}</span>
          <strong>{{ item.title }}</strong>
          <p>{{ item.text }}</p>
        </article>
      </div>
    </div>
  </section>

  <section v-else-if="block.block_type === 'cta'" :class="['section-tight', layoutClasses]">
    <div class="container">
      <div class="cta-panel scan-line">
        <div>
          <span v-if="block.eyebrow" class="eyebrow">{{ block.eyebrow }}</span>
          <h2>{{ block.title }}</h2>
          <div v-if="block.body" class="rich-body" v-html="block.body" />
        </div>
        <UButton :to="payload.button_url || '/demo'" color="primary" size="lg" trailing-icon="i-lucide-arrow-right">
          {{ payload.button_text || 'Запросить демо' }}
        </UButton>
      </div>
    </div>
  </section>

  <section v-else-if="block.block_type === 'steps'" :class="['section', layoutClasses]">
    <div class="container">
      <span v-if="block.eyebrow" class="eyebrow">{{ block.eyebrow }}</span>
      <h2 v-if="block.title" class="section-title">{{ block.title }}</h2>
      <div v-if="block.body" class="lead rich-body" v-html="block.body" />
      <div class="process-flow">
        <article v-for="(item, index) in items" :key="index" class="process-step">
          <span>{{ index + 1 }}</span>
          <h3>{{ item.title }}</h3>
          <p>{{ item.text }}</p>
        </article>
      </div>
    </div>
  </section>

  <section v-else-if="block.block_type === 'outcomes'" :class="['section-tight', layoutClasses]">
    <div class="container">
      <span v-if="block.eyebrow" class="eyebrow">{{ block.eyebrow }}</span>
      <h2 v-if="block.title" class="section-title">{{ block.title }}</h2>
      <div v-if="block.body" class="lead rich-body" v-html="block.body" />
      <div class="detail-grid">
        <article v-for="(item, index) in items" :key="index" class="detail-card">
          <h3>{{ item.title }}</h3>
          <p>{{ item.text }}</p>
        </article>
      </div>
    </div>
  </section>

  <section v-else-if="block.block_type === 'flow'" :class="['section dark-panel', layoutClasses]">
    <div class="container split">
      <div>
        <span v-if="block.eyebrow" class="eyebrow">{{ block.eyebrow }}</span>
        <h2 v-if="block.title" class="section-title">{{ block.title }}</h2>
        <div v-if="block.body" class="lead rich-body" v-html="block.body" />
      </div>
      <div class="flow-card">
        <WaterFlowAnimation :mode="payload.flow_mode || 'horizontal'" show-badge label="FLOW_STABLE" />
      </div>
    </div>
  </section>

  <!-- GALLERY BLOCK -->
  <section v-else-if="block.block_type === 'gallery'" :class="['section', layoutClasses]">
    <div class="container">
      <span v-if="block.eyebrow" class="eyebrow">{{ block.eyebrow }}</span>
      <h2 v-if="block.title" class="section-title">{{ block.title }}</h2>
      <div v-if="block.body" class="lead rich-body" v-html="block.body" />
      <div class="gallery-grid">
        <button
          v-for="(item, index) in items"
          :key="index"
          type="button"
          class="gallery-item"
          @click="openLightbox(index)"
        >
          <img :src="item.image" :alt="item.caption || `Фото ${index + 1}`" loading="lazy" />
          <div v-if="item.caption" class="gallery-caption">{{ item.caption }}</div>
        </button>
      </div>
    </div>

    <!-- Lightbox -->
    <dialog ref="lightboxRef" class="lightbox-dialog" @click.self="closeLightbox">
      <button type="button" class="lightbox-close" @click="closeLightbox">
        <UIcon name="i-lucide-x" />
      </button>
      <button v-if="lightboxIndex > 0" type="button" class="lightbox-prev" @click="lightboxIndex--">
        <UIcon name="i-lucide-chevron-left" />
      </button>
      <img v-if="items[lightboxIndex]" :src="items[lightboxIndex].image" :alt="items[lightboxIndex].caption" class="lightbox-img" />
      <div v-if="items[lightboxIndex]?.caption" class="lightbox-caption">{{ items[lightboxIndex].caption }}</div>
      <button v-if="lightboxIndex < items.length - 1" type="button" class="lightbox-next" @click="lightboxIndex++">
        <UIcon name="i-lucide-chevron-right" />
      </button>
    </dialog>
  </section>

  <!-- PRICING BLOCK -->
  <section v-else-if="block.block_type === 'pricing'" :class="['section', layoutClasses]">
    <div class="container">
      <div class="text-center" style="max-width: 700px; margin: 0 auto 40px;">
        <span v-if="block.eyebrow" class="eyebrow">{{ block.eyebrow }}</span>
        <h2 v-if="block.title" class="section-title" style="margin-top: 10px;">{{ block.title }}</h2>
        <div v-if="block.body" class="lead rich-body" v-html="block.body" style="margin-top: 10px;" />
      </div>
      <div class="pricing-grid">
        <article v-for="(item, index) in items" :key="index" class="pricing-card" :class="{ 'is-featured': item.featured }">
          <div v-if="item.featured" class="pricing-badge">Популярный</div>
          <h3 class="pricing-title">{{ item.title }}</h3>
          <div class="pricing-price">{{ item.price }}</div>
          <p class="pricing-desc">{{ item.text }}</p>
          <ul class="pricing-features">
            <li v-for="(feat, fIdx) in item.features" :key="fIdx">
              <UIcon name="i-lucide-check" class="text-primary" /> {{ feat }}
            </li>
          </ul>
          <UButton :to="item.button_url || '/demo'" :color="item.featured ? 'primary' : 'neutral'" :variant="item.featured ? 'solid' : 'outline'" block size="lg" style="margin-top: auto;">
            {{ item.button_text || 'Выбрать' }}
          </UButton>
        </article>
      </div>
    </div>
  </section>

  <!-- FAQ BLOCK -->
  <section v-else-if="block.block_type === 'faq'" :class="['section-tight', layoutClasses]">
    <div class="container" style="max-width: 800px;">
      <span v-if="block.eyebrow" class="eyebrow">{{ block.eyebrow }}</span>
      <h2 v-if="block.title" class="section-title">{{ block.title }}</h2>
      <div v-if="block.body" class="lead rich-body" v-html="block.body" />
      
      <div class="faq-list">
        <details v-for="(item, index) in items" :key="index" class="faq-item">
          <summary class="faq-summary">
            {{ item.title }}
            <UIcon name="i-lucide-chevron-down" class="faq-icon" />
          </summary>
          <div class="faq-content">
            <p>{{ item.text }}</p>
          </div>
        </details>
      </div>
    </div>
  </section>

  <!-- TESTIMONIALS BLOCK -->
  <section v-else-if="block.block_type === 'testimonials'" :class="['section', layoutClasses]">
    <div class="container">
      <span v-if="block.eyebrow" class="eyebrow">{{ block.eyebrow }}</span>
      <h2 v-if="block.title" class="section-title">{{ block.title }}</h2>
      
      <div class="testimonials-grid">
        <article v-for="(item, index) in items" :key="index" class="testimonial-card card card-pad">
          <div class="testimonial-content">"{{ item.text }}"</div>
          <div class="testimonial-author">
            <img v-if="item.image" :src="item.image" :alt="item.title" class="author-avatar" />
            <div v-else class="author-avatar-placeholder"><UIcon name="i-lucide-user" /></div>
            <div>
              <strong>{{ item.title }}</strong>
              <span>{{ item.role }}</span>
            </div>
          </div>
        </article>
      </div>
    </div>
  </section>

  <!-- LOGOS BLOCK -->
  <section v-else-if="block.block_type === 'logos'" :class="['section-tight', layoutClasses]">
    <div class="container text-center">
      <span v-if="block.eyebrow" class="eyebrow">{{ block.eyebrow }}</span>
      <h2 v-if="block.title" class="section-title" style="margin-top: 10px; font-size: 1.5rem;">{{ block.title }}</h2>
      
      <div class="logos-grid">
        <div v-for="(item, index) in items" :key="index" class="logo-item">
          <img :src="item.image" :alt="item.title || 'Логотип'" loading="lazy" />
        </div>
      </div>
    </div>
  </section>

  <!-- FORM BLOCK -->
  <CmsFormBlock
    v-else-if="block.block_type === 'form'"
    :class="layoutClasses"
    :block="block"
    :page-slug="pageSlug"
  />

  <!-- TEXT / GENERIC BLOCK -->
  <section v-else :class="['section', layoutClasses]">
    <div class="container">
      <div class="content-band">
        <div class="split-panel">
          <div>
            <span v-if="block.eyebrow" class="eyebrow">{{ block.eyebrow }}</span>
            <h2 v-if="block.title" class="section-title">{{ block.title }}</h2>
          </div>
          <div>
            <div v-if="block.body" class="lead text-lead rich-body" v-html="block.body" />
            <div v-if="items.length" class="module-list text-items">
              <div v-for="(item, index) in items" :key="index" class="module-row">
                <div class="icon-box"><UIcon :name="item.icon || 'i-lucide-check'" /></div>
                <div>
                  <h3>{{ item.title }}</h3>
                  <p>{{ item.text }}</p>
                </div>
              </div>
            </div>
            <!-- Optional CTA button in text block -->
            <div v-if="payload.button_text" class="text-block-cta">
              <UButton :to="payload.button_url || '#'" color="primary" trailing-icon="i-lucide-arrow-right">
                {{ payload.button_text }}
              </UButton>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import WaterFlowAnimation from '~/components/WaterFlowAnimation.vue'
import CmsFormBlock from '~/components/CmsFormBlock.vue'

export interface CmsBlock {
  id: number
  block_key: string
  block_type: string
  eyebrow?: string
  title?: string
  body?: string
  payload?: string
}

const props = defineProps<{
  block: CmsBlock
  pageSlug?: string
}>()

const payload = computed<Record<string, any>>(() => {
  try {
    return JSON.parse(props.block.payload || '{}')
  } catch {
    return {}
  }
})

const items = computed<Array<Record<string, any>>>(() => {
  return Array.isArray(payload.value.items) ? payload.value.items : []
})

// Первый экран главной показывает живую карту в окне программы; в CMS вид задаётся полем visual: 'map' | 'image'.
const heroVisual = computed(() => payload.value.visual || (props.pageSlug === 'home' ? 'map' : 'image'))

const layoutClasses = computed(() => {
  const l = payload.value.layout || {}
  return [
    l.bg === 'dark' ? 'bg-dark' : l.bg === 'brand' ? 'bg-brand' : '',
    l.padding === 'tight' ? 'pad-tight' : l.padding === 'large' ? 'pad-large' : '',
    l.align === 'center' ? 'text-center' : '',
    l.hiddenMobile ? 'hidden-mobile' : ''
  ].filter(Boolean).join(' ')
})

// Lightbox for gallery
const lightboxRef = ref<HTMLDialogElement | null>(null)
const lightboxIndex = ref(0)

const openLightbox = (index: number) => {
  lightboxIndex.value = index
  lightboxRef.value?.showModal()
}

const closeLightbox = () => {
  lightboxRef.value?.close()
}
</script>

<style scoped>
.bg-dark { background-color: var(--dark); color: var(--on-dark); }
.bg-brand { background-color: var(--sirius-red, #ff2c49); color: white; }
.bg-dark .section-title, .bg-dark .eyebrow, .bg-dark .rich-body, .bg-dark p, .bg-dark h2, .bg-dark h3,
.bg-brand .section-title, .bg-brand .eyebrow, .bg-brand .rich-body, .bg-brand p, .bg-brand h2, .bg-brand h3 { color: white !important; }
.bg-dark .card, .bg-brand .card { background-color: transparent; border: 1px solid var(--line-dark); }
.bg-dark .eyebrow { color: #ff6b5e !important; }
.bg-dark .lead, .bg-dark p { color: var(--on-dark-muted) !important; }
.pad-tight { padding-top: 32px !important; padding-bottom: 32px !important; }
.pad-large { padding-top: 120px !important; padding-bottom: 120px !important; }
.text-center { text-align: center; }
.text-center .metric-grid, .text-center .grid-3 { justify-content: center; }
.text-center .split-panel, .text-center .split { flex-direction: column; align-items: center; text-align: center; }

@media (max-width: 768px) {
  .hidden-mobile { display: none !important; }
}

.dynamic-hero {
  padding: 136px 0 80px;
  border-bottom: 1px solid var(--line);
}

/* Широкий первый экран: заголовок сверху, окно программы с картой на всю ширину. */
.hero-wide .hero-grid {
  grid-template-columns: minmax(0, 1fr);
  gap: 48px;
}

.hero-wide .display-title {
  max-width: 1040px;
  font-size: clamp(2.6rem, 6vw, 5rem);
}

.hero-wide .lead {
  max-width: 760px;
}

.hero-demo {
  min-width: 0;
}

.hero-grid {
  display: grid;
  grid-template-columns: minmax(0, 0.92fr) minmax(360px, 1.08fr);
  gap: 38px;
  align-items: center;
}

.hero-copy {
  min-width: 0;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 28px;
}

.hero-media {
  padding: 8px;
  border-radius: var(--radius);
  background: var(--dark);
}

.dynamic-cards,
.dynamic-metrics {
  margin-top: 28px;
}

.dynamic-cards h3 {
  margin: 22px 0 8px;
  color: var(--ink);
  font-family: var(--serif);
  font-size: 1.4rem;
  font-weight: 400;
  line-height: 1.2;
}

.dynamic-cards p {
  margin: 0;
  color: var(--muted);
  line-height: 1.65;
}

.cta-panel {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 32px;
  padding: 48px;
  border-radius: var(--radius);
  color: var(--on-dark);
  background: var(--dark);
}

.cta-panel .eyebrow {
  color: #ff6b5e;
}

.cta-panel h2 {
  max-width: 720px;
  margin: 14px 0 0;
  color: var(--on-dark);
  font-family: var(--serif);
  font-size: clamp(1.9rem, 3.4vw, 2.8rem);
  font-weight: 400;
  line-height: 1.1;
  letter-spacing: -0.015em;
}

.cta-panel .rich-body {
  max-width: 680px;
  margin: 14px 0 0;
  color: var(--on-dark-muted);
  font-family: var(--serif);
  font-size: 1.12rem;
}

/* На тёмной плашке основная кнопка — светлая. */
.cta-panel :deep(a[class*="bg-primary"]),
.cta-panel :deep(a[class*="bg-(--ui-primary)"]) {
  color: var(--ink);
  background: var(--on-dark);
}

.split {
  display: grid;
  grid-template-columns: 0.9fr 1.1fr;
  gap: 48px;
  align-items: center;
}

.flow-card {
  height: 360px;
  overflow: hidden;
  border: 1px solid var(--line-dark);
  border-radius: var(--radius);
  background: var(--dark-2);
}

.text-lead {
  margin-top: 0;
}

.text-items {
  margin-top: 18px;
}

.text-block-cta {
  margin-top: 24px;
}

/* Gallery */
.gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
  margin-top: 28px;
}

.gallery-item {
  position: relative;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  overflow: hidden;
  cursor: zoom-in;
  background: var(--paper-2);
  aspect-ratio: 4 / 3;
}

.gallery-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.5s cubic-bezier(0.2, 0.8, 0.2, 1);
}

.gallery-item:hover img {
  transform: scale(1.04);
}

.gallery-caption {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 8px 12px;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.6));
  color: white;
  font-size: 0.82rem;
  font-weight: 600;
}

/* Lightbox */
.lightbox-dialog {
  position: fixed;
  inset: 0;
  width: 100%;
  height: 100%;
  max-width: 100%;
  max-height: 100%;
  border: 0;
  padding: 0;
  background: rgba(0, 0, 0, 0.92);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  gap: 16px;
}

.lightbox-dialog::backdrop {
  background: transparent;
}

.lightbox-img {
  max-width: 90vw;
  max-height: 80vh;
  object-fit: contain;
  border-radius: 6px;
}

.lightbox-caption {
  color: rgba(255, 255, 255, 0.75);
  font-size: 0.9rem;
}

.lightbox-close {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 42px;
  height: 42px;
  border: 0;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.15);
  color: white;
  cursor: pointer;
  display: grid;
  place-items: center;
  font-size: 1.2rem;
  transition: background 0.2s;
}

.lightbox-close:hover {
  background: rgba(255, 255, 255, 0.25);
}

.lightbox-prev,
.lightbox-next {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 48px;
  height: 48px;
  border: 0;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.15);
  color: white;
  cursor: pointer;
  display: grid;
  place-items: center;
  font-size: 1.3rem;
  transition: background 0.2s;
}

.lightbox-prev { left: 20px; }
.lightbox-next { right: 20px; }
.lightbox-prev:hover,
.lightbox-next:hover { background: rgba(255, 255, 255, 0.3); }

/* Rich body HTML */
:deep(.rich-body p) { margin: 0 0 0.75em; }
:deep(.rich-body ul) { list-style: disc; padding-left: 20px; margin-bottom: 0.75em; }
:deep(.rich-body ol) { list-style: decimal; padding-left: 20px; margin-bottom: 0.75em; }
:deep(.rich-body li) { margin-bottom: 0.3em; }
:deep(.rich-body a) { color: var(--ink); text-decoration: underline; text-decoration-color: var(--sirius-red); text-underline-offset: 3px; }
:deep(.rich-body strong), :deep(.rich-body b) { font-weight: 700; }

@media (max-width: 900px) {
  .hero-grid, .split { grid-template-columns: 1fr; }
  .cta-panel { align-items: flex-start; flex-direction: column; padding: 32px 24px; }
}

@media (max-width: 640px) {
  .dynamic-hero { padding: 104px 0 56px; }
  .gallery-grid { grid-template-columns: 1fr 1fr; }
}

/* Pricing */
.pricing-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px; margin-top: 32px; }
.pricing-card { position: relative; display: flex; flex-direction: column; padding: 32px; border-radius: var(--radius); border: 1px solid var(--line); background: var(--surface); }
.pricing-card.is-featured { border-color: var(--ink); box-shadow: inset 0 3px 0 var(--sirius-red); }
.pricing-badge { position: absolute; top: -12px; left: 50%; transform: translateX(-50%); background: var(--sirius-red); color: white; padding: 4px 12px; border-radius: var(--radius-sm); font-family: var(--mono); font-size: 0.7rem; font-weight: 500; text-transform: uppercase; letter-spacing: 0.08em; }
.pricing-title { font-size: 1.2rem; font-weight: 700; margin: 0 0 12px; }
.pricing-price { font-family: var(--serif); font-size: 2.8rem; font-weight: 400; margin: 0 0 8px; color: var(--ink); }
.pricing-desc { color: var(--muted); font-size: 0.95rem; margin: 0 0 24px; }
.pricing-features { list-style: none; padding: 0; margin: 0 0 32px; flex-grow: 1; }
.pricing-features li { display: flex; align-items: flex-start; gap: 10px; margin-bottom: 12px; font-size: 0.95rem; color: var(--ink); }
.text-primary { color: var(--sirius-red); flex-shrink: 0; margin-top: 2px; }

/* FAQ */
.faq-list { display: flex; flex-direction: column; margin-top: 32px; border-bottom: 1px solid var(--line); }
.faq-item { border-top: 1px solid var(--line); overflow: hidden; }
.faq-summary { display: flex; justify-content: space-between; align-items: center; gap: 16px; padding: 22px 0; color: var(--ink); font-family: var(--serif); font-size: 1.3rem; cursor: pointer; user-select: none; list-style: none; }
.faq-summary::-webkit-details-marker { display: none; }
.faq-icon { transition: transform 0.2s; color: var(--muted); }
.faq-item[open] .faq-icon { transform: rotate(180deg); }
.faq-content { padding: 0 0 22px; color: var(--muted); line-height: 1.65; animation: faq-open 0.3s ease; }
@keyframes faq-open { from { opacity: 0; transform: translateY(-6px); } }
.faq-content p { margin: 0; }

/* Testimonials */
.testimonials-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 24px; margin-top: 32px; }
.testimonial-card { display: flex; flex-direction: column; justify-content: space-between; }
.testimonial-content { font-family: var(--serif); font-size: 1.3rem; line-height: 1.5; color: var(--ink); margin-bottom: 24px; }
.testimonial-author { display: flex; align-items: center; gap: 16px; }
.author-avatar, .author-avatar-placeholder { width: 48px; height: 48px; border-radius: 50%; object-fit: cover; }
.author-avatar-placeholder { background: var(--paper-2); display: grid; place-items: center; color: var(--muted); }
.testimonial-author strong { display: block; font-weight: 700; color: var(--ink); }
.testimonial-author span { display: block; font-size: 0.85rem; color: var(--muted); }

/* Logos */
.logos-grid { display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: 40px; margin-top: 32px; opacity: 0.7; }
.logo-item { width: 140px; height: 60px; display: flex; justify-content: center; align-items: center; filter: grayscale(100%); transition: filter 0.2s, opacity 0.2s; }
.logo-item:hover { filter: grayscale(0%); opacity: 1; }
.logo-item img { max-width: 100%; max-height: 100%; object-fit: contain; }
</style>
