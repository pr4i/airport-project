<template>
  <v-app>
    <!-- Верхний бар, как в Home.vue -->
    <v-app-bar app flat color="#07519a" dark>
      <v-toolbar-title>
        <v-icon left>mdi-airplane</v-icon>
        AIRWAY
      </v-toolbar-title>
      <v-spacer />
      <v-btn text @click="router.push('/home')">Главная</v-btn>
      <v-btn text @click="router.push('/flights')">Рейсы</v-btn>
      <v-btn text>Онлайн-табло</v-btn>
      <v-btn text @click="router.push('/dashboard')">Личный кабинет</v-btn>
      <v-btn icon><v-icon>mdi-account-circle</v-icon></v-btn>
    </v-app-bar>

    <v-main class="main-section">
      <v-container>
        <v-card class="flights-card">
          <v-card-title class="flights-title">Доступные рейсы</v-card-title>
          <v-table class="flights-table">
            <thead>
              <tr>
                <th>Номер рейса</th>
                <th>Откуда</th>
                <th>Куда</th>
                <th>Дата и время</th>
                <th>Самолёт</th>
                <th>Действие</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="flight in flights" :key="flight.id">
                <td>{{ flight.flight_number }}</td>
                <td>{{ flight.origin }}</td>
                <td>{{ flight.destination }}</td>
                <td>{{ formatDate(flight.departure_time) }}</td>
                <td>{{ flight.aircraft || '-' }}</td>
                <td>
                  <v-btn color="primary" @click="openDialog(flight)">Забронировать</v-btn>
                </td>
              </tr>
            </tbody>
          </v-table>
        </v-card>
      </v-container>

      <!-- Диалог бронирования -->
      <v-dialog v-model="dialog" max-width="400">
        <v-card>
          <v-card-title class="headline">Бронирование билета</v-card-title>
          <v-card-text>
            <div class="mb-2">
              <strong>Рейс:</strong> {{ selectedFlight?.flight_number }}<br>
              <strong>Маршрут:</strong> {{ selectedFlight?.origin }} → {{ selectedFlight?.destination }}<br>
              <strong>Дата:</strong> {{ formatDate(selectedFlight?.departure_time) }}
            </div>
            <v-select
              v-model="form.seatClass"
              :items="['Эконом', 'Бизнес']"
              label="Класс"
              required
              class="mb-3"
            />
            <v-text-field
              v-model="form.seatNumber"
              label="Место (например, 7A)"
              required
              class="mb-3"
            />
          </v-card-text>
          <v-card-actions>
            <v-btn variant="text" @click="dialog = false">Отмена</v-btn>
            <v-btn color="primary" @click="bookTicket" :loading="loading">Забронировать</v-btn>
          </v-card-actions>
          <v-alert v-if="error" type="error" class="mt-2">{{ error }}</v-alert>
          <v-alert v-if="success" type="success" class="mt-2">Бронирование успешно!</v-alert>
        </v-card>
      </v-dialog>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'
import { useRouter } from 'vue-router'

const router = useRouter()
const flights = ref([])
const dialog = ref(false)
const selectedFlight = ref(null)
const loading = ref(false)
const error = ref('')
const success = ref(false)

const form = ref({
  seatClass: 'Эконом',
  seatNumber: '',
})

onMounted(async () => {
  try {
    const res = await api.get('/api/flights')
    flights.value = res.data
  } catch (e) {
    // обработка ошибки
  }
})

function formatDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
}

function openDialog(flight) {
  selectedFlight.value = flight
  form.value = { seatClass: 'Эконом', seatNumber: '' }
  error.value = ''
  success.value = false
  dialog.value = true
}

async function bookTicket() {
  loading.value = true
  error.value = ''
  success.value = false
  try {
    await api.post('/api/tickets', {
      flight_id: selectedFlight.value.id,
      seat_number: form.value.seatNumber,
      seat_class: form.value.seatClass,
    })
    success.value = true
    setTimeout(() => { dialog.value = false }, 1500)
  } catch (e) {
    error.value = e.response?.data?.msg || 'Ошибка бронирования'
  }
  loading.value = false
}
</script>

<style scoped>
.main-section {
  background: linear-gradient(120deg, #07519a 70%, #e3f0fd 100%);
  min-height: 100vh;
  padding-top: 40px;
  padding-bottom: 40px;
}
.flights-card {
  margin: 2rem auto;
  border-radius: 18px;
  box-shadow: 0 2px 16px #1565c017;
  background: #fff;
  max-width: 1200px;
  padding-bottom: 20px;
}
.flights-title {
  font-size: 2rem;
  color: #1565c0;
  font-weight: bold;
  text-align: center;
  letter-spacing: 1px;
  margin-bottom: 10px;
}
.flights-table th,
.flights-table td {
  text-align: center;
  font-size: 1rem;
  padding: 12px 6px;
}
.flights-table th {
  color: #1565c0;
  background: #e3f0fd;
}
.v-btn {
  font-weight: 600;
}
.v-dialog .v-card-title {
  color: #1565c0;
  font-weight: 600;
}
.v-dialog .v-btn {
  min-width: 110px;
}
</style>
