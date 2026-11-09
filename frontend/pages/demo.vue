<template>
  <CmsPageRenderer slug="demo">
    <div class="page">
    <section class="page-hero">
      <div class="container demo-grid">
        <div>
          <UBadge color="primary" variant="subtle" size="lg">Демо</UBadge>
          <h1 class="display-title">Покажем ТГИД-07 на ваших сценариях</h1>
          <p class="lead">Оставьте заявку, и мы подготовим демонстрацию с фокусом на моделирование, ГИС, эксплуатацию, web-доступ или администрирование сайта.</p>
        </div>
        <form class="card card-pad demo-form" @submit.prevent="submitRequest">
          <label class="field-label">ФИО</label>
          <input v-model="form.full_name" class="field" required>
          <label class="field-label">Email</label>
          <input v-model="form.email" class="field" type="email" required>
          <label class="field-label">Телефон</label>
          <input v-model="form.phone" class="field">
          <label class="field-label">Компания</label>
          <input v-model="form.company" class="field">
          <label class="field-label">Что показать на демо</label>
          <textarea v-model="form.message" class="field" rows="4"></textarea>
          <button class="btn-link btn-primary" type="submit" :disabled="loading">
            {{ loading ? 'Отправляем...' : 'Отправить заявку' }}
          </button>
          <p v-if="success" class="form-success">Заявка отправлена. Мы свяжемся с вами.</p>
          <p v-if="error" class="form-error">{{ error }}</p>
        </form>
      </div>
    </section>
    </div>
  </CmsPageRenderer>
</template>

<script setup lang="ts">
useSEO({
  title: 'Запрос демонстрации ТГИД-07',
  description: 'Оставьте заявку на демонстрацию ТГИД-07 от ПКФ «Сириус».'
})

const config = useRuntimeConfig()
const loading = ref(false)
const success = ref(false)
const error = ref('')

const form = reactive({
  full_name: '',
  email: '',
  phone: '',
  company: '',
  message: ''
})

const submitRequest = async () => {
  loading.value = true
  success.value = false
  error.value = ''
  try {
    await $fetch(`${config.public.apiBase}/api/demo-requests`, { method: 'POST', body: form })
    success.value = true
    Object.assign(form, { full_name: '', email: '', phone: '', company: '', message: '' })
  } catch (err: any) {
    error.value = err?.data?.detail || 'Не удалось отправить заявку'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.page-hero { min-height: 100vh; display: grid; align-items: center; padding: 124px 0 70px; }
.demo-grid { display: grid; grid-template-columns: 1fr 0.78fr; gap: 42px; align-items: center; }
.demo-form { display: grid; gap: 10px; }
button { margin-top: 8px; }
.form-success { color: #166534; font-weight: 800; }
.form-error { color: #991b1b; font-weight: 800; }
@media (max-width: 900px) { .demo-grid { grid-template-columns: 1fr; } }
</style>
