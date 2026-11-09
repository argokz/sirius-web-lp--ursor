<template>
  <div class="admin-page builder-page">
    <div class="admin-page-header">
      <div>
        <span class="eyebrow">CMS-конструктор</span>
        <h1 class="admin-title">Управление сайтом</h1>
        <p class="admin-subtitle">Создавайте страницы, блоки, пункты меню и редактируйте контентную базу без деплоя.</p>
      </div>
      <div class="header-right">
        <div v-if="blockHistory.length" class="history-controls">
          <button class="btn-link btn-secondary btn-sm" type="button" :disabled="loading" @click="undoLastAction" title="Отменить (Ctrl+Z)">
            <UIcon name="i-lucide-rotate-ccw" />
            Отменить ({{ blockHistory.length }})
          </button>
        </div>
        <button class="btn-link btn-secondary" type="button" :disabled="loading" @click="loadAll">
          <UIcon name="i-lucide-refresh-cw" />
          Обновить
        </button>
      </div>
    </div>

    <Transition name="toast">
      <p v-if="message" class="toast toast-ok"><UIcon name="i-lucide-check-circle" />{{ message }}</p>
    </Transition>
    <Transition name="toast">
      <p v-if="error" class="toast toast-danger"><UIcon name="i-lucide-alert-circle" />{{ error }}</p>
    </Transition>

    <div class="builder-tabs">
      <button v-for="tab in tabs" :key="tab.key" type="button" :class="{ active: activeTab === tab.key }" @click="activeTab = tab.key">
        <UIcon :name="tab.icon" />
        {{ tab.title }}
        <span v-if="tab.key === 'pages' && pages.length" class="tab-badge">{{ pages.length }}</span>
      </button>
    </div>

    <!-- ==================== PAGES ==================== -->
    <section v-if="activeTab === 'pages'" class="builder-grid">
      <article class="card card-pad">
        <div class="panel-head">
          <div><h2>Страницы</h2><p>{{ pages.length }} в CMS</p></div>
          <div class="panel-head-actions">
            <button class="btn-link btn-accent" type="button" @click="showTemplateModal = true">
              <UIcon name="i-lucide-layout-template" />Из шаблона
            </button>
            <button class="btn-link btn-secondary" type="button" @click="resetPageForm">
              <UIcon name="i-lucide-plus" />Новая
            </button>
          </div>
        </div>
        <div class="item-list">
          <button v-for="page in pages" :key="page.id" type="button" :class="{ active: selectedPageId === page.id }" @click="editPage(page)">
            <span><strong>{{ page.title }}</strong><small>/{{ page.slug }}</small></span>
            <div class="item-right">
              <span v-if="pageBlockCounts[page.id]" class="block-count-badge">{{ pageBlockCounts[page.id] }}</span>
              <em :class="page.is_active ? 'status-ok' : 'status-warn'">{{ page.is_active ? 'Активна' : 'Скрыта' }}</em>
            </div>
          </button>
        </div>
      </article>

      <article class="card card-pad editor-card">
        <h2>{{ pageForm.id ? 'Редактирование страницы' : 'Новая страница' }}</h2>
        <label class="field-label">Название</label>
        <input v-model="pageForm.title" class="field" placeholder="Например: Кейсы внедрения">
        <label class="field-label">URL slug</label>
        <input v-model="pageForm.slug" class="field" placeholder="cases">
        <label class="check-row"><input v-model="pageForm.is_active" type="checkbox"><span>Показывать страницу</span></label>
        <div class="form-actions">
          <button class="btn-link btn-primary" type="button" :disabled="loading" @click="savePage"><UIcon name="i-lucide-save" />Сохранить</button>
          <a v-if="pageForm.slug" class="btn-link btn-secondary" :href="`/${pageForm.slug}`" target="_blank"><UIcon name="i-lucide-external-link" />Превью</a>
          <button v-if="pageForm.id" class="btn-link danger-soft" type="button" @click="deletePage"><UIcon name="i-lucide-trash-2" />Удалить</button>
        </div>
      </article>
    </section>

    <!-- ==================== BLOCKS ==================== -->
    <section v-if="activeTab === 'blocks'" :class="['builder-grid', { 'builder-grid-preview': previewEnabled }]">
      <!-- List -->
      <article class="card card-pad">
        <div class="panel-head">
          <div><h2>Блоки</h2><p>Выберите страницу.</p></div>
        </div>
        <div class="page-select-row">
          <select v-model.number="selectedPageId" class="field" @change="loadBlocks">
            <option v-for="page in pages" :key="page.id" :value="page.id">{{ page.title }} /{{ page.slug }}</option>
          </select>
          <button
            type="button"
            class="btn-icon preview-toggle"
            :class="{ active: previewEnabled }"
            title="Live Preview"
            @click="previewEnabled = !previewEnabled"
          >
            <UIcon name="i-lucide-monitor" />
          </button>
          <a v-if="selectedPageSlug" class="btn-icon" :href="`/${selectedPageSlug}`" target="_blank" title="Открыть страницу">
            <UIcon name="i-lucide-external-link" />
          </a>
        </div>

        <!-- Bulk toolbar -->
        <Transition name="slide-down">
          <div v-if="selectedBlockIds.length" class="bulk-toolbar">
            <span>Выбрано: {{ selectedBlockIds.length }}</span>
            <button type="button" class="btn-sm-flat" @click="bulkSetActive(true)"><UIcon name="i-lucide-eye" />Показать</button>
            <button type="button" class="btn-sm-flat" @click="bulkSetActive(false)"><UIcon name="i-lucide-eye-off" />Скрыть</button>
            <button type="button" class="btn-sm-flat danger-flat" @click="bulkDelete"><UIcon name="i-lucide-trash-2" />Удалить</button>
            <button type="button" class="btn-sm-flat" @click="selectedBlockIds = []"><UIcon name="i-lucide-x" /></button>
          </div>
        </Transition>

        <!-- Bulk select all -->
        <div v-if="blocks.length > 1" class="bulk-header">
          <label class="check-row mini">
            <input type="checkbox" :checked="isAllSelected" @change="toggleSelectAll" />
            <span>Выбрать все</span>
          </label>
        </div>

        <div class="item-list block-list" @dragover.prevent @drop="handleDrop">
          <div v-for="(block, idx) in blocks" :key="block.id" class="block-list-row" :class="{ 'is-selected': selectedBlockIds.includes(block.id) }">
            <label class="block-checkbox-label" @click.stop>
              <input type="checkbox" :checked="selectedBlockIds.includes(block.id)" @change="toggleBlockSelection(block.id)" />
            </label>
            <button
              type="button"
              class="block-btn"
              :class="{ active: blockForm.id === block.id }"
              draggable="true"
              @click="editBlock(block)"
              @dragstart="handleDragStart(idx, $event)"
              @dragenter.prevent="handleDragEnter(idx)"
              @dragend="handleDragEnd"
            >
              <span class="block-info">
                <span class="block-type-icon" :style="{ background: blockTypeColor(block.block_type) }">
                  <UIcon :name="blockTypeIcon(block.block_type)" />
                </span>
                <span>
                  <strong>{{ block.title || block.block_key }}</strong>
                  <small>{{ blockTypeLabel(block.block_type) }} · #{{ block.sort_order }}</small>
                </span>
              </span>
              <div class="item-right">
                <UIcon name="i-lucide-grip-vertical" class="drag-handle" />
                <em :class="block.is_active ? 'status-ok' : 'status-warn'">{{ block.is_active ? 'Видим' : 'Скрыт' }}</em>
              </div>
            </button>
          </div>
        </div>

        <button class="btn-link btn-secondary btn-sm" style="margin-top:10px;width:100%" type="button" @click="resetBlockForm">
          <UIcon name="i-lucide-plus" />Новый блок
        </button>
      </article>

      <!-- Editor -->
      <article class="card card-pad editor-card">
        <div class="panel-head compact">
          <div>
            <h2>{{ blockForm.id ? 'Редактирование блока' : 'Новый блок' }}</h2>
            <p>Визуально редактируйте содержимое секции.</p>
          </div>
          <div class="panel-head-actions">
            <div v-if="blockForm.id" class="copy-to-wrapper">
              <button type="button" class="btn-link btn-secondary btn-sm" @click="showCopyToMenu = !showCopyToMenu">
                <UIcon name="i-lucide-copy-plus" />Скопировать в...
              </button>
              <div v-if="showCopyToMenu" class="copy-to-dropdown">
                <button
                  v-for="page in otherPages"
                  :key="page.id"
                  type="button"
                  @click="copyToPage(page.id)"
                >
                  {{ page.title }}
                </button>
              </div>
            </div>
            <button v-if="blockForm.id" class="btn-link btn-secondary btn-sm" type="button" title="Дублировать" @click="duplicateBlock">
              <UIcon name="i-lucide-copy" />
            </button>
          </div>
        </div>

        <div class="form-grid">
          <label><span class="field-label">Ключ блока</span><input v-model="blockForm.block_key" class="field" placeholder="hero-main"></label>
          <label>
            <span class="field-label">Тип</span>
            <select v-model="blockForm.block_type" class="field" @change="applyBlockPreset">
              <option v-for="type in blockTypes" :key="type.value" :value="type.value">{{ type.title }}</option>
            </select>
          </label>
        </div>

        <label class="field-label">Надзаголовок</label>
        <input v-model="blockForm.eyebrow" class="field" placeholder="Цифровая платформа">
        <label class="field-label">Заголовок</label>
        <input v-model="blockForm.title" class="field" placeholder="Название блока">

        <label class="field-label">Текст (поддерживает форматирование)</label>
        <RichTextEditor v-model="blockForm.body" placeholder="Основное описание блока..." />

        <div class="form-grid">
          <label><span class="field-label">Порядок</span><input v-model.number="blockForm.sort_order" class="field" type="number"></label>
          <label class="check-row in-grid"><input v-model="blockForm.is_active" type="checkbox"><span>Показывать блок</span></label>
        </div>

        <div class="editor-mode-tabs">
          <button type="button" :class="{ active: editorMode === 'visual' }" @click="editorMode = 'visual'; syncPayloadFromRaw()">
            <UIcon name="i-lucide-eye" />Визуальный
          </button>
          <button type="button" :class="{ active: editorMode === 'style' }" @click="editorMode = 'style'; syncPayloadFromRaw()">
            <UIcon name="i-lucide-palette" />Стиль
          </button>
          <button type="button" :class="{ active: editorMode === 'code' }" @click="editorMode = 'code'">
            <UIcon name="i-lucide-code" />JSON
          </button>
        </div>

        <!-- STYLE EDITOR -->
        <div v-if="editorMode === 'style'" class="visual-form">
          <div class="form-grid">
            <label>
              <span class="field-label">Фон секции</span>
              <select v-model="parsedPayload.layout.bg" class="field">
                <option value="default">Стандартный (светлый)</option>
                <option value="dark">Темный (инверсия)</option>
                <option value="brand">Цвет бренда</option>
              </select>
            </label>
            <label>
              <span class="field-label">Отступы</span>
              <select v-model="parsedPayload.layout.padding" class="field">
                <option value="tight">Компактные</option>
                <option value="normal">Нормальные</option>
                <option value="large">Большие</option>
              </select>
            </label>
            <label>
              <span class="field-label">Выравнивание</span>
              <select v-model="parsedPayload.layout.align" class="field">
                <option value="left">По левому краю</option>
                <option value="center">По центру</option>
              </select>
            </label>
          </div>
          <label class="check-row" style="margin-top: 1rem;">
            <input v-model="parsedPayload.layout.hiddenMobile" type="checkbox">
            <span>Скрыть блок на мобильных устройствах</span>
          </label>
        </div>

        <!-- VISUAL EDITOR -->
        <div v-if="editorMode === 'visual'" class="visual-form">

          <!-- Hero / Flow image -->
          <div v-if="blockForm.block_type === 'hero' || blockForm.block_type === 'flow'" class="form-field">
            <span class="field-label">Изображение</span>
            <div class="image-uploader-container">
              <div v-if="parsedPayload.image" class="image-preview-wrapper">
                <img :src="parsedPayload.image" class="image-preview" alt="Превью" />
                <button type="button" class="btn-remove-image" @click="parsedPayload.image = ''"><UIcon name="i-lucide-trash-2" /></button>
              </div>
              <div class="uploader-controls">
                <input v-model="parsedPayload.image" class="field" placeholder="/main-func.webp">
                <button type="button" class="btn-link btn-secondary upload-action-btn" @click="triggerUpload('block')"><UIcon name="i-lucide-upload" />Загрузить</button>
                <button type="button" class="btn-link btn-secondary upload-action-btn" @click="showMediaPicker = true"><UIcon name="i-lucide-images" />Библиотека</button>
                <input ref="fileInput" type="file" accept="image/png,image/jpeg,image/webp,image/gif" style="display:none" @change="handleFileUpload($event, 'block')" />
              </div>
            </div>
          </div>

          <!-- Hero / CTA buttons -->
          <div v-if="blockForm.block_type === 'hero' || blockForm.block_type === 'cta'" class="form-grid">
            <label><span class="field-label">Текст кнопки</span><input v-model="parsedPayload.button_text" class="field" placeholder="Запросить демо"></label>
            <label><span class="field-label">Ссылка кнопки</span><input v-model="parsedPayload.button_url" class="field" placeholder="/demo"></label>
          </div>
          <div v-if="blockForm.block_type === 'hero'" class="form-grid">
            <label><span class="field-label">Текст 2-й кнопки</span><input v-model="parsedPayload.button2_text" class="field" placeholder="Связаться"></label>
            <label><span class="field-label">Ссылка 2-й кнопки</span><input v-model="parsedPayload.button2_url" class="field" placeholder="/contacts"></label>
          </div>

          <!-- Text block optional CTA -->
          <div v-if="blockForm.block_type === 'text'" class="form-grid">
            <label><span class="field-label">Текст кнопки (опционально)</span><input v-model="parsedPayload.button_text" class="field" placeholder="Узнать больше"></label>
            <label><span class="field-label">Ссылка кнопки</span><input v-model="parsedPayload.button_url" class="field" placeholder="/page"></label>
          </div>

          <!-- Flow mode -->
          <div v-if="blockForm.block_type === 'flow'" class="form-grid">
            <label><span class="field-label">Режим анимации</span>
              <select v-model="parsedPayload.flow_mode" class="field">
                <option value="horizontal">Горизонтальный</option>
                <option value="vertical">Вертикальный</option>
              </select>
            </label>
          </div>

          <!-- Form block settings -->
          <div v-if="blockForm.block_type === 'form'" class="visual-form">
            <label><span class="field-label">Текст кнопки отправки</span><input v-model="parsedPayload.submit_text" class="field" placeholder="Отправить"></label>
            <div class="form-grid">
              <label><span class="field-label">Placeholder Имени</span><input v-model="parsedPayload.name_placeholder" class="field" placeholder="Ваше имя"></label>
              <label><span class="field-label">Placeholder Email</span><input v-model="parsedPayload.email_placeholder" class="field" placeholder="email@example.com"></label>
            </div>
            <label><span class="field-label">Placeholder Сообщения</span><input v-model="parsedPayload.message_placeholder" class="field" placeholder="Ваш вопрос или пожелание"></label>
          </div>

          <!-- Items list -->
          <div v-if="['cards', 'metrics', 'text', 'steps', 'outcomes', 'gallery', 'pricing', 'faq', 'testimonials', 'logos'].includes(blockForm.block_type)" class="items-editor">
            <div class="items-header">
              <span class="field-label">Элементы ({{ parsedPayload.items?.length || 0 }})</span>
              <button type="button" class="btn-link btn-secondary btn-xs" @click="addItem"><UIcon name="i-lucide-plus" />Добавить</button>
            </div>

            <div v-if="parsedPayload.items?.length" class="items-list-container">
              <div v-for="(item, idx) in parsedPayload.items" :key="idx" class="item-editor-card card card-pad">
                <div class="item-card-header">
                  <strong>Элемент #{{ idx + 1 }}</strong>
                  <div class="item-card-actions">
                    <button type="button" class="btn-icon" :disabled="idx === 0" @click="moveItemUp(idx)"><UIcon name="i-lucide-arrow-up" /></button>
                    <button type="button" class="btn-icon" :disabled="idx === parsedPayload.items.length - 1" @click="moveItemDown(idx)"><UIcon name="i-lucide-arrow-down" /></button>
                    <button type="button" class="btn-icon danger-icon" @click="removeItem(idx)"><UIcon name="i-lucide-trash-2" /></button>
                  </div>
                </div>
                <div class="item-card-grid">
                  <!-- Metric value -->
                  <label v-if="blockForm.block_type === 'metrics'" class="item-field">
                    <span class="field-label text-xs">Значение (15-20%)</span>
                    <input v-model="item.value" class="field field-sm" placeholder="99.9%">
                  </label>
                  <!-- Icon picker for cards/text -->
                  <label v-if="blockForm.block_type === 'cards' || blockForm.block_type === 'text'" class="item-field">
                    <span class="field-label text-xs">Иконка</span>
                    <IconPicker v-model="item.icon" placeholder="i-lucide-check" />
                  </label>
                  <!-- Gallery / Logos image -->
                  <div v-if="['gallery', 'logos'].includes(blockForm.block_type)" class="item-field wide-field">
                    <span class="field-label text-xs">Изображение</span>
                    <div class="uploader-controls-compact">
                      <input v-model="item.image" class="field field-sm" placeholder="/uploads/photo.jpg">
                      <button type="button" class="btn-link btn-secondary btn-xs" @click="triggerItemUpload(idx)"><UIcon name="i-lucide-upload" /></button>
                      <button type="button" class="btn-link btn-secondary btn-xs" @click="openItemMediaPicker(idx)"><UIcon name="i-lucide-images" /></button>
                    </div>
                    <input :ref="(el) => setItemFileInput(el, idx)" type="file" accept="image/png,image/jpeg,image/webp,image/gif" style="display:none" @change="handleItemFileUpload($event, idx)" />
                    <div v-if="item.image" class="item-image-preview-sm">
                      <img :src="item.image" alt="thumb" />
                    </div>
                  </div>
                  <!-- Caption for gallery -->
                  <label v-if="blockForm.block_type === 'gallery'" class="item-field wide-field">
                    <span class="field-label text-xs">Подпись</span>
                    <input v-model="item.caption" class="field field-sm" placeholder="Описание фотографии">
                  </label>
                  
                  <!-- Pricing -->
                  <template v-else-if="blockForm.block_type === 'pricing'">
                    <label class="item-field"><span class="field-label text-xs">Название тарифа</span><input v-model="item.title" class="field field-sm" placeholder="Базовый"></label>
                    <label class="item-field"><span class="field-label text-xs">Цена</span><input v-model="item.price" class="field field-sm" placeholder="1000 ₽"></label>
                    <label class="item-field wide-field"><span class="field-label text-xs">Короткое описание</span><input v-model="item.text" class="field field-sm" placeholder="Для небольших команд"></label>
                    <label class="item-field wide-field"><span class="field-label text-xs">Фичи (каждая с новой строки)</span>
                      <textarea :value="Array.isArray(item.features) ? item.features.join('\n') : item.features" @input="item.features = ($event.target.value || '').split('\n').map(s=>s.trim()).filter(Boolean)" class="field field-sm" rows="4" placeholder="Фича 1&#10;Фича 2"></textarea>
                    </label>
                    <label class="item-field"><span class="field-label text-xs">Текст кнопки</span><input v-model="item.button_text" class="field field-sm" placeholder="Выбрать"></label>
                    <label class="item-field"><span class="field-label text-xs">Ссылка кнопки</span><input v-model="item.button_url" class="field field-sm" placeholder="/"></label>
                    <label class="check-row wide-field" style="margin-top:8px"><input v-model="item.featured" type="checkbox"><span>Выделить как "Популярный"</span></label>
                  </template>

                  <!-- Generic -->
                  <template v-else>
                    <label class="item-field"><span class="field-label text-xs">Заголовок</span><input v-model="item.title" class="field field-sm" placeholder="Заголовок"></label>
                    <label v-if="blockForm.block_type === 'testimonials'" class="item-field wide-field"><span class="field-label text-xs">Должность / Компания</span><input v-model="item.role" class="field field-sm" placeholder="CEO, Company"></label>
                    <label class="item-field wide-field" v-if="blockForm.block_type !== 'logos'"><span class="field-label text-xs">Описание / Текст</span><textarea v-model="item.text" class="field field-sm" rows="2" placeholder="Текст"></textarea></label>
                    <!-- image for cards/steps/outcomes/testimonials -->
                    <div v-if="['cards', 'steps', 'outcomes', 'testimonials'].includes(blockForm.block_type)" class="item-field wide-field">
                      <span class="field-label text-xs">Изображение (опционально)</span>
                      <div class="uploader-controls-compact">
                        <input v-model="item.image" class="field field-sm" placeholder="URL">
                        <button type="button" class="btn-link btn-secondary btn-xs" @click="triggerItemUpload(idx)"><UIcon name="i-lucide-upload" /></button>
                        <button type="button" class="btn-link btn-secondary btn-xs" @click="openItemMediaPicker(idx)"><UIcon name="i-lucide-images" /></button>
                      </div>
                      <input :ref="(el) => setItemFileInput(el, idx)" type="file" accept="image/png,image/jpeg,image/webp,image/gif" style="display:none" @change="handleItemFileUpload($event, idx)" />
                    </div>
                  </template>
                </div>
              </div>
            </div>
            <div v-else class="empty-items-placeholder">Список пуст. Нажмите «Добавить».</div>
          </div>
        </div>

        <!-- CODE EDITOR -->
        <div v-else class="code-editor-wrapper">
          <label class="field-label">JSON Payload</label>
          <textarea v-model="blockForm.payload" class="field code-field" rows="12" />
        </div>

        <div class="form-actions">
          <button class="btn-link btn-primary" type="button" :disabled="loading || !selectedPageId" @click="saveBlock"><UIcon name="i-lucide-save" />Сохранить блок</button>
          <button v-if="blockForm.id" class="btn-link danger-soft" type="button" @click="deleteBlock"><UIcon name="i-lucide-trash-2" />Удалить</button>
        </div>
      </article>

      <!-- LIVE PREVIEW IFRAME -->
      <article v-if="previewEnabled" class="preview-panel">
        <div class="preview-header">
          <span><UIcon name="i-lucide-monitor" />Превью: /{{ selectedPageSlug }}</span>
          <div style="display: flex; gap: 8px; align-items: center;">
            <button type="button" class="btn-link btn-primary btn-sm" :disabled="!selectedPageId || publishing" @click="publishPage">
              <UIcon name="i-lucide-globe" />
              Опубликовать
            </button>
            <button type="button" class="btn-icon" title="Обновить превью" @click="refreshPreview"><UIcon name="i-lucide-refresh-cw" /></button>
          </div>
        </div>
        <iframe v-if="selectedPageSlug" :src="previewUrl" class="preview-iframe" :key="previewTimestamp" />
        <div v-else class="preview-placeholder">Выберите страницу</div>
      </article>
    </section>

    <!-- ==================== MENU ==================== -->
    <section v-if="activeTab === 'menu'" class="builder-grid">
      <article class="card card-pad">
        <div class="panel-head">
          <div><h2>Пункты меню</h2><p>Порядок управляет шапкой сайта.</p></div>
          <button class="btn-link btn-secondary" type="button" @click="resetMenuForm"><UIcon name="i-lucide-plus" />Новый</button>
        </div>
        <div class="item-list">
          <button v-for="item in menuItems" :key="item.id" type="button" :class="{ active: menuForm.id === item.id }" @click="editMenuItem(item)">
            <span><strong>{{ item.title }}</strong><small>{{ item.url }} · {{ item.sort_order }}</small></span>
            <em :class="item.is_active ? 'status-ok' : 'status-warn'">{{ item.is_active ? 'В меню' : 'Скрыт' }}</em>
          </button>
        </div>
      </article>
      <article class="card card-pad editor-card">
        <h2>{{ menuForm.id ? 'Редактирование' : 'Новый пункт' }}</h2>
        <label class="field-label">Название</label><input v-model="menuForm.title" class="field" placeholder="Кейсы">
        <label class="field-label">URL</label><input v-model="menuForm.url" class="field" placeholder="/cases">
        <label class="field-label">Связанная страница</label>
        <select v-model="menuForm.page_id" class="field" @change="syncMenuUrl">
          <option :value="null">Без привязки</option>
          <option v-for="page in pages" :key="page.id" :value="page.id">{{ page.title }} /{{ page.slug }}</option>
        </select>
        <div class="form-grid">
          <label><span class="field-label">Иконка</span><IconPicker v-model="menuForm.icon" /></label>
          <label><span class="field-label">Порядок</span><input v-model.number="menuForm.sort_order" class="field" type="number"></label>
        </div>
        <label class="check-row"><input v-model="menuForm.is_active" type="checkbox"><span>В меню</span></label>
        <label class="check-row"><input v-model="menuForm.is_external" type="checkbox"><span>Внешняя ссылка</span></label>
        <div class="form-actions">
          <button class="btn-link btn-primary" type="button" :disabled="loading" @click="saveMenuItem"><UIcon name="i-lucide-save" />Сохранить</button>
          <button v-if="menuForm.id" class="btn-link danger-soft" type="button" @click="deleteMenuItem"><UIcon name="i-lucide-trash-2" />Удалить</button>
        </div>
      </article>
    </section>

    <!-- ==================== SETTINGS ==================== -->
    <section v-if="activeTab === 'settings'" class="settings-layout">
      <article class="card card-pad">
        <div class="panel-head">
          <div><h2>Настройки сайта</h2><p>Контакты, аналитика, тексты шапки и подвала.</p></div>
        </div>
        <div class="settings-grid">
          <label v-for="field in settingFields" :key="field.key" :class="{ wide: field.field_type === 'textarea' }">
            <span class="field-label">{{ field.label }}</span>
            <textarea v-if="field.field_type === 'textarea'" v-model="settingsForm[field.key]" class="field" rows="4" />
            <input v-else v-model="settingsForm[field.key]" class="field" :type="field.field_type" :placeholder="field.placeholder || ''" />
          </label>
        </div>
        <div class="form-actions">
          <button class="btn-link btn-primary" type="button" :disabled="loading" @click="saveSettings"><UIcon name="i-lucide-save" />Сохранить настройки</button>
        </div>
      </article>
    </section>

    <!-- ==================== SEO ==================== -->
    <section v-if="activeTab === 'seo'" class="builder-grid">
      <article class="card card-pad">
        <div class="panel-head"><div><h2>SEO-метаданные</h2><p>title, description и OpenGraph.</p></div></div>
        <label class="field-label">Страница</label>
        <select v-model="seoSelectedSlug" class="field" @change="loadSeo">
          <option v-for="page in pages" :key="page.id" :value="page.slug">{{ page.title }} /{{ page.slug }}</option>
        </select>
      </article>
      <article class="card card-pad editor-card">
        <h2>Настройки SEO</h2>
        <div class="seo-analyzer">
          <div class="seo-check" :class="seoTitleStatus.class"><UIcon :name="seoTitleStatus.icon" /><span>Title: {{ seoForm.title?.length || 0 }}/60</span></div>
          <div class="seo-check" :class="seoDescStatus.class"><UIcon :name="seoDescStatus.icon" /><span>Description: {{ seoForm.description?.length || 0 }}/160</span></div>
          <div class="seo-check" :class="seoForm.og_image ? 'seo-good' : 'seo-warn'"><UIcon :name="seoForm.og_image ? 'i-lucide-check-circle' : 'i-lucide-alert-triangle'" /><span>OG Image: {{ seoForm.og_image ? 'Установлено' : 'Нет' }}</span></div>
        </div>
        <div class="form-grid">
          <label><span class="field-label">Title</span><input v-model="seoForm.title" class="field" placeholder="Заголовок для поиска"></label>
          <label><span class="field-label">Keywords</span><input v-model="seoForm.keywords" class="field" placeholder="ключевые, слова"></label>
        </div>
        <label><span class="field-label">Description</span><textarea v-model="seoForm.description" class="field" rows="3" /></label>
        <h3 class="form-section-title">OpenGraph</h3>
        <div class="form-grid">
          <label><span class="field-label">OG Title</span><input v-model="seoForm.og_title" class="field"></label>
          <label><span class="field-label">OG Type</span>
            <select v-model="seoForm.og_type" class="field"><option value="website">website</option><option value="article">article</option><option value="product">product</option></select>
          </label>
        </div>
        <label><span class="field-label">OG Description</span><textarea v-model="seoForm.og_description" class="field" rows="2" /></label>
        <div class="form-field">
          <span class="field-label">OG Image</span>
          <div class="uploader-controls">
            <input v-model="seoForm.og_image" class="field" placeholder="URL изображения">
            <button type="button" class="btn-link btn-secondary upload-action-btn" @click="triggerUpload('seo')"><UIcon name="i-lucide-upload" />Загрузить</button>
            <button type="button" class="btn-link btn-secondary upload-action-btn" @click="showMediaPickerSeo = true"><UIcon name="i-lucide-images" />Библиотека</button>
            <input ref="seoFileInput" type="file" accept="image/png,image/jpeg,image/webp,image/gif" style="display:none" @change="handleFileUpload($event, 'seo')" />
          </div>
        </div>
        <h3 class="form-section-title">Twitter Card</h3>
        <div class="form-grid">
          <label><span class="field-label">Twitter Title</span><input v-model="seoForm.twitter_title" class="field"></label>
          <label><span class="field-label">Card Type</span>
            <select v-model="seoForm.twitter_card" class="field"><option value="summary_large_image">summary_large_image</option><option value="summary">summary</option></select>
          </label>
        </div>
        <label><span class="field-label">Twitter Description</span><textarea v-model="seoForm.twitter_description" class="field" rows="2" /></label>
        <label><span class="field-label">Twitter Image</span><input v-model="seoForm.twitter_image" class="field"></label>
        <div class="form-actions">
          <button class="btn-link btn-primary" type="button" :disabled="loading" @click="saveSeo"><UIcon name="i-lucide-save" />Сохранить SEO</button>
        </div>
      </article>
    </section>

    <!-- TEMPLATE MODAL -->
    <Teleport to="body">
      <Transition name="modal">
        <div v-if="showTemplateModal" class="modal-overlay" @click.self="showTemplateModal = false">
          <div class="modal-content">
            <div class="modal-header">
              <h2>Создать из шаблона</h2>
              <button type="button" class="btn-icon" @click="showTemplateModal = false"><UIcon name="i-lucide-x" /></button>
            </div>
            <div class="template-grid">
              <button v-for="tpl in pageTemplates" :key="tpl.key" type="button" class="template-card" @click="createFromTemplate(tpl)">
                <div class="template-icon" :style="{ background: tpl.color }"><UIcon :name="tpl.icon" /></div>
                <strong>{{ tpl.title }}</strong>
                <p>{{ tpl.description }}</p>
                <small>{{ tpl.blocks.length }} блоков</small>
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </Teleport>

    <!-- MEDIA PICKER -->
    <MediaPicker v-model="showMediaPicker" @select="onMediaPickerSelect" />
    <MediaPicker v-model="showMediaPickerSeo" @select="(url) => { seoForm.og_image = url }" />
    <MediaPicker v-model="showMediaPickerItem" @select="onItemMediaSelect" />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, reactive, ref, watch } from 'vue'

definePageMeta({ layout: 'admin', middleware: 'auth' })
useHead({ title: 'Конструктор сайта - CRM Sirius' })

type TabKey = 'pages' | 'blocks' | 'menu' | 'settings' | 'seo'

interface PageItem { id: number; slug: string; title: string; is_active: boolean }
interface PageBlock {
  id: number; page_id: number; block_key: string; block_type: string
  eyebrow?: string; title?: string; body?: string; payload?: string
  sort_order: number; is_active: boolean
}
interface MenuItem {
  id: number; title: string; url: string; page_id?: number | null
  icon?: string; sort_order: number; is_active: boolean; is_external: boolean
}
interface SiteSetting { key: string; value?: string; label?: string; group_name: string; field_type: string }

const tabs = [
  { key: 'pages', title: 'Страницы', icon: 'i-lucide-file-plus-2' },
  { key: 'blocks', title: 'Блоки', icon: 'i-lucide-layout-template' },
  { key: 'menu', title: 'Меню', icon: 'i-lucide-navigation' },
  { key: 'settings', title: 'Настройки', icon: 'i-lucide-settings-2' },
  { key: 'seo', title: 'SEO', icon: 'i-lucide-search' }
] as const

const blockTypes = [
  { value: 'hero', title: 'Hero / первый экран', icon: 'i-lucide-image', color: '#6366f1' },
  { value: 'text', title: 'Текстовый блок', icon: 'i-lucide-text', color: '#64748b' },
  { value: 'cards', title: 'Карточки', icon: 'i-lucide-layout-grid', color: '#0ea5e9' },
  { value: 'metrics', title: 'Метрики', icon: 'i-lucide-bar-chart-3', color: '#10b981' },
  { value: 'cta', title: 'CTA / призыв', icon: 'i-lucide-megaphone', color: '#f59e0b' },
  { value: 'steps', title: 'Шаги / этапы', icon: 'i-lucide-list-ordered', color: '#8b5cf6' },
  { value: 'flow', title: 'Анимация потока', icon: 'i-lucide-waves', color: '#06b6d4' },
  { value: 'outcomes', title: 'Результаты', icon: 'i-lucide-trophy', color: '#ec4899' },
  { value: 'gallery', title: 'Галерея', icon: 'i-lucide-images', color: '#f97316' },
  { value: 'form', title: 'Контактная форма', icon: 'i-lucide-mail', color: '#14b8a6' },
  { value: 'pricing', title: 'Тарифы', icon: 'i-lucide-credit-card', color: '#3b82f6' },
  { value: 'faq', title: 'Частые вопросы (FAQ)', icon: 'i-lucide-help-circle', color: '#8b5cf6' },
  { value: 'testimonials', title: 'Отзывы', icon: 'i-lucide-message-square-quote', color: '#f43f5e' },
  { value: 'logos', title: 'Логотипы партнеров', icon: 'i-lucide-building-2', color: '#64748b' }
]

const blockTypeIcon = (t: string) => blockTypes.find((b) => b.value === t)?.icon || 'i-lucide-box'
const blockTypeColor = (t: string) => blockTypes.find((b) => b.value === t)?.color || '#64748b'
const blockTypeLabel = (t: string) => blockTypes.find((b) => b.value === t)?.title || t

const settingFields = [
  { key: 'company_name', label: 'Название компании', group_name: 'brand', field_type: 'text', default: 'ПКФ «Сириус»', placeholder: '' },
  { key: 'product_name', label: 'Название продукта', group_name: 'brand', field_type: 'text', default: 'ТГИД-07', placeholder: '' },
  { key: 'contact_email', label: 'Email', group_name: 'contacts', field_type: 'email', default: 'info@itwin.kz', placeholder: '' },
  { key: 'contact_phone', label: 'Телефон', group_name: 'contacts', field_type: 'tel', default: '', placeholder: '' },
  { key: 'contact_address', label: 'Адрес', group_name: 'contacts', field_type: 'textarea', default: '', placeholder: '' },
  { key: 'telegram_url', label: 'Telegram URL', group_name: 'contacts', field_type: 'url', default: '', placeholder: '' },
  { key: 'whatsapp_url', label: 'WhatsApp URL', group_name: 'contacts', field_type: 'url', default: '', placeholder: '' },
  { key: 'footer_text', label: 'Текст в подвале', group_name: 'content', field_type: 'textarea', default: '', placeholder: '' },
  { key: 'google_analytics_id', label: 'Google Analytics ID (GA4)', group_name: 'analytics', field_type: 'text', default: '', placeholder: 'G-XXXXXXXXXX' }
]

const pageTemplates = [
  {
    key: 'landing', title: 'Лендинг продукта', description: 'Hero + карточки + метрики + CTA', icon: 'i-lucide-rocket', color: '#6366f1',
    blocks: [
      { block_key: 'hero', block_type: 'hero', eyebrow: 'Новый продукт', title: 'Заголовок продукта', body: 'Описание вашего продукта.', payload: { image: '/main-func.webp', button_text: 'Запросить демо', button_url: '/demo' } },
      { block_key: 'features', block_type: 'cards', eyebrow: 'Возможности', title: 'Ключевые возможности', body: '', payload: { items: [{ icon: 'i-lucide-zap', title: 'Быстрый старт', text: 'Начните за минуты.' }, { icon: 'i-lucide-shield', title: 'Безопасность', text: 'Защита данных.' }, { icon: 'i-lucide-bar-chart-3', title: 'Аналитика', text: 'Подробная статистика.' }] } },
      { block_key: 'metrics', block_type: 'metrics', eyebrow: 'В цифрах', title: 'Результаты', body: '', payload: { items: [{ value: '99.9%', title: 'Uptime', text: '' }, { value: '24/7', title: 'Поддержка', text: '' }] } },
      { block_key: 'cta', block_type: 'cta', eyebrow: 'Начните', title: 'Готовы попробовать?', body: 'Запросите демонстрацию.', payload: { button_text: 'Запросить демо', button_url: '/demo' } }
    ]
  },
  {
    key: 'solution', title: 'Страница решения', description: 'Hero + шаги + результаты + CTA', icon: 'i-lucide-puzzle', color: '#0ea5e9',
    blocks: [
      { block_key: 'hero', block_type: 'hero', eyebrow: 'Решение', title: 'Название решения', body: 'Описание решения.', payload: { image: '/main-func.webp', button_text: 'Узнать больше', button_url: '/demo' } },
      { block_key: 'steps', block_type: 'steps', eyebrow: 'Внедрение', title: 'Этапы', body: '', payload: { items: [{ title: 'Анализ', text: 'Изучаем инфраструктуру.' }, { title: 'Настройка', text: 'Конфигурируем.' }, { title: 'Запуск', text: 'Запускаем в работу.' }] } },
      { block_key: 'outcomes', block_type: 'outcomes', eyebrow: 'Результаты', title: 'Что вы получите', body: '', payload: { items: [{ title: 'Экономия', text: 'Снижение затрат.' }, { title: 'Скорость', text: 'Ускорение процессов.' }] } },
      { block_key: 'cta', block_type: 'cta', eyebrow: 'Следующий шаг', title: 'Обсудим проект?', body: '', payload: { button_text: 'Обсудить', button_url: '/demo' } }
    ]
  },
  {
    key: 'gallery-page', title: 'Фотогалерея', description: 'Hero + галерея + CTA', icon: 'i-lucide-images', color: '#f97316',
    blocks: [
      { block_key: 'hero', block_type: 'hero', eyebrow: 'Галерея', title: 'Наши проекты', body: 'Реализованные решения в фотографиях.', payload: { button_text: 'Связаться', button_url: '/contacts' } },
      { block_key: 'gallery', block_type: 'gallery', eyebrow: 'Проекты', title: 'Фотогалерея', body: '', payload: { items: [{ image: '/main-func.webp', caption: 'Объект 1' }] } },
      { block_key: 'cta', block_type: 'cta', eyebrow: 'Следующий шаг', title: 'Начнём сотрудничество?', body: '', payload: { button_text: 'Запросить демо', button_url: '/demo' } }
    ]
  },
  {
    key: 'contact', title: 'Контакты + форма', description: 'Hero + форма обратной связи', icon: 'i-lucide-mail', color: '#14b8a6',
    blocks: [
      { block_key: 'hero', block_type: 'hero', eyebrow: 'Контакты', title: 'Свяжитесь с нами', body: 'Мы ответим на ваши вопросы.', payload: {} },
      { block_key: 'form', block_type: 'form', eyebrow: 'Обратная связь', title: 'Напишите нам', body: '', payload: { submit_text: 'Отправить', name_placeholder: 'Ваше имя', email_placeholder: 'Email', message_placeholder: 'Ваш вопрос' } }
    ]
  },
  { key: 'empty', title: 'Пустая страница', description: 'Чистый лист для ручного наполнения', icon: 'i-lucide-file', color: '#94a3b8', blocks: [] }
]

const { token } = useAuth()
const config = useRuntimeConfig()
const activeTab = ref<TabKey>('pages')
const loading = ref(false)
const error = ref('')
const message = ref('')
const pages = ref<PageItem[]>([])
const blocks = ref<PageBlock[]>([])
const menuItems = ref<MenuItem[]>([])
const settings = ref<SiteSetting[]>([])
const selectedPageId = ref<number | null>(null)
const showTemplateModal = ref(false)
const showMediaPicker = ref(false)
const showMediaPickerSeo = ref(false)
const showMediaPickerItem = ref(false)
const currentItemMediaIdx = ref(-1)

// History for Undo
const blockHistory = ref<PageBlock[][]>([])

// Live preview
const previewEnabled = ref(false)
const previewTimestamp = ref(Date.now())
const previewUrl = computed(() => {
  if (!selectedPageSlug.value || !import.meta.client) return ''
  return `${window.location.origin}/${selectedPageSlug.value}?t=${previewTimestamp.value}`
})
const refreshPreview = () => { previewTimestamp.value = Date.now() }

// Bulk operations
const selectedBlockIds = ref<number[]>([])
const isAllSelected = computed(() => blocks.value.length > 0 && selectedBlockIds.value.length === blocks.value.length)

// Copy to page
const showCopyToMenu = ref(false)
const otherPages = computed(() => pages.value.filter((p) => p.id !== selectedPageId.value))

const authHeaders = computed(() => ({ Authorization: `Bearer ${token.value}` }))
const selectedPageSlug = computed(() => pages.value.find((p) => p.id === selectedPageId.value)?.slug || '')
const pageBlockCounts = ref<Record<number, number>>({})

// Forms
const pageForm = reactive({ id: null as number | null, slug: '', title: '', is_active: true })
const blockForm = reactive({
  id: null as number | null, block_key: 'hero', block_type: 'text', eyebrow: '', title: '', body: '',
  payload: '{}', sort_order: 10, is_active: true
})
const menuForm = reactive({
  id: null as number | null, title: '', url: '', page_id: null as number | null,
  icon: 'i-lucide-circle', sort_order: 10, is_active: true, is_external: false
})
const settingsForm = reactive<Record<string, string>>({})
const seoSelectedSlug = ref('')
const seoForm = reactive({
  title: '', description: '', keywords: '', og_title: '', og_description: '',
  og_image: '', og_type: 'website', twitter_card: 'summary_large_image',
  twitter_title: '', twitter_description: '', twitter_image: ''
})

// SEO analyzer
const seoTitleStatus = computed(() => {
  const len = seoForm.title?.length || 0
  if (!len) return { class: 'seo-warn', icon: 'i-lucide-alert-triangle' }
  if (len >= 50 && len <= 60) return { class: 'seo-good', icon: 'i-lucide-check-circle' }
  if (len > 60) return { class: 'seo-bad', icon: 'i-lucide-x-circle' }
  return { class: 'seo-ok', icon: 'i-lucide-minus-circle' }
})
const seoDescStatus = computed(() => {
  const len = seoForm.description?.length || 0
  if (!len) return { class: 'seo-warn', icon: 'i-lucide-alert-triangle' }
  if (len >= 150 && len <= 160) return { class: 'seo-good', icon: 'i-lucide-check-circle' }
  if (len > 160) return { class: 'seo-bad', icon: 'i-lucide-x-circle' }
  return { class: 'seo-ok', icon: 'i-lucide-minus-circle' }
})

const clearStatus = () => { error.value = ''; message.value = '' }
const notify = (text: string) => {
  message.value = text
  window.setTimeout(() => { if (message.value === text) message.value = '' }, 3000)
}

const apiFetch = <T>(url: string, options: any = {}) =>
  $fetch<T>(`${config.public.apiBase}${url}`, { ...options, headers: { ...authHeaders.value, ...(options.headers || {}) } })

// ───── DATA LOADING ─────
const loadPages = async () => {
  pages.value = await apiFetch<PageItem[]>('/api/admin/pages')
  if (!selectedPageId.value && pages.value.length) selectedPageId.value = pages.value[0].id
  if (!seoSelectedSlug.value && pages.value.length) seoSelectedSlug.value = pages.value[0].slug
  for (const page of pages.value) {
    try {
      const b = await apiFetch<PageBlock[]>(`/api/admin/pages/${page.id}/blocks`)
      pageBlockCounts.value[page.id] = b.length
    } catch { pageBlockCounts.value[page.id] = 0 }
  }
}

const loadBlocks = async () => {
  if (!selectedPageId.value) { blocks.value = []; return }
  blocks.value = await apiFetch<PageBlock[]>(`/api/admin/pages/${selectedPageId.value}/blocks`)
  if (selectedPageId.value) pageBlockCounts.value[selectedPageId.value] = blocks.value.length
}

const loadMenu = async () => { menuItems.value = await apiFetch<MenuItem[]>('/api/admin/menu-items') }

const loadSettings = async () => {
  settings.value = await apiFetch<SiteSetting[]>('/api/admin/settings')
  for (const field of settingFields) {
    const existing = settings.value.find((item) => item.key === field.key)
    settingsForm[field.key] = existing?.value ?? field.default
  }
}

const loadAll = async () => {
  loading.value = true
  clearStatus()
  try {
    await loadPages()
    await Promise.all([loadBlocks(), loadMenu(), loadSettings()])
  } catch (err: any) {
    error.value = err?.data?.detail || 'Не удалось загрузить данные'
  } finally {
    loading.value = false
  }
}

// ───── PAGES ─────
const resetPageForm = () => Object.assign(pageForm, { id: null, slug: '', title: '', is_active: true })

const editPage = async (page: PageItem) => {
  Object.assign(pageForm, page)
  selectedPageId.value = page.id
  await loadBlocks()
}

const savePage = async () => {
  loading.value = true; clearStatus()
  try {
    const saved = pageForm.id
      ? await apiFetch<PageItem>(`/api/admin/pages/${pageForm.id}`, { method: 'PUT', body: { slug: pageForm.slug, title: pageForm.title, is_active: pageForm.is_active } })
      : await apiFetch<PageItem>('/api/admin/pages', { method: 'POST', body: { slug: pageForm.slug, title: pageForm.title, is_active: pageForm.is_active } })
    await loadPages(); await editPage(saved); notify('Страница сохранена')
  } catch (err: any) {
    console.error('Ошибка:', err)
    alert(err?.data?.detail || 'Ошибка сохранения')
  } finally {
    loading.value = false
  }
}

const publishing = ref(false)
const publishPage = async () => {
  if (!selectedPageId.value) return
  if (!confirm('Вы уверены, что хотите опубликовать текущую версию страницы (все измененные блоки)?')) return
  
  publishing.value = true
  try {
    const res = await $fetch<{ message: string }>(`${config.public.apiBase}/api/admin/pages/${selectedPageId.value}/publish`, {
      method: 'POST',
      headers: { Authorization: `Bearer ${token.value}` }
    })
    alert(res.message)
    refreshPreview()
  } catch (err: any) {
    alert(err?.data?.detail || 'Ошибка публикации')
  } finally {
    publishing.value = false
  }
}

const deletePage = async () => {
  if (!pageForm.id || !window.confirm('Удалить страницу и блоки?')) return
  loading.value = true; clearStatus()
  try {
    await apiFetch(`/api/admin/pages/${pageForm.id}`, { method: 'DELETE' })
    resetPageForm(); selectedPageId.value = null; await loadAll(); notify('Страница удалена')
  } catch (err: any) { error.value = err?.data?.detail || 'Ошибка' } finally { loading.value = false }
}

// ───── BLOCKS VISUAL EDITOR ─────
const editorMode = ref<'visual' | 'style' | 'code'>('visual')
const fileInput = ref<HTMLInputElement | null>(null)
const seoFileInput = ref<HTMLInputElement | null>(null)
const itemFileInputs = ref<Record<number, HTMLInputElement>>({})
const setItemFileInput = (el: any, idx: number) => { if (el) itemFileInputs.value[idx] = el as HTMLInputElement }

const parsedPayload = reactive<Record<string, any>>({
  image: '', button_text: '', button_url: '', button2_text: '', button2_url: '',
  flow_mode: 'horizontal', submit_text: 'Отправить', name_placeholder: 'Ваше имя',
  email_placeholder: 'Email', message_placeholder: 'Ваше сообщение', items: [] as any[],
  layout: { bg: 'default', padding: 'normal', align: 'left', hiddenMobile: false }
})

const syncPayloadFromRaw = () => {
  try {
    const data = JSON.parse(blockForm.payload || '{}')
    parsedPayload.image = data.image || ''
    parsedPayload.button_text = data.button_text || ''
    parsedPayload.button_url = data.button_url || ''
    parsedPayload.button2_text = data.button2_text || ''
    parsedPayload.button2_url = data.button2_url || ''
    parsedPayload.flow_mode = data.flow_mode || 'horizontal'
    parsedPayload.submit_text = data.submit_text || 'Отправить'
    parsedPayload.name_placeholder = data.name_placeholder || 'Ваше имя'
    parsedPayload.email_placeholder = data.email_placeholder || 'Email'
    parsedPayload.message_placeholder = data.message_placeholder || 'Ваше сообщение'
    parsedPayload.items = Array.isArray(data.items) ? JSON.parse(JSON.stringify(data.items)) : []
    parsedPayload.layout = data.layout || { bg: 'default', padding: 'normal', align: 'left', hiddenMobile: false }
  } catch {
    parsedPayload.image = ''; parsedPayload.button_text = ''; parsedPayload.button_url = ''
    parsedPayload.items = []
    parsedPayload.layout = { bg: 'default', padding: 'normal', align: 'left', hiddenMobile: false }
  }
}

watch(parsedPayload, (newVal) => {
  if (editorMode.value === 'code') return
  const data: Record<string, any> = {}
  data.layout = JSON.parse(JSON.stringify(newVal.layout))
  if (blockForm.block_type === 'hero') {
    data.image = newVal.image; data.button_text = newVal.button_text; data.button_url = newVal.button_url
    if (newVal.button2_text) data.button2_text = newVal.button2_text
    if (newVal.button2_url) data.button2_url = newVal.button2_url
  } else if (blockForm.block_type === 'cta') {
    data.button_text = newVal.button_text; data.button_url = newVal.button_url
  } else if (blockForm.block_type === 'flow') {
    data.image = newVal.image; data.flow_mode = newVal.flow_mode
  } else if (blockForm.block_type === 'form') {
    data.submit_text = newVal.submit_text; data.name_placeholder = newVal.name_placeholder
    data.email_placeholder = newVal.email_placeholder; data.message_placeholder = newVal.message_placeholder
  } else if (blockForm.block_type === 'text') {
    data.items = newVal.items
    if (newVal.button_text) data.button_text = newVal.button_text
    if (newVal.button_url) data.button_url = newVal.button_url
  } else {
    data.items = newVal.items
  }
  blockForm.payload = JSON.stringify(data, null, 2)
}, { deep: true })

const resetBlockForm = () => {
  Object.assign(blockForm, {
    id: null, block_key: `block-${String(blocks.value.length + 1).padStart(2, '0')}`,
    block_type: 'text', eyebrow: '', title: '', body: '', payload: '{}',
    sort_order: (blocks.value.length + 1) * 10, is_active: true
  })
  syncPayloadFromRaw()
}

const editBlock = (block: PageBlock) => {
  Object.assign(blockForm, {
    id: block.id, block_key: block.block_key, block_type: block.block_type,
    eyebrow: block.eyebrow || '', title: block.title || '', body: block.body || '',
    payload: block.payload || '{}', sort_order: block.sort_order, is_active: block.is_active
  })
  syncPayloadFromRaw()
  showCopyToMenu.value = false
}

const applyBlockPreset = () => {
  const presets: Record<string, string> = {
    hero: JSON.stringify({ image: '/main-func.webp', button_text: 'Запросить демо', button_url: '/demo' }, null, 2),
    cards: JSON.stringify({ items: [{ title: 'Сценарий', text: 'Описание.', icon: 'i-lucide-gauge' }] }, null, 2),
    metrics: JSON.stringify({ items: [{ value: '24/7', title: 'Мониторинг', text: 'Постоянный контроль.' }] }, null, 2),
    cta: JSON.stringify({ button_text: 'Обсудить внедрение', button_url: '/demo' }, null, 2),
    steps: JSON.stringify({ items: [{ title: 'Этап 1', text: 'Описание шага.' }] }, null, 2),
    flow: JSON.stringify({ flow_mode: 'horizontal' }, null, 2),
    outcomes: JSON.stringify({ items: [{ title: 'Результат', text: 'Описание.' }] }, null, 2),
    text: JSON.stringify({ items: [{ title: 'Пункт', text: 'Текст.', icon: 'i-lucide-check' }] }, null, 2),
    gallery: JSON.stringify({ items: [{ image: '/main-func.webp', caption: 'Подпись' }] }, null, 2),
    form: JSON.stringify({ submit_text: 'Отправить', name_placeholder: 'Ваше имя', email_placeholder: 'Email', message_placeholder: 'Вопрос' }, null, 2),
    pricing: JSON.stringify({ items: [{ title: 'Базовый', price: '0 ₽', text: 'Для начала', button_text: 'Выбрать', button_url: '/demo', featured: false, features: ['Функция 1', 'Функция 2'] }] }, null, 2),
    faq: JSON.stringify({ items: [{ title: 'Вопрос 1', text: 'Ответ на вопрос.' }] }, null, 2),
    testimonials: JSON.stringify({ items: [{ title: 'Имя Фамилия', role: 'Должность', text: 'Отличный продукт!', image: '' }] }, null, 2),
    logos: JSON.stringify({ items: [{ title: 'Компания', image: '' }] }, null, 2)
  }
  blockForm.payload = presets[blockForm.block_type] || '{}'
  syncPayloadFromRaw()
}

// Items
const addItem = () => {
  const item: Record<string, any> = { title: '', text: '' }
  if (blockForm.block_type === 'cards' || blockForm.block_type === 'text') item.icon = 'i-lucide-check'
  if (blockForm.block_type === 'metrics') item.value = '100%'
  if (blockForm.block_type === 'gallery') { item.image = ''; item.caption = ''; delete item.title; delete item.text }
  if (blockForm.block_type === 'testimonials') { item.image = ''; item.role = ''; }
  if (blockForm.block_type === 'logos') { item.image = ''; delete item.text; }
  if (blockForm.block_type === 'pricing') { item.price = ''; item.button_text = 'Выбрать'; item.button_url = '/'; item.featured = false; item.features = ['Новая функция']; }
  parsedPayload.items.push(item)
}
const removeItem = (idx: number) => parsedPayload.items.splice(idx, 1)
const moveItemUp = (idx: number) => { if (idx === 0) return; const [item] = parsedPayload.items.splice(idx, 1); parsedPayload.items.splice(idx - 1, 0, item) }
const moveItemDown = (idx: number) => { if (idx >= parsedPayload.items.length - 1) return; const [item] = parsedPayload.items.splice(idx, 1); parsedPayload.items.splice(idx + 1, 0, item) }

// File uploads
const triggerUpload = (target: 'block' | 'seo') => target === 'seo' ? seoFileInput.value?.click() : fileInput.value?.click()
const triggerItemUpload = (idx: number) => itemFileInputs.value[idx]?.click()
const openItemMediaPicker = (idx: number) => { currentItemMediaIdx.value = idx; showMediaPickerItem.value = true }
const onItemMediaSelect = (url: string) => {
  const idx = currentItemMediaIdx.value
  if (idx >= 0 && parsedPayload.items[idx] !== undefined) parsedPayload.items[idx].image = url
}
const onMediaPickerSelect = (url: string) => { parsedPayload.image = url }

const handleFileUpload = async (event: Event, target: 'block' | 'seo') => {
  const el = event.target as HTMLInputElement
  const file = el.files?.[0]; if (!file) return
  const formData = new FormData(); formData.append('file', file)
  loading.value = true; clearStatus()
  try {
    const res = await apiFetch<{ filename: string; path: string }>('/api/admin/upload', { method: 'POST', body: formData })
    const url = `/${res.path}`
    if (target === 'seo') seoForm.og_image = url
    else parsedPayload.image = url
    notify('Изображение загружено!')
  } catch (err: any) { error.value = err?.data?.detail || 'Ошибка загрузки' } finally { loading.value = false; el.value = '' }
}

const handleItemFileUpload = async (event: Event, idx: number) => {
  const el = event.target as HTMLInputElement
  const file = el.files?.[0]; if (!file) return
  const formData = new FormData(); formData.append('file', file)
  loading.value = true; clearStatus()
  try {
    const res = await apiFetch<{ filename: string; path: string }>('/api/admin/upload', { method: 'POST', body: formData })
    if (parsedPayload.items[idx]) parsedPayload.items[idx].image = `/${res.path}`
    notify('Изображение загружено!')
  } catch (err: any) { error.value = err?.data?.detail || 'Ошибка загрузки' } finally { loading.value = false; el.value = '' }
}

// ───── HISTORY / UNDO ─────
const pushToHistory = () => {
  const snapshot = JSON.parse(JSON.stringify(blocks.value))
  blockHistory.value.push(snapshot)
  if (blockHistory.value.length > 10) blockHistory.value.shift()
}

const undoLastAction = async () => {
  if (!blockHistory.value.length) return
  const prev = blockHistory.value.pop()!
  loading.value = true
  try {
    for (const b of prev) {
      await apiFetch(`/api/admin/blocks/${b.id}`, {
        method: 'PUT',
        body: { block_key: b.block_key, block_type: b.block_type, eyebrow: b.eyebrow || '', title: b.title || '', body: b.body || '', payload: b.payload || '{}', sort_order: b.sort_order, is_active: b.is_active }
      })
    }
    await loadBlocks(); notify('Действие отменено')
  } catch { error.value = 'Не удалось отменить' } finally { loading.value = false }
}

const handleKeyDown = (e: KeyboardEvent) => {
  if ((e.ctrlKey || e.metaKey) && e.key === 'z' && !e.shiftKey) { e.preventDefault(); undoLastAction() }
}

// ───── BLOCK SAVE / DELETE / DRAG ─────
const saveBlock = async () => {
  if (!selectedPageId.value) return
  loading.value = true; clearStatus()
  pushToHistory()
  try {
    JSON.parse(blockForm.payload || '{}')
    const body = {
      block_key: blockForm.block_key, block_type: blockForm.block_type, eyebrow: blockForm.eyebrow,
      title: blockForm.title, body: blockForm.body, payload: blockForm.payload || '{}',
      sort_order: blockForm.sort_order, is_active: blockForm.is_active
    }
    const saved = blockForm.id
      ? await apiFetch<PageBlock>(`/api/admin/blocks/${blockForm.id}`, { method: 'PUT', body })
      : await apiFetch<PageBlock>(`/api/admin/pages/${selectedPageId.value}/blocks`, { method: 'POST', body })
    await loadBlocks(); editBlock(saved); refreshPreview(); notify('Блок сохранён')
  } catch (err: any) { error.value = err?.data?.detail || err?.message || 'Ошибка' } finally { loading.value = false }
}

const deleteBlock = async () => {
  if (!blockForm.id || !window.confirm('Удалить блок?')) return
  loading.value = true; clearStatus(); pushToHistory()
  try {
    await apiFetch(`/api/admin/blocks/${blockForm.id}`, { method: 'DELETE' })
    resetBlockForm(); await loadBlocks(); refreshPreview(); notify('Блок удалён')
  } catch (err: any) { error.value = err?.data?.detail || 'Ошибка' } finally { loading.value = false }
}

const duplicateBlock = async () => {
  if (!blockForm.id || !selectedPageId.value) return
  loading.value = true; clearStatus()
  try {
    const maxOrder = blocks.value.reduce((max, b) => Math.max(max, b.sort_order), 0)
    const saved = await apiFetch<PageBlock>(`/api/admin/pages/${selectedPageId.value}/blocks`, {
      method: 'POST', body: { block_key: blockForm.block_key + '-copy', block_type: blockForm.block_type, eyebrow: blockForm.eyebrow, title: blockForm.title, body: blockForm.body, payload: blockForm.payload || '{}', sort_order: maxOrder + 10, is_active: blockForm.is_active }
    })
    await loadBlocks(); editBlock(saved); notify('Блок дублирован')
  } catch (err: any) { error.value = err?.data?.detail || 'Ошибка' } finally { loading.value = false }
}

// ───── DRAG & DROP ─────
const dragIdx = ref<number | null>(null); const dropIdx = ref<number | null>(null)
const handleDragStart = (idx: number, e: DragEvent) => { dragIdx.value = idx; if (e.dataTransfer) e.dataTransfer.effectAllowed = 'move' }
const handleDragEnter = (idx: number) => { dropIdx.value = idx }
const handleDragEnd = () => { dragIdx.value = null; dropIdx.value = null }
const handleDrop = async () => {
  if (dragIdx.value === null || dropIdx.value === null || dragIdx.value === dropIdx.value) { dragIdx.value = null; dropIdx.value = null; return }
  const reordered = [...blocks.value]
  const [moved] = reordered.splice(dragIdx.value, 1)
  reordered.splice(dropIdx.value, 0, moved)
  blocks.value = reordered.map((b, i) => ({ ...b, sort_order: (i + 1) * 10 }))
  dragIdx.value = null; dropIdx.value = null
  loading.value = true
  try {
    for (const b of blocks.value) {
      await apiFetch(`/api/admin/blocks/${b.id}`, { method: 'PUT', body: { block_key: b.block_key, block_type: b.block_type, eyebrow: b.eyebrow || '', title: b.title || '', body: b.body || '', payload: b.payload || '{}', sort_order: b.sort_order, is_active: b.is_active } })
    }
    await loadBlocks(); notify('Порядок обновлён')
  } catch { error.value = 'Ошибка порядка' } finally { loading.value = false }
}

// ───── BULK OPERATIONS ─────
const toggleBlockSelection = (id: number) => {
  const idx = selectedBlockIds.value.indexOf(id)
  if (idx >= 0) selectedBlockIds.value.splice(idx, 1)
  else selectedBlockIds.value.push(id)
}
const toggleSelectAll = () => {
  selectedBlockIds.value = isAllSelected.value ? [] : blocks.value.map((b) => b.id)
}
const bulkSetActive = async (state: boolean) => {
  loading.value = true
  try {
    for (const id of selectedBlockIds.value) {
      const b = blocks.value.find((block) => block.id === id); if (!b) continue
      await apiFetch(`/api/admin/blocks/${id}`, { method: 'PUT', body: { block_key: b.block_key, block_type: b.block_type, eyebrow: b.eyebrow || '', title: b.title || '', body: b.body || '', payload: b.payload || '{}', sort_order: b.sort_order, is_active: state } })
    }
    await loadBlocks(); selectedBlockIds.value = []; notify(`${state ? 'Показано' : 'Скрыто'} ${selectedBlockIds.value.length} блоков`)
  } catch { error.value = 'Ошибка массового изменения' } finally { loading.value = false }
}
const bulkDelete = async () => {
  const count = selectedBlockIds.value.length
  if (!count || !window.confirm(`Удалить ${count} блоков?`)) return
  loading.value = true; pushToHistory()
  try {
    for (const id of selectedBlockIds.value) await apiFetch(`/api/admin/blocks/${id}`, { method: 'DELETE' })
    await loadBlocks(); selectedBlockIds.value = []; resetBlockForm(); notify(`Удалено ${count} блоков`)
  } catch { error.value = 'Ошибка удаления' } finally { loading.value = false }
}

// ───── COPY TO PAGE ─────
const copyToPage = async (targetPageId: number) => {
  showCopyToMenu.value = false; loading.value = true; clearStatus()
  try {
    const maxBlocks = await apiFetch<PageBlock[]>(`/api/admin/pages/${targetPageId}/blocks`)
    const maxOrder = maxBlocks.reduce((max, b) => Math.max(max, b.sort_order), 0)
    await apiFetch(`/api/admin/pages/${targetPageId}/blocks`, {
      method: 'POST',
      body: { block_key: blockForm.block_key + '-copy', block_type: blockForm.block_type, eyebrow: blockForm.eyebrow, title: blockForm.title, body: blockForm.body, payload: blockForm.payload || '{}', sort_order: maxOrder + 10, is_active: blockForm.is_active }
    })
    const target = pages.value.find((p) => p.id === targetPageId)
    notify(`Блок скопирован на «${target?.title || ''}»`)
  } catch { error.value = 'Не удалось скопировать' } finally { loading.value = false }
}

// ───── MENU ─────
const resetMenuForm = () => Object.assign(menuForm, { id: null, title: '', url: '', page_id: null, icon: 'i-lucide-circle', sort_order: (menuItems.value.length + 1) * 10, is_active: true, is_external: false })
const editMenuItem = (item: MenuItem) => Object.assign(menuForm, { id: item.id, title: item.title, url: item.url, page_id: item.page_id || null, icon: item.icon || 'i-lucide-circle', sort_order: item.sort_order, is_active: item.is_active, is_external: item.is_external })
const syncMenuUrl = () => {
  if (!menuForm.page_id) return
  const page = pages.value.find((p) => p.id === menuForm.page_id)
  if (page) { menuForm.url = `/${page.slug}`; if (!menuForm.title) menuForm.title = page.title }
}
const saveMenuItem = async () => {
  loading.value = true; clearStatus()
  try {
    const body = { title: menuForm.title, url: menuForm.url, page_id: menuForm.page_id, icon: menuForm.icon, sort_order: menuForm.sort_order, is_active: menuForm.is_active, is_external: menuForm.is_external }
    const saved = menuForm.id
      ? await apiFetch<MenuItem>(`/api/admin/menu-items/${menuForm.id}`, { method: 'PUT', body })
      : await apiFetch<MenuItem>('/api/admin/menu-items', { method: 'POST', body })
    await loadMenu(); editMenuItem(saved); notify('Пункт меню сохранён')
  } catch (err: any) { error.value = err?.data?.detail || 'Ошибка' } finally { loading.value = false }
}
const deleteMenuItem = async () => {
  if (!menuForm.id || !window.confirm('Удалить пункт меню?')) return
  loading.value = true
  try { await apiFetch(`/api/admin/menu-items/${menuForm.id}`, { method: 'DELETE' }); resetMenuForm(); await loadMenu(); notify('Пункт меню удалён') }
  catch (err: any) { error.value = err?.data?.detail || 'Ошибка' } finally { loading.value = false }
}

// ───── SETTINGS ─────
const saveSettings = async () => {
  loading.value = true; clearStatus()
  try {
    await apiFetch('/api/admin/settings', { method: 'PUT', body: settingFields.map((f) => ({ key: f.key, value: settingsForm[f.key] || '', label: f.label, group_name: f.group_name, field_type: f.field_type })) })
    await loadSettings(); notify('Настройки сохранены')
  } catch (err: any) { error.value = err?.data?.detail || 'Ошибка' } finally { loading.value = false }
}

// ───── SEO ─────
const loadSeo = async () => {
  if (!seoSelectedSlug.value) return
  try {
    const data = await apiFetch<any>('/api/admin/seo', { query: { page_slug: seoSelectedSlug.value } })
    for (const key of Object.keys(seoForm) as Array<keyof typeof seoForm>) {
      ;(seoForm[key] as string) = data?.[key] || (key === 'og_type' ? 'website' : key === 'twitter_card' ? 'summary_large_image' : '')
    }
  } catch {
    for (const key of Object.keys(seoForm) as Array<keyof typeof seoForm>) {
      ;(seoForm[key] as string) = key === 'og_type' ? 'website' : key === 'twitter_card' ? 'summary_large_image' : ''
    }
  }
}
const saveSeo = async () => {
  if (!seoSelectedSlug.value) return
  loading.value = true; clearStatus()
  try { await apiFetch('/api/admin/seo', { method: 'PUT', query: { page_slug: seoSelectedSlug.value }, body: seoForm }); notify('SEO сохранено') }
  catch (err: any) { error.value = err?.data?.detail || 'Ошибка' } finally { loading.value = false }
}

// ───── TEMPLATES ─────
const createFromTemplate = async (tpl: typeof pageTemplates[number]) => {
  loading.value = true; clearStatus(); showTemplateModal.value = false
  try {
    const slug = tpl.key + '-' + Date.now().toString(36)
    const newPage = await apiFetch<PageItem>('/api/admin/pages', { method: 'POST', body: { slug, title: tpl.title, is_active: true } })
    for (let i = 0; i < tpl.blocks.length; i++) {
      const b = tpl.blocks[i]
      await apiFetch(`/api/admin/pages/${newPage.id}/blocks`, { method: 'POST', body: { block_key: b.block_key, block_type: b.block_type, eyebrow: b.eyebrow || '', title: b.title || '', body: b.body || '', payload: JSON.stringify(b.payload || {}), sort_order: (i + 1) * 10, is_active: true } })
    }
    await loadPages(); await editPage(newPage); activeTab.value = 'blocks'; notify(`«${tpl.title}» создана с ${tpl.blocks.length} блоками`)
  } catch (err: any) { error.value = err?.data?.detail || 'Ошибка' } finally { loading.value = false }
}

watch(activeTab, (tab) => { if (tab === 'seo' && seoSelectedSlug.value) loadSeo() })

onMounted(() => { loadAll(); window.addEventListener('keydown', handleKeyDown) })
onUnmounted(() => { window.removeEventListener('keydown', handleKeyDown) })
</script>

<style scoped>
.builder-page { gap: 22px; }

.header-right { display: flex; gap: 10px; align-items: center; }
.history-controls { display: flex; align-items: center; }

/* Toast */
.toast { display: flex; align-items: center; gap: 10px; padding: 14px 20px; border-radius: 10px; font-weight: 700; font-size: 0.92rem; box-shadow: 0 8px 32px rgba(0,0,0,.12); }
.toast-ok { background: linear-gradient(135deg,#ecfdf5,#d1fae5); color: #065f46; border: 1px solid #a7f3d0; }
.toast-danger { background: linear-gradient(135deg,#fef2f2,#fee2e2); color: #991b1b; border: 1px solid #fca5a5; }
.toast-enter-active, .toast-leave-active { transition: all .3s ease; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateY(-12px); }

/* Tabs */
.builder-tabs { display: flex; flex-wrap: wrap; gap: 6px; padding: 6px; border: 1px solid var(--line); border-radius: 12px; background: white; box-shadow: 0 1px 3px rgba(0,0,0,.04); }
.builder-tabs button { display: inline-flex; align-items: center; gap: 8px; min-height: 42px; padding: 0 16px; border: 0; border-radius: 8px; color: #475569; background: transparent; font-weight: 800; cursor: pointer; transition: all .2s; }
.builder-tabs button:hover:not(.active) { background: #f1f5f9; color: #1e293b; }
.builder-tabs button.active { color: white; background: var(--sirius-red); box-shadow: 0 2px 8px rgba(227,6,19,.25); }
.tab-badge { display: inline-flex; align-items: center; justify-content: center; min-width: 22px; height: 22px; padding: 0 6px; border-radius: 999px; background: rgba(0,0,0,.1); font-size: .72rem; font-weight: 900; }
.builder-tabs button.active .tab-badge { background: rgba(255,255,255,.25); }

/* Grid layouts */
.builder-grid { display: grid; grid-template-columns: minmax(300px,.82fr) minmax(0,1.18fr); gap: 20px; align-items: start; }
.builder-grid-preview { grid-template-columns: minmax(240px,.55fr) minmax(0,.9fr) minmax(320px,.75fr); }
.settings-layout { display: grid; }

/* Panel heads */
.panel-head { display: flex; justify-content: space-between; gap: 14px; margin-bottom: 18px; }
.panel-head.compact { align-items: flex-start; }
.panel-head h2, .editor-card h2 { margin: 0; font-size: 1.15rem; font-weight: 920; }
.panel-head p { margin: 5px 0 0; color: var(--muted); }
.panel-head-actions { display: flex; gap: 8px; flex-shrink: 0; }
.page-select-row { display: flex; gap: 8px; align-items: stretch; }
.page-select-row .field { flex: 1; }

/* Preview toggle icon */
.preview-toggle { width: 38px; height: 38px; flex-shrink: 0; border: 1px solid var(--line); border-radius: 7px; background: #f8fafc; cursor: pointer; display: grid; place-items: center; font-size: 1rem; color: #475569; transition: all .15s; }
.preview-toggle:hover, .preview-toggle.active { background: var(--sirius-red); color: white; border-color: var(--sirius-red); }

/* Copy to dropdown */
.copy-to-wrapper { position: relative; }
.copy-to-dropdown { position: absolute; top: calc(100% + 6px); right: 0; z-index: 200; min-width: 200px; background: white; border: 1px solid var(--line); border-radius: 10px; box-shadow: 0 8px 32px rgba(0,0,0,.12); overflow: hidden; }
.copy-to-dropdown button { display: block; width: 100%; padding: 10px 16px; border: 0; background: transparent; text-align: left; cursor: pointer; font-size: .88rem; font-weight: 700; color: #334155; transition: background .12s; }
.copy-to-dropdown button:hover { background: #f1f5f9; }

/* Bulk toolbar */
.bulk-header { padding: 8px 0 2px; border-bottom: 1px solid var(--line); margin-bottom: 8px; }
.bulk-toolbar { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; padding: 10px 14px; border-radius: 8px; background: #1e293b; color: white; font-weight: 700; font-size: .84rem; margin-bottom: 10px; }
.slide-down-enter-active, .slide-down-leave-active { transition: all .25s ease; }
.slide-down-enter-from, .slide-down-leave-to { opacity: 0; transform: translateY(-8px); }
.btn-sm-flat { display: inline-flex; align-items: center; gap: 5px; padding: 5px 10px; border: 0; border-radius: 6px; background: rgba(255,255,255,.15); color: white; cursor: pointer; font-size: .82rem; font-weight: 700; transition: background .12s; }
.btn-sm-flat:hover { background: rgba(255,255,255,.28); }
.danger-flat { background: rgba(239,68,68,.5); }
.danger-flat:hover { background: rgba(239,68,68,.8); }

/* Block list rows */
.block-list-row { display: flex; align-items: stretch; gap: 6px; }
.block-list-row.is-selected .block-btn { background: rgba(227,6,19,.05); border-color: rgba(227,6,19,.3); }
.block-checkbox-label { display: grid; place-items: center; cursor: pointer; padding: 0 4px; }
.block-checkbox-label input { width: 15px; height: 15px; accent-color: var(--sirius-red); }
.block-btn { flex: 1; display: flex; align-items: center; justify-content: space-between; gap: 12px; padding: 12px; border: 1px solid var(--line); border-radius: 8px; background: white; text-align: left; cursor: pointer; transition: all .15s; }
.block-btn:hover { border-color: #cbd5e1; box-shadow: 0 2px 8px rgba(0,0,0,.04); }
.block-btn.active { border-color: rgba(227,6,19,.38); background: var(--sirius-red-soft); }
.block-btn[draggable="true"] { cursor: grab; }

/* Item list */
.item-list { display: grid; gap: 8px; max-height: 580px; overflow: auto; }
.item-list button { display: flex; align-items: center; justify-content: space-between; gap: 12px; width: 100%; padding: 12px; border: 1px solid var(--line); border-radius: 8px; background: white; text-align: left; cursor: pointer; transition: all .15s; }
.item-list button:hover { border-color: #cbd5e1; }
.item-list button.active { border-color: rgba(227,6,19,.38); background: var(--sirius-red-soft); }
.item-list strong, .item-list small { display: block; }
.item-list small { margin-top: 3px; color: var(--muted); }
.item-list em { flex: 0 0 auto; padding: 4px 8px; border-radius: 999px; font-size: .74rem; font-style: normal; font-weight: 800; }
.item-right { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.block-info { display: flex; align-items: center; gap: 12px; min-width: 0; }
.block-type-icon { flex: 0 0 32px; width: 32px; height: 32px; border-radius: 8px; display: grid; place-items: center; color: white; font-size: 1rem; }
.block-count-badge { display: inline-flex; align-items: center; justify-content: center; min-width: 24px; height: 24px; padding: 0 6px; border-radius: 6px; background: #e2e8f0; color: #475569; font-size: .72rem; font-weight: 900; }
.drag-handle { color: #cbd5e1; cursor: grab; }

/* Editor card */
.editor-card { display: grid; gap: 12px; }
.form-grid, .settings-grid { display: grid; grid-template-columns: repeat(2,minmax(0,1fr)); gap: 12px; }
.settings-grid .wide { grid-column: 1/-1; }
.check-row { display: inline-flex; align-items: center; gap: 10px; color: #334155; font-weight: 800; }
.check-row.mini { font-size: .84rem; font-weight: 700; color: var(--muted); }
.check-row.in-grid { align-self: end; min-height: 46px; }
.check-row input { width: 18px; height: 18px; accent-color: var(--sirius-red); }
.form-actions { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 8px; }
.danger-soft { color: #991b1b; background: #fee2e2; }
.btn-accent { color: white; background: #6366f1; }
.btn-accent:hover { background: #4f46e5; }
.btn-sm { min-height: 36px; padding: 0 12px; font-size: .88rem; }
.code-field { font-family: ui-monospace,monospace; font-size: .9rem; line-height: 1.55; }

/* Editor mode tabs */
.editor-mode-tabs { display: flex; gap: 4px; border-bottom: 2px solid var(--line); margin-bottom: 16px; }
.editor-mode-tabs button { display: inline-flex; align-items: center; gap: 6px; padding: 8px 16px; border: 0; background: transparent; color: var(--muted); font-weight: 700; cursor: pointer; border-bottom: 2px solid transparent; margin-bottom: -2px; transition: all .2s; }
.editor-mode-tabs button.active { color: var(--sirius-red); border-bottom-color: var(--sirius-red); }

/* Visual form */
.visual-form { display: grid; gap: 16px; }
.image-uploader-container { display: flex; flex-direction: column; gap: 10px; margin-top: 4px; }
.image-preview-wrapper { position: relative; width: 100%; max-width: 320px; border-radius: 8px; overflow: hidden; border: 1px solid var(--line); background: var(--panel-soft); }
.image-preview { width: 100%; height: 160px; object-fit: cover; display: block; }
.btn-remove-image { position: absolute; top: 8px; right: 8px; background: rgba(239,68,68,.95); color: white; border: 0; width: 32px; height: 32px; border-radius: 999px; display: grid; place-items: center; cursor: pointer; }
.uploader-controls { display: flex; gap: 10px; flex-wrap: wrap; }
.upload-action-btn { flex-shrink: 0; }

/* Items editor */
.items-editor { display: flex; flex-direction: column; gap: 12px; margin-top: 8px; }
.items-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--line); padding-bottom: 8px; }
.btn-xs { min-height: 32px; padding: 0 12px; font-size: .85rem; border-radius: 6px; }
.items-list-container { display: grid; gap: 12px; max-height: 480px; overflow-y: auto; padding-right: 4px; }
.item-editor-card { border-left: 4px solid var(--sirius-red); background: white; border-top-left-radius: 0; border-bottom-left-radius: 0; }
.item-card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px dashed var(--line); padding-bottom: 6px; }
.item-card-actions { display: flex; gap: 4px; }
.btn-icon { background: transparent; border: 0; width: 28px; height: 28px; border-radius: 4px; display: grid; place-items: center; cursor: pointer; color: var(--muted); transition: background .2s; }
.btn-icon:hover:not(:disabled) { background: #f1f5f9; color: var(--ink); }
.btn-icon:disabled { opacity: .35; cursor: not-allowed; }
.btn-icon.danger-icon:hover { background: #fee2e2; color: #991b1b; }
.item-card-grid { display: grid; grid-template-columns: repeat(2,minmax(0,1fr)); gap: 10px; }
.item-field { display: flex; flex-direction: column; gap: 4px; }
.wide-field { grid-column: 1/-1; }
.field-sm { min-height: 38px; padding: 8px 10px; font-size: .9rem; }
.empty-items-placeholder { padding: 30px; text-align: center; color: var(--muted); border: 2px dashed var(--line); border-radius: 8px; font-style: italic; }
.text-xs { font-size: .75rem; }
.item-image-preview-sm { width: 80px; height: 52px; border-radius: 5px; overflow: hidden; border: 1px solid var(--line); margin-top: 4px; }
.item-image-preview-sm img { width: 100%; height: 100%; object-fit: cover; }
.uploader-controls-compact { display: flex; gap: 6px; }
.uploader-controls-compact .field { flex: 1; }

/* Live Preview */
.preview-panel { display: flex; flex-direction: column; border: 1px solid var(--line); border-radius: 12px; overflow: hidden; background: white; min-height: 600px; }
.preview-header { display: flex; justify-content: space-between; align-items: center; padding: 10px 16px; border-bottom: 1px solid var(--line); background: #f8fafc; font-size: .84rem; font-weight: 700; color: #475569; gap: 8px; }
.preview-iframe { flex: 1; width: 100%; border: 0; }
.preview-placeholder { flex: 1; display: grid; place-items: center; color: #94a3b8; font-style: italic; }

/* SEO */
.form-section-title { margin: 8px 0 0; padding-top: 16px; border-top: 1px solid var(--line); font-size: 1rem; font-weight: 800; color: #334155; }
.seo-analyzer { display: flex; flex-wrap: wrap; gap: 12px; padding: 14px; border-radius: 8px; background: #f8fafc; border: 1px solid var(--line); }
.seo-check { display: flex; align-items: center; gap: 6px; font-size: .82rem; font-weight: 700; }
.seo-good { color: #059669; } .seo-ok { color: #0284c7; } .seo-warn { color: #d97706; } .seo-bad { color: #dc2626; }

/* Modal */
.modal-overlay { position: fixed; inset: 0; z-index: 999; display: grid; place-items: center; padding: 24px; background: rgba(0,0,0,.5); backdrop-filter: blur(4px); }
.modal-content { width: 100%; max-width: 720px; max-height: 80vh; overflow-y: auto; background: white; border-radius: 16px; padding: 28px; box-shadow: 0 24px 70px rgba(0,0,0,.2); }
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.modal-header h2 { margin: 0; font-size: 1.25rem; font-weight: 900; }
.modal-enter-active, .modal-leave-active { transition: all .25s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }

/* Templates */
.template-grid { display: grid; grid-template-columns: repeat(auto-fill,minmax(200px,1fr)); gap: 14px; }
.template-card { display: flex; flex-direction: column; align-items: flex-start; gap: 10px; padding: 18px; border: 2px solid var(--line); border-radius: 12px; background: white; cursor: pointer; text-align: left; transition: all .2s; }
.template-card:hover { border-color: var(--sirius-red); box-shadow: 0 4px 16px rgba(227,6,19,.1); transform: translateY(-2px); }
.template-icon { width: 42px; height: 42px; border-radius: 10px; display: grid; place-items: center; color: white; font-size: 1.15rem; }
.template-card strong { font-size: .95rem; }
.template-card p { margin: 0; color: var(--muted); font-size: .82rem; line-height: 1.5; }
.template-card small { color: #94a3b8; font-weight: 700; font-size: .75rem; }

@media (max-width: 1100px) {
  .builder-grid { grid-template-columns: 1fr; }
  .builder-grid-preview { grid-template-columns: 1fr; }
  .preview-panel { min-height: 400px; }
}
@media (max-width: 640px) {
  .form-grid, .settings-grid { grid-template-columns: 1fr; }
  .panel-head { flex-direction: column; }
  .builder-tabs button { padding: 0 10px; font-size: .82rem; }
  .template-grid { grid-template-columns: 1fr; }
}
</style>
