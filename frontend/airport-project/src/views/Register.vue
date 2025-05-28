<template>
  <v-container>
    <v-form @submit.prevent="submit">
      <v-text-field v-model="username" label="Username" required />
      <v-text-field v-model="email" label="Email" required />
      <v-text-field v-model="password" label="Password" type="password" required />
      <v-btn type="submit" color="primary">Register</v-btn>
    </v-form>
    <v-alert v-if="error" type="error" class="mt-3">{{ error }}</v-alert>
    <v-alert v-if="success" type="success" class="mt-3">Registration successful! Please login.</v-alert>
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
