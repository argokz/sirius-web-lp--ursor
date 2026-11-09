<template>
  <span class="split" :class="{ in: shown }" :aria-label="plain">
    <template v-for="(part, p) in parts" :key="p">
      <span :class="part.cls" aria-hidden="true"><template v-for="(word, w) in words(part.t)" :key="w"><span
        class="split-word"
      ><span
        class="split-inner"
        :style="{ transitionDelay: `${delay + (offsets[p]! + w) * step}ms` }"
      >{{ word }}</span></span>{{ w < words(part.t).length - 1 ? ' ' : '' }}</template></span>{{ p < parts.length - 1 ? ' ' : '' }}
    </template>
  </span>
</template>

<script setup lang="ts">
/**
 * Заголовок, слова которого поднимаются по очереди, когда он дошёл до экрана (как у felt.com).
 * parts — куски текста; у куска может быть класс (marker, em). Висячие предлоги и тире
 * склеиваются с соседним словом неразрывным пробелом, поэтому в начале строки их не бывает.
 */
interface Part { t: string; cls?: string }

const props = withDefaults(defineProps<{ parts: Part[]; delay?: number; step?: number }>(), {
  delay: 0,
  step: 55
})

// «и», «в», «на»… и тире не остаются в конце или начале строки: слово уходит на строку вместе с соседом.
const SHORT = /^(а|в|и|к|о|с|у|я|во|до|за|из|ко|на|не|ни|но|об|от|по|со|для|без|при|про|что|как)$/i

const words = (text: string) => {
  const raw = text.split(/\s+/).filter(Boolean)
  const out: string[] = []
  for (let i = 0; i < raw.length; i++) {
    const word = raw[i]!
    if (word === '—' && out.length) {
      out[out.length - 1] += `\u00a0—`
      continue
    }
    // «и в городе»: короткое слово может быть уже приклеено к предыдущему — проверяем последнее.
    if (SHORT.test(word.split(' ').pop() || '') && i < raw.length - 1) {
      raw[i + 1] = `${word}\u00a0${raw[i + 1]}`
      continue
    }
    out.push(word)
  }
  return out
}

const offsets = computed(() => {
  let total = 0
  return props.parts.map((part) => {
    const start = total
    total += words(part.t).length
    return start
  })
})

const plain = computed(() => props.parts.map((part) => part.t).join(' ').replace(/\s+/g, ' '))

const shown = ref(false)
const el = getCurrentInstance()
onMounted(() => {
  const root = el?.proxy?.$el as HTMLElement | undefined
  if (!root || typeof IntersectionObserver === 'undefined') {
    shown.value = true
    return
  }
  const observer = new IntersectionObserver(([entry]) => {
    if (!entry?.isIntersecting) return
    shown.value = true
    observer.disconnect()
  }, { threshold: 0.2 })
  observer.observe(root)
})
</script>

<style scoped>
.split-word {
  display: inline-block;
  overflow: hidden;
  padding-bottom: 0.08em;
  margin-bottom: -0.08em;
  vertical-align: top;
}

.split-inner {
  display: inline-block;
}

@media (scripting: enabled) and (prefers-reduced-motion: no-preference) {
  .split-inner {
    transform: translateY(105%);
    transition: transform 0.75s cubic-bezier(0.2, 0.75, 0.15, 1);
  }

  .in .split-inner {
    transform: none;
  }
}
</style>
