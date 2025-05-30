<template>
  <v-app>
    <v-main>
      <v-container class="fill-height d-flex align-center justify-center">
        <v-card width="400">
          <v-card-title class="justify-center">Sign in</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="submit">
              <v-text-field v-model="username" label="Username" required />
              <v-text-field v-model="password" label="Password" type="password" required />
              <v-btn type="submit" color="primary" class="mt-3" block>Login</v-btn>
            </v-form>
            <v-alert v-if="error" type="error" class="mt-3" density="compact">
              {{ error }}
            </v-alert>
          </v-card-text>
        </v-card>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/api'

const username = ref('')
const password = ref('')
const error = ref(null)
const router = useRouter()

async function submit() {
  error.value = null
  try {
    const res = await api.post('/auth/login', {
      username: username.value,
      password: password.value
    })
    // Сохраняем токен в localStorage
    localStorage.setItem('access_token', res.data.access_token)
    // После успешного входа переходим на Dashboard
    router.push('/dashboard')
  } catch (e) {
    error.value = 'Login failed. Check credentials.'
  }
}
</script>
