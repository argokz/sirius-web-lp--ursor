<template>
  <div class="dev">
    <svg class="dev-iso" viewBox="0 0 420 340" aria-hidden="true">
      <g v-for="(plate, i) in PLATES" :key="plate.label" class="dev-plate" :style="{ animationDelay: `${i * 0.18}s` }">
        <path :d="rhombus(CX, plate.y, plateW(i), plateH(i))" class="dev-plate-top" />
        <path :d="side(CX, plate.y, plateW(i), plateH(i))" class="dev-plate-side" />
        <text :x="CX + plateW(i) / 2 + 14" :y="plate.y - 2">{{ plate.label }}</text>
        <text :x="CX + plateW(i) / 2 + 14" :y="plate.y + 12" class="dev-sub">{{ plate.sub }}</text>
        <g v-for="(chip, j) in plate.chips" :key="chip" :transform="`translate(${CX + (j - (plate.chips.length - 1) / 2) * 46} ${plate.y})`">
          <path :d="rhombus(0, 0, 34, 13)" class="dev-chip" />
        </g>
      </g>
      <g class="dev-links">
        <path v-for="lx in LINKS" :key="lx" :d="`M${lx} ${PLATES[0]!.y}V${PLATES[2]!.y}`" />
        <circle v-for="(lx, i) in LINKS" :key="`p${lx}`" :cx="lx" :cy="PLATES[0]!.y" r="3" class="dev-packet" :style="{ animationDelay: `${i * 0.7}s` }" />
      </g>
    </svg>

    <div class="dev-code">
      <div class="dev-tabs" role="tablist">
        <button
          v-for="(sample, i) in SAMPLES"
          :key="sample.id"
          type="button"
          role="tab"
          :aria-selected="i === current"
          :class="{ active: i === current }"
          @click="current = i"
        >
          {{ sample.tab }}
        </button>
      </div>
      <pre :key="current" class="dev-pre"><code><span
        v-for="(row, i) in SAMPLES[current]!.lines"
        :key="i"
        class="dev-row"
        :class="row.kind"
        :style="{ animationDelay: `${i * 70}ms` }"
      >{{ row.text }}
</span></code></pre>
      <NuxtLink :to="SAMPLES[current]!.doc" class="dev-doc">
        {{ SAMPLES[current]!.docTitle }} <UIcon name="i-lucide-arrow-up-right" />
      </NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * «Разработчикам»: изометрическая схема слоёв (база города → API → клиенты) и примеры запросов
 * из справки 14-developers. Пакеты бегут по связям снизу вверх.
 */
const CX = 150
const LINKS = [CX - 46, CX, CX + 46]
const plateW = (i: number) => 236 - i * 34
const plateH = (i: number) => 94 - i * 12

const PLATES = [
  { y: 262, label: 'База города', sub: 'PostgreSQL · PostGIS', chips: ['a', 'b', 'c', 'd'] },
  { y: 182, label: 'API ТГИД', sub: 'v1 · v2 · OGC · MCP', chips: ['a', 'b', 'c'] },
  { y: 102, label: 'Ваши системы', sub: '1С · ERP · SCADA · ИИ', chips: ['a', 'b'] }
]

const SAMPLES = [
  {
    id: 'v2',
    tab: 'API v2',
    doc: '/docs/developers/api-v2',
    docTitle: 'API v2 для внешних систем',
    lines: [
      { kind: 'cmd', text: 'curl https://<город>/api/v2/outages?status=active \\' },
      { kind: 'cmd', text: '  -H "Authorization: Bearer $TGID_KEY"' },
      { kind: 'out', text: '{ "items": [ {' },
      { kind: 'out', text: '    "id": 318, "kind": "аварийное",' },
      { kind: 'out', text: '    "consumers": 37, "social": 2,' },
      { kind: 'out', text: '    "valves": ["2КД-9", "2КД-12"] } ] }' }
    ]
  },
  {
    id: 'hook',
    tab: 'Вебхуки',
    doc: '/docs/developers/webhooks',
    docTitle: 'Вебхуки: события и подпись',
    lines: [
      { kind: 'cmt', text: '# ТГИД присылает событие на ваш адрес' },
      { kind: 'cmd', text: 'POST /tgid-hook   webhook-id: msg_2f…' },
      { kind: 'cmd', text: 'webhook-signature: v1,K5o…   (Standard Webhooks)' },
      { kind: 'out', text: '{ "type": "defect.created",' },
      { kind: 'out', text: '  "data": { "section": 1494, "kind": "порыв" } }' }
    ]
  },
  {
    id: 'mcp',
    tab: 'MCP для ИИ',
    doc: '/docs/developers/mcp',
    docTitle: 'MCP: протокол для клиентов',
    lines: [
      { kind: 'cmt', text: '# Claude Desktop, Cursor и другие клиенты MCP' },
      { kind: 'cmd', text: 'POST /mcp  {"method": "tools/call",' },
      { kind: 'cmd', text: '  "params": {"name": "select_network",' },
      { kind: 'cmd', text: '   "arguments": {"question": "Ду 500 до 1980"}}}' },
      { kind: 'out', text: '→ 12 участков · 3,8 км · ваши права' }
    ]
  }
]

const current = ref(0)

const rhombus = (cx: number, cy: number, w: number, h: number) =>
  `M${cx} ${cy - h / 2}L${cx + w / 2} ${cy}L${cx} ${cy + h / 2}L${cx - w / 2} ${cy}Z`

const side = (cx: number, cy: number, w: number, h: number) => {
  const depth = 10
  return `M${cx - w / 2} ${cy}V${cy + depth}L${cx} ${cy + h / 2 + depth}L${cx + w / 2} ${cy + depth}V${cy}L${cx} ${cy + h / 2}Z`
}
</script>

<style scoped>
.dev {
  display: grid;
  grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr);
  gap: 40px;
  align-items: center;
}

.dev-iso {
  width: 100%;
  height: auto;
  overflow: visible;
}

/* Слои поднимаются, когда блок дошёл до экрана (v-reveal ставит data-in). */
[data-in] .dev-plate {
  animation: dev-rise 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) both;
}

.dev-plate-top {
  fill: rgba(246, 244, 238, 0.04);
  stroke: rgba(246, 244, 238, 0.7);
  stroke-width: 1;
}

.dev-plate-side {
  fill: rgba(246, 244, 238, 0.08);
  stroke: rgba(246, 244, 238, 0.35);
  stroke-width: 1;
}

.dev-chip {
  fill: none;
  stroke: #ff6b5e;
  stroke-width: 1;
}

.dev-iso text {
  fill: var(--on-dark);
  font-family: var(--serif);
  font-size: 13px;
}

.dev-iso text.dev-sub {
  fill: #8b867a;
  font-family: var(--mono);
  font-size: 8.5px;
  letter-spacing: 0.05em;
}

.dev-links path {
  stroke: rgba(246, 244, 238, 0.35);
  stroke-dasharray: 3 4;
}

.dev-packet {
  fill: #ff6b5e;
  animation: dev-packet 2.1s cubic-bezier(0.5, 0, 0.5, 1) infinite;
}

/* Пакет поднимается от базы (y 262) к вашим системам (y 102). */
@keyframes dev-packet {
  0% { transform: translateY(0); opacity: 0; }
  15% { opacity: 1; }
  85% { opacity: 1; }
  100% { transform: translateY(-160px); opacity: 0; }
}

@keyframes dev-rise {
  from { opacity: 0; transform: translateY(30px); }
}

.dev-code {
  overflow: hidden;
  border: 1px solid rgba(246, 244, 238, 0.14);
  border-radius: 8px;
  background: #121210;
}

.dev-tabs {
  display: flex;
  border-bottom: 1px solid rgba(246, 244, 238, 0.14);
}

.dev-tabs button {
  padding: 10px 16px;
  border: 0;
  border-right: 1px solid rgba(246, 244, 238, 0.1);
  color: #8b867a;
  background: transparent;
  font-family: var(--mono);
  font-size: 0.74rem;
  cursor: pointer;
}

.dev-tabs button.active {
  color: var(--on-dark);
  box-shadow: inset 0 -2px 0 #ff6b5e;
}

.dev-pre {
  min-height: 200px;
  margin: 0;
  padding: 18px;
  overflow-x: auto;
  font-family: var(--mono);
  font-size: 0.8rem;
  line-height: 1.7;
}

.dev-row {
  display: block;
  white-space: pre;
  animation: dev-type 0.35s ease both;
}

.dev-row.cmd { color: #f6f4ee; }
.dev-row.out { color: #9fd7a8; }
.dev-row.cmt { color: #8b867a; }

@keyframes dev-type {
  from { opacity: 0; transform: translateX(-8px); }
}

.dev-doc {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin: 0 18px 16px;
  color: #ff6b5e;
  font-size: 0.86rem;
}

@media (max-width: 900px) {
  .dev {
    grid-template-columns: 1fr;
  }

  .dev-iso {
    max-width: 420px;
    margin-inline: auto;
  }
}

@media (prefers-reduced-motion: reduce) {
  .dev-packet {
    display: none;
  }

  .dev-plate,
  .dev-row {
    animation: none;
  }
}
</style>
