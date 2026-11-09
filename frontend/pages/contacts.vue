<template>
  <CmsPageRenderer slug="contacts">
    <div class="page">
    <section class="page-hero">
      <div class="container">
        <UBadge color="primary" variant="subtle" size="lg">Контакты</UBadge>
        <h1 class="display-title">Свяжитесь с {{ companyName }}</h1>
        <p class="lead">
          Расскажите о вашей сети и задачах: мы подскажем, как лучше показать {{ productName }} и подготовить демонстрацию.
        </p>
      </div>
    </section>

    <section class="section-tight">
      <div class="container contact-grid">
        <form class="card card-pad" @submit.prevent="submit">
          <label class="field-label">Имя</label>
          <input v-model="form.name" class="field" required>
          <label class="field-label">Email</label>
          <input v-model="form.email" class="field" type="email" required>
          <label class="field-label">Телефон</label>
          <input v-model="form.phone" class="field">
          <label class="field-label">Сообщение</label>
          <textarea v-model="form.message" class="field" rows="5" required></textarea>
          <button class="btn-link btn-primary" type="submit" :disabled="loading">
            {{ loading ? 'Отправляем...' : 'Отправить сообщение' }}
          </button>
          <p v-if="success" class="form-success">Сообщение отправлено.</p>
          <p v-if="error" class="form-error">{{ error }}</p>
        </form>

        <div class="card card-pad contact-card">
          <SiriusLogo :width="171" />
          <div>
            <span>Email</span>
            <a :href="`mailto:${contactEmail}`">{{ contactEmail }}</a>
          </div>
          <div v-if="contactPhone">
            <span>Телефон</span>
            <a :href="`tel:${contactPhone}`">{{ contactPhone }}</a>
          </div>
          <div v-if="contactAddress">
            <span>Адрес</span>
            <p>{{ contactAddress }}</p>
          </div>
          <div v-if="telegramUrl || whatsappUrl" class="messenger-row">
            <a v-if="telegramUrl" :href="telegramUrl" target="_blank" rel="noopener noreferrer">
              <UIcon name="i-lucide-send" />
              Telegram
            </a>
            <a v-if="whatsappUrl" :href="whatsappUrl" target="_blank" rel="noopener noreferrer">
              <UIcon name="i-lucide-message-circle" />
              WhatsApp
            </a>
          </div>
          <div>
            <span>Демо</span>
            <NuxtLink to="/demo">Запросить демонстрацию</NuxtLink>
          </div>
          <div>
            <span>Справка</span>
            <NuxtLink to="/docs">Инструкции по всем функциям</NuxtLink>
          </div>
        </div>
      </div>
    </section>
    </div>
  </CmsPageRenderer>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from 'vue'

useSEO({
  title: 'Контакты — ПКФ «Сириус»',
  description: 'Контакты ПКФ «Сириус» и форма обратной связи.'
})

const config = useRuntimeConfig()
const { data: settings } = useSiteSettings()

const setting = (key: string, fallback: string) => computed(() => settings.value?.[key] || fallback)

const companyName = setting('company_name', 'ПКФ «Сириус»')
const productName = setting('product_name', 'ТГИД-07')
const contactEmail = setting('contact_email', 'info@itwin.kz')
const contactPhone = setting('contact_phone', '')
const contactAddress = setting('contact_address', '')
const telegramUrl = setting('telegram_url', '')
const whatsappUrl = setting('whatsapp_url', '')

const loading = ref(false)
const success = ref(false)
const error = ref('')
const form = reactive({ name: '', email: '', phone: '', message: '' })

const submit = async () => {
  loading.value = true
  success.value = false
  error.value = ''
  try {
    await $fetch(`${config.public.apiBase}/api/contact`, { method: 'POST', body: form })
    success.value = true
    Object.assign(form, { name: '', email: '', phone: '', message: '' })
  } catch (err: any) {
    error.value = err?.data?.detail || 'Не удалось отправить сообщение'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.page-hero {
  padding: 124px 0 56px;
}

.contact-grid {
  display: grid;
  grid-template-columns: 1fr 0.8fr;
  gap: 24px;
  align-items: start;
}

form {
  display: grid;
  gap: 10px;
}

button {
  margin-top: 8px;
}

.contact-card {
  display: grid;
  gap: 22px;
}

.contact-card span {
  display: block;
  color: var(--muted);
  font-weight: 800;
}

.contact-card a,
.contact-card p {
  margin: 6px 0 0;
  color: var(--sirius-red-dark);
  font-weight: 900;
}

.contact-card p {
  color: var(--ink);
  line-height: 1.55;
}

.messenger-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.messenger-row a {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 42px;
  padding: 0 14px;
  border-radius: 8px;
  color: white;
  background: var(--sirius-red);
}

.form-success {
  color: #166534;
  font-weight: 800;
}

.form-error {
  color: #991b1b;
  font-weight: 800;
}

@media (max-width: 840px) {
  .contact-grid {
    grid-template-columns: 1fr;
  }
}
</style>
