// this is only store store related data
import { ref, computed, watch } from "vue";
import { defineStore } from "pinia";

export const useShopStore = defineStore("shop", () => {
  const open_time = ref(null);
  const close_time = ref(null);
  const shutdown = ref(true);
  const breakfast = ref(null);
  const lunch = ref(null);
  const dinner = ref(null);

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
    // Timechange component
    hours,
    minutes,
    increaseHours,
    decreaseHours,
    increaseMinutes,
    decreaseMinutes,
  };
});
