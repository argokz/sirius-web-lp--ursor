export const useStructuredData = () => {
  const route = useRoute()
  
  const organizationSchema = {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: 'Сириус',
    url: 'https://itwin.kz',
    logo: 'https://itwin.kz/logo.png',
    description: 'Автоматизированная система управления теплоснабжением ТГИД-07',
    contactPoint: {
      '@type': 'ContactPoint',
      telephone: '+7-XXX-XXX-XX-XX',
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
    description: 'Многофункциональная автоматизированная система для цифрового моделирования и управления режимами теплоснабжения',
    offers: {
      '@type': 'Offer',
      priceCurrency: 'KZT',
      availability: 'https://schema.org/InStock'
    }
  }

  const websiteSchema = {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    name: 'Сириус - ТГИД-07',
    url: 'https://itwin.kz',
    potentialAction: {
      '@type': 'SearchAction',
      target: 'https://itwin.kz/search?q={search_term_string}',
      'query-input': 'required name=search_term_string'
    }
  }

  useHead({
    script: [
      {
        type: 'application/ld+json',
        children: JSON.stringify(organizationSchema)
      },
      ...(route.path === '/product' ? [{
        type: 'application/ld+json',
        children: JSON.stringify(productSchema)
      }] : []),
      {
        type: 'application/ld+json',
        children: JSON.stringify(websiteSchema)
      }
    ]
  })
}

