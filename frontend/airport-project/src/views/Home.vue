<template>
  <v-app>
    <!-- Верхний бар -->
    <v-app-bar app flat color="#07519a" dark>
      <v-toolbar-title>
        <v-icon left>mdi-airplane</v-icon>
        AIRWAY
      </v-toolbar-title>
      <v-spacer />
      <v-btn text>Бронирование</v-btn>
      <v-btn text>Управление</v-btn>
      <v-btn text>Онлайн-табло</v-btn>
      <v-btn text @click="router.push('/dashboard')">Личный кабинет</v-btn>
      <v-btn icon><v-icon>mdi-account-circle</v-icon></v-btn>
    </v-app-bar>

    <v-main>
      <v-container class="main-section" fluid>
        <!-- Баннер/фон -->
        <div class="banner">
          <h1>Планируйте свои путешествия с AIRWAY</h1>
          <p>Быстрое бронирование авиабилетов онлайн</p>
        </div>

        <!-- Форма поиска авиабилетов -->
        <v-card class="search-form" outlined>
          <v-form @submit.prevent="searchFlights">
            <v-row>
              <v-col cols="12" md="3">
                <v-text-field v-model="from" label="Откуда" prepend-inner-icon="mdi-airplane-takeoff" outlined />
              </v-col>
              <v-col cols="12" md="3">
                <v-text-field v-model="to" label="Куда" prepend-inner-icon="mdi-airplane-landing" outlined />
              </v-col>
              <v-col cols="12" md="3">
                <v-menu
                  v-model="menu"
                  :close-on-content-click="false"
                  transition="scale-transition"
                  offset-y
                  min-width="290px"
                >
                  <template #activator="{ on, attrs }">
                    <v-text-field
                      v-model="date"
                      label="Дата"
                      prepend-inner-icon="mdi-calendar"
                      readonly
                      v-bind="attrs"
                      v-on="on"
                      outlined
                    />
                  </template>
                  <v-date-picker v-model="date" @input="menu = false"></v-date-picker>
                </v-menu>
              </v-col>
              <v-col cols="12" md="2">
                <v-select
                  v-model="passengers"
                  :items="[1,2,3,4,5,6]"
                  label="Пассажиры"
                  prepend-inner-icon="mdi-account-multiple"
                  outlined
                />
              </v-col>
              <v-col cols="12" md="1" class="d-flex align-center">
                <v-btn color="primary" type="submit" block style="height: 56px;">
                  Поиск
                </v-btn>
              </v-col>
            </v-row>
          </v-form>
        </v-card>

        <!-- Дополнительные быстрые кнопки -->
        <v-row class="quick-links" justify="center" align="center">
          <v-col cols="12" md="3">
            <v-btn color="#07519a" dark block large>Спецпредложения</v-btn>
          </v-col>
          <v-col cols="12" md="3">
            <v-btn color="#1976d2" dark block large>Новости</v-btn>
          </v-col>
          <v-col cols="12" md="3">
            <v-btn color="#90caf9" dark block large>Онлайн-табло</v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
const router = useRouter()

const from = ref('')
const to = ref('')
const date = ref('')
const menu = ref(false)
const passengers = ref(1)

function searchFlights() {
  // Тут можно сделать редирект на /flights и передать параметры
  router.push('/flights')
}
</script>

<style scoped>
.main-section {
  background: linear-gradient(120deg, #07519a 70%, #e3f0fd 100%);
  min-height: 500px;
  padding-top: 40px;
  padding-bottom: 40px;
}
.banner {
  text-align: center;
  color: #fff;
  margin-bottom: 40px;
}
.banner h1 {
  font-size: 2.5rem;
  font-weight: bold;
}
.search-form {
  max-width: 1000px;
  margin: 0 auto 40px auto;
  padding: 24px 18px 8px 18px;
  border-radius: 20px;
  background: #fff;
}
.quick-links {
  margin-top: 16px;
}
</style>
