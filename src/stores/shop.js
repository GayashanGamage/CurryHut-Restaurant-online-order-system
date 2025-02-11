// this is only store store related data
import { ref, computed, watch } from "vue";
import { defineStore } from "pinia";
import axios from "axios";

export const useShopStore = defineStore("shop", () => {
  const open_time = ref(null);
  const close_time = ref(null);
  const shutdown = ref(true);
  const breakfast = ref(null);
  const lunch = ref(null);
  const dinner = ref(null);
  const menu = ref(null);

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

  function requestSettingData(token){
    axios
    .get(`${import.meta.env.VITE_url}/shopdetails`, {
      headers: {
        Authorization: "Bearer " + token,
      },
    })
    .then((response) => {
      if (response.status == 200) {
        // assign response data in to variabl 
        let APIdata = response.data.data;

        open_time.value = APIdata.open_time;
        close_time.value = APIdata.close_time;
        shutdown.value = APIdata.shutdown;
        breakfast.value = APIdata.breakfast;
        lunch.value = APIdata.lunch;
        dinner.value = APIdata.dinner;
        menu.value = APIdata.menu
      }
    })
    .catch((error) => {
      if (error.status == 401) {
        router.replace({ name: "login" });
      }
    });
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
    menu,
    increaseHours,
    decreaseHours,
    increaseMinutes,
    decreaseMinutes,
    requestSettingData,
  };
});
