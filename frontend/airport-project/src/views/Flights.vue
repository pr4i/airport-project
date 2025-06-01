<template>
  <v-app>
    <!-- Навигационный бар -->
    <v-app-bar app flat color="#07519a" dark>
      <v-toolbar-title>
        <v-icon left>mdi-airplane</v-icon>
        AIRWAY
      </v-toolbar-title>
      <v-spacer />
      <v-btn v-if="userStore?.isAdmin" text @click="router.push('/admin')">Админ-панель</v-btn>
      <v-btn text @click="router.push('/onlineboard')">Онлайн-табло</v-btn>
      <v-btn text @click="router.push('/flights')">Бронирование</v-btn>
      <v-btn text @click="goToLK">Личный кабинет</v-btn>
      <v-btn v-if="!isAuth" icon @click="router.push('/login')" title="Войти">
        <v-icon>mdi-account-circle</v-icon>
      </v-btn>
      <v-btn v-else icon @click="logout" title="Выйти">
        <v-icon>mdi-logout</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main class="main-bg">
      <v-container class="py-0">

        <!-- Поисковая панель на белой карточке с автокомплитами -->
        <v-row align="center" justify="center" no-gutters>
          <v-col cols="10">
            <div class="search-panel">
              <v-row>
                <v-col cols="4">
                  <v-autocomplete
                    v-model="fromCity"
                    :items="cities"
                    label="Город вылета"
                    variant="outlined"
                    class="white-input"
                    dense
                    hide-details
                    clearable
                  />
                </v-col>
                <v-col cols="4">
                  <v-autocomplete
                    v-model="toCity"
                    :items="cities"
                    label="Город прибытия"
                    variant="outlined"
                    class="white-input"
                    dense
                    hide-details
                    clearable
                  />
                </v-col>
                <v-col cols="2">
                  <v-text-field
                    v-model="date"
                    label="Дата"
                    variant="outlined"
                    class="white-input"
                    dense
                    type="date"
                    hide-details
                  />
                </v-col>
                <v-col cols="2">
                  <v-btn color="#3982e4" class="search-btn" @click="fetchFlights" block>НАЙТИ</v-btn>
                </v-col>
              </v-row>
            </div>
          </v-col>
        </v-row>

        <!-- Заголовки таблицы рейсов -->
        <v-row class="flight-table-header mb-2 px-1 white-table-head">
          <v-col md="2">ВЫЛЕТ</v-col>
          <v-col md="2">ПРИЛЕТ</v-col>
          <v-col md="2">ПЕРЕВОЗЧИК</v-col>
          <v-col md="2">РЕЙС</v-col>
          <v-col md="2">В ПУТИ</v-col>
          <v-col md="2" class="text-right">ЛУЧШАЯ ЦЕНА</v-col>
        </v-row>

        <!-- Список рейсов -->
        <div v-if="flights.length">
          <v-card
            v-for="flight in flights"
            :key="flight.id"
            class="flight-card mb-3"
          >
            <v-row>
              <v-col md="2">
                <span class="flight-time">{{ formatTime(flight.departure_time) }}</span><br>
                <span class="flight-airport">{{ flight.origin }}</span>
              </v-col>
              <v-col md="2">
                <span class="flight-time">{{ formatTime(flight.arrival_time) }}</span><br>
                <span class="flight-airport">{{ flight.destination }}</span>
              </v-col>
              <v-col md="2">
                <span class="flight-carrier">Аэрофлот</span>
              </v-col>
              <v-col md="2">
                <b>{{ flight.flight_number }}</b><br>
                <span class="plane-type">{{ flight.airplane }}</span>
              </v-col>
              <v-col md="2">
                <span>{{ calcDuration(flight.departure_time, flight.arrival_time) }}</span>
              </v-col>
              <v-col md="2" class="text-right d-flex flex-column align-end justify-center">
                <span class="flight-price"><b>от {{ flight.price }} ₽</b></span>
                <v-btn color="#1976d2" variant="outlined" @click="openDialog(flight)" style="min-width:140px;">ВЫБРАТЬ РЕЙС</v-btn>
              </v-col>
            </v-row>
          </v-card>
        </div>
        <div v-else class="text-center pa-8" style="font-size:1.12rem; color:#1976d2;">
          Рейсы на эту дату не найдены.
        </div>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import api from '@/api'

const router = useRouter()
const userStore = useUserStore()
const isAuth = computed(() => !!userStore.token)
const fromCity = ref('')
const toCity = ref('')
const date = ref('')
const flights = ref([])
const airports = ref([])

// Готовый список городов для автокомплита
const cities = computed(() => [...new Set(airports.value.map(a => a.city))])

onMounted(async () => {
  try {
    const res = await api.get('/api/airports')
    airports.value = res.data
  } catch (e) { }
})

async function fetchFlights() {
  if (!fromCity.value || !toCity.value) {
    flights.value = []
    return
  }
  try {
    const params = {
      origin: fromCity.value,
      destination: toCity.value
    }
    if (date.value) params.date = date.value
    const res = await api.get('/api/flights', { params })
    flights.value = res.data
  } catch (e) {
    flights.value = []
  }
}

function formatTime(dt) {
  if (!dt) return ''
  return new Date(dt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
function calcDuration(start, end) {
  if (!start || !end) return ''
  const t1 = new Date(start)
  const t2 = new Date(end)
  const min = Math.floor((t2 - t1) / (1000 * 60))
  const h = Math.floor(min / 60)
  const m = min % 60
  return `${h} ч. ${m > 0 ? m + ' мин.' : ''}`.trim()
}
function openDialog(flight) {
  // твоя логика бронирования
}
function goToLK() {
  if (isAuth.value) {
    router.push('/dashboard')
  } else {
    router.push('/login')
  }
}
function logout() {
  userStore.logout()
  router.push('/home')
}
</script>

<style scoped>
.main-bg {
  background: linear-gradient(120deg, #07519a 70%, #e3f0fd 100%);
  min-height: 100vh;
  padding-top: 40px;
}
.search-panel {
  background: #fff;
  border-radius: 20px;
  box-shadow: 0 4px 22px 0 #1d35571a;
  padding: 24px 30px 10px 30px;
  margin-top: 36px;
  margin-bottom: 34px;
}
.white-input .v-input__control {
  background: #fff !important;
  border-radius: 10px;
  box-shadow: 0 2px 10px #0001;
}
.white-table-head {
  background: #fff !important;
  color: #07519a !important;
  border-radius: 18px;
  box-shadow: 0 2px 12px 0 #1d355715;
  font-size: 1.09rem;
  font-weight: 700;
  margin-bottom: 14px;
}
.flight-table-header > .v-col {
  display: flex;
  align-items: center;
  justify-content: start;
}
.flight-card {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 4px 22px 0 #1d355715;
  padding: 15px 16px 10px 18px;
}
.flight-time {
  font-size: 1.22rem;
  font-weight: bold;
  color: #222;
  line-height: 1.1;
}
.flight-airport {
  font-size: 1.04rem;
  color: #1976d2;
}
.flight-carrier, .plane-type {
  font-size: 1.08rem;
  color: #333;
}
.flight-price {
  font-size: 1.14rem;
  color: #222;
  margin-bottom: 8px;
}
.search-btn {
  font-weight: 700;
  font-size: 1.06rem;
  border-radius: 10px;
  height: 42px;
}
</style>
