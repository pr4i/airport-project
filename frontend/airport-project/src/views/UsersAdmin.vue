<template>
  <v-card>
    <v-card-title>Пользователи</v-card-title>
    <v-table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Username</th>
          <th>Email</th>
          <th>Роль</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="u in users" :key="u.id">
          <td>{{ u.id }}</td>
          <td>{{ u.username }}</td>
          <td>{{ u.email }}</td>
          <td>
            <v-select
              :items="roles"
              v-model="u.roles[0]"
              @change="updateRole(u)"
              dense
              style="width:110px;"
            />
          </td>
          <td>
            <v-btn size="small" color="error" @click="deleteUser(u.id)" :disabled="isMe(u)">🗑</v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>
  </v-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'

// Возможные роли
const roles = ['user', 'admin']
const users = ref([])
const myId = ref(null)

async function loadUsers() {
  const res = await api.get('/api/users')
  users.value = res.data
  // Получим свой id для защиты от самоуничтожения :)
  const profile = await api.get('/api/profile')
  myId.value = profile.data.id
}

function isMe(u) {
  return myId.value === u.id
}

async function updateRole(user) {
  await api.put(`/api/users/${user.id}`, { roles: [user.roles[0]] })
  // Можно обновить список, но не обязательно — роль уже изменена локально
}

async function deleteUser(id) {
  if (confirm('Удалить пользователя?')) {
    await api.delete(`/api/users/${id}`)
    await loadUsers()
  }
}

onMounted(loadUsers)
</script>
