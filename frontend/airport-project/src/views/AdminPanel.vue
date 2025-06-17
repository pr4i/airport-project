<template>
  <v-app>
    <!-- Навигационный бар -->
    <v-app-bar app color="#07519a" dark style="box-shadow: 0 2px 6px rgba(0,0,0,0.3); border-bottom: 1px solid white;">
      <v-toolbar-title>
        <v-icon left>mdi-airplane</v-icon>
        AIRWAY
      </v-toolbar-title>
      <v-spacer />
      <v-btn text @click="router.push('/')">Главная</v-btn>
      <v-btn text @click="router.push('/onlineboard')">Онлайн-табло</v-btn>
      <v-btn text @click="router.push('/checkin')">Регистрация</v-btn>
      <v-btn text @click="router.push('/dashboard')">Личный кабинет</v-btn>
      <v-btn v-if="!isAuth" icon @click="router.push('/login')" title="Войти">
        <v-icon>mdi-account-circle</v-icon>
      </v-btn>
      <v-btn v-else text @click="logout">
        <v-icon left>mdi-logout</v-icon> Выйти
      </v-btn>
    </v-app-bar>

    <v-main class="admin-bg">
      <v-container class="py-6">
        <v-card class="pa-4 admin-card" elevation="10">
          <h2 class="mb-3">Админ-панель</h2>
          <v-tabs v-model="tab" color="primary" background-color="#e3f0fd" grow>
            <v-tab value="flights">Рейсы</v-tab>
            <v-tab value="tickets">Билеты</v-tab>
            <v-tab value="airports">Аэропорты</v-tab>
            <v-tab value="airplanes">Самолёты</v-tab>
            <v-tab value="users">Пользователи</v-tab>
          </v-tabs>

          <v-window v-model="tab" class="mt-4">
            <v-window-item value="flights"><FlightsAdmin /></v-window-item>
            <v-window-item value="tickets"><TicketsAdmin /></v-window-item>
            <v-window-item value="airports"><AirportsAdmin /></v-window-item>
            <v-window-item value="airplanes"><AirplanesAdmin /></v-window-item>
            <v-window-item value="users"><UsersAdmin /></v-window-item>
          </v-window>
        </v-card>
      </v-container>
    </v-main>

    <SiteFooter />
  </v-app>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import FlightsAdmin from './FlightsAdmin.vue'
import TicketsAdmin from './TicketsAdmin.vue'
import AirportsAdmin from './AirportsAdmin.vue'
import AirplanesAdmin from './AirplanesAdmin.vue'
import UsersAdmin from './UsersAdmin.vue'
import SiteFooter from '@/components/SiteFooter.vue'

const tab = ref('flights')
const router = useRouter()
const userStore = useUserStore()
const isAuth = computed(() => !!userStore.token)

function logout() {
  userStore.logout()
  router.push('/home')
}
</script>

<style scoped>
.admin-bg {
  background: linear-gradient(120deg, #07519a 70%, #e3f0fd 100%);
  min-height: 100vh;
}
.admin-card {
  border-radius: 16px;
  background: #fff;
}
</style>
