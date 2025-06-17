<template>
  <v-app>
    <!-- Навигационное меню -->
    <v-app-bar app color="#07519a" dark style="box-shadow: 0 2px 6px rgba(0,0,0,0.3); border-bottom: 1px solid white;">
      <v-toolbar-title>
        <v-icon left>mdi-airplane</v-icon>
        AIRWAY
      </v-toolbar-title>
      <v-spacer />
      <v-btn v-if="userStore.isAdmin" text @click="router.push('/admin')">Админ-панель</v-btn>
      <v-btn text @click="router.push('/')">Главная страница</v-btn>
      <v-btn text @click="router.push('/onlineboard')">Онлайн-табло</v-btn>
      <v-btn text @click="router.push('/flights')">Бронирование</v-btn>
      <v-btn text @click="goToLK">Личный кабинет</v-btn>
      <v-btn v-if="!isAuth" icon @click="router.push('/login')" title="Войти">
        <v-icon>mdi-account-circle</v-icon>
      </v-btn>
      <v-btn v-else text @click="logout">
        <v-icon left>mdi-logout</v-icon>
        Выйти
      </v-btn>
    </v-app-bar>

    <v-main class="checkin-bg">
      <v-container class="checkin-page" style="max-width: 480px;">
        <v-card class="pa-6 checkin-card" elevation="10">
          <v-card-title class="headline mb-2 checkin-title">Регистрация на рейс</v-card-title>
          <v-form @submit.prevent="submitCheckin">
            <v-text-field
              v-model="form.fullName"
              label="ФИО"
              required
              class="input"
            />
            <v-text-field
              v-model="form.passport"
              label="Паспортные данные"
              required
              class="input"
            />
            <v-select
              v-model="form.ticket_id"
              :items="tickets"
              label="Билет (Рейс и место)"
              item-title="label"
              item-value="id"
              required
              class="input"
            />
            <v-divider class="my-4" />
            <div v-for="(luggage, idx) in form.luggage" :key="idx" class="mb-2 luggage-row">
              <v-text-field
                v-model="luggage.description"
                label="Описание багажа"
                class="luggage-input"
              />
              <v-text-field
                v-model="luggage.weight"
                label="Вес (кг)"
                type="number"
                min="0"
                style="max-width: 100px"
              />
              <v-btn icon color="error" @click="removeLuggage(idx)" v-if="form.luggage.length > 1">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </div>
            <v-btn text color="primary" class="mb-4 luggage-btn" @click.prevent="addLuggage">
              <v-icon left>mdi-plus</v-icon>Добавить багаж
            </v-btn>
            <v-btn type="submit" color="primary" large class="mt-4 checkin-btn" :loading="loading">
              Зарегистрироваться на рейс
            </v-btn>
          </v-form>
          <v-alert v-if="error" type="error" class="mt-3 error-alert">{{ error }}</v-alert>
          <v-alert v-if="success" type="success" class="mt-3">Регистрация прошла успешно!</v-alert>
        </v-card>
      </v-container>
    </v-main>
    <SiteFooter />
  </v-app>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useUserStore } from '@/stores/user'
import api from '@/api'
import SiteFooter from '@/components/SiteFooter.vue'


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

const form = ref({
  fullName: '',
  passport: '',
  ticket_id: null,
  luggage: [{ description: '', weight: '' }],
})
const tickets = ref([])
const loading = ref(false)
const error = ref('')
const success = ref(false)

function addLuggage() {
  form.value.luggage.push({ description: '', weight: '' })
}
function removeLuggage(idx) {
  form.value.luggage.splice(idx, 1)
}

onMounted(async () => {
  const resp = await api.get('/api/tickets')
  tickets.value = resp.data.map(t => ({
    id: t.id,
    label: `${t.flight_number}, место ${t.seat_number}`,
  }))
})

async function submitCheckin() {
  loading.value = true
  error.value = ''
  success.value = false
  try {
    await api.post('/api/checkins', {
      ticket_id: form.value.ticket_id,
      full_name: form.value.fullName,
      passport: form.value.passport,
    })
    for (const luggage of form.value.luggage) {
      if (luggage.weight && luggage.description) {
        await api.post('/api/luggages', {
          ticket_id: form.value.ticket_id,
          weight: luggage.weight,
          description: luggage.description,
        })
      }
    }
    success.value = true
  } catch (e) {
    error.value = e.response?.data?.msg || e.response?.data?.error || 'Ошибка регистрации'
  }
  loading.value = false
}
</script>

<style scoped>
.checkin-bg {
  min-height: 100vh;
  background: linear-gradient(120deg, #07519a 0%, #e3f0fd 100%);
  padding-top: 80px;
  display: flex;
  align-items: flex-start;
  justify-content: center;
}
.checkin-card {
  border-radius: 20px;
  box-shadow: 0 8px 36px rgba(20,70,160,0.16), 0 1.5px 4px rgba(53,126,199,0.12);
}
.checkin-title {
  font-weight: 700;
  color: #07519a;
  letter-spacing: 1px;
}
.input {
  background: #f5f8fc;
  border-radius: 10px;
}
.luggage-row {
  display: flex;
  gap: 10px;
  align-items: center;
}
.luggage-btn {
  font-weight: 600;
  font-size: 1rem;
}
.checkin-btn {
  font-size: 1.1rem;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(53,126,199,0.09);
}
.error-alert {
  background: #b71c1c;
  color: #fff;
  font-weight: 600;
  border-radius: 8px;
}
</style>
