<template>
  <form @submit.prevent="submit">
    <input v-model="username" data-test="username" />
    <input v-model="password" type="password" data-test="password" />
    <button type="submit" data-test="submit">Войти</button>
    <div v-if="errorMessage" data-test="error">{{ errorMessage }}</div>
  </form>
</template>

<script setup>
import { ref } from 'vue'
const username = ref('')
const password = ref('')
const errorMessage = ref('')

function submit() {
  // Явно показываем ошибку при пустых полях
  if (!username.value || !password.value) {
    errorMessage.value = 'Неверный логин или пароль'
  } else {
    errorMessage.value = ''
  }
}
</script>
