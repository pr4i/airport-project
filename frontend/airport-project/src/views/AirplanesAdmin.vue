<template>
  <v-card>
    <v-card-title>Самолёты</v-card-title>
    <v-btn color="primary" @click="openDialog">Добавить самолёт</v-btn>
    <v-table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Модель</th>
          <th>Кол-во мест</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="a in airplanes" :key="a.id">
          <td>{{ a.id }}</td>
          <td>{{ a.model }}</td>
          <td>{{ a.seats_count }}</td>
          <td>
            <v-btn size="small" @click="editAirplane(a)">✏️</v-btn>
            <v-btn size="small" color="error" @click="deleteAirplane(a.id)">🗑</v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>
    <v-dialog v-model="dialog" max-width="400">
      <v-card>
        <v-card-title>{{ editingId ? 'Редактировать' : 'Добавить' }}</v-card-title>
        <v-card-text>
          <v-text-field v-model="form.model" label="Модель" required />
          <v-text-field v-model="form.seats_count" label="Кол-во мест" type="number" required />
        </v-card-text>
        <v-card-actions>
          <v-spacer/>
          <v-btn @click="dialog = false">Отмена</v-btn>
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
