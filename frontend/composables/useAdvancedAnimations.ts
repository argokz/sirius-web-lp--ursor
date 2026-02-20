export const useAdvancedAnimations = () => {
  const initScrollAnimations = () => {
    if (process.client) {
      const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
      }

      const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('animate-in')
            // Для элементов с задержкой
            const delay = entry.target.getAttribute('data-delay')
            if (delay) {
              entry.target.style.animationDelay = `${delay}ms`
            }
          }
        })
      }, observerOptions)

      // Анимация для элементов с классом scroll-reveal
      document.querySelectorAll('.scroll-reveal').forEach((el) => {
        observer.observe(el)
      })

      // Parallax эффект
      let ticking = false
      const parallaxElements = document.querySelectorAll('.parallax-element')
      
      const updateParallax = () => {
        const scrolled = window.pageYOffset
        parallaxElements.forEach((el) => {
          const speed = parseFloat(el.getAttribute('data-speed') || '0.5')
          const yPos = -(scrolled * speed)
          ;(el as HTMLElement).style.transform = `translateY(${yPos}px)`
        })
        ticking = false
      }

      const requestTick = () => {
        if (!ticking) {
          window.requestAnimationFrame(updateParallax)
          ticking = true
        }
      }

      window.addEventListener('scroll', requestTick)
    }
  }

  const initCounterAnimation = (element: HTMLElement, target: number, duration: number = 2000) => {
    let start = 0
    const increment = target / (duration / 16)
    
    const updateCounter = () => {
      start += increment
      if (start < target) {
        element.textContent = Math.floor(start).toString()
        requestAnimationFrame(updateCounter)
      } else {
        element.textContent = target.toString()
      }
    }
    
    updateCounter()
  }

  const initTypingEffect = (element: HTMLElement, text: string, speed: number = 50) => {
    let i = 0
    element.textContent = ''
    
    const type = () => {
      if (i < text.length) {
        element.textContent += text.charAt(i)
        i++
        setTimeout(type, speed)
      }
    }
    
    type()
  }

  const initFloatingAnimation = (element: HTMLElement) => {
    const duration = parseFloat(element.getAttribute('data-duration') || '3')
    const distance = parseFloat(element.getAttribute('data-distance') || '20')
    
    element.style.animation = `float ${duration}s ease-in-out infinite`
    element.style.setProperty('--float-distance', `${distance}px`)
  }

  return {
    initScrollAnimations,
    initCounterAnimation,
    initTypingEffect,
    initFloatingAnimation
  }
}

