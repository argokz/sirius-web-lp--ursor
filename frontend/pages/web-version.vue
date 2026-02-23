<template>
  <div class="web-version-page">
    <!-- Hero Section -->
    <section class="hero-section glass-effect">
      <v-container>
        <v-row align="center">
          <v-col cols="12" md="6">
            <div class="badge fade-in-up">Раздел 5. Web-версия</div>
            <h1 class="display-1 fade-in-up delay-1">Мобильность и доступность данных</h1>
            <p class="subtitle fade-in-up delay-2">
              Обеспечьте доступ к актуальной схеме теплоснабжения для руководства 
              и выездных бригад без установки сложного ПО.
            </p>
          </v-col>
          <v-col cols="12" md="6" class="scroll-reveal-right">
            <div class="device-mockup">
               <div class="smartphone">
                  <div class="screen">
                    <v-icon icon="mdi-web" size="48" color="primary" />
                  </div>
               </div>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Capabilities -->
    <section class="capabilities py-16">
      <v-container>
        <v-row>
          <v-col v-for="(cap, index) in capabilities" :key="index" cols="12" md="4" class="scroll-reveal">
            <v-hover v-slot="{ isHovering, props }">
              <v-card
                v-bind="props"
                :elevation="isHovering ? 12 : 2"
                class="cap-card pa-6"
                rounded="xl"
              >
                <v-icon :icon="cap.icon" size="40" color="primary" class="mb-4" />
                <h3 class="mb-2">{{ cap.title }}</h3>
                <p>{{ cap.description }}</p>
              </v-card>
            </v-hover>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Security & Access -->
    <section class="security py-16 bg-light">
      <v-container>
        <v-row align="center">
          <v-col cols="12" md="6" class="scroll-reveal-left">
            <h2 class="section-title">Безопасность и контроль</h2>
            <p>Разграничение прав доступа (только чтение или запись) и защита данных через SSL-шифрование корпоративного уровня.</p>
            <v-alert
              type="info"
              variant="tonal"
              title="Доступность"
              text="Работает в Chrome, Safari и любом другом браузере на ПК, планшете или смартфоне."
              class="mt-6"
            />
          </v-col>
          <v-col cols="12" md="6" class="scroll-reveal-right">
             <div class="security-visual">
                <v-icon icon="mdi-shield-lock-outline" size="150" color="primary" class="blur-effect" />
             </div>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- CTA -->
    <section class="cta-section py-16 text-center">
      <v-container>
        <v-btn size="x-large" color="primary" block sm="auto" rounded="pill" to="/demo">
          Запросить демо-доступ
          <v-icon end icon="mdi-account-key" />
        </v-btn>
      </v-container>
    </section>
  </div>
</template>

<script setup lang="ts">
const capabilities = [
  { title: 'Работа в браузере', description: 'Никаких установок. Мгновенный запуск на любом устройстве.', icon: 'mdi-monitor-cellphone' },
  { title: 'Поиск "в поле"', description: 'Быстрый поиск абонентов и камер прямо на объекте.', icon: 'mdi-map-marker-distance' },
  { title: 'Живые данные', description: 'Просмотр пьезометрических графиков и режимов удаленно.', icon: 'mdi-broadcast' }
]

const { observeElements } = useScrollAnimation()

onMounted(() => {
  observeElements()
})

useSEO({
  title: 'Web-версия ТГИД-07: Доступ к сети из любой точки мира',
  description: 'Мобильность для выездных бригад и прозрачность для руководства. Работайте с актуальной схемой теплоснабжения в браузере на любом устройстве.'
})
</script>

<style scoped>
.web-version-page { background: #ffffff; }

.hero-section {
  padding: 100px 0;
  background: radial-gradient(circle at 70% 30%, rgba(56, 189, 248, 0.05), transparent);
}

.badge {
  display: inline-block;
  padding: 6px 16px;
  background: rgba(14, 165, 233, 0.1);
  color: #0ea5e9;
  border-radius: 20px;
  font-weight: 600;
  margin-bottom: 24px;
}

.display-1 { font-size: 3rem; font-weight: 800; margin-bottom: 24px; }

.device-mockup {
  display: flex;
  justify-content: center;
  perspective: 1000px;
}

.smartphone {
  width: 200px;
  height: 400px;
  background: #1e293b;
  border-radius: 36px;
  padding: 12px;
  box-shadow: 0 50px 100px rgba(0,0,0,0.1);
  transform: rotateY(-20deg) rotateX(10deg);
}

.screen {
  width: 100%;
  height: 100%;
  background: #ffffff;
  border-radius: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cap-card {
  height: 100%;
  transition: all 0.3s ease;
  border: 1px solid #f1f5f9;
}

.bg-light { background: #f8fafc; }

.blur-effect {
  filter: drop-shadow(0 0 20px rgba(14, 165, 233, 0.2));
}

@media (max-width: 600px) {
  .display-1 { font-size: 2rem; }
  .smartphone { transform: none; width: 160px; height: 320px; }
}
</style>
