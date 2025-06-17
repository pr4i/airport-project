<template>
  <v-card class="pa-4 admin-section-card" elevation="4">
    <v-card-title class="text-h6 mb-4">Управление самолётами</v-card-title>

    <v-btn color="primary" @click="openDialog" class="mb-4">
      <v-icon left>mdi-plus</v-icon>Добавить самолёт
    </v-btn>

    <v-table class="elevation-1">
      <thead class="admin-table-head">
        <tr>
          <th>ID</th>
          <th>Модель</th>
          <th>Кол-во мест</th>
          <th class="text-center">Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="a in airplanes" :key="a.id">
          <td>{{ a.id }}</td>
          <td>{{ a.model }}</td>
          <td>{{ a.seats_count }}</td>
        <td class="text-center">
          <v-btn icon size="small" color="primary" @click="editAirplane(a)">
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
          <v-btn icon size="small" color="error" @click="deleteAirplane(a.id)">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </td>

        </tr>
      </tbody>
    </v-table>

    <!-- Диалог добавления/редактирования -->
    <v-dialog v-model="dialog" max-width="420">
      <v-card class="pa-4">
        <v-card-title class="text-h6 mb-2">{{ editingId ? 'Редактировать самолёт' : 'Добавить самолёт' }}</v-card-title>
        <v-card-text>
          <v-text-field v-model="form.model" label="Модель" required outlined dense />
          <v-text-field v-model="form.seats_count" label="Кол-во мест" type="number" required outlined dense />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="dialog = false">Отмена</v-btn>
          <v-btn color="primary" @click="saveAirplane">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'

const airplanes = ref([])
const dialog = ref(false)
const editingId = ref(null)
const form = ref({ model: '', seats_count: '' })

async function loadAirplanes() {
  const res = await api.get('/api/airplanes')
  airplanes.value = res.data
}
function openDialog() {
  editingId.value = null
  form.value = { model: '', seats_count: '' }
  dialog.value = true
}
function editAirplane(a) {
  editingId.value = a.id
  form.value = { model: a.model, seats_count: a.seats_count }
  dialog.value = true
}
async function saveAirplane() {
  if (editingId.value) {
    await api.put(`/api/airplanes/${editingId.value}`, form.value)
  } else {
    await api.post('/api/airplanes', form.value)
  }
  dialog.value = false
  await loadAirplanes()
}
async function deleteAirplane(id) {
  if (confirm('Удалить?')) {
    await api.delete(`/api/airplanes/${id}`)
    await loadAirplanes()
  }
}
onMounted(loadAirplanes)
</script>

<style scoped>
.admin-section-card {
  border-radius: 16px;
  background: #fff;
}
.admin-table-head th {
  background-color: #e3f0fd;
  color: #07519a;
  font-weight: 600;
  font-size: 1rem;
}
</style>
