<template>
  <v-container
    class="login-background"
    fluid
    style="min-height: 100vh; display: flex; align-items: center; justify-content: center;"
  >
    <v-card class="login-card">
      <v-card-title class="headline text-center mb-4">Войти в личный кабинет</v-card-title>
      <v-form @submit.prevent="submit">
        <v-text-field
          v-model="username"
          label="Логин"
          placeholder="Введите ваш логин"
          prepend-inner-icon="mdi-account"
          variant="outlined"
          class="mb-3"
          density="comfortable"
          required
        />
        <v-text-field
          v-model="password"
          label="Пароль"
          placeholder="Пароль"
          type="password"
          prepend-inner-icon="mdi-lock"
          variant="outlined"
          density="comfortable"
          class="mb-2"
          required
        />
        <div class="mb-2">
          <a href="#" class="forgot-link">Забыли пароль?</a>
        </div>
        <v-btn
          type="submit"
          color="primary"
          block
          class="login-btn"
          height="56"
        >
          Войти
        </v-btn>
        <v-btn
          variant="text"
          block
          class="mt-2"
          @click="router.push('/register')"
        >
          Зарегистрироваться
        </v-btn>
      </v-form>
      <v-alert v-if="error" type="error" class="mt-3">{{ error }}</v-alert>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const username = ref('')
const password = ref('')
const error = ref(null)
const router = useRouter()
const userStore = useUserStore()

async function submit() {
  error.value = null
  try {
    await userStore.login(username.value, password.value)
    router.push('/dashboard') // или '/flights'
  } catch (e) {
    error.value = 'Неверный логин или пароль'
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
  font-size: 30px;
  font-weight: 500;
}
</style>
