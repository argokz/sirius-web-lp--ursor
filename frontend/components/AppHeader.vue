<template>
  <v-app-bar 
    :class="{'header-scrolled': isScrolled}"
    elevation="0" 
    app
    height="80"
  >
    <v-container class="d-flex align-center">
      <v-btn
        v-if="$vuetify.display.smAndDown"
        icon="mdi-menu"
        variant="text"
        @click="drawer = !drawer"
        color="primary"
        class="mr-2"
      />
      
      <NuxtLink to="/" class="brand-link d-flex align-center text-decoration-none">
        <div class="logo-wrapper mr-3">
          <SiriusLogo size="40" />
        </div>
        <div class="brand-text">
          <span class="brand-name primary-gradient-text" :class="{'name-compact': isScrolled}">СИРИУС</span>
          <span v-if="!isScrolled" class="brand-tagline">Инновации в тепле</span>
        </div>
      </NuxtLink>
      
      <v-spacer />
      
      <div v-if="$vuetify.display.mdAndUp" class="nav-links d-flex align-center">
        <NuxtLink
          v-for="item in menuItems"
          :key="item.to"
          :to="item.to"
          class="nav-item text-decoration-none mx-3"
          active-class="nav-item-active"
        >
          {{ item.title }}
        </NuxtLink>
        
        <v-btn
          to="/demo"
          color="primary"
          variant="elevated"
          class="ml-6 action-btn shadow-premium"
          rounded="pill"
          size="large"
        >
          Заявка на демо
        </v-btn>
      </div>
    </v-container>
  </v-app-bar>

  <v-navigation-drawer
    v-model="drawer"
    temporary
    location="left"
    class="mobile-drawer"
    overlay-opacity="0.5"
  >
    <v-list class="pa-4">
      <div class="text-center mb-8 pt-4">
          <SiriusLogo size="60" class="mx-auto mb-2" />
          <h2 class="primary-gradient-text">СИРИУС</h2>
      </div>
      <v-list-item
        v-for="item in menuItems"
        :key="item.to"
        :to="item.to"
        @click="drawer = false"
        rounded="lg"
        class="mb-2"
        color="primary"
      >
        <v-list-item-title class="font-weight-bold">{{ item.title }}</v-list-item-title>
      </v-list-item>
      <v-divider class="my-4" />
      <v-btn
        block
        to="/demo"
        color="primary"
        size="x-large"
        rounded="pill"
        @click="drawer = false"
      >
        Заявка на демо
      </v-btn>
    </v-list>
  </v-navigation-drawer>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const drawer = ref(false)
const isScrolled = ref(false)

const handleScroll = () => {
  isScrolled.value = window.scrollY > 50
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

const menuItems = [
  { title: 'Главная', to: '/' },
  { title: 'Моделирование', to: '/modeling' },
  { title: 'ГИС', to: '/gis' },
  { title: 'Ремонты', to: '/maintenance' },
  { title: 'Web-версия', to: '/web-version' },
  { title: 'Контакты', to: '/contacts' },
]
</script>

<style scoped>
.v-app-bar {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
  background: rgba(255, 255, 255, 0.5) !important;
  backdrop-filter: blur(10px);
  border-bottom: 1px solid transparent !important;
}

.header-scrolled {
  height: 64px !important;
  background: rgba(255, 255, 255, 0.9) !important;
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(59, 130, 246, 0.1) !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05) !important;
}

.name-compact {
  font-size: 1.25rem !important;
}

.brand-link {
    transition: all 0.3s ease;
}

.brand-link:hover {
    transform: scale(1.02);
}

.logo-wrapper {
    filter: drop-shadow(0 4px 6px rgba(0,0,0,0.05));
}

.brand-text {
    display: flex;
    flex-direction: column;
}

.brand-name {
    font-size: 1.5rem;
    font-weight: 900;
    letter-spacing: 1px;
    line-height: 1;
}

.brand-tagline {
    font-size: 0.65rem;
    font-weight: 600;
    text-transform: uppercase;
    color: #64748b;
    letter-spacing: 2px;
    margin-top: 4px;
}

.nav-item {
    font-weight: 600;
    color: #1e293b;
    font-size: 0.95rem;
    position: relative;
    padding: 8px 0;
    transition: color 0.3s ease;
}

.nav-item::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 0;
    height: 2px;
    background: linear-gradient(90deg, #3b82f6, #8b5cf6);
    transition: width 0.3s ease;
    border-radius: 2px;
}

.nav-item:hover::after, .nav-item-active::after {
    width: 100%;
}

.nav-item:hover {
    color: #3b82f6;
}

.shadow-premium {
    box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.4) !important;
}

.action-btn {
    text-transform: none;
    font-weight: 700;
    letter-spacing: 0.5px;
}

.mobile-drawer {
    backdrop-filter: blur(10px);
}
</style>

