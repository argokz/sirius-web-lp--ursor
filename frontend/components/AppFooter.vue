<template>
  <footer class="site-footer">
    <div class="container footer-grid">
      <div>
        <SiriusLogo :width="162" />
        <p class="footer-text">{{ footerText }}</p>
        <div class="footer-badge">
          <UIcon name="i-lucide-shield-check" />
          Готовый к внедрению интерфейс
        </div>
      </div>

      <div>
        <h3>Продукт</h3>
        <NuxtLink v-for="link in productLinks" :key="link.to" :to="link.to">{{ link.title }}</NuxtLink>
      </div>

      <div>
        <h3>Компания</h3>
        <NuxtLink v-for="link in companyLinks" :key="link.to" :to="link.to">{{ link.title }}</NuxtLink>
      </div>

      <div>
        <h3>Связь</h3>
        <a :href="`mailto:${contactEmail}`">{{ contactEmail }}</a>
        <a v-if="contactPhone" :href="`tel:${contactPhone}`">{{ contactPhone }}</a>
        <NuxtLink to="/demo">Запросить демо</NuxtLink>
        <NuxtLink to="/contacts">Контакты</NuxtLink>
      </div>
    </div>

    <div class="container footer-bottom">
      <span>&copy; {{ new Date().getFullYear() }} {{ companyName }}. {{ productName }}</span>
      <span>itwin.kz</span>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const { data: settings } = useSiteSettings()

const setting = (key: string, fallback: string) => computed(() => settings.value?.[key] || fallback)

const companyName = setting('company_name', 'ПКФ «Сириус»')
const productName = setting('product_name', 'ТГИД-07')
const contactEmail = setting('contact_email', 'info@itwin.kz')
const contactPhone = setting('contact_phone', '')
const footerText = setting(
  'footer_text',
  'ТГИД-07 — профессиональный программный комплекс ПКФ «Сириус» для цифрового моделирования, паспортизации и предиктивного управления тепловыми сетями.'
)

const productLinks = [
  { title: 'О системе', to: '/product' },
  { title: 'Моделирование', to: '/modeling' },
  { title: 'ГИС', to: '/gis' },
  { title: 'Эксплуатация', to: '/maintenance' },
  { title: 'Web-версия', to: '/web-version' },
  { title: 'Документация', to: '/docs' },
  { title: 'Обучение', to: '/learn' }
]

const companyLinks = [
  { title: 'О компании', to: '/about' },
  { title: 'Решения', to: '/solutions' },
  { title: 'Возможности', to: '/features' },
  { title: 'Блог', to: '/blog' },
  { title: 'Контакты', to: '/contacts' }
]
</script>

<style scoped>
.site-footer {
  padding: 72px 0 28px;
  color: var(--on-dark-muted);
  background: var(--dark);
  border-top: 3px solid var(--sirius-red);
}

.footer-grid {
  display: grid;
  grid-template-columns: 1.4fr repeat(3, 1fr);
  gap: 36px;
}

.footer-text {
  max-width: 420px;
  margin: 22px 0;
  color: var(--on-dark-muted);
  font-family: var(--serif);
  font-size: 1.08rem;
  line-height: 1.6;
}

.footer-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 10px;
  border: 1px solid var(--line-dark);
  border-radius: var(--radius-sm);
  color: var(--on-dark);
  font-family: var(--mono);
  font-size: 0.72rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}

h3 {
  margin: 0 0 16px;
  color: #ff6b5e;
  font-family: var(--mono);
  font-size: 0.72rem;
  font-weight: 500;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

a {
  display: block;
  width: fit-content;
  margin: 0 0 11px;
  color: var(--on-dark-muted);
  background: linear-gradient(currentColor, currentColor) 0 100% / 0 1px no-repeat;
  transition: color 0.2s ease, background-size 0.3s ease;
}

a:hover {
  color: var(--on-dark);
  background-size: 100% 1px;
}

.footer-bottom {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  margin-top: 42px;
  padding-top: 24px;
  border-top: 1px solid var(--line-dark);
  color: #8f8a7d;
  font-family: var(--mono);
  font-size: 0.74rem;
  letter-spacing: 0.04em;
}

@media (max-width: 900px) {
  .footer-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 640px) {
  .footer-grid {
    grid-template-columns: 1fr;
  }

  .footer-bottom {
    flex-direction: column;
  }
}
</style>
