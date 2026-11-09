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
  const defaultImage = `${baseUrl}/og-sirius.jpg`
  
  const title = options.title || 'ТГИД-07 — ПКФ «Сириус»'
  const description = options.description || 'АСУП ТГИД-07 от ПКФ «Сириус»: цифровой контур моделирования, паспортизации и эксплуатации тепловых сетей.'
  const image = options.image || defaultImage
  const url = options.url || `${baseUrl}${route.path}`
  const type = options.type || 'website'

  useHead({
    title,
    meta: [
      { name: 'description', content: description },
      { name: 'keywords', content: 'ТГИД-07, ТГИД, теплоснабжение, автоматизация теплосетей, ПКФ Сириус, гидравлический расчет, ГИС теплосетей' },
      
      // Open Graph
      { property: 'og:title', content: title },
      { property: 'og:description', content: description },
      { property: 'og:image', content: image },
      { property: 'og:url', content: url },
      { property: 'og:type', content: type },
      { property: 'og:site_name', content: 'ПКФ «Сириус»' },
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

