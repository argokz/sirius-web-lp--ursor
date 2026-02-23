<template>
  <v-img
    :src="src"
    :alt="alt"
    :lazy-src="lazySrc"
    :loading="loading"
    v-bind="$attrs"
    @load="onLoad"
  >
    <template v-slot:placeholder>
      <v-row class="fill-height ma-0" align="center" justify="center">
        <v-progress-circular indeterminate color="primary" />
      </v-row>
    </template>
  </v-img>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps({
  src: {
    type: String,
    required: true
  },
  alt: {
    type: String,
    default: ''
  },
  lazySrc: {
    type: String,
    default: '/logo.png'
  }
})

const loading = ref(true)

const onLoad = () => {
  loading.value = false
}
</script>

