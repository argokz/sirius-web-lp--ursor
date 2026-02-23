<template>
  <v-app-bar 
    :class="{'header-scrolled': isScrolled}"
    elevation="0" 
    app
    height="80"
  >
    <v-container class="d-flex align-center">
      <div class="header-container-pipe">
        <v-btn
          v-if="$vuetify.display.smAndDown"
          icon="mdi-menu"
          variant="text"
          @click="drawer = !drawer"
          color="white"
          class="mr-2"
        />
        
        <NuxtLink to="/" class="brand-link d-flex align-center text-decoration-none">
          <div class="logo-wrapper mr-3">
            <SiriusLogo size="32" />
          </div>
          <div class="brand-text">
            <span class="brand-name">СИРИУС</span>
          </div>
        </NuxtLink>

        <!-- Small Industrial Manometer -->
        <div class="header-manometer ml-4 d-none d-md-flex">
           <svg width="24" height="24" viewBox="0 0 24 24">
             <circle cx="12" cy="12" r="10" fill="#1e293b" stroke="#64748b" stroke-width="1.5" />
             <circle cx="12" cy="12" r="8" fill="#f8fafc" />
             <g class="needle-anim">
               <line x1="12" y1="12" x2="12" y2="6" stroke="#ef4444" stroke-width="1.5" stroke-linecap="round" />
               <circle cx="12" cy="12" r="1.5" fill="#ef4444" />
             </g>
           </svg>
        </div>
        
        <v-spacer />
        
        <div v-if="$vuetify.display.mdAndUp" class="nav-links d-flex align-center">
          <NuxtLink
            v-for="item in menuItems"
            :key="item.to"
            :to="item.to"
            class="nav-item text-decoration-none"
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
            size="small"
          >
            Демо
          </v-btn>
        </div>
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
  background: transparent !important;
  border-bottom: none !important;
  overflow: visible !important;
}

:deep(.v-toolbar__content) {
  overflow: visible !important;
  padding: 0 16px !important;
}

.header-container-pipe {
  width: 100%;
  height: 60px;
  background: linear-gradient(180deg, 
    #0f172a 0%, 
    #334155 30%, 
    #64748b 50%, 
    #334155 70%, 
    #0f172a 100%
  );
  border-radius: 100px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  position: relative;
  display: flex;
  align-items: center;
  padding: 0 30px;
  box-shadow: 
    0 10px 25px rgba(0,0,0,0.4),
    inset 0 2px 4px rgba(255,255,255,0.1),
    inset 0 -2px 4px rgba(0,0,0,0.4);
  transition: all 0.4s ease;
}

.header-scrolled .header-container-pipe {
  height: 52px;
  margin-top: 4px;
  background: linear-gradient(180deg, 
    #1e293b 0%, 
    #475569 30%, 
    #94a3b8 50%, 
    #475569 70%, 
    #1e293b 100%
  );
  box-shadow: 0 5px 15px rgba(0,0,0,0.5);
}

/* Industrial Joint Accents */
.header-container-pipe::before,
.header-container-pipe::after {
  content: '';
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 12px;
  height: calc(100% + 10px);
  background: #1e293b;
  border: 1px solid #475569;
  border-radius: 4px;
  z-index: -1;
}

.header-container-pipe::before { left: 40px; }
.header-container-pipe::after { right: 40px; }

.brand-link {
    transition: all 0.3s ease;
    z-index: 2;
}

.brand-link:hover {
    transform: scale(1.05) rotate(-1deg);
}

.logo-wrapper {
    filter: drop-shadow(0 0 10px rgba(59, 130, 246, 0.5));
}

.brand-name {
    font-size: 1.4rem;
    font-weight: 950;
    letter-spacing: 2px;
    color: white;
    text-shadow: 0 2px 4px rgba(0,0,0,0.5);
}

.nav-item {
    font-weight: 700;
    color: rgba(255, 255, 255, 0.8) !important;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 6px 12px;
    border-radius: 6px;
    transition: all 0.3s ease;
    margin: 0 4px;
}

.nav-item:hover {
    color: #3b82f6 !important;
    background: rgba(255, 255, 255, 0.05);
}

.nav-item-active {
    color: #ffffff !important;
    background: rgba(59, 130, 246, 0.4);
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

.action-btn {
    background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    font-weight: 800 !important;
    font-size: 0.75rem !important;
    box-shadow: 0 4px 10px rgba(37, 99, 235, 0.4) !important;
}

@keyframes gauge-wiggle {
  0%, 100% { transform: rotate(-30deg); }
  50% { transform: rotate(45deg); }
}

.needle-anim {
  animation: gauge-wiggle 3s ease-in-out infinite;
  transform-origin: 12px 12px;
}

@media (max-width: 960px) {
  .header-container-pipe {
    padding: 0 15px;
    margin: 0 10px;
    width: calc(100% - 20px);
  }
}
</style>

