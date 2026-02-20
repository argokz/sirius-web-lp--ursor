<template>
  <v-footer class="premium-footer py-12">
    <div class="footer-blobs">
      <div class="footer-blob blob-1"></div>
      <div class="footer-blob blob-2"></div>
    </div>
    <v-container>
      <v-row>
        <v-col cols="12" md="4" class="mb-8 mb-md-0">
          <div class="footer-brand">
            <div class="d-flex align-center mb-4">
              <SiriusLogo size="40" class="mr-3" />
              <h2 class="primary-gradient-text font-weight-black">СИРИУС</h2>
            </div>
            <p class="footer-description mb-6">
              Комплексные инновационные решения для цифровизации и повышения энергетической эффективности систем теплоснабжения.
            </p>
          </div>
        </v-col>
        
        <v-col cols="12" sm="6" md="4" class="mb-8 mb-md-0">
          <h4 class="footer-title mb-6">Навигация</h4>
          <v-list class="bg-transparent pa-0">
            <v-list-item
              v-for="item in links"
              :key="item.to"
              :to="item.to"
              class="footer-link-item pa-0 mb-2"
              density="compact"
            >
              {{ item.title }}
            </v-list-item>
          </v-list>
        </v-col>
        
        <v-col cols="12" sm="6" md="4">
          <h4 class="footer-title mb-6">Контакты</h4>
          <div class="contact-info">
            <v-btn
              variant="text"
              prepend-icon="mdi-email"
              href="mailto:info@itwin.kz"
              class="contact-link mb-3"
            >
              info@itwin.kz
            </v-btn>
            <v-btn
              variant="text"
              prepend-icon="mdi-phone"
              class="contact-link mb-3"
            >
              +7 (XXX) XXX-XX-XX
            </v-btn>
            <div class="social-links mt-4">
              <v-btn icon="mdi-facebook" color="primary" variant="tonal" class="mr-2" />
              <v-btn icon="mdi-whatsapp" color="success" variant="tonal" />
            </div>
          </div>
        </v-col>
      </v-row>
      
      <v-divider class="my-8 footer-divider" />
      
      <div class="footer-bottom d-flex flex-column flex-md-row justify-space-between align-center">
        <p class="copyright mb-4 mb-md-0">
          &copy; {{ new Date().getFullYear() }} ТГИД-07. Все права защищены.
        </p>
        <div class="footer-bottom-links">
          <NuxtLink to="#" class="mr-6">Конфиденциальность</NuxtLink>
          <NuxtLink to="#">Оферта</NuxtLink>
        </div>
      </div>
    </v-container>
  </v-footer>
</template>

<script setup lang="ts">
const links = [
  { title: 'О системе', to: '/product' },
  { title: 'Моделирование', to: '/modeling' },
  { title: 'Паспортизация', to: '/gis' },
  { title: 'Ремонты', to: '/maintenance' },
  { title: 'Контакты', to: '/contacts' }
]
</script>

<style scoped>
.premium-footer {
  background: #0f172a !important;
  color: #94a3b8 !important;
  position: relative;
  overflow: hidden;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.footer-blobs {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  pointer-events: none;
}

.footer-blob {
  position: absolute;
  width: 300px;
  height: 300px;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.1;
}

.blob-1 {
  background: #3b82f6;
  top: -150px;
  left: -50px;
}

.blob-2 {
  background: #8b5cf6;
  bottom: -150px;
  right: -50px;
}

.footer-description {
  line-height: 1.8;
  font-size: 0.95rem;
}

.footer-title {
  color: white;
  font-size: 1.1rem;
  letter-spacing: 1px;
  text-transform: uppercase;
  font-weight: 700;
}

.footer-link-item {
  color: #94a3b8 !important;
  transition: all 0.3s ease;
}

.footer-link-item:hover {
  color: white !important;
  padding-left: 8px !important;
}

.contact-link {
  color: #94a3b8 !important;
  padding-left: 0 !important;
  font-size: 1rem !important;
  text-transform: none !important;
}

.contact-link:hover {
  color: white !important;
}

.footer-divider {
  border-color: rgba(255, 255, 255, 0.05) !important;
}

.copyright {
  font-size: 0.9rem;
}

.footer-bottom-links a {
  color: #64748b;
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.3s ease;
}

.footer-bottom-links a:hover {
  color: white;
}
</style>

