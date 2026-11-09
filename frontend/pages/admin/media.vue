<template>
  <div class="admin-page">
    <div class="admin-page-header">
      <div>
        <span class="eyebrow">CMS</span>
        <h1 class="admin-title">Медиа-библиотека</h1>
        <p class="admin-subtitle">{{ files.length }} файлов · {{ totalSizeFormatted }}</p>
      </div>
      <div class="header-actions">
        <label class="btn-link btn-primary upload-label">
          <UIcon name="i-lucide-upload" />
          Загрузить файл
          <input ref="fileInputRef" type="file" accept="image/*,application/pdf,.doc,.docx,.xls,.xlsx" multiple style="display:none" @change="uploadFiles" />
        </label>
        <button class="btn-link btn-secondary" type="button" :disabled="loading" @click="loadFiles">
          <UIcon name="i-lucide-refresh-cw" />
          Обновить
        </button>
      </div>
    </div>

    <!-- Drag & drop zone -->
    <div
      class="drop-zone"
      :class="{ 'drop-active': isDragging }"
      @dragover.prevent="isDragging = true"
      @dragleave="isDragging = false"
      @drop.prevent="handleDrop"
    >
      <UIcon name="i-lucide-upload-cloud" />
      <span>Перетащите файлы сюда для загрузки</span>
    </div>

    <Transition name="toast">
      <p v-if="toastMsg" class="toast toast-ok">
        <UIcon name="i-lucide-check-circle" />
        {{ toastMsg }}
      </p>
    </Transition>
    <Transition name="toast">
      <p v-if="errorMsg" class="toast toast-danger">
        <UIcon name="i-lucide-alert-circle" />
        {{ errorMsg }}
      </p>
    </Transition>

    <!-- Filters & search -->
    <div class="media-toolbar">
      <div class="media-search">
        <UIcon name="i-lucide-search" />
        <input v-model="query" class="field field-sm" placeholder="Поиск по имени файла..." />
      </div>
      <div class="media-filters">
        <button
          v-for="f in filters"
          :key="f.key"
          type="button"
          :class="{ active: activeFilter === f.key }"
          @click="activeFilter = f.key"
        >
          <UIcon :name="f.icon" />
          {{ f.label }}
        </button>
      </div>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="media-loading">
      <UIcon name="i-lucide-loader-circle" class="spin" />
      Загрузка медиа...
    </div>

    <!-- Empty -->
    <div v-else-if="!filtered.length" class="media-empty">
      <UIcon name="i-lucide-image-off" />
      <h3>Файлов не найдено</h3>
      <p>Загрузите первый файл, нажав кнопку выше или перетащив в зону.</p>
    </div>

    <!-- Grid -->
    <div v-else class="media-grid">
      <div
        v-for="file in filtered"
        :key="file.filename"
        class="media-card"
        :class="{ selected: selectedFiles.includes(file.filename) }"
        @click="toggleSelect(file.filename)"
      >
        <div class="media-thumb">
          <img v-if="file.is_image" :src="apiBase + file.url" :alt="file.filename" loading="lazy" />
          <div v-else class="file-type-icon">
            <UIcon :name="fileIcon(file.ext)" />
            <span>{{ file.ext.toUpperCase() }}</span>
          </div>
          <div class="media-overlay">
            <button type="button" class="copy-btn" title="Скопировать URL" @click.stop="copyUrl(file.url)">
              <UIcon name="i-lucide-copy" />
            </button>
            <button type="button" class="delete-btn" title="Удалить" @click.stop="deleteFile(file.filename)">
              <UIcon name="i-lucide-trash-2" />
            </button>
          </div>
        </div>
        <div class="media-info">
          <div class="media-name" :title="file.filename">{{ shortName(file.filename) }}</div>
          <div class="media-meta">{{ formatSize(file.size) }} · {{ formatDate(file.modified) }}</div>
        </div>
      </div>
    </div>

    <!-- Bulk actions -->
    <Transition name="toast">
      <div v-if="selectedFiles.length" class="bulk-bar">
        <span>Выбрано: {{ selectedFiles.length }}</span>
        <button type="button" class="btn-link btn-secondary btn-sm" @click="selectedFiles = []">
          Снять
        </button>
        <button type="button" class="btn-link danger-soft btn-sm" @click="bulkDelete">
          <UIcon name="i-lucide-trash-2" />
          Удалить выбранные
        </button>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

definePageMeta({ layout: 'admin', middleware: 'auth' })
useHead({ title: 'Медиа-библиотека - CRM Sirius' })

interface MediaFile {
  filename: string
  path: string
  url: string
  size: number
  modified: number
  is_image: boolean
  ext: string
}

const { token } = useAuth()
const config = useRuntimeConfig()
const apiBase = config.public.apiBase

const files = ref<MediaFile[]>([])
const loading = ref(false)
const query = ref('')
const activeFilter = ref('all')
const selectedFiles = ref<string[]>([])
const isDragging = ref(false)
const toastMsg = ref('')
const errorMsg = ref('')

const filters = [
  { key: 'all', label: 'Все', icon: 'i-lucide-layout-grid' },
  { key: 'image', label: 'Изображения', icon: 'i-lucide-image' },
  { key: 'doc', label: 'Документы', icon: 'i-lucide-file-text' }
]

const authHeaders = computed(() => ({ Authorization: `Bearer ${token.value}` }))

const totalSizeFormatted = computed(() => {
  const total = files.value.reduce((acc, f) => acc + f.size, 0)
  if (total < 1024 * 1024) return `${(total / 1024).toFixed(0)} KB`
  return `${(total / 1024 / 1024).toFixed(1)} MB`
})

const filtered = computed(() => {
  let list = files.value
  if (activeFilter.value === 'image') list = list.filter((f) => f.is_image)
  if (activeFilter.value === 'doc') list = list.filter((f) => !f.is_image)
  const q = query.value.toLowerCase()
  return q ? list.filter((f) => f.filename.toLowerCase().includes(q)) : list
})

const notify = (msg: string, type: 'ok' | 'err' = 'ok') => {
  if (type === 'ok') { toastMsg.value = msg; setTimeout(() => { toastMsg.value = '' }, 3000) }
  else { errorMsg.value = msg; setTimeout(() => { errorMsg.value = '' }, 4000) }
}

const loadFiles = async () => {
  loading.value = true
  try {
    files.value = await $fetch<MediaFile[]>(`${apiBase}/api/admin/media`, { headers: authHeaders.value })
  } catch {
    notify('Не удалось загрузить файлы', 'err')
  } finally {
    loading.value = false
  }
}

const doUpload = async (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  const res = await $fetch<{ filename: string; path: string }>(`${apiBase}/api/admin/upload`, {
    method: 'POST',
    headers: authHeaders.value,
    body: formData
  })
  return res
}

const uploadFiles = async (e: Event) => {
  const input = e.target as HTMLInputElement
  const fileList = Array.from(input.files || [])
  if (!fileList.length) return
  loading.value = true
  try {
    await Promise.all(fileList.map(doUpload))
    await loadFiles()
    notify(`Загружено ${fileList.length} файлов`)
  } catch (err: any) {
    notify(err?.data?.detail || 'Ошибка загрузки', 'err')
  } finally {
    loading.value = false
    input.value = ''
  }
}

const handleDrop = async (e: DragEvent) => {
  isDragging.value = false
  const fileList = Array.from(e.dataTransfer?.files || [])
  if (!fileList.length) return
  loading.value = true
  try {
    await Promise.all(fileList.map(doUpload))
    await loadFiles()
    notify(`Загружено ${fileList.length} файлов`)
  } catch {
    notify('Ошибка загрузки', 'err')
  } finally {
    loading.value = false
  }
}

const deleteFile = async (filename: string) => {
  if (!window.confirm(`Удалить файл "${shortName(filename)}"?`)) return
  try {
    await $fetch(`${apiBase}/api/admin/media/${filename}`, {
      method: 'DELETE',
      headers: authHeaders.value
    })
    files.value = files.value.filter((f) => f.filename !== filename)
    selectedFiles.value = selectedFiles.value.filter((n) => n !== filename)
    notify('Файл удалён')
  } catch {
    notify('Не удалось удалить файл', 'err')
  }
}

const bulkDelete = async () => {
  if (!window.confirm(`Удалить ${selectedFiles.value.length} файлов?`)) return
  loading.value = true
  try {
    await Promise.all(
      selectedFiles.value.map((name) =>
        $fetch(`${apiBase}/api/admin/media/${name}`, {
          method: 'DELETE',
          headers: authHeaders.value
        })
      )
    )
    await loadFiles()
    const count = selectedFiles.value.length
    selectedFiles.value = []
    notify(`Удалено ${count} файлов`)
  } catch {
    notify('Ошибка при удалении', 'err')
  } finally {
    loading.value = false
  }
}

const copyUrl = async (url: string) => {
  try {
    await navigator.clipboard.writeText(url)
    notify('URL скопирован в буфер')
  } catch {
    notify('Не удалось скопировать', 'err')
  }
}

const toggleSelect = (name: string) => {
  const idx = selectedFiles.value.indexOf(name)
  if (idx >= 0) selectedFiles.value.splice(idx, 1)
  else selectedFiles.value.push(name)
}

const fileIcon = (ext: string) => {
  const icons: Record<string, string> = {
    pdf: 'i-lucide-file-type-2',
    doc: 'i-lucide-file-text',
    docx: 'i-lucide-file-text',
    xls: 'i-lucide-file-spreadsheet',
    xlsx: 'i-lucide-file-spreadsheet'
  }
  return icons[ext] || 'i-lucide-file'
}

const shortName = (name: string) => (name.length > 26 ? name.slice(0, 12) + '...' + name.slice(-10) : name)
const formatSize = (bytes: number) => {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`
  return `${(bytes / 1024 / 1024).toFixed(1)} MB`
}
const formatDate = (ts: number) => new Date(ts * 1000).toLocaleDateString('ru-RU', { day: '2-digit', month: 'short' })

onMounted(loadFiles)
</script>

<style scoped>
.header-actions {
  display: flex;
  gap: 10px;
}

.upload-label {
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

/* Drop zone */
.drop-zone {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 20px;
  border: 2px dashed var(--line);
  border-radius: 10px;
  color: #94a3b8;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.2s;
  background: #f8fafc;
  cursor: pointer;
}

.drop-zone.drop-active {
  border-color: var(--sirius-red);
  background: rgba(227, 6, 19, 0.04);
  color: var(--sirius-red);
}

.drop-zone .iconify { font-size: 1.5rem; }

/* Toast */
.toast {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 20px;
  border-radius: 10px;
  font-weight: 700;
  font-size: 0.92rem;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
}
.toast-ok { background: linear-gradient(135deg, #ecfdf5, #d1fae5); color: #065f46; border: 1px solid #a7f3d0; }
.toast-danger { background: linear-gradient(135deg, #fef2f2, #fee2e2); color: #991b1b; border: 1px solid #fca5a5; }
.toast-enter-active, .toast-leave-active { transition: all 0.3s ease; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateY(-12px); }

/* Toolbar */
.media-toolbar {
  display: flex;
  gap: 14px;
  align-items: center;
  flex-wrap: wrap;
}

.media-search {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
  min-width: 220px;
  color: #94a3b8;
}

.media-search .field {
  flex: 1;
}

.media-filters {
  display: flex;
  gap: 4px;
  padding: 4px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: white;
}

.media-filters button {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border: 0;
  border-radius: 6px;
  font-weight: 700;
  font-size: 0.84rem;
  color: #475569;
  cursor: pointer;
  background: transparent;
  transition: all 0.15s;
}

.media-filters button.active {
  background: var(--sirius-red);
  color: white;
}

/* States */
.media-loading, .media-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 80px 0;
  color: #94a3b8;
  font-size: 1.1rem;
}

.media-empty h3 { margin: 0; color: #475569; }
.media-empty p { margin: 0; font-size: 0.9rem; }

/* Grid */
.media-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 14px;
}

.media-card {
  border: 2px solid transparent;
  border-radius: 10px;
  overflow: hidden;
  background: white;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
  cursor: pointer;
  transition: all 0.15s;
}

.media-card:hover {
  border-color: #e2e8f0;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.media-card.selected {
  border-color: var(--sirius-red);
  box-shadow: 0 0 0 4px rgba(227, 6, 19, 0.1);
}

.media-thumb {
  position: relative;
  width: 100%;
  aspect-ratio: 4 / 3;
  background: #f1f5f9;
  overflow: hidden;
}

.media-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.file-type-icon {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  gap: 6px;
  color: #64748b;
  font-size: 2rem;
}

.file-type-icon span {
  font-size: 0.72rem;
  font-weight: 900;
}

.media-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: rgba(0, 0, 0, 0.5);
  opacity: 0;
  transition: opacity 0.15s;
}

.media-thumb:hover .media-overlay {
  opacity: 1;
}

.copy-btn,
.delete-btn {
  width: 36px;
  height: 36px;
  border: 0;
  border-radius: 8px;
  display: grid;
  place-items: center;
  cursor: pointer;
  font-size: 0.95rem;
  transition: background 0.15s;
}

.copy-btn { background: rgba(255, 255, 255, 0.9); color: #334155; }
.copy-btn:hover { background: white; }
.delete-btn { background: rgba(239, 68, 68, 0.9); color: white; }
.delete-btn:hover { background: rgb(220, 38, 38); }

.media-info {
  padding: 10px 12px;
}

.media-name {
  font-size: 0.8rem;
  font-weight: 700;
  color: #334155;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.media-meta {
  font-size: 0.72rem;
  color: #94a3b8;
  margin-top: 3px;
}

/* Bulk bar */
.bulk-bar {
  position: fixed;
  bottom: 24px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 20px;
  border-radius: 999px;
  background: #1e293b;
  color: white;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25);
  z-index: 100;
  font-weight: 700;
  font-size: 0.9rem;
}

.bulk-bar .btn-sm {
  min-height: 32px;
  padding: 0 12px;
  font-size: 0.84rem;
  border-radius: 6px;
}

.spin { animation: spin 1s linear infinite; }
@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }

@media (max-width: 640px) {
  .media-grid { grid-template-columns: repeat(2, 1fr); }
  .media-toolbar { flex-direction: column; align-items: stretch; }
}
</style>
