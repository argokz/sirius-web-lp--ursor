export default defineNuxtConfig({
  ssr: true,
  modules: ['@pinia/nuxt', '@nuxt/image', '@nuxtjs/sitemap'],
  css: ['~/assets/css/main.css'],
  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE_URL || 'http://localhost:8009'
    }
  },
  app: {
    head: {
      htmlAttrs: {
        lang: 'ru'
      },
      meta: [
        { name: 'viewport', content: 'width=device-width, initial-scale=1' }
      ],
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
        { rel: 'manifest', href: '/manifest.json' }
      ]
    }
  },
  sitemap: {
    siteUrl: 'https://itwin.kz'
  },
  routeRules: {
    '/admin/**': {
      robots: false
    },
    '/login': {
      robots: false
    }
  },
  typescript: {
    strict: false,
    typeCheck: false
  }
})
