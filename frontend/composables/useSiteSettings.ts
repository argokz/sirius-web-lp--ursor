export const useSiteSettings = () => {
  const config = useRuntimeConfig()

  return useLazyAsyncData<Record<string, string>>(
    'site-settings',
    async () => {
      try {
        return await $fetch<Record<string, string>>(`${config.public.apiBase}/api/site-settings`, {
          timeout: 900
        })
      } catch {
        return {}
      }
    },
    {
      server: false,
      default: () => ({})
    }
  )
}
