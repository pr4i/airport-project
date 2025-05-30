<template>
  <v-container
    class="login-background"
    fluid
    style="min-height: 100vh; display: flex; align-items: center; justify-content: center;"
  >
    <v-card class="login-card">
      <v-card-title class="headline text-center mb-4">Регистрация</v-card-title>
      <v-form @submit.prevent="submit">
        <v-text-field
          v-model="username"
          label="Логин"
          placeholder="Придумайте логин"
          prepend-inner-icon="mdi-account"
          variant="outlined"
          class="mb-3"
          density="comfortable"
          required
        />
        <v-text-field
          v-model="email"
          label="Email"
          placeholder="example@email.com"
          prepend-inner-icon="mdi-email"
          variant="outlined"
          class="mb-3"
          density="comfortable"
          required
        />
        <v-text-field
          v-model="password"
          label="Пароль"
          placeholder="Придумайте пароль"
          type="password"
          prepend-inner-icon="mdi-lock"
          variant="outlined"
          class="mb-2"
          density="comfortable"
          required
        />
        <v-btn
          type="submit"
          color="primary"
          block
          class="login-btn"
          height="56"
        >
          Зарегистрироваться
        </v-btn>
        <v-btn
          variant="text"
          block
          class="mt-2"
          @click="router.push('/login')"
        >
          Уже есть аккаунт? Войти
        </v-btn>
      </v-form>
      <v-alert v-if="error" type="error" class="mt-3">{{ error }}</v-alert>
      <v-alert v-if="success" type="success" class="mt-3">Регистрация успешна! Пожалуйста, войдите.</v-alert>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/api'
import { useRouter } from 'vue-router'

const username = ref('')
const email = ref('')
const password = ref('')
const error = ref(null)
const success = ref(false)
const router = useRouter()

async function submit() {
  error.value = null
  success.value = false
  try {
    await api.post('/auth/register', {
      username: username.value,
      email: email.value,
      password: password.value,
    })
    success.value = true
    setTimeout(() => router.push('/login'), 2000)
  } catch (e) {
    error.value = e.response?.data?.msg || 'Registration failed'
  }
}
</script>


<style scoped>
.login-background {
  background: #07519a !important;
}
.login-card {
  max-width: 450px;
  width: 100%;
  padding: 36px 32px 32px 32px;
  border-radius: 14px;
  box-shadow: 0 10px 36px rgba(7, 81, 154, 0.08);
}
.login-btn {
  font-size: 20px;
  font-weight: 600;
  background: #07519a;
  color: #fff;
}
.forgot-link {
  color: #216ad7;
  font-size: 15px;
  text-decoration: none;
}
.headline {
  font-size: 32px;
  font-weight: 500;
}
</style>

