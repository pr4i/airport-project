<template>
  <v-app>
    <v-main>
      <RouterView />
    </v-main>
  </v-app>
</template>

<script setup>
import { VApp, VAppBar, VToolbarTitle, VMain } from 'vuetify/components'
</script>

<style>
@import 'vuetify/styles';  /* Подключаем стили Vuetify */
</style>
