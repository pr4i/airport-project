<template>
  <v-container>
    <v-toolbar flat>
      <v-toolbar-title>My Tickets</v-toolbar-title>
    </v-toolbar>
    <v-list>
      <v-list-item v-for="ticket in tickets" :key="ticket.id">
        <v-list-item-content>
          <v-list-item-title>Flight: {{ ticket.flight_number }}</v-list-item-title>
          <v-list-item-subtitle>Seat: {{ ticket.seat_number }} — Status: {{ ticket.status }}</v-list-item-subtitle>
        </v-list-item-content>
        <v-list-item-action>
          <v-btn icon @click="cancelTicket(ticket.id)">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </v-list-item-action>
      </v-list-item>
    </v-list>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'

const tickets = ref([])

async function loadTickets() {
  const res = await api.get('/api/tickets')
  tickets.value = res.data
}

async function cancelTicket(id) {
  await api.delete(`/api/tickets/${id}`)
  await loadTickets()
}

onMounted(loadTickets)
</script>
