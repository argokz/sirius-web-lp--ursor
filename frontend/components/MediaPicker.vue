<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="modelValue" class="media-picker-overlay" @click.self="$emit('update:modelValue', false)">
        <div class="media-picker-modal">
          <div class="mp-header">
            <div>
              <h2>Медиа-библиотека</h2>
              <p>{{ files.length }} файлов</p>
            </div>
            <div class="mp-header-actions">
              <label class="btn-link btn-primary upload-label">
                <UIcon name="i-lucide-upload" />
                Загрузить
                <input type="file" accept="image/*" style="display:none" @change="uploadFile" />
              </label>
              <button type="button" class="btn-icon" @click="$emit('update:modelValue', false)">
                <UIcon name="i-lucide-x" />
              </button>
            </div>
          </div>

          <div class="mp-search">
            <UIcon name="i-lucide-search" />
            <input v-model="query" class="mp-search-input" placeholder="Поиск по имени файла..." />
          </div>

          <div v-if="loading" class="mp-loading">
            <UIcon name="i-lucide-loader-circle" class="spin" />
            Загрузка...
          </div>
          <div v-else-if="!filtered.length" class="mp-empty">
            <UIcon name="i-lucide-image-off" />
            <p>Нет файлов. Загрузите первый.</p>
          </div>
          <div v-else class="mp-grid">
            <button
              v-for="file in filtered"
              :key="file.filename"
              type="button"
              class="mp-item"
              :class="{ selected: selected === file.url }"
              @click="selectFile(file)"
            >
              <div class="mp-thumb">
                <img v-if="file.is_image" :src="apiBase + file.url" :alt="file.filename" loading="lazy" />
                <div v-else class="mp-file-icon">
                  <UIcon name="i-lucide-file-text" />
                  <span>{{ file.ext }}</span>
                </div>
              </div>
              <div class="mp-name">{{ shortName(file.filename) }}</div>
              <div class="mp-size">{{ formatSize(file.size) }}</div>
            </button>
          </div>

          <div v-if="selected" class="mp-footer">
            <span class="mp-selected-url">{{ selected }}</span>
            <button class="btn-link btn-primary" type="button" @click="confirm">
              <UIcon name="i-lucide-check" />
              Выбрать
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed, watch } from 'vue'

interface MediaFile {
  filename: string
  path: string
  url: string
  size: number
  modified: number
  is_image: boolean
  ext: string
}

const props = defineProps<{
  modelValue: boolean
}>()

const emit = defineEmits<{
  'update:modelValue': [val: boolean]
  select: [url: string]
}>()

const { token } = useAuth()
const config = useRuntimeConfig()
const apiBase = config.public.apiBase

const files = ref<MediaFile[]>([])
const loading = ref(false)
const query = ref('')
const selected = ref('')

const filtered = computed(() => {
  const q = query.value.toLowerCase()
  return q ? files.value.filter((f) => f.filename.toLowerCase().includes(q)) : files.value
})

const loadFiles = async () => {
  loading.value = true
  try {
    files.value = await $fetch<MediaFile[]>(`${apiBase}/api/admin/media`, {
      headers: { Authorization: `Bearer ${token.value}` }
    })
  } catch {
    files.value = []
  } finally {
    loading.value = false
  }
}

const selectFile = (file: MediaFile) => {
  selected.value = file.url
}

const confirm = () => {
  if (selected.value) {
    emit('select', selected.value)
    emit('update:modelValue', false)
    selected.value = ''
  }
}

const uploadFile = async (e: Event) => {
  const input = e.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return

  const formData = new FormData()
  formData.append('file', file)
  loading.value = true

  try {
    const res = await $fetch<{ filename: string; path: string }>(`${apiBase}/api/admin/upload`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token.value}` },
      body: formData
    })
    await loadFiles()
    selected.value = `/${res.path}`
  } catch {
    // silently ignore
  } finally {
    loading.value = false
    input.value = ''
  }
}

const shortName = (name: string) => (name.length > 22 ? name.slice(0, 10) + '...' + name.slice(-8) : name)
const formatSize = (bytes: number) => {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`
}

watch(
  () => props.modelValue,
  (val) => {
    if (val) {
      selected.value = ''
      loadFiles()
    }
  }
)
</script>

<style scoped>
.media-picker-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background: rgba(0, 0, 0, 0.55);
  backdrop-filter: blur(4px);
  display: grid;
  place-items: center;
  padding: 24px;
}

.media-picker-modal {
  width: 100%;
  max-width: 820px;
  max-height: 84vh;
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 24px 80px rgba(0, 0, 0, 0.2);
}

.mp-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 20px 24px;
  border-bottom: 1px solid var(--line);
  flex-shrink: 0;
}

.mp-header h2 {
  margin: 0;
  font-size: 1.15rem;
  font-weight: 900;
}

.mp-header p {
  margin: 4px 0 0;
  color: var(--muted);
  font-size: 0.82rem;
}

.mp-header-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

.upload-label {
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.mp-search {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 24px;
  border-bottom: 1px solid var(--line);
  color: #94a3b8;
  flex-shrink: 0;
}

.mp-search-input {
  flex: 1;
  border: 0;
  outline: none;
  font-size: 0.92rem;
  color: #1e293b;
  background: transparent;
}

.mp-loading,
.mp-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 48px;
  color: #94a3b8;
  font-size: 1.1rem;
}

.mp-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
  gap: 10px;
  padding: 16px 24px;
  overflow-y: auto;
  flex: 1;
}

.mp-item {
  display: flex;
  flex-direction: column;
  gap: 6px;
  border: 2px solid transparent;
  border-radius: 10px;
  overflow: hidden;
  background: #f8fafc;
  cursor: pointer;
  transition: all 0.15s;
  text-align: left;
}

.mp-item:hover {
  border-color: #e2e8f0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.mp-item.selected {
  border-color: var(--sirius-red);
  background: rgba(227, 6, 19, 0.04);
}

.mp-thumb {
  width: 100%;
  height: 100px;
  background: #f1f5f9;
  overflow: hidden;
  display: grid;
  place-items: center;
}

.mp-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.mp-file-icon {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  color: #64748b;
  font-size: 1.5rem;
}

.mp-file-icon span {
  font-size: 0.7rem;
  font-weight: 900;
  text-transform: uppercase;
}

.mp-name {
  padding: 0 8px;
  font-size: 0.72rem;
  font-weight: 700;
  color: #334155;
  word-break: break-all;
  line-height: 1.3;
}

.mp-size {
  padding: 0 8px 8px;
  font-size: 0.68rem;
  color: #94a3b8;
}

.mp-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 14px 24px;
  border-top: 1px solid var(--line);
  background: #f8fafc;
  flex-shrink: 0;
}

.mp-selected-url {
  font-size: 0.8rem;
  color: #64748b;
  font-family: monospace;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.modal-enter-active,
.modal-leave-active {
  transition: all 0.25s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .media-picker-modal,
.modal-leave-to .media-picker-modal {
  transform: scale(0.95) translateY(10px);
}
</style>
