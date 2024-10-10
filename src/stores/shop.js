import { ref, computed, watch } from "vue";
import { defineStore } from "pinia";

export const useShopStore = defineStore("shop", () => {
  // current time
  const time_now = ref(new Date());
  const shop_status = ref(false); // true : close, false : open

  const open_time = ref(null);
  const close_time = ref(null);
  const shutdown = ref(true);
  const breakfast = ref(null);
  const lunch = ref(null);
  const dinner = ref(null);

  // update time_now variable after every 15 seconds and update shop_status accordinly
  // setInterval(() => {
  //   time_now.value = new Date();
  //   if (
  //     time_now.value >
  //     new Date(
  //       time_now.value.getFullYear(),
  //       time_now.value.getMonth(),
  //       time_now.value.getDate(),
  //       close_time.value.slice(0, 2),
  //       close_time.value.slice(3, 5),
  //       close_time.value.slice(6, 8)
  //     )
  //   ) {
  //     shop_status.value = true;
  //   } else {
  //     shop_status.value = false;
  //   }
  // }, 1000);

  // Timechange component
  const hours = ref(0);
  const minutes = ref(0);

  function increaseHours() {
    if (hours.value == 23) {
      hours.value = 0;
    } else {
      hours.value += 1;
    }
  }

  function decreaseHours() {
    if (hours.value == 0) {
      hours.value = 23;
    } else {
      hours.value -= 1;
    }
  }

  function increaseMinutes() {
    if (minutes.value == 59) {
      minutes.value = 0;
    } else {
      minutes.value += 1;
    }
  }

  function decreaseMinutes() {
    if (minutes.value == 0) {
      minutes.value = 59;
    } else {
      minutes.value -= 1;
    }
  }

  return {
    open_time,
    close_time,
    shutdown,
    breakfast,
    lunch,
    dinner,

    time_now,
    shop_status,

    // Timechange component
    hours,
    minutes,
    increaseHours,
    decreaseHours,
    increaseMinutes,
    decreaseMinutes,
  };
});
