<template>
  <section v-if="!submitted" class="cms-form-block">
    <div class="container">
      <span v-if="block.eyebrow" class="eyebrow">{{ block.eyebrow }}</span>
      <h2 v-if="block.title" class="section-title">{{ block.title }}</h2>
      <p v-if="block.body" class="lead" v-html="block.body" />

      <form class="block-form" @submit.prevent="submitForm">
        <p v-if="formError" class="form-msg form-err">{{ formError }}</p>

        <div class="block-form-grid">
          <label>
            <span class="form-label">Имя *</span>
            <input v-model="fields.name" class="form-field" :placeholder="payload.name_placeholder || 'Ваше имя'" required />
          </label>
          <label>
            <span class="form-label">Email *</span>
            <input v-model="fields.email" type="email" class="form-field" :placeholder="payload.email_placeholder || 'email@example.com'" required />
          </label>
        </div>

        <label>
          <span class="form-label">Сообщение</span>
          <textarea v-model="fields.message" class="form-field" rows="4" :placeholder="payload.message_placeholder || 'Ваш вопрос или пожелание'" />
        </label>

        <button class="btn-link btn-primary" type="submit" :disabled="submitting">
          <UIcon v-if="submitting" name="i-lucide-loader-circle" class="spin" />
          {{ submitting ? 'Отправляем...' : (payload.submit_text || 'Отправить') }}
        </button>
      </form>
    </div>
  </section>

  <section v-else class="cms-form-block form-success">
    <div class="container">
      <div class="success-card">
        <div class="success-icon">
          <UIcon name="i-lucide-check-circle" />
        </div>
        <h2>Сообщение отправлено!</h2>
        <p>Мы свяжемся с вами в ближайшее время.</p>
        <button class="btn-link btn-secondary" type="button" @click="submitted = false">Отправить ещё</button>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { reactive, ref, computed } from 'vue'

const props = defineProps<{
  block: {
    eyebrow?: string
    title?: string
    body?: string
    payload?: string
  }
  pageSlug?: string
}>()

const config = useRuntimeConfig()

const payload = computed<Record<string, any>>(() => {
  try {
    return JSON.parse(props.block.payload || '{}')
  } catch {
    return {}
  }
})

const fields = reactive({ name: '', email: '', message: '' })
const submitting = ref(false)
const submitted = ref(false)
const formError = ref('')

const submitForm = async () => {
  formError.value = ''
  submitting.value = true
  try {
    await $fetch(`${config.public.apiBase}/api/site/form-submit`, {
      method: 'POST',
      body: {
        name: fields.name,
        email: fields.email,
        message: fields.message,
        page_slug: props.pageSlug || ''
      }
    })
    submitted.value = true
    Object.assign(fields, { name: '', email: '', message: '' })
  } catch (err: any) {
    formError.value = err?.data?.detail || 'Не удалось отправить. Попробуйте позже.'
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.cms-form-block {
  padding: var(--section-pad) 0;
}

.block-form {
  display: grid;
  gap: 16px;
  max-width: 640px;
  margin-top: 28px;
}

.block-form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.form-label {
  display: block;
  font-size: 0.82rem;
  font-weight: 800;
  color: #475569;
  margin-bottom: 6px;
  letter-spacing: 0.02em;
  text-transform: uppercase;
}

.form-field {
  display: block;
  width: 100%;
  min-height: 46px;
  padding: 10px 14px;
  border: 1px solid var(--line);
  border-radius: 8px;
  font-size: 0.95rem;
  background: white;
  transition: border-color 0.15s;
  outline: none;
}

.form-field:focus {
  border-color: #94a3b8;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.08);
}

textarea.form-field {
  min-height: 110px;
  resize: vertical;
  line-height: 1.6;
}

.form-msg {
  padding: 12px 16px;
  border-radius: 8px;
  font-weight: 700;
}

.form-err {
  background: #fee2e2;
  color: #991b1b;
}

.form-success {
  text-align: center;
}

.success-card {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
  padding: 48px 40px;
  border: 1px solid var(--line);
  border-radius: 16px;
  background: white;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

.success-icon {
  width: 64px;
  height: 64px;
  border-radius: 999px;
  background: #dcfce7;
  color: #16a34a;
  display: grid;
  place-items: center;
  font-size: 1.8rem;
}

.success-card h2 {
  margin: 0;
}

.success-card p {
  margin: 0;
  color: var(--muted);
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@media (max-width: 640px) {
  .block-form-grid {
    grid-template-columns: 1fr;
  }
}
</style>
