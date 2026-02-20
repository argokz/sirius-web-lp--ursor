<template>
  <v-container class="my-10">
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card elevation="2">
          <v-card-title class="text-h4 text-center pa-6">
            Заявка на демо-версию ТГИД-07
          </v-card-title>
          <v-card-text>
            <v-form ref="form" v-model="valid">
              <v-text-field
                v-model="form.full_name"
                label="ФИО"
                :rules="[rules.required]"
                required
                prepend-inner-icon="mdi-account"
              />
              <v-text-field
                v-model="form.email"
                label="Email"
                type="email"
                :rules="[rules.required, rules.email]"
                required
                prepend-inner-icon="mdi-email"
              />
              <v-text-field
                v-model="form.phone"
                label="Телефон"
                prepend-inner-icon="mdi-phone"
              />
              <v-text-field
                v-model="form.company"
                label="Компания"
                prepend-inner-icon="mdi-office-building"
              />
              <v-textarea
                v-model="form.message"
                label="Дополнительная информация"
                rows="4"
                prepend-inner-icon="mdi-message-text"
              />
              <v-btn
                color="primary"
                size="large"
                variant="elevated"
                block
                @click="submitRequest"
                :disabled="!valid || loading"
                :loading="loading"
              >
                Отправить заявку
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>

        <v-alert
          v-if="success"
          type="success"
          class="mt-4"
        >
          Заявка успешно отправлена! Мы свяжемся с вами в ближайшее время.
        </v-alert>

        <v-alert
          v-if="error"
          type="error"
          class="mt-4"
        >
          {{ error }}
        </v-alert>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'

useSEO({
  title: 'Заявка на демо - ТГИД-07',
  description: 'Оставьте заявку на получение демо-версии системы ТГИД-07'
})
useStructuredData()

const valid = ref(false)
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

const rules = {
  required: (value: string) => !!value || 'Обязательное поле',
  email: (value: string) => {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return pattern.test(value) || 'Некорректный email'
  }
}

const submitRequest = async () => {
  loading.value = true
  error.value = ''
  success.value = false

  try {
    const config = useRuntimeConfig()
    const response = await $fetch(`${config.public.apiBase}/api/demo-requests`, {
      method: 'POST',
      body: form
    })

    success.value = true
    // Reset form
    Object.keys(form).forEach(key => {
      form[key as keyof typeof form] = ''
    })
  } catch (err: any) {
    error.value = err.message || 'Произошла ошибка при отправке заявки'
  } finally {
    loading.value = false
  }
}
</script>

