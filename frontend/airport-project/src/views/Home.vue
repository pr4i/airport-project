<template>
  <v-app>
    <!-- Верхний бар -->
      <v-app-bar app color="#07519a" dark style="box-shadow: 0 2px 6px rgba(0,0,0,0.3); border-bottom: 1px solid white;">
      <v-toolbar-title>
        <v-icon left>mdi-airplane</v-icon>
        AIRWAY
      </v-toolbar-title>
      <v-spacer />
      <v-btn v-if="userStore.isAdmin" text @click="router.push('/admin')">Админ-панель</v-btn>
      <v-btn text @click="router.push('/onlineboard')">Онлайн-табло</v-btn>
      <v-btn text @click="router.push('/flights')">Бронирование</v-btn>
      <v-btn text @click="router.push('/checkin')">Регистрация</v-btn>
      <v-btn text @click="goToLK">Личный кабинет</v-btn>
      <v-btn
        v-if="!isAuth"
        icon
        @click="router.push('/login')"
        title="Войти"
      >
        <v-icon>mdi-account-circle</v-icon>
      </v-btn>
      <v-btn
        v-else
        icon
        @click="logout"
        title="Выйти"
      >
        <v-icon>mdi-logout</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <v-container class="main-section" fluid>
        <!-- Баннер/фон -->
        <div class="banner">
          <h1>Планируйте свои путешествия с AIRWAY</h1>
          <p>Быстрое бронирование авиабилетов онлайн</p>
          <v-btn
            v-if="!isAuth"
            color="primary"
            large
            class="mt-4"
            @click="router.push('/login')"
          >
            Войти или зарегистрироваться
          </v-btn>
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
        <!-- Дополнительные услуги -->
        <div class="additional-services-title">
          <h2>Дополнительные услуги</h2>
        </div>
        <v-row class="additional-services" dense>
          <v-col cols="12" md="4" lg="3">
            <v-card class="service-card" outlined>
              <v-img src="https://i.pinimg.com/originals/08/07/e7/0807e7c5852f9ec0e29a757990878c3e.jpg" height="130" cover />
              <v-card-title class="service-title">Предварительный выбор мест</v-card-title>
              <v-card-text>Выбрать и купить места заранее.</v-card-text>
              <v-card-actions>
                <v-btn color="primary" variant="outlined">Подробнее</v-btn>
                <v-spacer />
              </v-card-actions>
            </v-card>
          </v-col>
          <v-col cols="12" md="4" lg="3">
            <v-card class="service-card" outlined>
              <v-img src="https://i.pinimg.com/originals/56/7e/11/567e11da74ded69f50141d7a01e850e8.jpg" height="130" cover />
              <v-card-title class="service-title">Предварительно оплаченный багаж</v-card-title>
              <v-card-text>Выгодные условия и цены при оформлении услуги заранее.</v-card-text>
              <v-card-actions>
                <v-btn color="primary" variant="outlined">Подробнее</v-btn>
                <v-spacer />
              </v-card-actions>
            </v-card>
          </v-col>
          <v-col cols="12" md="4" lg="3">
            <v-card class="service-card" outlined>
              <v-img src="https://avatars.mds.yandex.net/i?id=4851476a9c4b1031ebc84894d342a9f25d94cc49-4055877-images-thumbs&n=13" height="130" cover />
              <v-card-title class="service-title">Аэроэкспресс</v-card-title>
              <v-card-text>Быстрый способ добраться до аэропортов Москвы или в город.</v-card-text>
              <v-card-actions>
                <v-btn color="primary" variant="outlined">Подробнее</v-btn>
                <v-spacer />
              </v-card-actions>
            </v-card>
          </v-col>
          <v-col cols="12" md="6" lg="3">
            <v-card class="service-card" outlined>
              <v-img src="https://avatars.mds.yandex.net/get-altay/5482460/2a0000017efd36a6f2e3bb1efd997775d199/XXXL" height="130" cover />
              <v-card-title class="service-title">VIP, бизнес-залы, Fast Track и Meet&Assist</v-card-title>
              <v-card-text>Всё для комфортного ожидания рейса и быстрого прохождения формальностей.</v-card-text>
              <v-card-actions>
                <v-btn color="primary" variant="outlined">Подробнее</v-btn>
                <v-spacer />
              </v-card-actions>
              <v-card-subtitle class="service-sub">Реклама. ООО «Терсона тревел» ИНН 7713570937</v-card-subtitle>
            </v-card>
          </v-col>
          <v-col cols="12" md="6" lg="3">
            <v-card class="service-card" outlined>
              <v-img src="https://assets-webflow.ngcdn.ru/cdn.prod/599873abab717100012c91ea/6764595a21ec71fb6ba794cb_c84626bad453144a67c5d9627002a780.jpeg" height="130" cover />
              <v-card-title class="service-title">Полетная страховка</v-card-title>
              <v-card-text>Подарите себе больше уверенности</v-card-text>
              <v-card-actions>
                <v-btn color="primary" variant="outlined">Подробнее</v-btn>
                <v-spacer />
              </v-card-actions>
              <v-card-subtitle class="service-sub">Реклама. АО «АльфаСтрахование» ИНН 7713056834</v-card-subtitle>
            </v-card>
          </v-col>
        </v-row>

      </v-container>
    </v-main>
    <!-- ФУТЕР -->
<v-footer class="custom-footer" padless>
  <v-container>
    <v-row>
      <!-- Контакты -->
      <v-col cols="12" md="4" class="footer-block">
        <h2 class="footer-title">Контакты</h2>
        <div class="footer-contacts">
          <div class="footer-phone">8 (888) 444-55-55 бесплатно по России</div>
          <div class="footer-subtext">
            для международных звонков в соответствии с тарифами вашего оператора связи
          </div>
          <div class="footer-link"><a href="#">Обратная связь</a></div>
          <v-btn color="orange" class="footer-call-btn">Позвонить с сайта</v-btn>
          <div class="footer-socials mt-4 d-flex">
            <v-icon class="footer-icon" aria-label="Telegram">mdi-telegram</v-icon>
            <v-icon class="footer-icon" aria-label="VK">mdi-vk</v-icon>
            <v-icon class="footer-icon" aria-label="Twitter">mdi-twitter</v-icon>
            <v-icon class="footer-icon" aria-label="Facebook">mdi-facebook</v-icon>
            <v-icon class="footer-icon" aria-label="YouTube">mdi-youtube</v-icon>
          </div>
        </div>
      </v-col>

      <!-- Компания -->
      <v-col cols="12" md="4" class="footer-block">
        <h2 class="footer-title">Компания</h2>
        <div class="footer-links">
          <div><a href="#">О компании</a></div>
          <div><a href="#">Контакты</a></div>
          <div><a href="#">Работа в AIRWAY</a></div>
          <div><a href="#">Политика конфиденциальности</a></div>
          <div><a href="#">Противодействие коррупции</a></div>
          <div><a href="#">Карта сайта</a></div>
        </div>
      </v-col>

      <!-- Партнерам -->
      <v-col cols="12" md="4" class="footer-block">
        <h2 class="footer-title">Партнерам</h2>
        <div class="footer-links">
          <div><a href="#">Агентам</a></div>
          <div><a href="#">Грузовые перевозки</a></div>
          <div><a href="#">Группа AIRWAY</a></div>
          <div><a href="#">Акционерам и инвесторам</a></div>
          <div><a href="#">Общее собрание акционеров 2025</a></div>
          <div><a href="#">Раскрытие информации для инвесторов</a></div>
        </div>
      </v-col>
    </v-row>

    <v-divider class="my-2" color="#1976d2" />

    <v-row align="center" class="footer-bottom">
      <v-col cols="12" md="6" class="text-md-left text-center">
        <span>© Авиакомпания «AIRWAY» 2008–2025</span>
      </v-col>
      <v-col cols="12" md="6" class="text-md-right text-center d-flex align-center justify-end justify-md-end justify-center">
        <v-icon class="mr-2" color="white">mdi-cellphone</v-icon>
        <div>Приложение «AIRWAY»<br />для вашего мобильного устройства</div>
      </v-col>
    </v-row>
  </v-container>
</v-footer>


  </v-app>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()
const { token } = storeToRefs(userStore)
const isAuth = computed(() => !!token.value)

const from = ref('')
const to = ref('')
const date = ref('')
const menu = ref(false)
const passengers = ref(1)

function searchFlights() {
  // Тут можно сделать редирект на /flights и передать параметры (по желанию)
  router.push('/flights')
}

function goToLK() {
  if (isAuth.value) {
    router.push('/dashboard')
  } else {
    router.push('/login')
  }
}


function logout() {
  userStore.logout()
  router.push('/home')
}
</script>

<style scoped>
.custom-footer {
  background: #1565c0 !important;
  color: #fff !important;
  padding-top: 18px;    /* было 38px */
  padding-bottom: 6px;  /* было 12px */
  margin-top: 0;
  font-size: 0.97rem;   /* было 1.02rem */
}
.footer-title {
  font-size: 1.15rem;   /* было 1.5rem */
  color: #bbdefb;
  font-weight: bold;
  margin-bottom: 7px;   /* было 10px */
}
.footer-phone-main {
  font-size: 1.7rem;    /* было 2.5rem */
  font-weight: 600;
  color: #fff;
  vertical-align: middle;
}
.footer-phone-icon {
  font-size: 1.2rem !important; /* было 2.1rem */
  margin-right: 4px;
}
.footer-link, .footer-links a {
  color: #fff;
  text-decoration: none;
  transition: color .2s;
}
.footer-link:hover, .footer-links a:hover {
  color: #ffa726;
  text-decoration: underline;
}
.footer-call-btn {
  margin-top: 7px;      /* было 10px */
  font-size: 0.97rem;   /* было 1.05rem */
  min-height: 30px;     /* сделаем кнопку ниже */
  padding: 0 14px;
}
.footer-block {
  margin-bottom: 14px;  /* было 30px */
}
.footer-bottom {
  font-size: 0.92rem;
  margin-top: 2px !important;
  margin-bottom: 0 !important;
  padding-bottom: 0 !important;
}
.footer-socials .v-icon {
  opacity: 0.84;
  cursor: pointer;
  transition: opacity .2s;
  font-size: 23px !important; /* было 28px */
  margin-right: 6px !important;
}
.footer-socials .v-icon:hover {
  opacity: 1;
  color: #ffa726 !important;
}
.footer-socials .v-icon:last-child {
  margin-right: 0 !important;
}

.custom-footer .v-container {
  padding-bottom: 0 !important;
  padding-top: 0 !important;
}

/* Стили для дополнительных услуг */
.additional-services-title {
  font-size: 2rem;
  color: #fff;
  margin: 40px 0 16px 0;
  font-weight: bold;
  position: relative;
}
.additional-services {
  margin-bottom: 36px;
}
.service-card {
  border-radius: 18px;
  min-height: 320px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  margin-bottom: 12px;
}
.service-title {
  color: #1565c0;
  font-weight: bold;
  font-size: 1.1rem;
}
.service-sub {
  font-size: 0.8rem;
  color: #888;
  padding-left: 8px;
  padding-bottom: 8px;
}

/* Основные стили */
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
.custom-footer {
  background: linear-gradient(0deg, #0d47a1 0%, #1565c0 100%);
  color: #fff;
  padding-top: 24px;
  padding-bottom: 16px;
  font-size: 0.95rem;
  border-top: 2px solid #0d47a1;
}
.footer-title {
  font-size: 1.2rem;
  color: #bbdefb;
  font-weight: 700;
  margin-bottom: 12px;
}
.footer-block {
  line-height: 1.6;
  margin-bottom: 24px;
}
.footer-link a {
  color: #fff;
  text-decoration: none;
}
.footer-link a:hover,
.footer-links a:hover {
  color: #ffa726;
  text-decoration: underline;
}
.footer-call-btn {
  margin-top: 10px;
  font-size: 0.95rem;
  font-weight: 600;
  min-height: 34px;
  padding: 4px 16px;
}
.footer-subtext {
  font-size: 0.85rem;
  color: #bbdefb;
  margin-bottom: 4px;
}
.footer-socials {
  margin-top: 8px;
  gap: 10px;
}
.footer-icon {
  font-size: 22px;
  cursor: pointer;
  transition: transform 0.2s ease, color 0.2s ease;
}
.footer-icon:hover {
  transform: scale(1.2);
  color: #ffa726 !important;
}
.footer-bottom {
  font-size: 0.85rem;
  margin-top: 8px;
}

</style>

