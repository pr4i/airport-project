<template>
  <v-app>
    <!-- Верхняя навигационная панель -->
      <v-app-bar app color="#07519a" dark style="box-shadow: 0 2px 6px rgba(0,0,0,0.3); border-bottom: 1px solid white;">
      <v-toolbar-title class="airway-title">
        <v-icon left>mdi-airplane</v-icon>
        AIRWAY
      </v-toolbar-title>
      <v-spacer />
      <v-btn v-if="userStore.isAdmin" text @click="router.push('/admin')">Админ-панель</v-btn>
      <v-btn text class="nav-link" @click="router.push('/')">Главная cтраница</v-btn>
      <v-btn text class="nav-link" @click="router.push('/onlineboard')">Онлайн-табло</v-btn>
      <v-btn text class="nav-link" @click="router.push('/flights')">Бронирование</v-btn>
      <v-btn text class="nav-link" @click="router.push('/register')">Регистрация</v-btn>
      <v-btn
        color="error"
        text
        class="nav-link"
        @click="logout"
      >
        <v-icon left>mdi-logout</v-icon> Выйти
      </v-btn>
    </v-app-bar>

    <v-main class="dashboard-bg">
      <v-container>
        <!-- Блок приветствия -->
        <div class="welcome-block">
          <h2>Здравствуйте, <span class="user-name">{{ userName || 'User' }}</span>!</h2>
          <div class="divider-bar"></div>
          <p>Добро пожаловать в ваш личный кабинет управления полётами!</p>
        </div>

        <!-- Карточки статистики -->
        <v-row class="mb-8" justify="center">
          <v-col cols="12" md="3" v-for="card in cards" :key="card.title">
            <v-card class="stat-card">
              <div class="stat-value">{{ card.value }}</div>
              <div class="stat-title">{{ card.title }}</div>
            </v-card>
          </v-col>
        </v-row>

        <!-- Блок с последними бронированиями -->
        <v-row justify="center">
          <v-col cols="12" md="8">
            <v-card class="recent-card">
              <v-card-title class="recent-title justify-center">Последние бронирования</v-card-title>
              <v-table class="recent-table">
                <thead>
                  <tr>
                    <th>Рейс</th>
                    <th>Место</th>
                    <th>Дата</th>
                    <th>Статус</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="ticket in recentTickets" :key="ticket.id">
                    <td>{{ ticket.flight_number }}</td>
                    <td>{{ ticket.seat_number }}</td>
                    <td>{{ formatDate(ticket.purchase_date) }}</td>
                    <td>
                      <v-chip :color="ticket.status === 'booked' ? 'primary' : 'grey'" dark>
                        {{ ticket.status }}
                      </v-chip>
                    </td>
                  </tr>
                </tbody>
              </v-table>
            </v-card>
          </v-col>
        </v-row>

        <!-- Блок с чек-инами -->
        <v-row justify="center">
          <v-col cols="12" md="8">
            <v-card class="recent-card">
              <v-card-title class="recent-title justify-center">Мои чекины</v-card-title>
              <v-table class="recent-table">
                <thead>
                  <tr>
                    <th>Рейс</th>
                    <th>Место</th>
                    <th>Дата чекина</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="checkin in checkins" :key="checkin.id">
                    <td>{{ checkin.flight_number }}</td>
                    <td>{{ checkin.seat_number }}</td>
                    <td>{{ formatDate(checkin.checkin_time) }}</td>
                  </tr>
                </tbody>
              </v-table>
              <div v-if="!checkins.length" class="text-center py-4" style="color:#1976d2;">У вас пока нет чекинов.</div>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
    <SiteFooter />

  </v-app>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'
import { useUserStore } from '@/stores/user'
import SiteFooter from '@/components/SiteFooter.vue'


const flightsCount = ref('-')
const checkinsCount = ref('-')
const bookingsCount = ref('-')
const maintenanceCount = ref('-')
const router = useRouter()
const userStore = useUserStore()

const userName = ref('')
const recentTickets = ref([])
const checkins = ref([]) // Список чек-инов

function formatDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
}

onMounted(async () => {
  try {
    const profileRes = await api.get('/api/profile')
    userName.value = profileRes.data.username

    const flightsRes = await api.get('/api/flights')
    const today = new Date().toISOString().slice(0, 10)
    flightsCount.value = flightsRes.data.filter(f =>
      f.departure_time && f.departure_time.slice(0, 10) === today
    ).length

    const ticketsRes = await api.get('/api/tickets')
    bookingsCount.value = ticketsRes.data.length
    recentTickets.value = ticketsRes.data.slice(-5).reverse()

    // Загружаем чекины для пользователя
    const checkinsRes = await api.get('/api/checkins')
    // Формируем удобный вид (flight_number, seat_number из связанного ticket)
    checkins.value = (checkinsRes.data || []).map(item => ({
      id: item.id,
      flight_number: item.flight_number || (item.ticket && item.ticket.flight_number),
      seat_number: item.seat_number || (item.ticket && item.ticket.seat_number),
      checkin_time: item.checkin_time,
    }))
    checkinsCount.value = checkins.value.length

    // Обслуживание (например, багажа)
    const luggagesRes = await api.get('/api/luggages')
    maintenanceCount.value = luggagesRes.data.length
  } catch (e) {
    flightsCount.value = checkinsCount.value = bookingsCount.value = maintenanceCount.value = '!'
  }
})

const cards = computed(() => [
  { title: "Рейсы сегодня", value: flightsCount.value },
  { title: "Чекины", value: checkinsCount.value },
  { title: "Бронирования", value: bookingsCount.value },
  { title: "Обслуживание", value: maintenanceCount.value },
])

function logout() {
  userStore.logout()
  router.push('/home')
}
</script>

<style scoped>
.main-app-bar {
  background: #07519a !important;
}
.airway-title {
  font-size: 1.3rem;
  font-weight: bold;
  letter-spacing: 1.5px;
}
.nav-link {
  font-size: 1rem;
  font-weight: 500;
  color: #fff !important;
  margin: 0 4px;
  text-transform: none;
}
.nav-link:hover {
  background: #1976d2 !important;
}
.dashboard-bg {
  background: linear-gradient(120deg, #07519a 70%, #e3f0fd 100%);
  min-height: 100vh;
  padding-top: 42px;
}
.welcome-block {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 2px 16px #07519a22;
  padding: 28px 32px 18px 32px;
  margin: 40px auto 24px auto;
  max-width: 600px;
  text-align: center;
}
.welcome-block h2 {
  color: #07519a;
  font-weight: 700;
  font-size: 2rem;
}
.welcome-block .user-name {
  color: #1976d2;
}
.divider-bar {
  width: 50px;
  height: 3px;
  margin: 12px auto;
  background: #1976d2;
  border-radius: 6px;
}
.stat-card {
  background: #e3f0fd;
  color: #07519a;
  border-radius: 16px;
  box-shadow: 0 2px 16px #07519a13;
  min-height: 112px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.stat-value {
  font-size: 2.2rem;
  font-weight: 700;
  color: #07519a;
  margin-bottom: 4px;
}
.stat-title {
  font-size: 1.08rem;
  font-weight: 500;
  color: #1976d2;
  letter-spacing: 0.6px;
}
.recent-card {
  margin-top: 2rem;
  border-radius: 16px;
  background: #fff;
  box-shadow: 0 2px 16px #1565c017;
}
.recent-title {
  font-weight: bold;
  color: #07519a;
  font-size: 1.3rem;
  letter-spacing: 1px;
}
.recent-table th,
.recent-table td {
  text-align: center;
  color: #222;
  font-size: 1rem;
}
.v-chip {
  font-weight: 500;
  font-size: 1rem;
  border-radius: 8px;
  letter-spacing: 0.2px;
}
</style>
