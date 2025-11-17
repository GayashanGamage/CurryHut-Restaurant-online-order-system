<template>
  <div class="c-level-one-container">
    <div class="c-level-two-container">
      <div class="c-level-three-container window-header">
        <p class="window-title">{{ uiStore.windowTitle }}</p>
      </div>
      <div class="c-level-three-container time-setter">
        <div class="watch hour" id="hour">
          <p class="time-intro">Hour</p>
          <div class="arrow-button up">
            <span class="material-symbols-outlined" @click="shop.increaseHours">
              keyboard_arrow_up
            </span>
          </div>
          <div class="counter">
            {{ String(shop.hours).padStart(2, "0") }}
          </div>
          <div class="arrow-button down" @click="shop.decreaseHours">
            <span class="material-symbols-outlined"> keyboard_arrow_down </span>
          </div>
        </div>
        <div class="watch doted" id="doted">:</div>
        <div class="watch minutes" id="minutes">
          <p class="time-intro">Minutes</p>
          <div class="arrow-button up">
            <span
              class="material-symbols-outlined"
              @click="shop.increaseMinutes"
            >
              keyboard_arrow_up
            </span>
          </div>
          <div class="counter">
            {{ String(shop.minutes).padStart(2, "0") }}
          </div>
          <div class="arrow-button down" @click="shop.decreaseMinutes">
            <span class="material-symbols-outlined"> keyboard_arrow_down </span>
          </div>
        </div>
      </div>
      <p class="expain-text" v-if="uiStore.mealtimeOrShoptime">
        your lunch time will start
        {{
          shop.hours > 12
            ? String(shop.hours - 12).padStart(2, "0")
            : String(shop.hours).padStart(2, "0")
        }}:{{ String(shop.minutes).padStart(2, "0") }}
        {{ shop.hours >= 12 ? " p.m" : " a.m" }}
        from today
      </p>
      <p class="expain-text" v-if="!uiStore.mealtimeOrShoptime">
        your shop
        {{ uiStore.timeDescription }} will be
        {{
          shop.hours > 12
            ? String(shop.hours - 12).padStart(2, "0")
            : String(shop.hours).padStart(2, "0")
        }}:{{ String(shop.minutes).padStart(2, "0") }}
        {{ shop.hours >= 12 ? " p.m" : " a.m" }}
        from today
      </p>
      <div class="button-container">
        <button
          class="action-button cancel"
          @click="uiStore.closeTimeChangeWindow"
        >
          Cancel
        </button>
        <button class="action-button" @click="saveChangeTime">Confirm</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import router from "@/router";
import { useAuthonticationStore } from "@/stores/authontication";
import { useShopStore } from "@/stores/shop";
import { useUiStore } from "@/stores/ui";
import axios from "axios";
import { useToast } from "vue-toast-notification";

const toast = useToast();

// pinia stores
const shop = useShopStore();
const uiStore = useUiStore();
const authontication = useAuthonticationStore();

const saveChangeTime = () => {
  // function : change meal time and shop time
  // 1. check credencials
  // 2. if timeDescription is breakfast, lunch, meal -> '/changeMealTime'
  // 3. if timeDescription is open_time, close_time -> '/changeShopTime'
  // 4. send API request
  // 5. if successfull then show successfull message and close timechangwindow
  // 6. otherwise show error message and close timechangewindow

  // check authontication
  if (
    authontication.cookies_token == null ||
    authontication.local_storage_email == null
  ) {
    const credencials = authontication.restoreCredentials();
    if (credencials == false) {
      router.replace({ name: "login" });
    }
  } else {
    sendRequest();
  }
};

const sendRequest = () => {
  if (
    uiStore.timeDescription == "breakfast" ||
    uiStore.timeDescription == "lunch" ||
    uiStore.timeDescription == "dinner"
  ) {
    axios
      .patch(`${import.meta.env.VITE_url}/changeMealTime`, null, {
        params: {
          mealTime: uiStore.timeDescription,
          h: shop.hours,
          m: shop.minutes,
        },
        headers: {
          Authorization: "Bearer " + authontication.cookies_token,
        },
      })
      .then((responce) => {
        if (responce.status == 200) {
          uiStore.refresh = true;
          toast.success(`${uiStore.timeDescription} updated successfully`);
          uiStore.closeTimeChangeWindow();
        }
      })
      .catch((error) => {
        if (error.status == 400) {
          toast.error(error.response.data);
        }
      });
  } else if (
    uiStore.timeDescription == "open_time" ||
    uiStore.timeDescription == "close_time"
  ) {
    axios
      .patch(`${import.meta.env.VITE_url}/changeShopTime`, null, {
        params: {
          shopTime: uiStore.timeDescription,
          h: parseInt(shop.hours),
          m: parseInt(shop.minutes),
        },

        headers: {
          Authorization: "Bearer " + authontication.cookies_token,
        },
      })
      .then((responce) => {
        if (responce.status == 200) {
          uiStore.refresh = true;
          toast.success(`${uiStore.timeDescription} update successfully`);
          uiStore.closeTimeChangeWindow();
        }
      })
      .catch((error) => {
        if (error.response.status == 400) {
          toast.error(error.response.data);
        } else if (
          error.response.status == 500 ||
          error.response.status == 404
        ) {
          toast.error(error.response.data);
          uiStore.closeTimeChangeWindow();
        }
      });
  }
};
</script>

<style scoped>
.c-level-one-container {
  width: 100vw;
  height: 100vh;
  background-color: rgba(24, 28, 20, 0.8);
  position: fixed;
  top: 1;
  bottom: 1;
  left: 1;
  right: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}
.c-level-two-container {
  border-radius: 6px;
  background: #fff;
  width: 514px;
  height: auto;
  display: flex;
  flex-direction: column;
}
.window-header {
  width: 514px;
  height: 60px;
  flex-shrink: 0;
  border-radius: 6px 6px 0px 0px;
  background: #41b06e;
  display: flex;
  justify-content: center;
  align-items: center;
}
.window-title {
  color: #fff;
  font-family: "Space Grotesk";
  font-size: 24px;
  font-weight: 700;
  text-transform: uppercase;
}
.time-setter {
  height: 200px;
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 2fr;
  grid-gap: 10px;
  grid-template-areas: ". hour dot minutes .";
}
#hour {
  grid-area: hour;
}
#doted {
  grid-area: dot;
  padding-top: 85px;
}
#minutes {
  grid-area: minutes;
}
.watch {
  padding-top: 15px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.arrow-button {
  border-radius: 30px;
  background: #f3f3f3;
  width: 40px;
  height: 40px;
  flex-shrink: 0;
  user-select: none;
}
.arrow-button:hover {
  background-color: #d6d6d6;
}
.material-symbols-outlined {
  font-size: 40px;
  user-select: none;
  color: #8f8f8f;
}
.material-symbols-outlined:hover {
  color: #000;
}
.doted {
  font-family: "Space Grotesk";
  font-size: 48px;
  font-weight: 900;
  user-select: none;
}
.counter {
  color: #000;
  font-family: "Space Grotesk";
  font-size: 48px;
  font-style: normal;
  font-weight: 300;
  text-transform: uppercase;
  user-select: none;
}
.button-container {
  display: flex;
  justify-content: right;
}
.action-button {
  width: 110px;
  height: 30px;
  flex-shrink: 0;
  border-radius: 4px;
  border: 1px solid #41b06e;
  background: #fff;
  color: #41b06e;
  font-family: "Space Grotesk";
  font-size: 18px;
  font-style: normal;
  font-weight: 600;
  line-height: normal;
  align-self: flex-end;
  margin: 10px 24px 15px 0px;
}
.action-button:hover {
  border: 1.5px solid #41b06e;
  background: #41b06e;
  color: #fff;
}
.cancel {
  color: #ff204e;
  border: 1px solid #ff204e;
  background: #fff;
}
.cancel:hover {
  border: 1px solid #ff204e;
  background: #ff204e;
  color: #fff;
}
.time-intro {
  font-family: "Space Grotesk";
  font-size: 14px;
  color: #41b06e;
  padding-bottom: 20px;
}
.expain-text {
  font-family: "Space Grotesk";
  font-size: 18px;
  color: #fff;
  background-color: #41b06e;
  align-self: center;
  margin: 10px 0px;
  width: 450px;
  text-align: center;
  border-radius: 20px;
  height: 25px;
}
</style>
