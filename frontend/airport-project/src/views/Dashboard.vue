<template>
  <v-app>
    <!-- Боковая панель -->
    <v-navigation-drawer app permanent class="sidebar">
      <v-list>
        <v-list-item class="sidebar-title">
          <v-icon class="mr-2 blue--text text--darken-3">mdi-airplane</v-icon>
          <span class="text-h6 font-weight-bold airline-title">AIRWAY</span>
        </v-list-item>
        <v-divider />
        <v-list-item prepend-icon="mdi-view-dashboard" class="sidebar-link">Dashboard</v-list-item>
        <v-list-item prepend-icon="mdi-ticket" class="sidebar-link">Bookings</v-list-item>
        <v-list-item prepend-icon="mdi-check" class="sidebar-link">Check-in</v-list-item>
        <v-list-item prepend-icon="mdi-briefcase" class="sidebar-link">Baggage</v-list-item>
        <v-list-item prepend-icon="mdi-cog" class="sidebar-link">Maintenance</v-list-item>
      </v-list>
    </v-navigation-drawer>

    <!-- Верхняя панель -->
    <v-app-bar app color="white" flat class="app-bar-elevated">
      <v-toolbar-title>
        <span class="welcome">Добро пожаловать, <b>{{ userName ? userName : 'User' }}</b>!</span>
      </v-toolbar-title>
      <v-spacer />
      <v-btn icon><v-icon color="blue darken-2">mdi-bell</v-icon></v-btn>
      <v-btn icon><v-icon color="blue darken-2">mdi-account</v-icon></v-btn>
    </v-app-bar>

    <v-main class="dashboard-bg">
      <v-container>
        <!-- Карточки статистики -->
        <v-row>
          <v-col cols="12" md="3" v-for="card in cards" :key="card.title">
            <v-card class="stat-card">
              <v-card-title>
                <span :class="card.color">{{ card.value }}</span>
              </v-card-title>
              <v-card-subtitle>{{ card.title }}</v-card-subtitle>
            </v-card>
          </v-col>
        </v-row>

        <!-- Recent Bookings по центру -->
        <v-row justify="center">
          <v-col cols="12" md="8">
            <v-card class="recent-card">
              <v-card-title class="justify-center recent-title">Recent Bookings</v-card-title>
              <v-table class="recent-table">
                <thead>
                  <tr>
                    <th>Flight</th>
                    <th>Seat</th>
                    <th>Date</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="ticket in recentTickets" :key="ticket.id">
                    <td>{{ ticket.flight_number }}</td>
                    <td>{{ ticket.seat_number }}</td>
                    <td>{{ formatDate(ticket.purchase_date) }}</td>
                    <td>
                      <v-chip :color="ticket.status === 'booked' ? 'blue darken-1' : 'grey'" dark>
                        {{ ticket.status }}
                      </v-chip>
                    </td>
                  </tr>
                </tbody>
              </v-table>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '@/api'

const flightsCount = ref('-')
const checkinsCount = ref('-')
const bookingsCount = ref('-')
const maintenanceCount = ref('-')

const userName = ref('')
const recentTickets = ref([])

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

    checkinsCount.value = '-'
    const luggagesRes = await api.get('/api/luggages')
    maintenanceCount.value = luggagesRes.data.length
  } catch (e) {
    flightsCount.value = checkinsCount.value = bookingsCount.value = maintenanceCount.value = '!'
  }
})

const cards = computed(() => [
  { title: "Today's Flights", value: flightsCount.value, color: 'primary-text' },
  { title: 'Check-ins', value: checkinsCount.value, color: 'primary-text' },
  { title: 'Bookings', value: bookingsCount.value, color: 'primary-text' },
  { title: 'Maintenance Tasks', value: maintenanceCount.value, color: 'primary-text' },
])
</script>

<style scoped>
/* Цвета */
.dashboard-bg {
  background: #f5f8fd;
  min-height: 100vh;
}
.sidebar {
  background: #1565c0 !important;
  color: #fff !important;
}
.sidebar-title {
  margin-bottom: 8px;
  color: #fff !important;
}
.airline-title {
  color: #fff;
  font-weight: bold;
  letter-spacing: 0.5px;
}
.sidebar-link {
  color: #cfd8dc !important;
  font-weight: 500;
}
.sidebar-link:hover {
  background: #1976d2 !important;
  color: #fff !important;
}

.app-bar-elevated {
  box-shadow: 0 2px 8px 0 #1565c022;
}

.stat-card {
  background: #fff;
  color: #1565c0;
  border-radius: 18px;
  box-shadow: 0 2px 16px #1565c015;
  min-height: 120px;
  text-align: center;
}
.stat-card .v-card-title {
  font-size: 2.4rem;
  font-weight: bold;
  color: #1565c0;
}
.stat-card .v-card-subtitle {
  color: #444;
  font-size: 1rem;
  margin-top: -10px;
}
.primary-text {
  color: #1565c0 !important;
}

.recent-card {
  margin-top: 2rem;
  border-radius: 16px;
  background: #fff;
  box-shadow: 0 2px 16px #1565c017;
}

.recent-title {
  font-weight: bold;
  color: #1565c0;
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
.welcome {
  color: #1565c0;
  font-size: 1.15rem;
  font-weight: 500;
  letter-spacing: 0.3px;
}
</style>
