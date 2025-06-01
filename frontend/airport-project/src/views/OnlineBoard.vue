<template>
  <v-app>
    <!-- Навигационный верхний бар -->
    <v-app-bar app flat color="#07519a" dark>
      <v-toolbar-title>
        <v-icon left>mdi-airplane</v-icon>
        AIRWAY
      </v-toolbar-title>
      <v-spacer />
      <v-btn v-if="userStore.isAdmin" text @click="router.push('/admin')">Админ-панель</v-btn>
      <v-btn text @click="router.push('/onlineboard')">Онлайн-табло</v-btn>
      <v-btn text @click="router.push('/flights')">Бронирование</v-btn>
      <v-btn text @click="goToLK">Личный кабинет</v-btn>
      <v-btn
        v-if="!isAuth"
        icon
        @click="router.push('/login')"
        title="Войти"
      >
        <v-icon>mdi-account-circle</v-icon>
      </v-btn>
      <v-btn
        v-else
        icon
        @click="logout"
        title="Выйти"
      >
        <v-icon>mdi-logout</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main class="onlineboard-bg">
      <v-container>
        <v-row justify="center">
          <v-col cols="12" md="12" lg="10">
            <div class="board-card">
              <h2 class="text-center mb-4 onlineboard-title">
                <v-icon color="#07519a" class="mr-2">mdi-airplane-takeoff</v-icon>
                Онлайн-табло вылетов
              </h2>
              <v-text-field
                v-model="search"
                label="Поиск по номеру рейса, городу или статусу"
                prepend-inner-icon="mdi-magnify"
                variant="outlined"
                dense
                class="search-field mb-4"
                hide-details
                clearable
              />
              <div class="table-scroll">
                <v-table class="flight-table">
                  <thead>
                    <tr>
                      <th>Время</th>
                      <th>Направление</th>
                      <th>Рейс</th>
                      <th>Терминал</th>
                      <th>Статус</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="f in filteredFlights"
                      :key="f.id"
                      class="flight-row"
                      :class="{ 'selected-row': f.status === 'посадка' }"
                    >
                      <td>{{ formatTime(f.departure_time) }}</td>
                      <td>{{ f.destination }}</td>
                      <td><b>{{ f.flight_number }}</b></td>
                      <td>{{ f.terminal || '—' }}</td>
                      <td>
                        <span
                          :class="{
                            'on-time': f.status === 'отправлен',
                            'delayed': f.status === 'задержан',
                            'boarding': f.status === 'посадка',
                            'in-flight': f.status === 'в полете'
                          }"
                        >{{ f.status }}</span>
                      </td>
                    </tr>
                    <tr v-if="!filteredFlights.length">
                      <td colspan="5" class="no-flights">Рейсы не найдены</td>
                    </tr>
                  </tbody>
                </v-table>
              </div>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useUserStore } from '@/stores/user'
import api from '@/api'

const router = useRouter()
const userStore = useUserStore()
const { token } = storeToRefs(userStore)
const isAuth = computed(() => !!token.value)

function goToLK() {
  if (isAuth.value) router.push('/dashboard')
  else router.push('/login')
}
function logout() {
  userStore.logout()
  router.push('/home')
}

const flights = ref([])
const search = ref('')

onMounted(async () => {
  const res = await api.get('/api/flights')
  flights.value = res.data
})

const filteredFlights = computed(() => {
  const q = search.value.trim().toLowerCase()
  if (!q) return flights.value
  return flights.value.filter(f =>
    (f.destination || '').toLowerCase().includes(q) ||
    (f.flight_number || '').toLowerCase().includes(q) ||
    (f.status || '').toLowerCase().includes(q)
  )
})

function formatTime(dt) {
  if (!dt) return ''
  return new Date(dt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
.onlineboard-bg {
  background: linear-gradient(120deg, #07519a 65%, #e3f0fd 100%);
  min-height: 100vh;
  padding-top: 40px;
}
.board-card {
  background: #fff;
  box-shadow: 0 8px 32px 0 #0b30631a;
  padding: 38px 40px 22px 40px;
  margin-top: 36px;
  margin-bottom: 32px;
}
.onlineboard-title {
  color: #07519a;
  font-weight: 700;
  font-size: 2rem;
  letter-spacing: 1.2px;
  margin-bottom: 26px;
}
.search-field .v-input__control {
  background: #e3f0fd !important;
  border-radius: 10px;
}
.table-scroll {
  max-height: 520px;
  overflow-y: auto;
}
.flight-table th {
  color: #07519a;
  font-size: 1.13rem;
  background: #e3f0fd;
  font-weight: 700;
  border: none;
  letter-spacing: 0.5px;
}
.flight-table td {
  background: #fff;
  font-size: 1.14rem;
  padding: 14px 10px;
  border-bottom: 1.5px solid #e3f0fd;
  transition: background 0.2s;
}
.flight-row.selected-row td {
  background: #e6f1fd !important;
}
.no-flights {
  color: #1976d2;
  text-align: center;
  font-size: 1.16rem;
  padding: 24px;
}

.on-time    { color: #388e3c; font-weight: 700; }
.delayed    { color: #d32f2f; font-weight: 700; }
.boarding   { color: #ffa726; font-weight: 700; }
.in-flight  { color: #1976d2; font-weight: 700; }

@media (max-width: 900px) {
  .board-card { padding: 14px 4px 8px 4px; }
  .flight-table th, .flight-table td { font-size: 1rem; }
}
</style>
