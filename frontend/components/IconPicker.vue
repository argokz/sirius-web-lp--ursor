<template>
  <div class="icon-picker" ref="pickerRef">
    <div class="icon-input-row">
      <div class="icon-preview-box">
        <UIcon v-if="modelValue" :name="modelValue" />
        <UIcon v-else name="i-lucide-image" style="opacity: 0.3" />
      </div>
      <input
        :value="modelValue"
        class="field field-sm"
        :placeholder="placeholder"
        @input="onManualInput"
        @focus="open = true"
      />
      <button type="button" class="btn-icon picker-toggle" @click="toggleDropdown">
        <UIcon name="i-lucide-chevron-down" />
      </button>
    </div>

    <div v-if="open" class="icon-dropdown">
      <div class="icon-search-row">
        <UIcon name="i-lucide-search" />
        <input ref="searchRef" v-model="query" class="icon-search-input" placeholder="Поиск иконки..." @keydown.esc="open = false" />
      </div>
      <div class="icon-grid">
        <button
          v-for="icon in filtered"
          :key="icon"
          type="button"
          :class="{ active: modelValue === `i-lucide-${icon}` }"
          :title="icon"
          @click="select(icon)"
        >
          <UIcon :name="`i-lucide-${icon}`" />
        </button>
      </div>
      <div v-if="!filtered.length" class="icon-empty">Иконки не найдены</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick } from 'vue'
import { onClickOutside } from '@vueuse/core'

const props = withDefaults(defineProps<{
  modelValue: string
  placeholder?: string
}>(), {
  placeholder: 'i-lucide-check'
})

const emit = defineEmits<{ 'update:modelValue': [value: string] }>()

const open = ref(false)
const query = ref('')
const pickerRef = ref<HTMLElement | null>(null)
const searchRef = ref<HTMLInputElement | null>(null)

const ALL_ICONS = [
  'check', 'x', 'plus', 'minus', 'circle', 'square',
  'search', 'filter', 'settings', 'settings-2', 'sliders-horizontal',
  'edit', 'edit-2', 'edit-3', 'pen', 'pencil',
  'trash', 'trash-2', 'copy', 'clipboard', 'external-link', 'link', 'link-2',
  'eye', 'eye-off', 'lock', 'unlock', 'key', 'shield',
  'user', 'users', 'user-circle', 'user-plus', 'user-minus', 'user-check',
  'building', 'building-2', 'home', 'map-pin', 'map', 'navigation', 'compass', 'globe', 'globe-2',
  'briefcase', 'package', 'truck', 'shopping-cart', 'tag', 'tags', 'boxes', 'box',
  'bar-chart-3', 'bar-chart-2', 'chart-line', 'pie-chart', 'trending-up', 'trending-down', 'activity',
  'dollar-sign', 'credit-card', 'wallet', 'coins', 'banknote',
  'mail', 'inbox', 'send', 'message-circle', 'message-square', 'phone', 'phone-call',
  'bell', 'bell-ring', 'rss',
  'file', 'file-text', 'file-image', 'image', 'images', 'video', 'camera', 'book', 'book-open', 'newspaper',
  'code', 'code-2', 'terminal', 'cpu', 'database', 'server', 'cloud', 'wifi',
  'network', 'layers', 'layout', 'layout-grid', 'list', 'table', 'grid',
  'wrench', 'hammer', 'tool', 'gauge', 'radio-tower', 'calculator', 'ruler',
  'waves', 'thermometer', 'droplets', 'wind', 'sun', 'moon', 'cloud-rain',
  'zap', 'bolt', 'flame', 'sparkles', 'wand', 'wand-2',
  'arrow-right', 'arrow-left', 'arrow-up', 'arrow-down',
  'chevron-right', 'chevron-left', 'chevron-up', 'chevron-down',
  'download', 'upload', 'refresh-cw', 'rotate-ccw', 'share', 'share-2',
  'play', 'pause', 'stop-circle',
  'check-circle', 'x-circle', 'alert-circle', 'alert-triangle', 'info', 'help-circle',
  'star', 'heart', 'thumbs-up', 'thumbs-down', 'flag', 'bookmark',
  'clock', 'calendar', 'timer', 'watch',
  'award', 'trophy', 'medal', 'target',
  'maximize', 'minimize', 'expand', 'shrink',
  'chart-no-axes-combined', 'scan-line', 'radio',
  'microchip', 'chip', 'hard-drive', 'usb',
  'map-pin-check', 'locate', 'crosshair'
]

const filtered = computed(() => {
  const q = query.value.toLowerCase().trim()
  if (!q) return ALL_ICONS
  return ALL_ICONS.filter((icon) => icon.includes(q))
})

const toggleDropdown = () => {
  open.value = !open.value
  if (open.value) {
    nextTick(() => searchRef.value?.focus())
  }
}

const select = (icon: string) => {
  emit('update:modelValue', `i-lucide-${icon}`)
  open.value = false
  query.value = ''
}

const onManualInput = (e: Event) => {
  emit('update:modelValue', (e.target as HTMLInputElement).value)
}

onClickOutside(pickerRef, () => {
  open.value = false
})

watch(open, (val) => {
  if (val) {
    query.value = ''
    nextTick(() => searchRef.value?.focus())
  }
})
</script>

<style scoped>
.icon-picker {
  position: relative;
}

.icon-input-row {
  display: flex;
  gap: 6px;
  align-items: stretch;
}

.icon-input-row .field {
  flex: 1;
}

.icon-preview-box {
  display: grid;
  place-items: center;
  width: 38px;
  height: 38px;
  border: 1px solid var(--line);
  border-radius: 7px;
  background: #f8fafc;
  font-size: 1.1rem;
  flex-shrink: 0;
  color: #334155;
}

.picker-toggle {
  width: 38px;
  height: 38px;
  flex-shrink: 0;
  border: 1px solid var(--line);
  border-radius: 7px;
  background: #f8fafc;
  cursor: pointer;
  color: #475569;
  display: grid;
  place-items: center;
  transition: background 0.15s;
}

.picker-toggle:hover {
  background: #e2e8f0;
}

.icon-dropdown {
  position: absolute;
  top: calc(100% + 6px);
  left: 0;
  z-index: 200;
  width: 340px;
  max-height: 320px;
  display: flex;
  flex-direction: column;
  border: 1px solid var(--line);
  border-radius: 10px;
  background: white;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  overflow: hidden;
}

.icon-search-row {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border-bottom: 1px solid var(--line);
  color: #94a3b8;
  flex-shrink: 0;
}

.icon-search-input {
  flex: 1;
  border: 0;
  outline: none;
  font-size: 0.9rem;
  color: #1e293b;
  background: transparent;
}

.icon-grid {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 2px;
  padding: 8px;
  overflow-y: auto;
}

.icon-grid button {
  display: grid;
  place-items: center;
  width: 36px;
  height: 36px;
  border: 0;
  border-radius: 6px;
  background: transparent;
  cursor: pointer;
  font-size: 1.1rem;
  color: #475569;
  transition: all 0.12s;
}

.icon-grid button:hover {
  background: #f1f5f9;
  color: #1e293b;
}

.icon-grid button.active {
  background: rgba(227, 6, 19, 0.1);
  color: var(--sirius-red);
}

.icon-empty {
  padding: 20px;
  text-align: center;
  color: #94a3b8;
  font-size: 0.87rem;
}
</style>
