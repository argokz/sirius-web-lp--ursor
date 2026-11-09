import type { Ref } from 'vue'

/**
 * true, когда элемент впервые дошёл до экрана (дальше не сбрасывается) — для инфографики,
 * которая рисуется один раз. Без IntersectionObserver считается видимым сразу.
 */
export function useInView(target: Ref<HTMLElement | null>, threshold = 0.3): Ref<boolean> {
  const inView = ref(false)
  let observer: IntersectionObserver | null = null

  onMounted(() => {
    if (!target.value || typeof IntersectionObserver === 'undefined') {
      inView.value = true
      return
    }
    observer = new IntersectionObserver(([entry]) => {
      if (!entry?.isIntersecting) return
      inView.value = true
      observer?.disconnect()
    }, { threshold })
    observer.observe(target.value)
  })

  onBeforeUnmount(() => observer?.disconnect())
  return inView
}

/** Пользователь не просил убрать движение (на сервере — false: анимации стартуют только в браузере). */
export function useMotionAllowed(): Ref<boolean> {
  const allowed = ref(false)
  onMounted(() => {
    allowed.value = !window.matchMedia('(prefers-reduced-motion: reduce)').matches
  })
  return allowed
}
