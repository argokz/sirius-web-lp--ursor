export const useAnalytics = () => {
  const config = useRuntimeConfig()

  const loadGA = async () => {
    if (!import.meta.client || import.meta.dev) return

    try {
      const settings = await $fetch<Record<string, string>>(
        `${config.public.apiBase}/api/site-settings`
      )
      const gaId = settings.google_analytics_id?.trim()

      if (!gaId || !gaId.startsWith('G-')) return

      // Inject gtag.js script
      const script = document.createElement('script')
      script.async = true
      script.src = `https://www.googletagmanager.com/gtag/js?id=${gaId}`
      document.head.appendChild(script)

      // Initialize dataLayer
      ;(window as any).dataLayer = (window as any).dataLayer || []
      function gtag(...args: any[]) {
        ;(window as any).dataLayer.push(args)
      }
      gtag('js', new Date())
      gtag('config', gaId)
    } catch {
      // Silently fail - analytics is non-critical
    }
  }

  onMounted(loadGA)
}
