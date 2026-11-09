<template>
  <div class="login-page">
    <form class="login-card card card-pad" @submit.prevent="handleLogin">
      <SiriusLogo :width="171" />
      <div>
        <h1>Вход в CRM</h1>
        <p>Панель управления контентом, заявками, SEO и пользователями.</p>
      </div>
      <label class="field-label">Email</label>
      <input v-model="email" class="field" type="email" required autocomplete="email">
      <label class="field-label">Пароль</label>
      <input v-model="password" class="field" type="password" required autocomplete="current-password">
      <button class="btn-link btn-primary" type="submit" :disabled="loading">
        {{ loading ? 'Входим...' : 'Войти' }}
      </button>
      <p v-if="error" class="form-error">{{ error }}</p>
    </form>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: false
})

useHead({
  title: 'Вход в CRM - Sirius'
})

const { login, isAuthenticated } = useAuth()
const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

onMounted(() => {
  if (isAuthenticated.value) navigateTo('/admin')
})

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  const result = await login(email.value, password.value)
  loading.value = false
  if (result.success) {
    navigateTo('/admin')
  } else {
    error.value = result.error || 'Не удалось войти'
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 24px;
  background:
    radial-gradient(circle at 24% 20%, rgba(227, 6, 19, 0.16), transparent 28rem),
    #f8fafc;
}

.login-card {
  width: min(100%, 440px);
  display: grid;
  gap: 12px;
}

h1 {
  margin: 16px 0 6px;
  font-size: 2rem;
  font-weight: 930;
}

p {
  margin: 0;
  color: var(--muted);
}

.form-error {
  color: #991b1b;
  font-weight: 800;
}
</style>
