<template>
  <v-app>
    <v-app-bar app>
      <v-toolbar-title>My App</v-toolbar-title>
    </v-app-bar>
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
