<template>
  <v-container class="my-10">
    <v-row>
      <v-col cols="12" class="text-center mb-8">
        <h1 class="text-h3 mb-4">Блог и новости</h1>
        <p class="text-h6 text-grey">Актуальные новости и статьи о системе ТГИД-07</p>
      </v-col>
    </v-row>

    <v-row>
      <v-col
        cols="12"
        md="4"
        v-for="(post, index) in posts"
        :key="index"
      >
        <v-card elevation="2" height="100%">
          <v-img
            :src="post.image"
            height="200"
            cover
          />
          <v-card-title>{{ post.title }}</v-card-title>
          <v-card-subtitle>{{ post.date }}</v-card-subtitle>
          <v-card-text>
            <p>{{ post.excerpt }}</p>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" variant="text">Читать далее</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
useSEO({
  title: 'Блог - Сириус',
  description: 'Новости и статьи о системе ТГИД-07 и автоматизации теплоснабжения'
})
useStructuredData()

const posts = [
  {
    title: 'Новые возможности ТГИД-07',
    date: '15 января 2024',
    excerpt: 'Рассказываем о последних обновлениях системы и новых функциях',
    image: '/main-func.png'
  },
  {
    title: 'Внедрение системы на объекте',
    date: '10 января 2024',
    excerpt: 'Кейс успешного внедрения ТГИД-07 на крупном теплоснабжающем предприятии',
    image: '/main-func.png'
  },
  {
    title: 'Оптимизация режимов работы',
    date: '5 января 2024',
    excerpt: 'Как система ТГИД-07 помогает оптимизировать режимы работы тепловых сетей',
    image: '/main-func.png'
  }
]
</script>

