import { readFileSync } from 'node:fs'

// Адреса справки для sitemap.xml — из данных, которые собирает scripts/sync-manual.mjs.
const manualUrls = () => {
  const manual = JSON.parse(readFileSync(new URL('./server/data/manual.json', import.meta.url), 'utf8'))
  const sectionUrls = manual.sections.map((section: { slug: string }) => `/docs/${section.slug}`)
  const pageUrls = Object.values(manual.pages).map((page: any) => ({ loc: page.url, lastmod: manual.generatedAt }))
  return ['/docs', '/docs/troubleshooting', ...sectionUrls, ...pageUrls]
}

const securityHeaders = {
  'X-Content-Type-Options': 'nosniff',
  'X-Frame-Options': 'SAMEORIGIN',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'Permissions-Policy': 'camera=(), microphone=(), geolocation=()',
  'Strict-Transport-Security': 'max-age=31536000; includeSubDomains'
}

export default defineNuxtConfig({
  ssr: true,
  routeRules: {
    '/**': { headers: securityHeaders },
    // Снимки справки меняются только вместе с инструкцией (ролики — server/routes/docs-media).
    '/manual/**': { headers: { ...securityHeaders, 'Cache-Control': 'public, max-age=604800' } }
  },
  modules: ['@pinia/nuxt', '@nuxt/image', '@nuxtjs/sitemap', '@nuxt/ui'],
  css: [
    '~/assets/css/main.css'
  ],
  // Сайт рисуется только в светлой «бумажной» теме.
  ui: {
    colorMode: false
  },
  // Шрифты загружаются на сервер сборки и отдаются с сайта; кириллица обязательна.
  fonts: {
    defaults: {
      subsets: ['cyrillic', 'cyrillic-ext', 'latin', 'latin-ext'],
      weights: [400, 500, 600, 700]
    },
    families: [
      { name: 'Inter', provider: 'google', global: true, weights: [400, 500, 600, 700] },
      { name: 'Source Serif 4', provider: 'google', global: true, weights: [400, 500], styles: ['normal', 'italic'] },
      { name: 'JetBrains Mono', provider: 'google', global: true, weights: [400, 500] }
    ]
  },
  runtimeConfig: {
    /** Ролики справки (scripts/sync-manual.mjs): NUXT_MANUAL_MEDIA_DIR, по умолчанию manual-media в рабочей папке */
    manualMediaDir: '',
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
        { rel: 'icon', type: 'image/png', sizes: '16x16', href: '/favicon-16x16.png' },
        { rel: 'icon', type: 'image/png', sizes: '32x32', href: '/favicon-32x32.png' },
        { rel: 'apple-touch-icon', sizes: '180x180', href: '/apple-touch-icon.png' },
        { rel: 'manifest', href: '/manifest.json' }
      ]
    }
  },
  site: {
    url: 'https://itwin.kz'
  },
  sitemap: {
    exclude: ['/admin/**', '/login'],
    urls: manualUrls
  },
  typescript: {
    strict: false,
    typeCheck: false
  },
  nitro: {
    compressPublicAssets: true,
    experimental: {
      wasm: true
    }
  }
})
