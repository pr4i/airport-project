<template>
  <v-container>
    <v-toolbar flat>
      <v-toolbar-title>Flights</v-toolbar-title>
    </v-toolbar>

    <!-- Flights List -->
    <v-list>
      <v-list-item v-for="flight in flights" :key="flight.id">
        <v-list-item-content>
          <v-list-item-title>{{ flight.flight_number }}</v-list-item-title>
          <v-list-item-subtitle>
            {{ flight.origin }} → {{ flight.destination }}  
            ({{ new Date(flight.departure_time).toLocaleString() }})
          </v-list-item-subtitle>
        </v-list-item-content>

        <!-- Book Button -->
        <v-list-item-action>
          <v-btn color="primary" @click="bookTicket(flight.id)">Book</v-btn>
        </v-list-item-action>
      </v-list-item>
    </v-list>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'
import { useRouter } from 'vue-router'

const flights = ref([])
const router = useRouter()

// Получаем список рейсов при монтировании компонента
onMounted(async () => {
  const res = await api.get('/api/flights')
  flights.value = res.data
})

// Обработка бронирования билета
async function bookTicket(flightId) {
  try {
    await api.post('/api/tickets', {
      flight_id: flightId,
      seat_number: '1A' // временно выбираем место 1A
    })
    alert('Ticket booked!')
    router.push('/tickets') // Перенаправляем на страницу с билетами
  } catch (e) {
    alert('Booking failed')
  }
}
</script>

<style scoped>
/* Дополнительные стили для улучшения визуала */
.v-list-item {
  margin-bottom: 1rem;
}
</style>
