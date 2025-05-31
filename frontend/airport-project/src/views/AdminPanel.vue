<template>
  <v-container>
    <h2 class="mb-3">Админ-панель</h2>
    <v-tabs v-model="tab">
      <v-tab value="flights">Рейсы</v-tab>
      <v-tab value="tickets">Билеты</v-tab>
      <v-tab value="airports">Аэропорты</v-tab>
      <v-tab value="airplanes">Самолёты</v-tab>
      <v-tab value="users">Пользователи</v-tab>
    </v-tabs>

    <v-window v-model="tab" class="mt-3">
      <v-window-item value="flights">
        <FlightsAdmin />
      </v-window-item>
      <v-window-item value="tickets">
        <TicketsAdmin />
      </v-window-item>
      <v-window-item value="airports">
        <AirportsAdmin />
      </v-window-item>
      <v-window-item value="airplanes">
        <AirplanesAdmin />
      </v-window-item>
      <v-window-item value="users">
        <UsersAdmin />
      </v-window-item>
    </v-window>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import FlightsAdmin from './FlightsAdmin.vue'
import TicketsAdmin from './TicketsAdmin.vue'
import AirportsAdmin from './AirportsAdmin.vue'
import AirplanesAdmin from './AirplanesAdmin.vue'
import UsersAdmin from './UsersAdmin.vue'

const tab = ref('flights')
</script>
