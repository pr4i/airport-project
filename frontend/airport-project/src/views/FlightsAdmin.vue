<template>
  <v-card>
    <v-card-title>Управление рейсами</v-card-title>
    <v-btn color="primary" @click="openAddDialog" class="mb-2">Добавить рейс</v-btn>
    <v-table>
      <thead>
        <tr>
          <th>Номер рейса</th>
          <th>Откуда</th>
          <th>Куда</th>
          <th>Вылет</th>
          <th>Прилет</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="flight in flights" :key="flight.id">
          <td>{{ flight.flight_number }}</td>
          <td>{{ flight.origin }}</td>
          <td>{{ flight.destination }}</td>
          <td>{{ formatDate(flight.departure_time) }}</td>
          <td>{{ formatDate(flight.arrival_time) }}</td>
          <td>
            <v-btn size="small" @click="editFlight(flight)">Редактировать</v-btn>
            <v-btn size="small" color="error" @click="deleteFlight(flight.id)">Удалить</v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>

    <!-- Диалог добавления/редактирования -->
    <v-dialog v-model="dialog" max-width="500">
      <v-card>
        <v-card-title>{{ editingFlight ? 'Редактировать рейс' : 'Добавить рейс' }}</v-card-title>
        <v-card-text>
          <v-form>
            <v-text-field v-model="form.flight_number" label="Номер рейса" required />
            <v-text-field v-model="form.origin_id" label="ID аэропорта отправления" required />
            <v-text-field v-model="form.destination_id" label="ID аэропорта прибытия" required />
            <v-text-field v-model="form.airplane_id" label="ID самолёта" required />
            <v-text-field v-model="form.departure_time" label="Время вылета (YYYY-MM-DDTHH:mm)" required />
            <v-text-field v-model="form.arrival_time" label="Время прилёта (YYYY-MM-DDTHH:mm)" required />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn @click="dialog = false">Отмена</v-btn>
          <v-btn color="primary" @click="saveFlight">{{ editingFlight ? 'Сохранить' : 'Добавить' }}</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'

const flights = ref([])
const dialog = ref(false)
const editingFlight = ref(null)
const form = ref({
  flight_number: '',
  origin_id: '',
  destination_id: '',
  airplane_id: '',
  departure_time: '',
  arrival_time: '',
})

function formatDate(dt) {
  if (!dt) return ''
  return new Date(dt).toLocaleString()
}

async function loadFlights() {
  const res = await api.get('/api/flights')
  flights.value = res.data
}

function openAddDialog() {
  editingFlight.value = null
  form.value = {
    flight_number: '',
    origin_id: '',
    destination_id: '',
    airplane_id: '',
    departure_time: '',
    arrival_time: '',
  }
  dialog.value = true
}

function editFlight(flight) {
  editingFlight.value = flight.id
  form.value = {
    flight_number: flight.flight_number,
    origin_id: flight.origin_id || '',
    destination_id: flight.destination_id || '',
    airplane_id: flight.airplane_id || '',
    departure_time: flight.departure_time.slice(0, 16),
    arrival_time: flight.arrival_time.slice(0, 16),
  }
  dialog.value = true
}

async function saveFlight() {
  if (editingFlight.value) {
    // update
    await api.put(`/api/flights/${editingFlight.value}`, form.value)
  } else {
    // add
    await api.post('/api/flights', form.value)
  }
  dialog.value = false
  await loadFlights()
}

async function deleteFlight(id) {
  if (confirm('Удалить рейс?')) {
    await api.delete(`/api/flights/${id}`)
    await loadFlights()
  }
}

onMounted(loadFlights)
</script>
