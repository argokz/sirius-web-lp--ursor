export const useStructuredData = () => {
  const route = useRoute()
  
  const organizationSchema = {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: 'ПКФ «Сириус»',
    url: 'https://itwin.kz',
    logo: 'https://itwin.kz/logo.png',
    description: 'Разработчик инженерных цифровых решений и систем управления теплоснабжением',
    contactPoint: {
      '@type': 'ContactPoint',
      contactType: 'customer service',
      email: 'info@itwin.kz'
    }
  }

  const productSchema = {
    '@context': 'https://schema.org',
    '@type': 'SoftwareApplication',
    name: 'ТГИД-07',
    applicationCategory: 'BusinessApplication',
    operatingSystem: 'Web',
    description: 'Автоматизированная система для теплогидравлического моделирования, ГИС-паспортизации и управления эксплуатацией тепловых сетей',
    offers: {
      '@type': 'Offer',
      priceCurrency: 'KZT',
      availability: 'https://schema.org/InStock'
    }
  }

  const websiteSchema = {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    name: 'ТГИД-07 — ПКФ «Сириус»',
    url: 'https://itwin.kz',
    potentialAction: {
      '@type': 'SearchAction',
      target: 'https://itwin.kz/docs?q={search_term_string}',
      'query-input': 'required name=search_term_string'
    }
  }

  useHead({
    script: [
      {
        type: 'application/ld+json',
        innerHTML: JSON.stringify(organizationSchema)
      },
      ...(route.path === '/product' ? [{
        type: 'application/ld+json',
        innerHTML: JSON.stringify(productSchema)
      }] : []),
      {
        type: 'application/ld+json',
        innerHTML: JSON.stringify(websiteSchema)
      }
    ] as any
  })
}

