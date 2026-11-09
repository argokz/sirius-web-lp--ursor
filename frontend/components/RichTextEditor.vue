<template>
  <div class="rich-editor" :class="{ focused }">
    <div class="rich-toolbar">
      <button v-for="btn in toolbarButtons" :key="btn.cmd" type="button" :title="btn.title" @mousedown.prevent="btn.action ? btn.action() : exec(btn.cmd)">
        <UIcon :name="btn.icon" />
      </button>
    </div>
    <div
      ref="editorRef"
      class="rich-content"
      contenteditable="true"
      @input="onInput"
      @paste="onPaste"
      @focus="focused = true"
      @blur="focused = false"
    />
    <div v-if="!modelValue" class="rich-placeholder">{{ placeholder }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, nextTick } from 'vue'

const props = withDefaults(
  defineProps<{
    modelValue: string
    placeholder?: string
  }>(),
  { placeholder: 'Введите текст...' }
)

const emit = defineEmits<{ 'update:modelValue': [value: string] }>()

const editorRef = ref<HTMLDivElement | null>(null)
const focused = ref(false)
let isUpdating = false

const toolbarButtons = [
  { cmd: 'bold', icon: 'i-lucide-bold', title: 'Жирный (Ctrl+B)' },
  { cmd: 'italic', icon: 'i-lucide-italic', title: 'Курсив (Ctrl+I)' },
  { cmd: 'underline', icon: 'i-lucide-underline', title: 'Подчёркивание (Ctrl+U)' },
  { cmd: 'sep' },
  { cmd: 'insertUnorderedList', icon: 'i-lucide-list', title: 'Маркированный список' },
  { cmd: 'insertOrderedList', icon: 'i-lucide-list-ordered', title: 'Нумерованный список' },
  { cmd: 'sep' },
  { cmd: 'link', icon: 'i-lucide-link', title: 'Добавить ссылку', action: () => insertLink() },
  { cmd: 'removeFormat', icon: 'i-lucide-remove-formatting', title: 'Убрать форматирование' }
].filter((b) => b.cmd !== 'sep' || (b as any).icon === undefined ? false : true) as Array<{ cmd: string; icon: string; title: string; action?: () => void }>

const toolbarWithSeps = [
  { cmd: 'bold', icon: 'i-lucide-bold', title: 'Жирный' },
  { cmd: 'italic', icon: 'i-lucide-italic', title: 'Курсив' },
  { cmd: 'underline', icon: 'i-lucide-underline', title: 'Подчёркивание' },
  { cmd: 'SEP' },
  { cmd: 'insertUnorderedList', icon: 'i-lucide-list', title: 'Список' },
  { cmd: 'insertOrderedList', icon: 'i-lucide-list-ordered', title: 'Нумерованный список' },
  { cmd: 'SEP' },
  { cmd: 'link', icon: 'i-lucide-link', title: 'Ссылка', action: () => insertLink() },
  { cmd: 'removeFormat', icon: 'i-lucide-remove-formatting', title: 'Убрать форматирование' }
]

onMounted(() => {
  if (editorRef.value) {
    editorRef.value.innerHTML = props.modelValue || ''
  }
})

watch(
  () => props.modelValue,
  (val) => {
    if (isUpdating || !editorRef.value) return
    if (editorRef.value.innerHTML !== (val || '')) {
      editorRef.value.innerHTML = val || ''
    }
  }
)

const onInput = () => {
  isUpdating = true
  emit('update:modelValue', editorRef.value?.innerHTML || '')
  nextTick(() => {
    isUpdating = false
  })
}

const onPaste = (e: ClipboardEvent) => {
  e.preventDefault()
  const text = e.clipboardData?.getData('text/plain') || ''
  document.execCommand('insertText', false, text)
}

const exec = (cmd: string, value?: string) => {
  editorRef.value?.focus()
  document.execCommand(cmd, false, value)
  onInput()
}

const insertLink = () => {
  const selection = window.getSelection()
  const selectedText = selection?.toString() || ''
  const url = window.prompt('Введите URL ссылки:', 'https://')
  if (url) {
    editorRef.value?.focus()
    if (selectedText) {
      document.execCommand('createLink', false, url)
    } else {
      const link = `<a href="${url}" target="_blank">${url}</a>`
      document.execCommand('insertHTML', false, link)
    }
    onInput()
  }
}
</script>

<style scoped>
.rich-editor {
  position: relative;
  border: 1px solid var(--line);
  border-radius: 8px;
  overflow: hidden;
  transition: border-color 0.15s;
  background: white;
}

.rich-editor.focused {
  border-color: #94a3b8;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.08);
}

.rich-toolbar {
  display: flex;
  align-items: center;
  gap: 2px;
  padding: 6px 8px;
  border-bottom: 1px solid var(--line);
  background: #f8fafc;
  flex-wrap: wrap;
}

.rich-toolbar button {
  display: grid;
  place-items: center;
  width: 30px;
  height: 30px;
  border: 0;
  border-radius: 5px;
  background: transparent;
  color: #475569;
  cursor: pointer;
  font-size: 0.95rem;
  transition: all 0.15s;
}

.rich-toolbar button:hover {
  background: #e2e8f0;
  color: #1e293b;
}

.rich-content {
  min-height: 120px;
  max-height: 320px;
  overflow-y: auto;
  padding: 12px 14px;
  outline: none;
  font-size: 0.95rem;
  line-height: 1.7;
  color: #1e293b;
}

.rich-content:empty::before {
  content: attr(data-placeholder);
  color: #94a3b8;
  pointer-events: none;
}

.rich-placeholder {
  position: absolute;
  top: calc(30px + 6px + 12px);
  left: 14px;
  color: #94a3b8;
  font-size: 0.95rem;
  pointer-events: none;
  user-select: none;
}

:deep(.rich-content ul) {
  list-style: disc;
  padding-left: 22px;
}

:deep(.rich-content ol) {
  list-style: decimal;
  padding-left: 22px;
}

:deep(.rich-content a) {
  color: #6366f1;
  text-decoration: underline;
}

:deep(.rich-content strong),
:deep(.rich-content b) {
  font-weight: 700;
}
</style>
