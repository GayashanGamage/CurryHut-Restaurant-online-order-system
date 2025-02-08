// import './assets/main.css'

import { createPinia } from "pinia";
import { createApp } from "vue";
import ToastPlugin from "vue-toast-notification";

import App from "./App.vue";
import router from "./router";

const app = createApp(App);
app.use(createPinia());

app.use(router);

app.mount("#app");
