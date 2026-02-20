<template>
  <v-app>
    <v-navigation-drawer
      v-model="drawer"
      :temporary="$vuetify.display.mobile"
      permanent
      location="left"
    >
      <v-list>
        <v-list-item>
          <v-list-item-title class="text-h6 font-weight-bold">
            Панель управления
          </v-list-item-title>
        </v-list-item>
        <v-divider />
        <v-list-item
          v-for="item in menuItems"
          :key="item.to"
          :to="item.to"
          :prepend-icon="item.icon"
        >
          <v-list-item-title>{{ item.title }}</v-list-item-title>
        </v-list-item>
        <v-divider />
        <v-list-item @click="handleLogout" prepend-icon="mdi-logout">
          <v-list-item-title>Выход</v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar color="primary" elevation="2">
      <v-app-bar-nav-icon
        v-if="$vuetify.display.mobile"
        @click="drawer = !drawer"
      />
      <v-toolbar-title>Админ-панель Сириус</v-toolbar-title>
      <v-spacer />
      <v-btn icon="mdi-account-circle" />
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <slot />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { ref } from 'vue'

definePageMeta({
  middleware: 'auth'
})

const { logout } = useAuth()
const drawer = ref(true)

const menuItems = [
  { title: 'Контент', to: '/admin/content', icon: 'mdi-file-document' },
  { title: 'SEO метатеги', to: '/admin/seo', icon: 'mdi-search-web' },
  { title: 'Заявки на демо', to: '/admin/demo-requests', icon: 'mdi-email' },
  { title: 'Пользователи', to: '/admin/users', icon: 'mdi-account-group' },
  { title: 'Аналитика', to: '/admin/analytics', icon: 'mdi-chart-line' }
]

const handleLogout = () => {
  logout()
}
</script>

