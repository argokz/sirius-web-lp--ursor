<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card elevation="2">
          <v-card-title class="text-h5 text-center pa-6">
            Вход в систему
          </v-card-title>
          <v-card-text>
            <v-form ref="form" v-model="valid">
              <v-text-field
                v-model="email"
                label="Email"
                type="email"
                :rules="[rules.required, rules.email]"
                required
                prepend-inner-icon="mdi-email"
              />
              <v-text-field
                v-model="password"
                label="Пароль"
                type="password"
                :rules="[rules.required]"
                required
                prepend-inner-icon="mdi-lock"
              />
              <v-alert
                v-if="error"
                type="error"
                class="mt-4"
              >
                {{ error }}
              </v-alert>
              <v-btn
                color="primary"
                size="large"
                variant="elevated"
                block
                @click="handleLogin"
                :disabled="!valid || loading"
                :loading="loading"
                class="mt-4"
              >
                Войти
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref } from 'vue'

definePageMeta({
  layout: false
})

useHead({
  title: 'Вход - Сириус',
})

const { login } = useAuth()

const valid = ref(false)
const loading = ref(false)
const error = ref('')
const email = ref('')
const password = ref('')

const rules = {
  required: (value: string) => !!value || 'Обязательное поле',
  email: (value: string) => {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return pattern.test(value) || 'Некорректный email'
  }
}

const handleLogin = async () => {
  loading.value = true
  error.value = ''

  const result = await login(email.value, password.value)
  
  if (result.success) {
    navigateTo('/admin')
  } else {
    error.value = result.error || 'Ошибка входа'
  }
  
  loading.value = false
}
</script>

