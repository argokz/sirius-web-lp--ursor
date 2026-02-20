<template>
  <v-container class="my-10">
    <v-row>
      <v-col cols="12" class="text-center mb-8">
        <h1 class="text-h3 mb-4">Контакты</h1>
        <p class="text-h6 text-grey">Свяжитесь с нами любым удобным способом</p>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="6">
        <v-card elevation="2">
          <v-card-title>Оставьте сообщение</v-card-title>
          <v-card-text>
            <v-form ref="form" v-model="valid">
              <v-text-field
                v-model="form.name"
                label="Ваше имя"
                :rules="[rules.required]"
                required
              />
              <v-text-field
                v-model="form.email"
                label="Email"
                type="email"
                :rules="[rules.required, rules.email]"
                required
              />
              <v-text-field
                v-model="form.phone"
                label="Телефон"
              />
              <v-textarea
                v-model="form.message"
                label="Сообщение"
                :rules="[rules.required]"
                required
              />
              <v-btn
                color="primary"
                variant="elevated"
                @click="submitForm"
                :disabled="!valid"
              >
                Отправить
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="12" md="6">
        <v-card elevation="2">
          <v-card-title>Контактная информация</v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item prepend-icon="mdi-email">
                <v-list-item-title>Email</v-list-item-title>
                <v-list-item-subtitle>info@itwin.kz</v-list-item-subtitle>
              </v-list-item>
              <v-list-item prepend-icon="mdi-phone">
                <v-list-item-title>Телефон</v-list-item-title>
                <v-list-item-subtitle>+7 (XXX) XXX-XX-XX</v-list-item-subtitle>
              </v-list-item>
              <v-list-item prepend-icon="mdi-whatsapp">
                <v-list-item-title>WhatsApp</v-list-item-title>
                <v-list-item-subtitle>
                  <v-btn
                    color="success"
                    size="small"
                    href="https://wa.me/7XXXXXXXXXX"
                    target="_blank"
                  >
                    Написать в WhatsApp
                  </v-btn>
                </v-list-item-subtitle>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'

useSEO({
  title: 'Контакты - Сириус',
  description: 'Свяжитесь с компанией Сириус для получения информации о системе ТГИД-07'
})
useStructuredData()

const valid = ref(false)
const form = reactive({
  name: '',
  email: '',
  phone: '',
  message: ''
})

const rules = {
  required: (value: string) => !!value || 'Обязательное поле',
  email: (value: string) => {
    const pattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    return pattern.test(value) || 'Некорректный email'
  }
}

const submitForm = async () => {
  try {
    const config = useRuntimeConfig()
    await $fetch(`${config.public.apiBase}/api/contact`, {
      method: 'POST',
      body: form
    })
    // Show success message
    alert('Сообщение успешно отправлено!')
    // Reset form
    Object.keys(form).forEach(key => {
      form[key as keyof typeof form] = ''
    })
  } catch (error) {
    console.error('Error submitting form:', error)
    alert('Произошла ошибка при отправке сообщения')
  }
}
</script>

