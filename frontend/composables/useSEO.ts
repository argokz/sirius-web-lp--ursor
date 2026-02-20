export const useSEO = (options: {
  title?: string
  description?: string
  image?: string
  url?: string
  type?: string
}) => {
  const config = useRuntimeConfig()
  const route = useRoute()
  
  const baseUrl = 'https://itwin.kz'
  const defaultImage = `${baseUrl}/logo.png`
  
  const title = options.title || 'Сириус - ТГИД-07'
  const description = options.description || 'Автоматизированная система управления теплоснабжением ТГИД-07'
  const image = options.image || defaultImage
  const url = options.url || `${baseUrl}${route.path}`
  const type = options.type || 'website'

  useHead({
    title,
    meta: [
      { name: 'description', content: description },
      { name: 'keywords', content: 'ТГИД-07, теплоснабжение, автоматизация, Сириус' },
      
      // Open Graph
      { property: 'og:title', content: title },
      { property: 'og:description', content: description },
      { property: 'og:image', content: image },
      { property: 'og:url', content: url },
      { property: 'og:type', content: type },
      { property: 'og:site_name', content: 'Сириус' },
      { property: 'og:locale', content: 'ru_RU' },
      
      // Twitter Card
      { name: 'twitter:card', content: 'summary_large_image' },
      { name: 'twitter:title', content: title },
      { name: 'twitter:description', content: description },
      { name: 'twitter:image', content: image },
      
      // WhatsApp
      { property: 'og:image:width', content: '1200' },
      { property: 'og:image:height', content: '630' },
    ],
    link: [
      { rel: 'canonical', href: url }
    ]
  })
}

