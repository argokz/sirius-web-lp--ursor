export default defineNuxtPlugin(() => {
  // Просмотры с dev-сервера не должны попадать в статистику сайта.
  if (import.meta.dev) return

  const router = useRouter()
  const config = useRuntimeConfig()
  let lastTracked = ''

  const send = (path: string) => {
    $fetch(`${config.public.apiBase}/api/analytics/page-view`, {
      method: 'POST',
      body: {
        path,
        title: document.title,
        referrer: document.referrer
      }
    }).catch(() => {})
  }

  const track = (path: string) => {
    // Первую загрузку видят и router.afterEach, и app:mounted — считаем её один раз.
    if (path === lastTracked) return
    lastTracked = path

    if (window.requestIdleCallback) {
      window.requestIdleCallback(() => send(path))
    } else {
      setTimeout(() => send(path), 700)
    }
  }

  router.afterEach((to) => {
    track(to.fullPath)
  })

  useNuxtApp().hook('app:mounted', () => {
    track(router.currentRoute.value.fullPath)
  })
})
