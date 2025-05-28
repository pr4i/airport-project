<template>
  <v-container>
    <h1>Profile</h1>
    <div v-if="user">
      <p><strong>Username:</strong> {{ user.username }}</p>
      <p><strong>Email:</strong> {{ user.email }}</p>
      <p><strong>Roles:</strong> {{ user.roles.join(', ') }}</p>
    </div>
  </v-container>
</template>

<script setup>
import { computed } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const user = computed(() => userStore.userInfo)
</script>
