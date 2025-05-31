<template>
  <v-card>
    <v-card-title>Аэропорты</v-card-title>
    <v-btn color="primary" @click="openDialog">Добавить аэропорт</v-btn>
    <v-table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Название</th>
          <th>Город</th>
          <th>Код</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="a in airports" :key="a.id">
          <td>{{ a.id }}</td>
          <td>{{ a.name }}</td>
          <td>{{ a.city }}</td>
          <td>{{ a.code }}</td>
          <td>
            <v-btn size="small" @click="editAirport(a)">✏️</v-btn>
            <v-btn size="small" color="error" @click="deleteAirport(a.id)">🗑</v-btn>
          </td>
        </tr>
      </tbody>
    </v-table>
    <v-dialog v-model="dialog" max-width="400">
      <v-card>
        <v-card-title>{{ editingId ? 'Редактировать' : 'Добавить' }}</v-card-title>
        <v-card-text>
          <v-text-field v-model="form.name" label="Название" required />
          <v-text-field v-model="form.city" label="Город" required />
          <v-text-field v-model="form.code" label="Код (IATA)" required />
        </v-card-text>
        <v-card-actions>
          <v-spacer/>
          <v-btn @click="dialog = false">Отмена</v-btn>
          <v-btn color="primary" @click="saveAirport">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'

const airports = ref([])
const dialog = ref(false)
const editingId = ref(null)
const form = ref({ name: '', city: '', code: '' })

async function loadAirports() {
  const res = await api.get('/api/airports')
  airports.value = res.data
}
function openDialog() {
  editingId.value = null
  form.value = { name: '', city: '', code: '' }
  dialog.value = true
}
function editAirport(a) {
  editingId.value = a.id
  form.value = { name: a.name, city: a.city, code: a.code }
  dialog.value = true
}
async function saveAirport() {
  if (editingId.value) {
    await api.put(`/api/airports/${editingId.value}`, form.value)
  } else {
    await api.post('/api/airports', form.value)
  }
  dialog.value = false
  await loadAirports()
}
async function deleteAirport(id) {
  if (confirm('Удалить?')) {
    await api.delete(`/api/airports/${id}`)
    await loadAirports()
  }
}
onMounted(loadAirports)
</script>
