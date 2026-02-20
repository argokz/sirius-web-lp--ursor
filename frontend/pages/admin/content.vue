<template>
  <div>
    <div class="d-flex justify-space-between align-center mb-4">
      <h1 class="text-h4">Управление контентом</h1>
      <v-btn color="primary" @click="showDialog = true">
        <v-icon icon="mdi-plus" class="mr-2" />
        Добавить контент
      </v-btn>
    </div>

    <v-card elevation="2">
      <v-data-table
        :headers="headers"
        :items="items"
        :loading="loading"
      >
        <template v-slot:item.actions="{ item }">
          <v-btn
            icon="mdi-pencil"
            size="small"
            @click="editItem(item)"
          />
          <v-btn
            icon="mdi-delete"
            size="small"
            color="error"
            @click="deleteItem(item)"
          />
        </template>
      </v-data-table>
    </v-card>

    <v-dialog v-model="showDialog" max-width="600">
      <v-card>
        <v-card-title>
          {{ editingItem ? 'Редактировать контент' : 'Добавить контент' }}
        </v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-text-field
              v-model="form.content_key"
              label="Ключ контента"
              :rules="[rules.required]"
            />
            <v-select
              v-model="form.content_type"
              label="Тип контента"
              :items="['text', 'heading', 'title']"
              :rules="[rules.required]"
            />
            <v-textarea
              v-model="form.content_value"
              label="Значение"
              :rules="[rules.required]"
              rows="4"
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="showDialog = false">Отмена</v-btn>
          <v-btn color="primary" @click="saveItem" :disabled="!valid">
            Сохранить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'admin',
  middleware: 'auth'
})

useHead({
  title: 'Управление контентом - Сириус'
})

const { token } = useAuth()
const config = useRuntimeConfig()

const loading = ref(false)
const showDialog = ref(false)
const valid = ref(false)
const editingItem = ref<any>(null)
const items = ref([])

const form = reactive({
  content_key: '',
  content_type: '',
  content_value: ''
})

const headers = [
  { title: 'Ключ', key: 'content_key' },
  { title: 'Тип', key: 'content_type' },
  { title: 'Значение', key: 'content_value' },
  { title: 'Действия', key: 'actions', sortable: false }
]

const rules = {
  required: (value: string) => !!value || 'Обязательное поле'
}

const fetchItems = async () => {
  loading.value = true
  try {
    items.value = await $fetch(`${config.public.apiBase}/api/admin/content`, {
      headers: {
        Authorization: `Bearer ${token.value}`
      }
    })
  } catch (error) {
    console.error('Error fetching content:', error)
  } finally {
    loading.value = false
  }
}

const saveItem = async () => {
  try {
    if (editingItem.value) {
      await $fetch(`${config.public.apiBase}/api/admin/content/${editingItem.value.id}`, {
        method: 'PUT',
        headers: {
          Authorization: `Bearer ${token.value}`
        },
        body: form
      })
    } else {
      await $fetch(`${config.public.apiBase}/api/admin/content`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${token.value}`
        },
        body: form
      })
    }
    showDialog.value = false
    editingItem.value = null
    Object.keys(form).forEach(key => {
      form[key as keyof typeof form] = ''
    })
    fetchItems()
  } catch (error) {
    console.error('Error saving content:', error)
  }
}

const editItem = (item: any) => {
  editingItem.value = item
  form.content_key = item.content_key
  form.content_type = item.content_type
  form.content_value = item.content_value
  showDialog.value = true
}

const deleteItem = async (item: any) => {
  if (confirm('Удалить этот элемент контента?')) {
    try {
      await $fetch(`${config.public.apiBase}/api/admin/content/${item.id}`, {
        method: 'DELETE',
        headers: {
          Authorization: `Bearer ${token.value}`
        }
      })
      fetchItems()
    } catch (error) {
      console.error('Error deleting content:', error)
    }
  }
}

onMounted(() => {
  fetchItems()
})
</script>

