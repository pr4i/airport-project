<template>
  <v-footer class="site-footer" padless>
    <v-container>
      <v-row>
        <!-- Контакты -->
        <v-col cols="12" md="4" class="site-footer-block">
          <h2 class="site-footer-title">Контакты</h2>
          <div>8 (888) 444-55-55 бесплатно по России</div>
          <div class="site-footer-subtext">
            для международных звонков в соответствии с тарифами вашего оператора связи
          </div>
          <div class="site-footer-link"><a href="#">Обратная связь</a></div>
          <v-btn color="orange" class="site-footer-call-btn">Позвонить с сайта</v-btn>
          <div class="site-footer-socials mt-4">
            <v-icon class="site-footer-icon">mdi-telegram</v-icon>
            <v-icon class="site-footer-icon">mdi-vk</v-icon>
            <v-icon class="site-footer-icon">mdi-twitter</v-icon>
            <v-icon class="site-footer-icon">mdi-facebook</v-icon>
            <v-icon class="site-footer-icon">mdi-youtube</v-icon>
          </div>
        </v-col>

        <!-- Компания -->
        <v-col cols="12" md="4" class="site-footer-block">
          <h2 class="site-footer-title">Компания</h2>
          <div class="site-footer-links">
            <div><a href="#">О компании</a></div>
            <div><a href="#">Контакты</a></div>
            <div><a href="#">Работа в AIRWAY</a></div>
            <div><a href="#">Политика конфиденциальности</a></div>
            <div><a href="#">Противодействие коррупции</a></div>
            <div><a href="#">Карта сайта</a></div>
          </div>
        </v-col>

        <!-- Партнерам -->
        <v-col cols="12" md="4" class="site-footer-block">
          <h2 class="site-footer-title">Партнерам</h2>
          <div class="site-footer-links">
            <div><a href="#">Агентам</a></div>
            <div><a href="#">Грузовые перевозки</a></div>
            <div><a href="#">Группа AIRWAY</a></div>
            <div><a href="#">Акционерам и инвесторам</a></div>
            <div><a href="#">Собрание акционеров 2025</a></div>
            <div><a href="#">Раскрытие информации</a></div>
          </div>
        </v-col>
      </v-row>

      <v-divider class="my-2" color="#1976d2" />

      <v-row align="center" class="site-footer-bottom">
        <v-col cols="12" md="6" class="text-md-left text-center">
          © Авиакомпания «AIRWAY» 2008–2025
        </v-col>
        <v-col cols="12" md="6" class="text-md-right text-center d-flex align-center justify-end justify-md-end justify-center">
          <v-icon class="mr-2" color="white">mdi-cellphone</v-icon>
          <div>Приложение «AIRWAY»<br />для вашего мобильного устройства</div>
        </v-col>
      </v-row>
    </v-container>
  </v-footer>
</template>

<style scoped>
.site-footer {
  background: linear-gradient(0deg, #0d47a1 0%, #1565c0 100%);
  color: #fff;
  padding-top: 24px;
  padding-bottom: 16px;
  font-size: 0.95rem;
  border-top: 2px solid #0d47a1;
}
.site-footer .v-container {
  padding-bottom: 0 !important;
  padding-top: 0 !important;
}

.site-footer-title {
  font-size: 1.2rem;
  color: #bbdefb;
  font-weight: 700;
  margin-bottom: 12px;
}

.site-footer-block {
  line-height: 1.6;
  margin-bottom: 24px;
}

.site-footer-subtext {
  font-size: 0.85rem;
  color: #bbdefb;
  margin-bottom: 4px;
}

.site-footer-call-btn {
  margin-top: 10px;
  font-size: 0.95rem;
  font-weight: 600;
  min-height: 34px;
  padding: 4px 16px;
}

.site-footer-link a,
.site-footer-links a {
  color: #fff;
  text-decoration: none;
  transition: color 0.2s ease;
}
.site-footer-link a:hover,
.site-footer-links a:hover {
  color: #ffa726;
  text-decoration: underline;
}

.site-footer-socials {
  margin-top: 8px;
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.site-footer-icon {
  font-size: 22px;
  cursor: pointer;
  transition: transform 0.2s ease, color 0.2s ease;
}
.site-footer-icon:hover {
  transform: scale(1.2);
  color: #ffa726 !important;
}

.site-footer-bottom {
  font-size: 0.85rem;
  margin-top: 8px;
}

/* Адаптивность */
@media (max-width: 768px) {
  .site-footer-block {
    text-align: center;
  }
  .site-footer-socials {
    justify-content: center;
  }
}
</style>

