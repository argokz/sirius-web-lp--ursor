<template>
  <div class="roles">
    <div class="roles-tabs" role="tablist" aria-label="Роль">
      <button
        v-for="(role, i) in ROLES"
        :key="role.id"
        type="button"
        role="tab"
        :aria-selected="i === current"
        :class="{ active: i === current }"
        @click="current = i"
      >
        <UIcon :name="role.icon" />
        <span>{{ role.title }}</span>
      </button>
    </div>

    <div class="roles-body" role="tabpanel">
      <p class="roles-lead">{{ role.lead }}</p>
      <TransitionGroup tag="ol" name="role-list" class="roles-list">
        <li v-for="(item, i) in role.pages" :key="`${role.id}-${item.url}`" :style="{ transitionDelay: `${i * 45}ms` }">
          <NuxtLink :to="item.url">
            <span class="roles-num">{{ String(i + 1).padStart(2, '0') }}</span>
            <span class="roles-title">{{ item.title }}</span>
            <span class="roles-url">{{ item.url.replace('/docs/', '') }}</span>
          </NuxtLink>
        </li>
      </TransitionGroup>
      <div class="roles-actions">
        <NuxtLink v-if="role.track" :to="`/learn/${role.track.id}`" class="roles-btn">
          <UIcon name="i-lucide-graduation-cap" /> Трек курса «{{ role.track.title }}»
        </NuxtLink>
        <NuxtLink v-if="role.journey" :to="role.journey" class="roles-btn ghost">
          <UIcon name="i-lucide-circle-play" /> Ролик «от начала до конца»
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
/** Маршрут чтения справки по роли: шесть страниц по порядку, трек курса и сквозной ролик. */
const ROLES = [
  {
    id: 'operations',
    icon: 'i-lucide-hard-hat',
    title: 'Диспетчер',
    lead: 'Авария, отключение, бригада: найти, локализовать, оповестить и закрыть наряд.',
    track: { id: 'operations', title: 'Эксплуатация и диспетчер' },
    journey: '/docs/journeys/incident',
    pages: [
      { title: 'Локализация аварий', url: '/docs/operations/outage-simulation' },
      { title: 'Отключения', url: '/docs/operations/outages' },
      { title: 'Наряды и заявки', url: '/docs/operations/work-orders' },
      { title: 'Трассировка сети', url: '/docs/operations/network-trace' },
      { title: 'Нарушения', url: '/docs/operations/defect' },
      { title: 'Показатели', url: '/docs/operations/kpi-dashboard' }
    ]
  },
  {
    id: 'regime',
    icon: 'i-lucide-gauge',
    title: 'Режимщик',
    lead: 'Расчёт режима и разбор результата: протокол, анализ, пьезометр, сценарии «что если».',
    track: { id: 'regime', title: 'Режимщик' },
    journey: '/docs/journeys/calculation',
    pages: [
      { title: 'Расчёт режима', url: '/docs/analysis/calculation' },
      { title: 'Протокол расчёта', url: '/docs/analysis/protocol' },
      { title: 'Анализ режима', url: '/docs/analysis/regime-analysis' },
      { title: 'Пьезометрический график', url: '/docs/analysis/piezometer' },
      { title: 'Гидравлический режим на карте', url: '/docs/analysis/hydraulic-thematic' },
      { title: 'Сценарии «что если»', url: '/docs/source-data/scenarios' }
    ]
  },
  {
    id: 'editor',
    icon: 'i-lucide-pen-tool',
    title: 'Редактор сети',
    lead: 'Паспорт и схема сети: правка с проверкой после каждого шага и откатом.',
    track: { id: 'editor', title: 'Редактор сети' },
    journey: '/docs/journeys/network-edit',
    pages: [
      { title: 'Редактор сети', url: '/docs/source-data/network-editor' },
      { title: 'Трасса: предпросмотр и создание', url: '/docs/source-data/chain' },
      { title: 'Проверка после правки', url: '/docs/source-data/topology-check' },
      { title: 'История правок и откат', url: '/docs/source-data/edit-history' },
      { title: 'Импорт SHP / Excel / координат', url: '/docs/source-data/network-import' },
      { title: 'Качество данных', url: '/docs/source-data/data-quality' }
    ]
  },
  {
    id: 'chief',
    icon: 'i-lucide-chart-line',
    title: 'Руководитель',
    lead: 'Состояние сети в цифрах: износ, прогноз аварийности, план перекладок и отчёты.',
    track: { id: 'novice', title: 'Новичок' },
    journey: '/docs/journeys/reports',
    pages: [
      { title: 'Показатели', url: '/docs/operations/kpi-dashboard' },
      { title: 'Износ и план ремонтов', url: '/docs/analysis/wear-index' },
      { title: 'Прогноз аварийности', url: '/docs/analysis/failure-forecast' },
      { title: 'Перспективный прирост нагрузки', url: '/docs/analysis/load-perspective' },
      { title: 'Тематическая карта', url: '/docs/analysis/thematic-map' },
      { title: 'Записка к плану ремонтов (ИИ)', url: '/docs/ai/repair-memo' }
    ]
  },
  {
    id: 'admin',
    icon: 'i-lucide-server-cog',
    title: 'Администратор',
    lead: 'Пользователи и права, журнал действий, города, резервные копии и персональные данные.',
    track: { id: 'admin', title: 'Администратор' },
    journey: '/docs/journeys/admin',
    pages: [
      { title: 'Пользователи', url: '/docs/admin/users-admin' },
      { title: 'Роли и права', url: '/docs/administration/roles-rights' },
      { title: 'Журнал действий', url: '/docs/admin/activity-log' },
      { title: 'Несколько городов на одном API', url: '/docs/administration/cities' },
      { title: 'Резервные копии и данные', url: '/docs/administration/backups' },
      { title: 'Персональные данные', url: '/docs/administration/personal-data' }
    ]
  },
  {
    id: 'dev',
    icon: 'i-lucide-code-xml',
    title: 'Разработчик',
    lead: 'Подключить свою систему: API v2, вебхуки, MCP, OGC и встраиваемая карта.',
    track: { id: 'dev', title: 'Разработчик' },
    journey: '',
    pages: [
      { title: 'API v2 для внешних систем', url: '/docs/developers/api-v2' },
      { title: 'Вебхуки: события и подпись', url: '/docs/developers/webhooks' },
      { title: 'MCP: протокол для клиентов', url: '/docs/developers/mcp' },
      { title: 'OGC API — Features и Processes', url: '/docs/developers/ogc' },
      { title: 'Встраивание карты: SDK', url: '/docs/developers/embed' },
      { title: 'Устройство кода', url: '/docs/developers/architecture' }
    ]
  }
]

const current = ref(0)
const role = computed(() => ROLES[current.value]!)
</script>

<style scoped>
.roles {
  display: grid;
  grid-template-columns: 240px minmax(0, 1fr);
  border-top: 1px solid var(--ink);
}

.roles-tabs {
  display: flex;
  flex-direction: column;
  border-right: 1px solid var(--line);
}

.roles-tabs button {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px 14px 0;
  border: 0;
  border-bottom: 1px solid var(--line);
  color: var(--muted);
  background: transparent;
  font-size: 0.98rem;
  text-align: left;
  cursor: pointer;
  transition: color 0.2s ease, padding 0.25s ease;
}

.roles-tabs button:hover {
  color: var(--ink);
}

.roles-tabs button.active {
  padding-left: 12px;
  color: var(--ink);
  box-shadow: inset 2px 0 0 var(--sirius-red);
}

.roles-tabs svg {
  width: 18px;
  height: 18px;
}

.roles-body {
  padding: 18px 0 0 32px;
}

.roles-lead {
  margin: 0 0 14px;
  color: var(--ink-2);
  font-family: var(--serif);
  font-size: 1.15rem;
}

.roles-list {
  margin: 0;
  padding: 0;
  list-style: none;
}

.roles-list a {
  display: grid;
  grid-template-columns: 34px minmax(0, 1fr) auto;
  gap: 12px;
  align-items: baseline;
  padding: 11px 0;
  border-bottom: 1px solid var(--line);
  color: var(--ink);
  transition: padding 0.25s ease, color 0.2s ease;
}

.roles-list a:hover {
  padding-left: 8px;
  color: var(--accent);
}

.roles-num {
  color: var(--accent);
  font-family: var(--mono);
  font-size: 0.72rem;
}

.roles-url {
  color: var(--muted);
  font-family: var(--mono);
  font-size: 0.68rem;
}

.roles-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 20px;
}

.roles-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border: 1px solid var(--ink);
  border-radius: var(--radius-sm);
  color: var(--on-dark);
  background: var(--ink);
  font-size: 0.9rem;
}

.roles-btn.ghost {
  color: var(--ink);
  background: transparent;
}

.role-list-enter-active {
  transition: opacity 0.35s ease, transform 0.35s ease;
}

.role-list-enter-from {
  opacity: 0;
  transform: translateX(-10px);
}

.role-list-leave-active {
  display: none;
}

@media (max-width: 760px) {
  .roles {
    grid-template-columns: 1fr;
  }

  .roles-tabs {
    flex-direction: row;
    overflow-x: auto;
    border-right: 0;
    border-bottom: 1px solid var(--line);
  }

  .roles-tabs button {
    flex: 0 0 auto;
    padding: 12px 14px;
    border-bottom: 0;
  }

  .roles-tabs button.active {
    padding-left: 14px;
    box-shadow: inset 0 -2px 0 var(--sirius-red);
  }

  .roles-body {
    padding-left: 0;
  }

  .roles-url {
    display: none;
  }
}
</style>
