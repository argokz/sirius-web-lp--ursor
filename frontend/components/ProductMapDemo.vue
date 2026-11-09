<template>
  <figure class="map-demo">
    <!-- Окно повторяет веб-ТГИД (web-itwin-v4, Vuetify): шапка, панель «Слои», инструменты карты,
         всплывающее окно участка. Значки — пути MDI из самого приложения. -->
    <div :key="run" ref="windowEl" class="map-window" :class="{ waiting }" aria-hidden="true">
      <header class="app-bar">
        <span class="app-brand">
          <svg class="app-logo" viewBox="245 60 710 612">
            <defs>
              <linearGradient :id="`${uid}-base`" x1="0%" y1="75%" x2="100%" y2="10%">
                <stop offset="0" stop-color="#0757E8" />
                <stop offset=".28" stop-color="#0A7AF2" />
                <stop offset=".53" stop-color="#14C7E8" />
                <stop offset=".78" stop-color="#15DEC5" />
                <stop offset="1" stop-color="#03CBA6" />
              </linearGradient>
              <linearGradient :id="`${uid}-deep`" x1="5%" y1="20%" x2="90%" y2="90%">
                <stop offset="0" stop-color="#0068EC" />
                <stop offset=".57" stop-color="#0046B8" />
                <stop offset="1" stop-color="#007DDF" />
              </linearGradient>
              <linearGradient :id="`${uid}-panel`" x1="0%" y1="30%" x2="100%" y2="70%">
                <stop offset="0" stop-color="#72B7FB" stop-opacity=".3" />
                <stop offset=".47" stop-color="#1491DE" stop-opacity=".42" />
                <stop offset="1" stop-color="#2EF1C7" stop-opacity=".34" />
              </linearGradient>
              <linearGradient :id="`${uid}-rim`" x1="0%" y1="0%" x2="100%" y2="0%">
                <stop offset="0" stop-color="#025ED8" />
                <stop offset=".55" stop-color="#1469DC" />
                <stop offset="1" stop-color="#00AA96" />
              </linearGradient>
              <clipPath :id="`${uid}-cut`"><path d="M600 68 L940 238 L600 408 L260 238 Z" /></clipPath>
            </defs>
            <path d="M600 315 L949 490 L600 665 L251 490 Z" :fill="`url(#${uid}-panel)`" />
            <path d="M600 237 L945 410 L600 583 L255 410 Z" :fill="`url(#${uid}-panel)`" />
            <path d="M260 238 L600 408 L940 238 L940 252 L600 423 L260 252 Z" :fill="`url(#${uid}-rim)`" />
            <path d="M600 68 L940 238 L600 408 L260 238 Z" :fill="`url(#${uid}-base)`" />
            <g :clip-path="`url(#${uid}-cut)`">
              <path d="M225 286 C344 201 435 212 487 302 C550 373 611 353 659 313 C710 264 764 250 841 276 L1030 380 L612 475 Z" :fill="`url(#${uid}-deep)`" opacity=".77" />
              <g fill="none" stroke="#F5FFFF" stroke-width="2.1" stroke-opacity=".9">
                <path d="M656.7,96.3 L316.7,266.3 M770,153 L430,323 M883.3,209.7 L543.3,379.7 M543.3,96.3 L883.3,266.3 M430,153 L770,323 M316.7,209.7 L656.7,379.7" />
              </g>
            </g>
          </svg>
          <b>ITwin</b>&nbsp;Map
        </span>
        <span class="app-context">
          <svg class="mi" viewBox="0 0 24 24"><path :d="ICONS.pin" /></svg>
          Алматы · Администратор
        </span>
        <span class="app-menu">
          <span class="app-menu-item calc-button"><svg class="mi" viewBox="0 0 24 24"><path :d="ICONS.calc" /></svg>Расчёт</span>
          <span class="app-menu-item"><svg class="mi" viewBox="0 0 24 24"><path :d="ICONS.console" /></svg>Протокол</span>
          <span class="app-menu-item">
            <svg class="mi" viewBox="0 0 24 24"><path :d="ICONS.export" /></svg>Выгрузка
            <svg class="mi chevron" viewBox="0 0 24 24"><path :d="ICONS.chevronDown" /></svg>
          </span>
        </span>
        <span class="app-search">
          <svg class="mi" viewBox="0 0 24 24"><path :d="ICONS.search" /></svg>
          <span class="search-hint">Узел, адрес, журнал, команда</span>
          <kbd>Ctrl K</kbd>
        </span>
        <span class="app-icons">
          <svg class="mi" viewBox="0 0 24 24"><path :d="ICONS.toolbox" /></svg>
          <span class="users">
            <svg class="mi" viewBox="0 0 24 24"><path :d="ICONS.users" /></svg>
            <i>1</i>
          </span>
          <span class="avatar">НА</span>
        </span>
      </header>

      <div class="map-canvas">
        <svg :viewBox="`0 0 ${W} ${H}`" preserveAspectRatio="xMidYMid slice">
          <g class="parks">
            <polygon v-for="(park, i) in map.parks" :key="i" class="fade" :points="park" style="--d: 0.7s" />
          </g>

          <!-- Как на бумаге: сначала пером проводятся бровки улиц, потом проезжая часть заливается белым -->
          <g class="streets">
            <path v-for="(street, i) in map.streets" :key="`f${i}`" class="fade road" :d="street.d" :style="{ '--d': `${street.delay + 0.7}s`, '--w': `${street.half * 2 + 1}px` }" />
            <template v-for="(street, i) in map.streets" :key="`e${i}`">
              <path v-for="(edge, k) in street.edges" :key="k" class="draw edge" :d="edge" pathLength="1" :style="{ '--d': `${street.delay + k * 0.08}s`, '--t': '1.1s' }" />
            </template>
          </g>

          <path class="draw canal" :d="map.canal" pathLength="1" style="--d: 0.4s; --t: 1.4s" />

          <g class="plots">
            <polygon v-for="(plot, i) in map.plots" :key="i" class="fade" :points="plot" style="--d: 1.4s" />
          </g>

          <!-- Контур дома проводится пером, затем дом «вырастает» -->
          <g class="sketches">
            <path v-for="(building, i) in map.buildings" :key="i" class="draw sketch" :d="building.sketch" pathLength="1" :style="{ '--d': `${building.sketchDelay}s`, '--t': '0.5s' }" />
          </g>

          <!-- Здания MapTiler в 3D: цвет по назначению (utils/buildingStyle.ts), стены темнее крыши -->
          <g class="buildings">
            <g v-for="(building, i) in map.buildings" :key="i" class="rise" :style="{ '--d': `${building.delay}s` }">
              <polygon v-for="(wall, k) in building.walls" :key="k" :points="wall.points" :fill="wall.fill" />
              <polygon :points="building.top" :fill="building.topFill" />
            </g>
          </g>

          <!-- Контуры зданий-потребителей (zdaniya_tu) поверх объёмов -->
          <g class="consumers">
            <polygon v-for="(outline, i) in map.outlines" :key="i" class="fade" :points="outline.points" :style="{ '--d': `${outline.delay}s` }" />
          </g>

          <g class="map-text">
            <text v-for="(label, i) in map.mapLabels" :key="i" class="fade" :class="label.kind" :transform="`translate(${label.x} ${label.y}) rotate(${label.angle})`" text-anchor="middle" :style="{ '--d': `${label.delay}s` }">
              {{ label.text }}
            </text>
          </g>

          <!-- Сеть как в стиле heatpipesections_gid: подача #7f0000 слева по ходу, обратка #00007f справа -->
          <g class="pipes return">
            <path v-for="(pipe, i) in map.returns" :key="i" class="draw" :class="pipe.kind" :d="pipe.d" pathLength="1" :style="{ '--d': `${pipe.delay}s`, '--t': `${pipe.duration}s` }" />
          </g>
          <g class="pipes supply">
            <path v-for="(pipe, i) in map.supplies" :key="i" class="draw" :class="pipe.kind" :d="pipe.d" pathLength="1" :style="{ '--d': `${pipe.delay}s`, '--t': `${pipe.duration}s` }" />
          </g>

          <!-- Кончик пера ведёт каждую трубу, пока она рисуется -->
          <g class="pens">
            <g v-for="(pen, i) in map.pens" :key="i" class="pen" :style="{ '--d': `${pen.begin}s`, '--t': `${pen.duration}s` }">
              <circle class="pen-glow" r="7" />
              <circle class="pen-nib" r="2.8" />
              <animateMotion :path="pen.path" :begin="`${pen.begin}s`" :dur="`${pen.duration}s`" fill="freeze" calcMode="spline" keyTimes="0;1" keyPoints="0;1" keySplines="0.55 0.1 0.35 1" />
            </g>
          </g>

          <g class="selected">
            <path class="selected-line" :d="map.selected.d" />
            <circle :cx="map.selected.from[0]" :cy="map.selected.from[1]" r="2.6" />
          </g>

          <g class="flow">
            <circle v-for="n in 3" :key="`a${n}`" r="2.4">
              <animateMotion :path="map.flowA" dur="6.5s" :begin="`${3.2 + (n - 1) * 2.1}s`" repeatCount="indefinite" />
            </circle>
            <circle v-for="n in 2" :key="`b${n}`" r="2.4">
              <animateMotion :path="map.flowB" dur="7s" :begin="`${3.6 + (n - 1) * 3.4}s`" repeatCount="indefinite" />
            </circle>
          </g>

          <g class="nodes">
            <circle v-for="(node, i) in map.smallNodes" :key="`s${i}`" class="pop small" :cx="node.x" :cy="node.y" r="2.6" :style="{ '--d': `${node.delay}s` }" />
            <g v-for="(node, i) in map.namedNodes" :key="`n${i}`" class="pop named" :style="{ '--d': `${node.delay}s` }">
              <circle :cx="node.x" :cy="node.y" r="5.4" />
              <circle class="dot" :cx="node.x" :cy="node.y" r="2" />
            </g>
          </g>

          <g class="net-text">
            <text v-for="(label, i) in map.netLabels" :key="i" class="fade" :class="label.kind" :transform="`translate(${label.x} ${label.y}) rotate(${label.angle})`" text-anchor="middle" :style="{ '--d': `${label.delay}s` }">
              {{ label.text }}
            </text>
          </g>
        </svg>

        <aside class="layers-panel">
          <div class="panel-head">
            <div>
              <strong>Слои</strong>
              <small>Видимость и порядок</small>
            </div>
            <svg class="mi" viewBox="0 0 24 24"><path :d="ICONS.close" /></svg>
          </div>
          <nav class="panel-tabs">
            <span class="active">Слои</span>
            <span>Фрагменты <i class="badge" style="--d: 1.7s">1</i></span>
            <span>Подписи <i class="badge" style="--d: 3.3s">2</i></span>
            <span>ПТС</span>
          </nav>
          <div class="panel-body">
            <div class="group-head">
              <svg class="mi" viewBox="0 0 24 24"><path :d="ICONS.earth" /></svg>
              Слои контекста
              <svg class="mi end" viewBox="0 0 24 24"><path :d="ICONS.chevronUp" /></svg>
            </div>
            <div class="switch-row"><span class="switch" />Режим наведения (атрибуты)</div>
            <div v-for="layer in CONTEXT_LAYERS" :key="layer.name" class="layer-row">
              <span class="check" :class="{ on: layer.on }">
                <svg class="mi" viewBox="0 0 24 24"><path :d="ICONS.boxBlank" /></svg>
                <svg v-if="layer.on" class="mi tick" viewBox="0 0 24 24"><path :d="ICONS.boxChecked" /></svg>
              </span>
              <span class="layer-text">
                <b>{{ layer.name }}</b>
                <small>{{ layer.source }}</small>
                <span v-if="layer.on" class="legend">
                  <span v-for="[name, color] in BUILDING_LEGEND" :key="name"><i :style="{ background: color }" />{{ name }}</span>
                </span>
              </span>
            </div>
            <div class="group-head">
              <svg class="mi" viewBox="0 0 24 24"><path :d="ICONS.layersPlus" /></svg>
              Внешние слои
              <svg class="mi end" viewBox="0 0 24 24"><path :d="ICONS.plus" /></svg>
              <svg class="mi" viewBox="0 0 24 24"><path :d="ICONS.chevronUp" /></svg>
            </div>
            <p class="group-note">Подложки и данные других серверов: ГИС «Панорама», ArcGIS, акиматы. Нажмите «+».</p>
            <div class="group-head">
              <svg class="mi" viewBox="0 0 24 24"><path :d="ICONS.earth" /></svg>
              Слои Planet V4
              <svg class="mi end" viewBox="0 0 24 24"><path :d="ICONS.chevronUp" /></svg>
            </div>
            <div v-for="group in PLANET_GROUPS" :key="group.name" class="planet-row">
              <svg class="mi" viewBox="0 0 24 24"><path :d="ICONS[group.icon]" /></svg>
              {{ group.name }}
              <svg class="mi end" viewBox="0 0 24 24"><path :d="ICONS.minusBox" /></svg>
              <svg class="mi" viewBox="0 0 24 24"><path :d="ICONS.chevronDown" /></svg>
            </div>
          </div>
          <div class="panel-foot"><span>Применить</span></div>
        </aside>

        <div class="map-modes glass">
          <span><svg class="mi" viewBox="0 0 24 24"><path :d="ICONS.ruler" /></svg></span>
          <span><svg class="mi" viewBox="0 0 24 24"><path :d="ICONS.trace" /></svg></span>
          <span><svg class="mi" viewBox="0 0 24 24"><path :d="ICONS.chart" /></svg></span>
          <span class="tool-info"><svg class="mi" viewBox="0 0 24 24"><path :d="ICONS.info" /></svg></span>
        </div>

        <div class="map-controls">
          <div class="glass control-group">
            <span><svg class="mi" viewBox="0 0 24 24"><path :d="ICONS.home" /></svg></span>
            <span><svg class="mi" viewBox="0 0 24 24"><path :d="ICONS.link" /></svg></span>
            <span><svg class="mi" viewBox="0 0 24 24"><path :d="ICONS.locate" /></svg></span>
            <span class="text">2D</span>
            <span><svg class="mi" viewBox="0 0 24 24"><path :d="ICONS.earth" /></svg></span>
          </div>
          <div class="glass control-group">
            <span><svg class="mi" viewBox="0 0 24 24"><path :d="ICONS.plus" /></svg></span>
            <span><svg class="mi" viewBox="0 0 24 24"><path :d="ICONS.minus" /></svg></span>
          </div>
        </div>

        <div class="snackbar">
          <svg class="mi" viewBox="0 0 24 24"><path :d="ICONS.checkCircle" /></svg>
          Расчёт выполнен · 1 284 узла · 0,7 с
        </div>

        <div class="map-popover" :style="{ left: `${(map.selected.at[0] / W) * 100}%`, top: `${(map.selected.at[1] / H) * 100}%` }">
          <header>
            <svg class="mi" viewBox="0 0 24 24"><path :d="ICONS.infoOutline" /></svg>
            <div>
              <strong>М2 2КД-10 - М2 2КД-11</strong>
              <small>Участок 1494</small>
            </div>
            <svg class="mi close" viewBox="0 0 24 24"><path :d="ICONS.close" /></svg>
          </header>
          <dl>
            <template v-for="[label, value] in SECTION_SUMMARY" :key="label + value">
              <dt>{{ label }}</dt>
              <dd>{{ value }}</dd>
            </template>
          </dl>
          <footer>
            <span class="btn primary"><svg class="mi" viewBox="0 0 24 24"><path :d="ICONS.card" /></svg>Карточка</span>
            <span class="btn"><svg class="mi" viewBox="0 0 24 24"><path :d="ICONS.pencil" /></svg>Редактировать</span>
            <svg class="mi end" viewBox="0 0 24 24"><path :d="ICONS.defect" /></svg>
            <svg class="mi" viewBox="0 0 24 24"><path :d="ICONS.excel" /></svg>
          </footer>
        </div>

        <div class="scale-box">30 м</div>
        <div class="cursor-coords">
          <b>WGS84</b>
          <svg class="mi caret" viewBox="0 0 24 24"><path :d="ICONS.menuUp" /></svg>
          <span class="coords-value">43,248846° с. ш. 76,922616° в. д.</span>
          <svg class="mi" viewBox="0 0 24 24"><path :d="ICONS.copy" /></svg>
        </div>
      </div>

      <!-- Курсор, как в демонстрации Felt: «Расчёт» → инструмент сведений → участок -->
      <div v-if="cursorReady" class="cursor" :style="cursorVars">
        <svg viewBox="0 0 14 20"><path d="M1 1 L1 16.5 L5 12.8 L8 19 L10.6 17.8 L7.7 11.8 L13 11.8 Z" /></svg>
        <span class="click" />
      </div>
    </div>
    <figcaption>
      <span>Веб-ТГИД: слои, сеть, гидравлический расчёт и сведения об участке на одной карте</span>
      <button type="button" class="replay" @click="run++">
        <UIcon name="i-lucide-rotate-ccw" />
        Показать ещё раз
      </button>
    </figcaption>
  </figure>
</template>

<script setup lang="ts">
const W = 1000
const H = 540

const run = ref(0)
const uid = useId().replace(/[^a-zA-Z0-9_-]/g, '')

// Пути значков Material Design Icons — те же, что рисует веб-ТГИД.
const ICONS = {
  pin: 'M12,11.5A2.5,2.5 0 0,1 9.5,9A2.5,2.5 0 0,1 12,6.5A2.5,2.5 0 0,1 14.5,9A2.5,2.5 0 0,1 12,11.5M12,2A7,7 0 0,0 5,9C5,14.25 12,22 12,22C12,22 19,14.25 19,9A7,7 0 0,0 12,2Z',
  calc: 'M19 3H5C3.9 3 3 3.9 3 5V19C3 20.1 3.9 21 5 21H19C20.1 21 21 20.1 21 19V5C21 3.9 20.1 3 19 3M13 7.1L14.1 6L15.5 7.4L16.9 6L18 7.1L16.6 8.5L18 9.9L16.9 11L15.5 9.6L14.1 11L13 9.9L14.4 8.5L13 7.1M6.2 7.7H11.2V9.2H6.2V7.7M11.5 16H9.5V18H8V16H6V14.5H8V12.5H9.5V14.5H11.5V16M18 17.2H13V15.7H18V17.2M18 14.8H13V13.3H18V14.8Z',
  console: 'M13,19V16H21V19H13M8.5,13L2.47,7H6.71L11.67,11.95C12.25,12.54 12.25,13.5 11.67,14.07L6.74,19H2.5L8.5,13Z',
  export: 'M23,12L19,8V11H10V13H19V16M1,18V6C1,4.89 1.9,4 3,4H15A2,2 0 0,1 17,6V9H15V6H3V18H15V15H17V18A2,2 0 0,1 15,20H3A2,2 0 0,1 1,18Z',
  search: 'M9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11 15.41,12.59 14.44,13.73L14.71,14H15.5L20.5,19L19,20.5L14,15.5V14.71L13.73,14.44C12.59,15.41 11.11,16 9.5,16A6.5,6.5 0 0,1 3,9.5A6.5,6.5 0 0,1 9.5,3M9.5,5C7,5 5,7 5,9.5C5,12 7,14 9.5,14C12,14 14,12 14,9.5C14,7 12,5 9.5,5Z',
  toolbox: 'M20 8H17V6C17 4.9 16.1 4 15 4H9C7.9 4 7 4.9 7 6V8H4C2.9 8 2 8.9 2 10V20H22V10C22 8.9 21.1 8 20 8M9 6H15V8H9V6M20 18H4V15H6V16H8V15H16V16H18V15H20V18M18 13V12H16V13H8V12H6V13H4V10H20V13H18Z',
  users: 'M16 17V19H2V17S2 13 9 13 16 17 16 17M12.5 7.5A3.5 3.5 0 1 0 9 11A3.5 3.5 0 0 0 12.5 7.5M15.94 13A5.32 5.32 0 0 1 18 17V19H22V17S22 13.37 15.94 13M15 4A3.39 3.39 0 0 0 13.07 4.59A5 5 0 0 1 13.07 10.41A3.39 3.39 0 0 0 15 11A3.5 3.5 0 0 0 15 4Z',
  ruler: 'M1.39,18.36L3.16,16.6L4.58,18L5.64,16.95L4.22,15.54L5.64,14.12L8.11,16.6L9.17,15.54L6.7,13.06L8.11,11.65L9.53,13.06L10.59,12L9.17,10.59L10.59,9.17L13.06,11.65L14.12,10.59L11.65,8.11L13.06,6.7L14.47,8.11L15.54,7.05L14.12,5.64L15.54,4.22L18,6.7L19.07,5.64L16.6,3.16L18.36,1.39L22.61,5.64L5.64,22.61L1.39,18.36Z',
  trace: 'M2 3V9H4.95L6.95 15H6V21H12V16.41L17.41 11H22V5H16V9.57L10.59 15H9.06L7.06 9H8V3H2M4 5H6V7H4V5M18 7H20V9H18V7M21.15 13C21 13 20.87 13.05 20.76 13.16L19.75 14.18L21.82 16.25L22.84 15.24C23.05 15.03 23.05 14.67 22.84 14.46L21.54 13.16C21.43 13.05 21.29 13 21.15 13M19.15 14.76L13 20.91V23H15.09L21.23 16.84L19.15 14.76M8 17H10V19H8V17Z',
  chart: 'M16,11.78L20.24,4.45L21.97,5.45L16.74,14.5L10.23,10.75L5.46,19H22V21H2V3H4V17.54L9.5,8L16,11.78Z',
  info: 'M13,9H11V7H13M13,17H11V11H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z',
  infoOutline: 'M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z',
  home: 'M10,20V14H14V20H19V12H22L12,3L2,12H5V20H10Z',
  link: 'M10.59,13.41C11,13.8 11,14.44 10.59,14.83C10.2,15.22 9.56,15.22 9.17,14.83C7.22,12.88 7.22,9.71 9.17,7.76V7.76L12.71,4.22C14.66,2.27 17.83,2.27 19.78,4.22C21.73,6.17 21.73,9.34 19.78,11.29L18.29,12.78C18.3,11.96 18.17,11.14 17.89,10.36L18.36,9.88C19.54,8.71 19.54,6.81 18.36,5.64C17.19,4.46 15.29,4.46 14.12,5.64L10.59,9.17C9.41,10.34 9.41,12.24 10.59,13.41M13.41,9.17C13.8,8.78 14.44,8.78 14.83,9.17C16.78,11.12 16.78,14.29 14.83,16.24V16.24L11.29,19.78C9.34,21.73 6.17,21.73 4.22,19.78C2.27,17.83 2.27,14.66 4.22,12.71L5.71,11.22C5.7,12.04 5.83,12.86 6.11,13.65L5.64,14.12C4.46,15.29 4.46,17.19 5.64,18.36C6.81,19.54 8.71,19.54 9.88,18.36L13.41,14.83C14.59,13.66 14.59,11.76 13.41,10.59C13,10.2 13,9.56 13.41,9.17Z',
  locate: 'M12,8A4,4 0 0,1 16,12A4,4 0 0,1 12,16A4,4 0 0,1 8,12A4,4 0 0,1 12,8M3.05,13H1V11H3.05C3.5,6.83 6.83,3.5 11,3.05V1H13V3.05C17.17,3.5 20.5,6.83 20.95,11H23V13H20.95C20.5,17.17 17.17,20.5 13,20.95V23H11V20.95C6.83,20.5 3.5,17.17 3.05,13M12,5A7,7 0 0,0 5,12A7,7 0 0,0 12,19A7,7 0 0,0 19,12A7,7 0 0,0 12,5Z',
  earth: 'M17.9,17.39C17.64,16.59 16.89,16 16,16H15V13A1,1 0 0,0 14,12H8V10H10A1,1 0 0,0 11,9V7H13A2,2 0 0,0 15,5V4.59C17.93,5.77 20,8.64 20,12C20,14.08 19.2,15.97 17.9,17.39M11,19.93C7.05,19.44 4,16.08 4,12C4,11.38 4.08,10.78 4.21,10.21L9,15V16A2,2 0 0,0 11,18M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z',
  plus: 'M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z',
  minus: 'M19,13H5V11H19V13Z',
  menuUp: 'M7,15L12,10L17,15H7Z',
  copy: 'M19,21H8V7H19M19,5H8A2,2 0 0,0 6,7V21A2,2 0 0,0 8,23H19A2,2 0 0,0 21,21V7A2,2 0 0,0 19,5M16,1H4A2,2 0 0,0 2,3V17H4V3H16V1Z',
  close: 'M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z',
  chevronUp: 'M7.41,15.41L12,10.83L16.59,15.41L18,14L12,8L6,14L7.41,15.41Z',
  chevronDown: 'M7.41,8.58L12,13.17L16.59,8.58L18,10L12,16L6,10L7.41,8.58Z',
  boxBlank: 'M19,3H5C3.89,3 3,3.89 3,5V19C3,20.1 3.9,21 5,21H19C20.1,21 21,20.1 21,19V5C21,3.89 20.1,3 19,3M19,5V19H5V5H19Z',
  boxChecked: 'M10,17L5,12L6.41,10.58L10,14.17L17.59,6.58L19,8M19,3H5C3.89,3 3,3.89 3,5V19C3,20.1 3.9,21 5,21H19C20.1,21 21,20.1 21,19V5C21,3.89 20.1,3 19,3Z',
  minusBox: 'M17,13H7V11H17M19,3H5C3.89,3 3,3.89 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5C21,3.89 20.1,3 19,3Z',
  layersPlus: 'M17,14H19V17H22V19H19V22H17V19H14V17H17V14M11,16L2,9L11,2L20,9L11,16M11,18.54L12,17.75V18C12,18.71 12.12,19.39 12.35,20L11,21.07L2,14.07L3.62,12.81L11,18.54Z',
  tree: 'M11,21V16.74C10.53,16.91 10.03,17 9.5,17C7,17 5,15 5,12.5C5,11.23 5.5,10.09 6.36,9.27C6.13,8.73 6,8.13 6,7.5C6,5 8,3 10.5,3C12.06,3 13.44,3.8 14.25,5C14.33,5 14.41,5 14.5,5A5.5,5.5 0 0,1 20,10.5A5.5,5.5 0 0,1 14.5,16C14,16 13.5,15.93 13,15.79V21H11Z',
  landUse: 'M3,3V21H21V3H3M5,5H19V19H5V5M7,17L17,7V9L9,17H7M7,13L13,7H15L7,15V13M11,17L17,11V13L13,17H11Z',
  water: 'M12,20A6,6 0 0,1 6,14C6,10 12,3.25 12,3.25C12,3.25 18,10 18,14A6,6 0 0,1 12,20Z',
  flag: 'M14.4,6L14,4H5V21H7V14H12.6L13,16H20V6H14.4Z',
  card: 'M20,20H4A2,2 0 0,1 2,18V6A2,2 0 0,1 4,4H20A2,2 0 0,1 22,6V18A2,2 0 0,1 20,20M4,6V18H20V6H4M6,9H18V11H6V9M6,13H16V15H6V13Z',
  pencil: 'M14.06,9L15,9.94L5.92,19H5V18.08L14.06,9M17.66,3C17.41,3 17.15,3.1 16.96,3.29L15.13,5.12L18.88,8.87L20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18.17,3.09 17.92,3 17.66,3M14.06,6.19L3,17.25V21H6.75L17.81,9.94L14.06,6.19Z',
  defect: 'M23,12L20.56,14.78L20.9,18.46L17.29,19.28L15.4,22.46L12,21L8.6,22.47L6.71,19.29L3.1,18.47L3.44,14.78L1,12L3.44,9.21L3.1,5.53L6.71,4.72L8.6,1.54L12,3L15.4,1.54L17.29,4.72L20.9,5.54L20.56,9.22L23,12M20.33,12L18.5,9.89L18.74,7.1L16,6.5L14.58,4.07L12,5.18L9.42,4.07L8,6.5L5.26,7.09L5.5,9.88L3.67,12L5.5,14.1L5.26,16.9L8,17.5L9.42,19.93L12,18.81L14.58,19.92L16,17.5L18.74,16.89L18.5,14.1L20.33,12M11,15H13V17H11V15M11,7H13V13H11V7',
  excel: 'M16.2,17H14.2L12,13.2L9.8,17H7.8L11,12L7.8,7H9.8L12,10.8L14.2,7H16.2L13,12M19,3H5C3.89,3 3,3.89 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5C21,3.89 20.1,3 19,3Z',
  checkCircle: 'M12 2C6.5 2 2 6.5 2 12S6.5 22 12 22 22 17.5 22 12 17.5 2 12 2M10 17L5 12L6.41 10.59L10 14.17L17.59 6.58L19 8L10 17Z'
}

// Цвета зданий по назначению — utils/buildingStyle.ts веб-ТГИД.
const BUILDING_COLORS = {
  residential: '#cfc6b4',
  commercial: '#e0b77f',
  education: '#9fc9a6',
  outbuilding: '#dcd8cf',
  other: '#c4c8d4'
}
type BuildingClass = keyof typeof BUILDING_COLORS

const BUILDING_LEGEND = [
  ['Жилое', '#cfc6b4'], ['Коммерческое', '#e0b77f'], ['Производственное', '#a9a6bd'], ['Образование', '#9fc9a6'],
  ['Медицина', '#e8a3a3'], ['Общественное', '#a8c1de'], ['Религиозное', '#c9a9dc'], ['Транспорт', '#b9bcc2'],
  ['Хозпостройка', '#dcd8cf'], ['Прочие', '#c4c8d4']
]

const CONTEXT_LAYERS = [
  { name: 'Изолинии', source: 'MapTiler · рельеф, подписи высот (±5 м)', on: false },
  { name: 'Здания', source: 'MapTiler · высота и назначение (цвет)', on: true },
  { name: 'Затенение рельефа', source: 'MapTiler · рельеф (hillshade)', on: false },
  { name: 'Рельеф и 3D', source: 'MapTiler · Terrain RGB', on: false }
]

const PLANET_GROUPS = [
  { name: 'Природа и покров', icon: 'tree' },
  { name: 'Землепользование', icon: 'landUse' },
  { name: 'Вода', icon: 'water' },
  { name: 'Границы', icon: 'flag' }
] as const

const SECTION_SUMMARY = [
  ['Код расчетной схемы', 'М2'],
  ['Наименование узла присоединения', '2КД-10'],
  ['Код расчетной схемы', 'М2'],
  ['Наименование узла присоединения', '2КД-11'],
  ['Признак участка трубопровода', 'общий']
]

type Point = [number, number]
// Улицы — прямые с небольшим наклоном: «вертикальные» x = a + b·y, «горизонтальные» y = c + d·x.
interface VLine { a: number; b: number }
interface HLine { c: number; d: number }
interface Label { text: string; x: number; y: number; angle: number; kind: string; delay: number }
interface Pipe { d: string; delay: number; duration: number; kind: 'mag' | 'dist' | 'stub' }

// Улица задана осью и полушириной проезжей части (магистральные улицы шире).
const VERTICALS: Array<VLine & { half: number }> = [
  { a: -150, b: 0.035, half: 6.5 },
  { a: 80, b: 0.036, half: 6.5 },
  { a: 300, b: 0.034, half: 6.5 },
  { a: 505, b: 0.035, half: 10 },
  { a: 725, b: 0.036, half: 6.5 },
  { a: 930, b: 0.034, half: 6.5 },
  { a: 1150, b: 0.035, half: 6.5 }
]
const HORIZONTALS: Array<HLine & { half: number }> = [
  { c: -95, d: -0.035, half: 6.5 },
  { c: 82, d: -0.035, half: 6.5 },
  { c: 252, d: -0.035, half: 10 },
  { c: 425, d: -0.035, half: 10 },
  { c: 640, d: -0.035, half: 6.5 }
]
const PIPE_OFFSET = 3.5 // труба идёт вдоль края проезжей части
const BLOCK_OFFSET = 7 // квартал начинается за тротуаром

// Карта строится из одного и того же зерна, поэтому сервер и браузер рисуют одинаковую картинку.
const random = (() => {
  let seed = 7
  return () => {
    seed = (seed + 0x6d2b79f5) | 0
    let t = Math.imul(seed ^ (seed >>> 15), 1 | seed)
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
})()

const round = (n: number) => Math.round(n * 10) / 10
const pathOf = (points: Point[]) => points.map(([x, y], i) => `${i ? 'L' : 'M'}${round(x)} ${round(y)}`).join('')
const pointsOf = (points: Point[]) => points.map(([x, y]) => `${round(x)},${round(y)}`).join(' ')
const xAt = (v: VLine, y: number) => v.a + v.b * y
const yAt = (h: HLine, x: number) => h.c + h.d * x
const meet = (v: VLine, h: HLine): Point => {
  const x = (v.a + v.b * h.c) / (1 - v.b * h.d)
  return [x, yAt(h, x)]
}
const lerp = (a: Point, b: Point, t: number): Point => [a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t]

const hexToRgb = (hex: string) => [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16))
const rgbToHex = (rgb: number[]) => `#${rgb.map((c) => Math.round(Math.min(255, Math.max(0, c))).toString(16).padStart(2, '0')).join('')}`
const shade = (hex: string, k: number) => rgbToHex(hexToRgb(hex).map((c) => c * k))
const mix = (a: string, b: string, t: number) => {
  const [ca, cb] = [hexToRgb(a), hexToRgb(b)]
  return rgbToHex(ca.map((c, i) => c + (cb[i] - c) * t))
}

const buildMap = () => {
  const verticalPath = (v: VLine, dx = 0) => pathOf([[xAt(v, -20) + dx, -20], [xAt(v, H + 20) + dx, H + 20]])
  const horizontalPath = (h: HLine, dy = 0) => pathOf([[-20, yAt(h, -20) + dy], [W + 20, yAt(h, W + 20) + dy]])
  const streets = [
    ...VERTICALS.map((v, i) => ({
      d: verticalPath(v),
      edges: [verticalPath(v, -v.half - 0.5), verticalPath(v, v.half + 0.5)],
      half: v.half,
      delay: round(0.1 + i * 0.06)
    })),
    ...HORIZONTALS.map((h, j) => ({
      d: horizontalPath(h),
      edges: [horizontalPath(h, -h.half - 0.5), horizontalPath(h, h.half + 0.5)],
      half: h.half,
      delay: round(0.2 + j * 0.08)
    }))
  ]

  // Арык вдоль западной стороны улицы — как Есентай на карте Алматы.
  const canalLine = { a: VERTICALS[2].a - VERTICALS[2].half - 4, b: VERTICALS[2].b }
  const canalPoints: Point[] = []
  for (let y = -20; y <= H + 20; y += 20) canalPoints.push([xAt(canalLine, y) + 1.5 * Math.sin(y / 23), y])

  const parks: string[] = []
  const plots: string[] = []
  const outlines: Array<{ points: string; delay: number }> = []
  const mapLabels: Label[] = []
  const placed: Array<[number, number, number]> = []
  // Подписи не накладываются: занятые места запоминаются прямоугольниками.
  const fits = (x: number, y: number, width: number) => {
    if (x < 20 || x > W - 20 || y < 14 || y > H - 8) return false
    if (placed.some(([px, py, pw]) => Math.abs(px - x) < (pw + width) / 2 + 6 && Math.abs(py - y) < 13)) return false
    placed.push([x, y, width])
    return true
  }

  interface Building {
    walls: Array<{ points: string; fill: string }>
    top: string
    topFill: string
    sketch: string
    sketchDelay: number
    delay: number
    sortY: number
  }
  const buildings: Building[] = []
  const frontConsumers: Array<{ x: number; y: number; row: number; delay: number }> = []

  const addBuilding = (footprint: Point[], kind: BuildingClass, height: number, consumer: boolean, row: number, front: boolean) => {
    const cx = footprint.reduce((s, p) => s + p[0], 0) / 4
    const cy = footprint.reduce((s, p) => s + p[1], 0) / 4
    // Дома прорисовываются слева направо: сначала контур пером, через полсекунды — объём.
    const sketchDelay = round(0.6 + Math.min(1, Math.max(0, cx / W)) * 0.9 + random() * 0.15)
    const delay = round(sketchDelay + 0.45)
    // Потребитель (zdaniya_tu) поверх объёма даёт розоватый оттенок, как на карте.
    const base = consumer ? mix(BUILDING_COLORS[kind], '#f0b49a', 0.4) : BUILDING_COLORS[kind]
    const roof = footprint.map(([x, y]): Point => [x, y - height])
    // Стены по сторонам света: север, восток, запад и последней — ближняя южная.
    const order = [0, 1, 3, 2]
    const tones = [0.8, 0.76, 0.9, 0.84]
    const walls = order.map((k) => {
      const next = (k + 1) % 4
      return { points: pointsOf([footprint[k], footprint[next], roof[next], roof[k]]), fill: shade(base, tones[k]) }
    })
    buildings.push({
      walls,
      top: pointsOf(roof),
      topFill: mix(base, '#ffffff', 0.14),
      sketch: `${pathOf(footprint)}Z`,
      sketchDelay,
      delay,
      sortY: Math.max(...footprint.map((p) => p[1]))
    })
    if (!consumer) return
    outlines.push({ points: pointsOf(footprint), delay: round(delay + 0.5) })
    const value = (0.05 + random() * 0.6).toFixed(3).replace(/0+$/, '')
    const text = `Qсум=${value}`
    if (fits(cx, cy - height + 3, text.length * 5.4)) mapLabels.push({ text, x: round(cx), y: round(cy - height + 3), angle: 0, kind: 'load', delay: round(3.4 + random() * 0.4) })
    if (front) {
      const mid = lerp(footprint[0], footprint[1], 0.5)
      frontConsumers.push({ x: mid[0], y: mid[1], row, delay })
    }
  }

  const PARK_BLOCK = '4:3'
  const PLOT_BLOCK = '2:2'
  for (let i = 0; i < VERTICALS.length - 1; i++) {
    for (let j = 0; j < HORIZONTALS.length - 1; j++) {
      const left = { a: VERTICALS[i].a + VERTICALS[i].half + BLOCK_OFFSET, b: VERTICALS[i].b }
      const right = { a: VERTICALS[i + 1].a - VERTICALS[i + 1].half - BLOCK_OFFSET, b: VERTICALS[i + 1].b }
      const top = { c: HORIZONTALS[j].c + HORIZONTALS[j].half + BLOCK_OFFSET, d: HORIZONTALS[j].d }
      const bottom = { c: HORIZONTALS[j + 1].c - HORIZONTALS[j + 1].half - BLOCK_OFFSET, d: HORIZONTALS[j + 1].d }
      const [p0, p1, p2, p3] = [meet(left, top), meet(right, top), meet(right, bottom), meet(left, bottom)]
      if (p1[0] < -30 || p0[0] > W + 30 || p3[1] < -30 || p0[1] > H + 30) continue

      const bw = Math.hypot(p1[0] - p0[0], p1[1] - p0[1])
      const bh = Math.hypot(p3[0] - p0[0], p3[1] - p0[1])
      // Прямоугольник в пикселях от левого верхнего угла квартала.
      const rect = (x0: number, x1: number, y0: number, y1: number): Point[] => {
        const at = (x: number, y: number) => lerp(lerp(p0, p1, x / bw), lerp(p3, p2, x / bw), y / bh)
        return [at(x0, y0), at(x1, y0), at(x1, y1), at(x0, y1)]
      }
      const pickClass = (): BuildingClass => {
        const roll = random()
        return roll < 0.42 ? 'residential' : roll < 0.84 ? 'other' : 'commercial'
      }
      const heightOf = (kind: BuildingClass) => round(kind === 'commercial' ? 5 + random() * 4 : kind === 'outbuilding' ? 2.5 : 8 + random() * 9)

      if (`${i}:${j}` === PARK_BLOCK) {
        parks.push(pointsOf([p0, p1, p2, p3]))
        const school = rect(bw * 0.3, bw * 0.72, 22, 58)
        addBuilding(school, 'education', 7, true, j, false)
        const [sx, sy] = lerp(school[2], school[3], 0.5)
        if (fits(sx, sy + 16, 90)) mapLabels.push({ text: 'Школа-гимназия №8', x: round(sx), y: round(sy + 16), angle: 0, kind: 'poi', delay: 1.6 })
        continue
      }
      if (`${i}:${j}` === PLOT_BLOCK) plots.push(pointsOf(rect(3, bw - 3, 3, bh - 3)))

      if (random() < 0.6) {
        // Периметральная застройка: дома вдоль улиц, во дворе — гаражи и сараи.
        for (const [y0, y1, front] of [[4, 22, true], [bh - 22, bh - 4, false]] as const) {
          const count = 2 + Math.floor(random() * 2)
          const span = (bw - 16) / count
          for (let k = 0; k < count; k++) {
            const kind = pickClass()
            addBuilding(rect(8 + k * span, 8 + (k + 1) * span - 9, y0, y1), kind, heightOf(kind), kind !== 'other' && random() < 0.7, j, front)
          }
        }
        const kind = pickClass()
        addBuilding(rect(8, 24, 34, bh - 34), kind, heightOf(kind), random() < 0.4, j, false)
        for (let k = 0; k < 2; k++) {
          const x = 48 + random() * (bw - 80)
          const y = 40 + random() * (bh - 80)
          addBuilding(rect(x, x + 12, y, y + 10), 'outbuilding', 2.5, false, j, false)
        }
      } else {
        // Микрорайон: секции поперёк квартала и магазин у дороги.
        const count = 3 + Math.floor(random() * 2)
        const step = (bw - 30) / count
        for (let k = 0; k < count; k++) {
          const kind = pickClass()
          const y0 = k % 2 ? 26 : 4
          addBuilding(rect(10 + k * step, 10 + k * step + 16, y0, y0 + bh * 0.62), kind, heightOf(kind), kind !== 'other' && random() < 0.6, j, y0 === 4)
        }
        addBuilding(rect(bw - 34, bw - 8, bh - 26, bh - 6), 'commercial', heightOf('commercial'), true, j, false)
      }
    }
  }
  buildings.sort((a, b) => a.sortY - b.sortY)

  // Сеть: две магистрали вдоль больших улиц, перемычка и распределительные трубы вдоль поперечных улиц.
  const supplies: Pipe[] = []
  const returns: Pipe[] = []
  const pens: Array<{ path: string; begin: number; duration: number }> = []
  const GAPS = { mag: 1.9, dist: 1.4, stub: 0.9 }
  const offset = (points: Point[], distance: number): Point[] => points.map((point, i) => {
    const [a, b] = i < points.length - 1 ? [point, points[i + 1]] : [points[i - 1], point]
    const len = Math.hypot(b[0] - a[0], b[1] - a[1])
    // Левая нормаль к направлению участка (ось y экрана смотрит вниз).
    return [point[0] + ((b[1] - a[1]) / len) * distance, point[1] - ((b[0] - a[0]) / len) * distance]
  })
  const addPipe = (points: Point[], delay: number, duration: number, kind: Pipe['kind']) => {
    const d = pathOf(offset(points, GAPS[kind]))
    supplies.push({ d, delay: round(delay), duration, kind })
    returns.push({ d: pathOf(offset(points, -GAPS[kind])), delay: round(delay + 0.1), duration, kind })
    if (kind !== 'stub') pens.push({ path: d, begin: round(delay), duration })
  }

  const mainLine = (j: number): HLine => ({ c: HORIZONTALS[j].c + HORIZONTALS[j].half + PIPE_OFFSET, d: HORIZONTALS[j].d })
  const branchLine = (i: number): VLine => ({ a: VERTICALS[i].a + VERTICALS[i].half + PIPE_OFFSET, b: VERTICALS[i].b })
  const MAIN_DURATION = 1.5
  const mains = [
    { line: mainLine(2), start: 1.7, label: 'Ду 500', labelAt: [255, 805] },
    { line: mainLine(3), start: 1.95, label: 'Ду 600', labelAt: [245, 905] }
  ]
  const reach = (main: (typeof mains)[number], x: number) => main.start + MAIN_DURATION * ((x + 10) / (W + 20))
  const [mainA, mainB] = mains
  const angleH = round((Math.atan(HORIZONTALS[2].d) * 180) / Math.PI)

  const netLabels: Label[] = []
  for (const main of mains) {
    addPipe([[-10, yAt(main.line, -10)], [W + 10, yAt(main.line, W + 10)]], main.start, MAIN_DURATION, 'mag')
    for (const x of main.labelAt) netLabels.push({ text: main.label, x, y: round(yAt(main.line, x) + 3.6), angle: angleH, kind: 'diameter', delay: 3.3 })
  }

  const branches = [
    { i: 2, from: mainA, to: mainB, label: 'Ду 300', kind: 'dist' as const },
    { i: 4, from: mainA, to: -10, label: 'Ду 200', kind: 'dist' as const },
    { i: 3, from: mainB, to: H + 10, label: 'Ду 200', kind: 'dist' as const },
    { i: 5, from: mainB, to: H + 10, label: 'Ду 400', kind: 'mag' as const }
  ]
  const junctions = new Map<(typeof mains)[number], number[]>([[mainA, []], [mainB, []]])
  for (const branch of branches) {
    const line = branchLine(branch.i)
    const start = meet(line, branch.from.line)
    const end = typeof branch.to === 'number' ? [xAt(line, branch.to), branch.to] as Point : meet(line, branch.to.line)
    const delay = reach(branch.from, start[0])
    addPipe([start, end], delay, 0.6, branch.kind)
    junctions.get(branch.from)!.push(start[0])
    if (typeof branch.to !== 'number') junctions.get(branch.to)!.push(end[0])
    const mid = lerp(start, end, typeof branch.to === 'number' ? 0.55 : 0.5)
    const angleV = round((Math.atan2(1, line.b) * 180) / Math.PI)
    netLabels.push({ text: branch.label, x: round(mid[0] + 3.6), y: round(mid[1]), angle: angleV, kind: 'diameter', delay: 3.4 })
  }

  // Узлы с именами — камеры на магистралях, мелкие — ответвления к домам.
  const namedNodes: Array<{ x: number; y: number; delay: number }> = []
  const smallNodes: Array<{ x: number; y: number; delay: number }> = []
  const nodeXs = new Map<(typeof mains)[number], number[]>()
  const NAMES = new Map([
    [mainA, ['2ВВ-3', '2ВВ-5', '2ВВ-8', '2ВВ-9А', '1В3-10', '1В3-11']],
    [mainB, ['2КД-7', '2КД-8', '2КД-9Б', '2КД-9В', '2КД-10', '2КД-11', '2КД-12']]
  ])
  const EXTRA_NODES = new Map([[mainA, [190, 430, 610, 870]], [mainB, [150, 380, 645, 790]]])
  for (const main of mains) {
    const xs = [...EXTRA_NODES.get(main)!, ...junctions.get(main)!].sort((a, b) => a - b)
    nodeXs.set(main, xs)
    const names = NAMES.get(main)!
    xs.forEach((x, k) => {
      const y = yAt(main.line, x)
      const delay = round(reach(main, x) + 0.05)
      namedNodes.push({ x: round(x), y: round(y), delay })
      netLabels.push({ text: names[k], x: round(x - 4), y: round(y - 10), angle: 0, kind: 'node', delay: round(delay + 0.35) })
    })
  }

  for (const consumer of frontConsumers) {
    const main = consumer.row === 2 ? mainA : consumer.row === 3 ? mainB : null
    if (!main || consumer.x < 40 || consumer.x > W - 60) continue
    const nearNode = nodeXs.get(main)!.some((x) => Math.abs(x - consumer.x) < 16)
    if (nearNode) continue
    const pipeY = yAt(main.line, consumer.x)
    const delay = reach(main, consumer.x) + 0.1
    addPipe([[consumer.x, pipeY], [consumer.x, consumer.y]], delay, 0.3, 'stub')
    smallNodes.push({ x: round(consumer.x), y: round(pipeY), delay: round(delay) })
  }

  // Выбранный участок — между 2КД-10 и 2КД-11, его сведения показывает всплывающее окно.
  const from: Point = [645, yAt(mainB.line, 645)]
  const to: Point = [790, yAt(mainB.line, 790)]
  const at = lerp(from, to, 0.5)

  // После расчёта на трубах появляются расходы Gп/Gо — синим, как подписи веб-ТГИД.
  const flowLabel = (main: (typeof mains)[number], x: number, text: string): Label => ({ text, x, y: round(yAt(main.line, x) + 3.6), angle: angleH, kind: 'flow', delay: 5 })
  const c3 = branchLine(5)
  const c3Mid = lerp(meet(c3, mainB.line), [xAt(c3, H + 10), H + 10], 0.55)
  netLabels.push(
    flowLabel(mainA, 520, 'Gп=136; Gо=216'),
    flowLabel(mainB, 465, 'Gп=284; Gо=301'),
    { text: 'Gп=16; Gо=12', x: round(c3Mid[0] - 9), y: round(c3Mid[1] - 46), angle: round((Math.atan2(1, c3.b) * 180) / Math.PI), kind: 'flow', delay: 5.1 }
  )

  const streetLabel = (v: VLine, y: number, text: string): Label => ({ text, x: round(xAt(v, y)), y, angle: round((Math.atan2(1, v.b) * 180) / Math.PI), kind: 'street', delay: 1.2 })
  mapLabels.push(
    streetLabel(VERTICALS[4], 160, 'Мұратбаев көшесі'),
    streetLabel(VERTICALS[3], 500, 'Мұқанов көшесі'),
    { ...streetLabel(canalLine, 470, 'Есентай'), x: round(xAt(canalLine, 470) - 7), kind: 'water' },
    { text: 'Жамбыл көшесі', x: 620, y: round(yAt(HORIZONTALS[1], 620) + 3), angle: angleH, kind: 'street', delay: 1.2 }
  )

  return {
    streets,
    canal: pathOf(canalPoints),
    parks,
    plots,
    buildings,
    outlines,
    mapLabels,
    supplies,
    returns,
    pens,
    namedNodes,
    smallNodes,
    netLabels,
    flowA: supplies[0].d,
    flowB: supplies[1].d,
    selected: { d: pathOf([from, to]), from, at }
  }
}

const map = buildMap()

// Анимация начинается, когда окно попадает на экран: на телефоне первый экран занят заголовком.
const windowEl = ref<HTMLElement | null>(null)
const waiting = ref(false)
const cursorReady = ref(false)
const cursorVars = ref<Record<string, string>>({})
const VISIBLE_SHARE = 0.3

// Курсор ходит по настоящим местам кнопок, поэтому их положение меряется после отрисовки и при смене ширины.
const measureCursor = () => {
  const root = windowEl.value
  if (!root) return
  const box = root.getBoundingClientRect()
  const centerOf = (selector: string) => {
    const rect = root.querySelector(selector)?.getBoundingClientRect()
    if (!rect || (!rect.width && !rect.height)) return null
    return [rect.left + rect.width / 2 - box.left, rect.top + rect.height / 2 - box.top]
  }
  const targets = { calc: centerOf('.calc-button'), info: centerOf('.tool-info'), sel: centerOf('.selected-line') }
  if (!targets.calc || !targets.info || !targets.sel) {
    cursorReady.value = false
    return
  }
  const vars: Record<string, string> = { '--start-x': `${box.width * 0.62}px`, '--start-y': `${box.height * 0.92}px` }
  for (const [name, [x, y]] of Object.entries(targets) as Array<[string, number[]]>) {
    vars[`--${name}-x`] = `${Math.round(x)}px`
    vars[`--${name}-y`] = `${Math.round(y)}px`
  }
  cursorVars.value = vars
  cursorReady.value = true
}

let observer: IntersectionObserver | null = null

onMounted(() => {
  measureCursor()
  window.addEventListener('resize', measureCursor, { passive: true })
  const rect = windowEl.value?.getBoundingClientRect()
  if (!rect || rect.top < window.innerHeight * (1 - VISIBLE_SHARE)) return
  waiting.value = true
  observer = new IntersectionObserver(([entry]) => {
    if (!entry?.isIntersecting) return
    waiting.value = false
    run.value++
    observer?.disconnect()
  }, { threshold: VISIBLE_SHARE })
  if (windowEl.value) observer.observe(windowEl.value)
})

onBeforeUnmount(() => {
  observer?.disconnect()
  window.removeEventListener('resize', measureCursor)
})

watch(run, () => nextTick(measureCursor))
</script>

<style scoped>
.map-demo {
  margin: 0;
}

.map-window {
  --panel-w: clamp(196px, 25%, 272px);
  overflow: hidden;
  border: 1px solid var(--ink);
  border-radius: 8px;
  color: #18181b;
  background: #f4f4f5;
  box-shadow: 0 1px 0 var(--line), 0 30px 60px -40px rgba(28, 27, 24, 0.45);
  font-family: Roboto, var(--font-sans), sans-serif;
}

.mi {
  width: 1em;
  height: 1em;
  flex-shrink: 0;
  fill: currentColor;
}

/* Шапка приложения (v-toolbar) */
.app-bar {
  position: relative;
  z-index: 1;
  display: flex;
  align-items: center;
  gap: 10px;
  height: 42px;
  padding: 0 10px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 0 1px rgba(24, 39, 75, 0.25), 0 2px 4px -2px rgba(24, 39, 75, 0.12);
  font-size: 12px;
  white-space: nowrap;
}

.app-brand {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #52525b;
  font-size: 14px;
}

.app-brand b {
  color: #18181b;
  font-weight: 600;
}

.app-logo {
  width: 20px;
  height: 20px;
}

.app-context {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  height: 22px;
  padding: 0 9px;
  border-radius: 11px;
  color: #52525b;
  background: #f4f4f5;
  font-size: 11px;
}

.app-menu {
  display: inline-flex;
  gap: 2px;
}

.app-menu-item {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  height: 28px;
  padding: 0 8px;
  border-radius: 4px;
  font-weight: 500;
}

.app-menu-item .mi {
  font-size: 16px;
}

.app-menu-item .chevron {
  margin-left: -2px;
}

/* «Нажатие» на «Расчёт» после того, как сеть нарисована. */
.calc-button {
  animation: press 0.9s ease 4.3s both;
}

@keyframes press {
  0% { background: transparent; }
  30% { background: rgba(21, 101, 192, 0.16); transform: scale(0.96); }
  100% { background: rgba(24, 39, 75, 0.06); transform: none; }
}

.app-search {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
  height: 28px;
  margin-left: auto;
  padding: 0 6px 0 9px;
  border-radius: 6px;
  color: #52525b;
  background: rgba(24, 39, 75, 0.05);
}

.app-search .mi {
  font-size: 17px;
}

.search-hint {
  overflow: hidden;
  min-width: 0;
  max-width: 190px;
  text-overflow: ellipsis;
}

.app-search kbd {
  padding: 1px 5px;
  border: 1px solid rgba(24, 39, 75, 0.14);
  border-radius: 4px;
  background: #fff;
  font-family: inherit;
  font-size: 10px;
}

.app-icons {
  display: inline-flex;
  align-items: center;
  gap: 14px;
  margin-left: 6px;
  font-size: 19px;
}

.users {
  position: relative;
  display: inline-flex;
}

.users i {
  position: absolute;
  top: -7px;
  right: -7px;
  display: grid;
  width: 13px;
  height: 13px;
  place-items: center;
  border-radius: 50%;
  color: #fff;
  background: #4caf50;
  font-size: 8px;
  font-style: normal;
}

.avatar {
  display: grid;
  width: 24px;
  height: 24px;
  place-items: center;
  border-radius: 50%;
  background: #e4e4e7;
  font-size: 9.5px;
  font-weight: 600;
}

/* Карта */
.map-canvas {
  position: relative;
  aspect-ratio: 1000 / 540;
  overflow: hidden;
  background: #efede8;
}

.map-canvas > svg {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
}

.draw {
  fill: none;
  stroke-dasharray: 1;
  stroke-dashoffset: 1;
  animation: draw var(--t, 1.2s) cubic-bezier(0.55, 0.1, 0.35, 1) var(--d, 0s) forwards;
}

@keyframes draw {
  to { stroke-dashoffset: 0; }
}

.pop {
  opacity: 0;
  transform-box: fill-box;
  transform-origin: center;
  animation: pop 0.45s ease var(--d, 0s) forwards;
}

@keyframes pop {
  from { opacity: 0; transform: scale(0.4); }
  to { opacity: 1; transform: scale(1); }
}

.fade {
  opacity: 0;
  animation: fade 0.6s ease var(--d, 0s) forwards;
}

@keyframes fade {
  to { opacity: 1; }
}

/* Дома «вырастают» из земли, квартал за кварталом. */
.rise {
  opacity: 0;
  transform: translateY(7px);
  animation: rise 0.7s cubic-bezier(0.2, 0.8, 0.2, 1) var(--d, 0s) forwards;
}

@keyframes rise {
  to { opacity: 1; transform: none; }
}

.parks polygon {
  fill: #d6e8cb;
}

.streets .road {
  fill: none;
  stroke: #fff;
  stroke-width: var(--w);
}

/* Бровка рисуется чернилами и потом выцветает до цвета обводки дорог подложки. */
.streets .draw.edge {
  stroke: #4b483f;
  stroke-width: 1;
  animation:
    draw var(--t) cubic-bezier(0.55, 0.1, 0.35, 1) var(--d) forwards,
    settle-edge 0.9s ease calc(var(--d) + var(--t)) forwards;
}

@keyframes settle-edge {
  to { stroke: #d6d2c8; }
}

.sketches .draw.sketch {
  stroke: #4b483f;
  stroke-width: 0.8;
  stroke-linejoin: round;
  animation:
    draw var(--t) cubic-bezier(0.55, 0.1, 0.35, 1) var(--d) forwards,
    settle-sketch 0.6s ease calc(var(--d) + 1.1s) forwards;
}

@keyframes settle-sketch {
  to { opacity: 0; }
}

.pen {
  opacity: 0;
  animation: pen-life var(--t) linear var(--d) forwards;
}

@keyframes pen-life {
  0%, 92% { opacity: 1; }
  100% { opacity: 0; }
}

.pen-glow {
  fill: rgba(127, 0, 0, 0.16);
}

.pen-nib {
  fill: #7f0000;
  stroke: #fff;
  stroke-width: 1.2;
}

/* Пока окно не на экране, анимация стоит на нуле. */
.map-window.waiting *,
.map-window.waiting *::before,
.map-window.waiting *::after {
  animation-play-state: paused !important;
}

.cursor {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 3;
  width: 14px;
  height: 20px;
  pointer-events: none;
  opacity: 0;
  animation: cursor-path 2.3s cubic-bezier(0.45, 0.05, 0.3, 1) 3.7s forwards;
}

.cursor svg {
  position: absolute;
  top: -1px;
  left: -1px;
  width: 14px;
  height: 20px;
  fill: #111;
  stroke: #fff;
  stroke-width: 1.2;
  stroke-linejoin: round;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.3));
  animation: cursor-hide 0.5s ease 8.6s forwards;
}

@keyframes cursor-path {
  0% { opacity: 0; left: var(--start-x); top: var(--start-y); }
  8% { opacity: 1; left: var(--start-x); top: var(--start-y); }
  26%, 30% { opacity: 1; left: var(--calc-x); top: var(--calc-y); }
  70%, 74% { opacity: 1; left: var(--info-x); top: var(--info-y); }
  93%, 100% { opacity: 1; left: var(--sel-x); top: var(--sel-y); }
}

@keyframes cursor-hide {
  to { opacity: 0; }
}

/* Круг нажатия — на «Расчёте», инструменте сведений и участке. */
.cursor .click {
  position: absolute;
  top: -10px;
  left: -10px;
  width: 20px;
  height: 20px;
  border: 2px solid #1565c0;
  border-radius: 50%;
  opacity: 0;
  animation:
    click 0.5s ease-out 4.3s,
    click 0.5s ease-out 5.35s,
    click 0.5s ease-out 5.86s;
}

@keyframes click {
  from { opacity: 0.9; transform: scale(0.3); }
  to { opacity: 0; transform: scale(1.4); }
}

.canal {
  stroke: #9cc7e6;
  stroke-width: 1.6;
}

.plots polygon {
  fill: rgba(233, 154, 82, 0.07);
  stroke: #e99a52;
  stroke-width: 1;
}

.consumers polygon {
  fill: none;
  stroke: #e99a52;
  stroke-width: 1;
}

.map-text text,
.net-text text {
  paint-order: stroke;
  stroke: #fff;
  stroke-width: 3px;
  stroke-linejoin: round;
}

.map-text .load {
  fill: #555;
  font-size: 9px;
}

.map-text .street {
  fill: #8c8a84;
  font-size: 9px;
}

.map-text .water {
  fill: #6b8fb5;
  font-size: 9px;
  font-style: italic;
}

.map-text .poi {
  fill: #5d6b57;
  font-size: 9.5px;
}

.pipes path {
  stroke-linecap: round;
  stroke-linejoin: round;
}

.pipes.supply path {
  stroke: #7f0000;
}

.pipes.return path {
  stroke: #00007f;
}

.pipes path.mag {
  stroke-width: 2.5;
}

.pipes path.dist {
  stroke-width: 1.8;
}

.pipes path.stub {
  stroke-width: 1.1;
}

/* Выделение участка — как в веб-ТГИД (utils/selectionHighlight.ts). */
.selected {
  opacity: 0;
  animation: fade 0.3s ease 5.86s forwards;
}

.selected-line {
  fill: none;
  stroke: #00c8ff;
  stroke-width: 4.5;
  stroke-linecap: round;
  opacity: 0.9;
}

.selected circle {
  fill: #00c8ff;
}

.flow circle {
  fill: #fff;
  stroke: #7f0000;
  stroke-width: 1.3;
  opacity: 0;
  animation: fade 0.4s ease 3.2s forwards;
}

.nodes .named circle {
  fill: #fff;
  stroke: #111;
  stroke-width: 1.7;
}

.nodes .named .dot {
  fill: #111;
  stroke: none;
}

.nodes .small {
  fill: #fff;
  stroke: #111;
  stroke-width: 1.2;
}

.net-text .node {
  fill: #2b2b2b;
  font-size: 10.5px;
}

.net-text .diameter {
  fill: #2b2b2b;
  font-size: 10.5px;
  font-style: italic;
  font-weight: 600;
}

.net-text .flow {
  fill: #2a5fc1;
  font-size: 10px;
  font-weight: 500;
}

/* Плавающие панели (glass-surface веб-ТГИД) */
.layers-panel,
.glass,
.map-popover {
  position: absolute;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 0 1px rgba(24, 39, 75, 0.24), 0 12px 24px -8px rgba(24, 39, 75, 0.16);
}

.layers-panel {
  top: 10px;
  bottom: 10px;
  left: 10px;
  display: flex;
  flex-direction: column;
  width: var(--panel-w);
  overflow: hidden;
  background: #fff;
  font-size: 11px;
}

.panel-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  padding: 10px 10px 6px 14px;
}

.panel-head strong {
  display: block;
  font-size: 14px;
  font-weight: 600;
}

.panel-head small {
  color: #71717a;
  font-size: 10.5px;
}

.panel-head .mi {
  margin-top: 4px;
  color: #3f3f46;
  font-size: 17px;
}

.panel-tabs {
  display: flex;
  justify-content: space-between;
  padding: 0 10px;
  border-bottom: 1px solid rgba(24, 39, 75, 0.1);
  font-size: 11.5px;
  font-weight: 500;
}

.panel-tabs span {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 7px 4px;
}

.panel-tabs .active {
  color: #1565c0;
  box-shadow: inset 0 -2px 0 #1565c0;
}

.badge {
  display: inline-grid;
  min-width: 15px;
  height: 15px;
  place-items: center;
  padding: 0 4px;
  border-radius: 8px;
  color: #1565c0;
  background: #e3ecfa;
  font-size: 9.5px;
  font-style: normal;
  transform: scale(0);
  animation: tick 0.3s ease var(--d) forwards;
}

.panel-body {
  flex: 1;
  min-height: 0;
  overflow: hidden;
  padding: 4px 0;
}

.group-head,
.planet-row {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 12px;
  color: #3f3f46;
  font-size: 11px;
  font-weight: 600;
}

.group-head .end,
.planet-row .end {
  margin-left: auto;
}

.planet-row {
  font-weight: 400;
}

.switch-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 4px 14px 8px;
  font-size: 11.5px;
}

.switch {
  position: relative;
  width: 26px;
  height: 11px;
  flex-shrink: 0;
  border-radius: 6px;
  background: #c4c4c8;
}

.switch::after {
  content: "";
  position: absolute;
  top: -3px;
  left: -2px;
  width: 17px;
  height: 17px;
  border-radius: 50%;
  background: #fff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.35);
}

.layer-row {
  display: flex;
  gap: 8px;
  padding: 5px 12px 5px 16px;
}

.check {
  position: relative;
  color: #6b6b70;
  font-size: 18px;
  line-height: 0;
}

/* Галочка ставится в тот момент, когда здания начинают вырастать. */
.check .tick {
  position: absolute;
  inset: 0;
  color: #1565c0;
  transform: scale(0);
  animation: tick 0.25s ease 0.9s forwards;
}

@keyframes tick {
  to { transform: scale(1); }
}

.layer-text {
  min-width: 0;
}

.layer-text b {
  display: block;
  font-size: 12px;
  font-weight: 500;
}

.layer-text small {
  display: block;
  overflow: hidden;
  color: #71717a;
  font-size: 10.5px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.legend {
  display: grid;
  grid-template-columns: repeat(2, max-content);
  gap: 1px 8px;
  margin-top: 3px;
  color: #52525b;
  font-size: 9.5px;
}

.legend span {
  display: inline-flex;
  align-items: center;
  gap: 3px;
}

.legend i {
  width: 8px;
  height: 8px;
  border: 1px solid rgba(0, 0, 0, 0.18);
}

.group-note {
  margin: 0;
  padding: 0 14px 6px;
  color: #52525b;
  font-size: 10.5px;
  line-height: 1.45;
}

.panel-foot {
  display: flex;
  justify-content: flex-end;
  padding: 8px 10px;
  background: #fff;
}

.panel-foot span {
  padding: 5px 12px;
  border-radius: 4px;
  color: #fff;
  background: #9dbde6;
  font-size: 11px;
  font-weight: 500;
}

/* Инструменты карты и кнопки вида */
.map-modes {
  top: 10px;
  left: calc(50% + var(--panel-w) / 2);
  display: flex;
  padding: 3px;
  transform: translateX(-50%);
}

.map-modes > span,
.control-group > span {
  display: grid;
  width: 34px;
  height: 34px;
  place-items: center;
  border-radius: 6px;
  color: #52525b;
  font-size: 17px;
}

.tool-info {
  animation: tool-on 0.3s ease 5.35s forwards;
}

@keyframes tool-on {
  to { color: #000; background: rgba(24, 39, 75, 0.1); }
}

.map-controls {
  position: absolute;
  right: 10px;
  bottom: 10px;
  display: grid;
  gap: 10px;
}

.control-group {
  position: static;
  padding: 3px;
}

.control-group .text {
  font-size: 11px;
  font-weight: 600;
}

.scale-box {
  position: absolute;
  bottom: 10px;
  left: calc(var(--panel-w) + 22px);
  width: 54px;
  padding: 0 4px;
  border: 2px solid #333;
  border-top: 0;
  color: #333;
  background: rgba(255, 255, 255, 0.75);
  font-size: 9.5px;
  line-height: 15px;
}

.cursor-coords {
  position: absolute;
  bottom: 8px;
  left: calc(50% + var(--panel-w) / 2);
  display: inline-flex;
  align-items: center;
  gap: 6px;
  height: 26px;
  padding: 0 9px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 1px 6px rgba(0, 0, 0, 0.18);
  font-size: 10.5px;
  white-space: nowrap;
  transform: translateX(-50%);
}

.cursor-coords b {
  color: #1565c0;
  font-weight: 600;
}

.cursor-coords .caret {
  margin-left: -5px;
  color: #1565c0;
}

.coords-value {
  padding-left: 8px;
  border-left: 1px solid rgba(118, 118, 118, 0.3);
}

/* Сообщение о завершении расчёта (v-snackbar) */
.snackbar {
  position: absolute;
  bottom: 46px;
  left: calc(50% + var(--panel-w) / 2);
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  border-radius: 4px;
  color: #fff;
  background: #333;
  box-shadow: 0 6px 16px -6px rgba(0, 0, 0, 0.45);
  font-size: 11.5px;
  white-space: nowrap;
  opacity: 0;
  transform: translate(-50%, 8px);
  animation: toast 4s ease 4.7s forwards;
}

.snackbar .mi {
  color: #6fcf73;
  font-size: 15px;
}

@keyframes toast {
  0% { opacity: 0; transform: translate(-50%, 8px); }
  10%, 80% { opacity: 1; transform: translate(-50%, 0); }
  100% { opacity: 0; transform: translate(-50%, 8px); }
}

/* Всплывающее окно участка (map-popover) — над выделенным участком, со стрелкой вниз */
.map-popover {
  width: 288px;
  background: #fff;
  font-size: 11.5px;
  opacity: 0;
  transform: translate(-50%, calc(-100% - 4px));
  animation: popover 0.45s cubic-bezier(0.2, 0.8, 0.2, 1) 5.95s forwards;
}

.map-popover::after {
  content: "";
  position: absolute;
  bottom: -6px;
  left: 50%;
  width: 12px;
  height: 12px;
  background: #fff;
  box-shadow: 2px 2px 3px -1px rgba(24, 39, 75, 0.12);
  transform: translateX(-50%) rotate(45deg);
}

@keyframes popover {
  to { opacity: 1; transform: translate(-50%, calc(-100% - 12px)); }
}

.map-popover header {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 8px 8px 4px 11px;
}

.map-popover header > .mi {
  margin-top: 2px;
  font-size: 17px;
}

.map-popover header strong {
  display: block;
  font-size: 13px;
  font-weight: 600;
}

.map-popover header small {
  color: rgba(0, 0, 0, 0.6);
  font-size: 11px;
}

.map-popover .close {
  margin-left: auto;
  color: #52525b;
  font-size: 16px;
}

.map-popover dl {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 4px 12px;
  margin: 0;
  padding: 4px 12px 8px;
}

.map-popover dt {
  color: rgba(0, 0, 0, 0.6);
}

.map-popover dd {
  margin: 0;
  font-weight: 500;
  text-align: right;
}

.map-popover footer {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 8px 8px;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  height: 26px;
  padding: 0 10px;
  border-radius: 4px;
  font-size: 11.5px;
  font-weight: 500;
}

.btn.primary {
  color: #fff;
  background: #1565c0;
}

.map-popover footer > .mi {
  margin: 0 5px;
  font-size: 17px;
}

.map-popover footer > .end {
  margin-left: auto;
}

figcaption {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-top: 14px;
  color: var(--muted);
  font-family: var(--mono);
  font-size: 0.74rem;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.replay {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  flex-shrink: 0;
  padding: 6px 10px;
  border: 1px solid var(--line-strong);
  border-radius: var(--radius-sm);
  color: var(--ink);
  background: transparent;
  font: inherit;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.replay:hover {
  background: var(--paper-2);
}

@media (max-width: 1100px) {
  .app-menu-item:not(.calc-button),
  .app-context,
  .app-icons .users,
  .app-icons > .mi {
    display: none;
  }
}

@media (max-width: 760px) {
  .map-window {
    --panel-w: 0px;
  }

  .map-canvas {
    aspect-ratio: 4 / 3.4;
  }

  .layers-panel,
  .map-text,
  .net-text,
  .search-hint,
  .coords-value,
  .control-group:first-child,
  .scale-box {
    display: none;
  }

  /* На узком экране окно участка не привязано к точке, а прижато к низу карты. */
  .map-popover {
    inset: auto auto 44px 8px !important;
    width: min(250px, 74%);
    font-size: 10.5px;
    transform: translateY(8px);
    animation-name: popover-docked;
  }

  .map-popover::after {
    display: none;
  }

  @keyframes popover-docked {
    to { opacity: 1; transform: none; }
  }

  .snackbar {
    display: none;
  }

  figcaption {
    flex-direction: column;
    align-items: flex-start;
  }
}

@media (prefers-reduced-motion: reduce) {
  .map-window *,
  .map-window *::before,
  .map-window *::after {
    animation-delay: 0s !important;
  }

  .flow,
  .pens,
  .cursor,
  .snackbar {
    display: none;
  }
}
</style>
