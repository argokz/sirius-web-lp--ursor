export const useScrollAnimation = () => {
  const observeElements = () => {
    if (process.client) {
      setTimeout(() => {
        const observer = new IntersectionObserver(
          (entries) => {
            entries.forEach((entry) => {
              if (entry.isIntersecting) {
                entry.target.classList.add('visible')
                entry.target.classList.add('animate-in')

                const delay = entry.target.getAttribute('data-delay')
                if (delay) {
                  ; (entry.target as HTMLElement).style.transitionDelay = `${delay}ms`
                }

                // Once visible, we can stop observing if we want to save resources
                // observer.unobserve(entry.target)
              }
            })
          },
          {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
          }
        )

        // All reveal types
        const elements = document.querySelectorAll('.scroll-reveal, .scroll-reveal-left, .scroll-reveal-right, .scroll-reveal-scale, .stagger-children')
        elements.forEach((el) => {
          observer.observe(el)
        })

        // Parallax effect initialization
        const parallaxElements = document.querySelectorAll('.parallax-element')
        if (parallaxElements.length > 0) {
          let ticking = false
          const updateParallax = () => {
            const scrolled = window.pageYOffset
            parallaxElements.forEach((el) => {
              const speed = parseFloat(el.getAttribute('data-speed') || '0.5')
              const yPos = -(scrolled * speed)
                ; (el as HTMLElement).style.transform = `translateY(${yPos}px)`
            })
            ticking = false
          }

          const requestTick = () => {
            if (!ticking) {
              window.requestAnimationFrame(updateParallax)
              ticking = true
            }
          }

          window.addEventListener('scroll', requestTick, { passive: true })
        }
      }, 200) // Small delay to ensure DOM is ready
    }
  }

  return { observeElements }
}

