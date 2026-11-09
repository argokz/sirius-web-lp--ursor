/**
 * v-reveal — блок проявляется, когда доходит до экрана (как секции felt.com).
 * Значение — задержка в мс: v-reveal="120". Модификатор .stagger — дети по очереди.
 * На сервере ставится только data-reveal, прячет блок CSS и только при включённом JS
 * (@media (scripting: enabled)) — без скриптов и при reduced motion всё видно сразу.
 */
import type { Directive } from 'vue'

const VISIBLE_SHARE = 0.15
const STAGGER_STEP_MS = 70

let observer: IntersectionObserver | null = null

const getObserver = () => {
  if (observer) return observer
  observer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue
      // Атрибут, а не класс: Vue переписывает class корня компонента при каждом обновлении :class.
      entry.target.setAttribute('data-in', '')
      observer?.unobserve(entry.target)
    }
  }, { threshold: VISIBLE_SHARE, rootMargin: '0px 0px -40px 0px' })
  return observer
}

const reveal: Directive<HTMLElement, number | undefined> = {
  getSSRProps(binding) {
    return {
      'data-reveal': binding.modifiers.stagger ? 'stagger' : '',
      style: binding.value ? `--reveal-delay: ${binding.value}ms` : undefined
    }
  },
  mounted(el, binding) {
    el.dataset.reveal = binding.modifiers.stagger ? 'stagger' : ''
    if (binding.value) el.style.setProperty('--reveal-delay', `${binding.value}ms`)
    if (binding.modifiers.stagger) {
      Array.from(el.children).forEach((child, index) => {
        (child as HTMLElement).style.setProperty('--reveal-i', String(index))
        ;(child as HTMLElement).style.setProperty('--reveal-step', `${STAGGER_STEP_MS}ms`)
      })
    }
    if (typeof IntersectionObserver === 'undefined') {
      el.setAttribute('data-in', '')
      return
    }
    getObserver().observe(el)
  },
  beforeUnmount(el) {
    observer?.unobserve(el)
  }
}

export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.vueApp.directive('reveal', reveal)
})
