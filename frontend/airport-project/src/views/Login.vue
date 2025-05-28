<template>
  <v-container>
    <v-form @submit.prevent="submit">
      <v-text-field v-model="username" label="Username" required />
      <v-text-field v-model="password" label="Password" type="password" required />
      <v-btn type="submit" color="primary">Login</v-btn>
    </v-form>
    <v-alert v-if="error" type="error" class="mt-3">{{ error }}</v-alert>
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
    router.push('/flights')
  } catch (e) {
    error.value = 'Login failed. Check credentials.'
  }
}
</script>
