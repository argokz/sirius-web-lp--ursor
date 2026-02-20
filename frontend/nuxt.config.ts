// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  
  modules: [
    // Vuetify настраивается через plugin
  ],

  css: [
    '~/assets/css/main.css',
    'vuetify/styles',
    '@mdi/font/css/materialdesignicons.css'
  ],

  app: {
    head: {
      charset: 'utf-8',
      viewport: 'width=device-width, initial-scale=1',
      title: 'Сириус - ТГИД-07',
      meta: [
        { name: 'description', content: 'Автоматизированная система управления теплоснабжением ТГИД-07' },
        { name: 'theme-color', content: '#6A1B9A' }
      ],
      link: [
        { rel: 'icon', type: 'image/png', href: '/favicon.ico' },
        { rel: 'apple-touch-icon', href: '/apple-touch-icon.png' },
        { rel: 'manifest', href: '/manifest.json' }
      ]
    }
  },

  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE_URL || (process.env.NODE_ENV === 'production' ? 'https://itwin.kz/api-sirius' : 'http://localhost:8009')
    }
  },

  devServer: {
    port: 3006
  },
  
  // Если используете отдельный путь /sirius/ в nginx, раскомментируйте:
  // app: {
  //   baseURL: '/sirius/'
  // },

  ssr: true,
  
  vite: {
    optimizeDeps: {
      include: ['vuetify']
    },
    ssr: {
      noExternal: ['vuetify']
    }
  },
  
  nitro: {
    // Исключаем CSS файлы из серверного бандла
    experimental: {
      wasm: true
    }
  },
  
  // Настройка для правильной обработки CSS в SSR
  build: {
    transpile: ['vuetify']
  }
})
