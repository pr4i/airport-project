<template>
  <v-card>
    <v-card-title>
      Управление билетами
      <v-spacer />
      <v-btn color="primary" @click="openAddDialog">Добавить билет</v-btn>
    </v-card-title>

    <v-table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Пассажир</th>
          <th>Рейс</th>
          <th>Класс</th>
          <th>Место</th>
          <th>Дата</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="ticket in tickets" :key="ticket.id">
          <td>{{ ticket.id }}</td>
          <td>{{ ticket.passenger_name }}</td>
          <td>{{ ticket.flight_number }}</td>
          <td>{{ ticket.seat_class }}</td>
          <td>{{ ticket.seat_number }}</td>
          <td>{{ formatDate(ticket.date) }}</td>
          <td>
            <v-btn size="small" color="primary" @click="editTicket(ticket)">Редактировать</v-btn>
            <v-btn size="small" color="error" @click="deleteTicket(ticket.id)">Удалить</v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>

    <!-- Диалог создания/редактирования билета -->
    <v-dialog v-model="dialog" max-width="500">
      <v-card>
        <v-card-title>
          {{ editMode ? 'Редактировать билет' : 'Добавить билет' }}
        </v-card-title>
        <v-card-text>
          <v-form ref="form" @submit.prevent="saveTicket">
            <v-text-field v-model="currentTicket.passenger_name" label="Пассажир" required />
            <v-text-field v-model="currentTicket.flight_number" label="Рейс" required />
            <v-text-field v-model="currentTicket.seat_class" label="Класс" required />
            <v-text-field v-model="currentTicket.seat_number" label="Место" required />
            <v-text-field v-model="currentTicket.date" label="Дата" required />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn @click="dialog = false">Отмена</v-btn>
          <v-btn color="primary" @click="saveTicket">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'

const tickets = ref([])
const dialog = ref(false)
const editMode = ref(false)
const currentTicket = ref({
  id: null,
  passenger_name: '',
  flight_number: '',
  seat_class: '',
  seat_number: '',
  date: ''
})

function formatDate(dateStr) {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
}

async function loadTickets() {
  const res = await api.get('/api/tickets')
  tickets.value = res.data
}

function openAddDialog() {
  editMode.value = false
  currentTicket.value = {
    id: null,
    passenger_name: '',
    flight_number: '',
    seat_class: '',
    seat_number: '',
    date: ''
  }
  dialog.value = true
}

function editTicket(ticket) {
  editMode.value = true
  currentTicket.value = { ...ticket }
  dialog.value = true
}

async function saveTicket() {
  if (editMode.value) {
    // update
    await api.put(`/api/tickets/${currentTicket.value.id}`, currentTicket.value)
  } else {
    // create
    await api.post('/api/tickets', currentTicket.value)
  }
  dialog.value = false
  await loadTickets()
}

async function deleteTicket(id) {
  if (confirm('Удалить билет?')) {
    await api.delete(`/api/tickets/${id}`)
    await loadTickets()
  }
}

onMounted(loadTickets)
</script>
