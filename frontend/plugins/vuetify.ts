import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'

export default defineNuxtPlugin((nuxtApp) => {
  const vuetify = createVuetify({
    components,
    directives,
    icons: {
      defaultSet: 'mdi',
      aliases,
      sets: {
        mdi,
      },
    },
    theme: {
      defaultTheme: 'light',
      themes: {
        light: {
          colors: {
            primary: '#6A1B9A',
            secondary: '#FF6F00',
            accent: '#FFC107',
            error: '#D32F2F',
            info: '#1976D2',
            success: '#388E3C',
            warning: '#F57C00',
          },
        },
      },
    },
    ssr: true, // Включаем SSR поддержку
  })

  nuxtApp.vueApp.use(vuetify)
})
