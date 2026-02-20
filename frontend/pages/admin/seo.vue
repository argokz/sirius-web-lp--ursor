<template>
  <div>
    <h1 class="text-h4 mb-4">SEO метатеги</h1>
    
    <v-card elevation="2">
      <v-tabs v-model="tab">
        <v-tab value="general">Общие</v-tab>
        <v-tab value="og">Open Graph</v-tab>
        <v-tab value="twitter">Twitter</v-tab>
      </v-tabs>

      <v-card-text>
        <v-tabs-window v-model="tab">
          <v-tabs-window-item value="general">
            <v-form>
              <v-text-field v-model="seo.title" label="Title" />
              <v-textarea v-model="seo.description" label="Description" rows="3" />
              <v-text-field v-model="seo.keywords" label="Keywords" />
            </v-form>
          </v-tabs-window-item>
          <v-tabs-window-item value="og">
            <v-form>
              <v-text-field v-model="seo.og_title" label="OG Title" />
              <v-textarea v-model="seo.og_description" label="OG Description" rows="3" />
              <v-text-field v-model="seo.og_image" label="OG Image URL" />
              <v-text-field v-model="seo.og_type" label="OG Type" />
            </v-form>
          </v-tabs-window-item>
          <v-tabs-window-item value="twitter">
            <v-form>
              <v-text-field v-model="seo.twitter_title" label="Twitter Title" />
              <v-textarea v-model="seo.twitter_description" label="Twitter Description" rows="3" />
              <v-text-field v-model="seo.twitter_image" label="Twitter Image URL" />
            </v-form>
          </v-tabs-window-item>
        </v-tabs-window>
        
        <v-btn color="primary" class="mt-4" @click="saveSEO">
          Сохранить
        </v-btn>
      </v-card-text>
    </v-card>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'admin',
  middleware: 'auth'
})

useHead({
  title: 'SEO метатеги - Сириус'
})

const tab = ref('general')
const seo = reactive({
  title: '',
  description: '',
  keywords: '',
  og_title: '',
  og_description: '',
  og_image: '',
  og_type: 'website',
  twitter_title: '',
  twitter_description: '',
  twitter_image: ''
})

const saveSEO = () => {
  // TODO: Implement SEO save API
  console.log('Saving SEO:', seo)
}
</script>

