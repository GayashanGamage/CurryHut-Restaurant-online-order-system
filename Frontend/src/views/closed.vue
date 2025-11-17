<template>
  <div class="menubar">
    <h1 class="site-title">Curry Hut</h1>
  </div>
  <div class="main">
    <div class="message">
      <H2 class="message-title">SORRY</H2>
      <p class="message-description">Tomorrow will be tasty sunday</p>
    </div>
    <div class="content">
      <div class="time-bar">
        <div class="time-container">
          <p class="time-description">we usually close</p>
          <p class="time">
            {{
              String(new Date(uiStore.shopClose).getHours()).padStart(2, "0")
            }}:{{
              String(new Date(uiStore.shopClose).getMinutes()).padStart(2, "0")
            }}
          </p>
        </div>
        <hr class="devider" />
        <div class="time-container">
          <p class="time-description">it's now</p>
          <p class="time">
            {{ hours }}:{{ minuts }}
            <span class="seconds">{{ String(seconds).padStart(2, "0") }}</span>
          </p>
        </div>
        <hr class="devider" />
        <div class="time-container">
          <p class="time-description">we open tommorow</p>
          <p class="time">
            {{
              String(new Date(uiStore.shopOpen).getHours()).padStart(2, "0")
            }}:{{
              String(new Date(uiStore.shopOpen).getMinutes()).padStart(2, "0")
            }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";
import router from "@/router";
import { useUiStore } from "@/stores/ui";
import { useFoodStore } from "@/stores/food";

// ui store import
const uiStore = useUiStore();
const foodstore = useFoodStore();

const redirect = () => {
  router.push('/');
}


onMounted(() => {
  if(uiStore.shopOpen == null){
    axios
    .get(`${import.meta.env.VITE_url}/customer/`)
    .then((response) => {
      if(response.status == 200){
        foodstore.foodInfo = response.data.data;
        uiStore.mainProductSection = true
        uiStore.categorySection = true
        redirect()
      }
    })
    .catch((error) => {
      if (error.status === 403) {
        uiStore.shopClose = error.response.data["close_time"];
        uiStore.shopOpen = error.response.data["open_time"];
      }
    });
  }
});


// get current time
const abc = ref(
  new Date().getHours() * 3600 +
    new Date().getMinutes() * 60 +
    new Date().getSeconds()
);

// assign current time in to hours, minutes and seconds
const hours = ref(Math.floor(abc.value / 3600));
const minuts = ref(Math.floor((abc.value % 3600) / 60));
const seconds = ref(abc.value % 60);

// run current time in updated way
setInterval(() => {
  abc.value++;
  hours.value = Math.floor(abc.value / 3600);
  minuts.value = Math.floor((abc.value % 3600) / 60);
  seconds.value = abc.value % 60;
}, 1000);

// // watch difference of current time and open time - if that is less than 600 seconds, then show notification
// watch(abc, (newValue) => {
//   // open hour and minute
//   const [openHour, openMinute] = uiStore.shopOpen.split(":");
//   const shopOpenInMinutes = openHour * 3600 + openMinute * 60;

//   // close hour and minute
//   const [closeHour, closeMinute] = uiStore.shopClose.split(":");
//   const shopCloseInMinutes = closeHour * 3600 + closeMinute * 60;

//   // if current time is less than open time or greater than close time, then redirect to home page
//   if (shopOpenInMinutes - newValue < 0 && shopCloseInMinutes - newValue > 0) {
//     router.push("/");
//   }
// });

// // when directly request close page, eveluate open and close time
// onBeforeMount(() => {
//   const [openHour, openMinute] = uiStore.shopOpen.split(":");
//   const [closeHour, closeMinute] = uiStore.shopClose.split(":");

//   const shopOpenInMinutes = openHour * 3600 + openMinute * 60;
//   const shopCloseInMinutes = closeHour * 3600 + closeMinute * 60;

//   if (abc.value < shopOpenInMinutes || abc.value < shopCloseInMinutes) {
//     router.push("/");
//   }
// });
</script>

<style scoped>
.menubar {
  width: 100%;
  height: auto;
  background: #ff5e5e;
}
.site-title {
  margin: 0;
  padding: 10px 40px;
  font-size: 28px;
  color: white;
}
.main {
  display: flex;
  width: 80%;
  flex-direction: column;
  align-items: center;
  gap: 48px;
  margin-inline: auto;
  margin-top: 15vh;
}
.content {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.message-title {
  color: #ff5e5e;
  text-align: center;
  font-size: 64px;
  font-style: normal;
  font-weight: 100;
  line-height: normal;
  text-transform: uppercase;
  align-self: stretch;
}
.message-description {
  color: #ff5e5e;
  text-align: center;
  font-size: 16px;
  font-style: normal;
  font-weight: 300;
  line-height: normal;
  text-transform: uppercase;
  align-self: stretch;
}
.time-bar {
  /* width: fit-content; */
  display: flex;
  flex-wrap: wrap;
  padding: 16px 42px;
  align-items: center;
  gap: 76px;
  align-self: stretch;
  border-radius: 6px;
  background: #fff;
}
.time-container {
  display: flex;
  width: auto;
  flex-direction: column;
  align-items: center;
}
.time-description {
  color: #ff5e5e;
  text-align: center;
  font-size: 16px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
  text-transform: uppercase;
  align-self: stretch;
}
.time {
  color: #ff5e5e;
  text-align: center;
  font-size: 64px;
  font-style: normal;
  font-weight: 900;
  line-height: normal;
  align-self: stretch;
}
.seconds {
  font-size: 16px;
  font-style: normal;
  font-weight: 800;
  margin-left: -15px;
}
.devider {
  width: 2px;
  height: 96px;
  background: #ff5e5e;
  border: none;
}
.notification {
  display: flex;
  padding: 8px 50px;
  justify-content: center;
  align-items: center;
  gap: 8px;
  align-self: stretch;
  border-radius: 4px;
  background: #ff5e5e;
}
.notification-text {
  color: #fff;
  font-size: 16px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
  text-transform: uppercase;
  flex: 1 0 0;
}
</style>
