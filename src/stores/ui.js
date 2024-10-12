import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useShopStore } from "./shop";

export const useUiStore = defineStore("ui", () => {
  // other pinia stors
  const shopStore = useShopStore();

  // Passwordchange component
  const logoutPopupWindow = ref(false);
  const PasswordChangeWindow = ref(false);
  const CodeVerify = ref(true); //subwindow of CodeVerificationWindow
  const PasswordRest = ref(false); //subwindow of CodeVerificationWindow

  // Timechange component
  const TimeChangeWindow = ref(false);
  const timeDescription = ref(null); // meal-time : breakfast, lunch, dinner, shop-time : open_time, close_time
  const mealtimeOrShoptime = ref(true); // true = mealtime, false = shoptime

  function openLogoutPopup() {
    logoutPopupWindow.value = true;
  }

  function closeLogoutPopup() {
    logoutPopupWindow.value = false;
  }

  function closeCodeVerifyPopup() {
    PasswordChangeWindow.value = false;
  }

  function openTimeChangeWindow(mealTime) {
    timeDescription.value = mealTime;
    TimeChangeWindow.value = true;
    if (mealTime === "breakfast") {
      shopStore.hours = new Date(`19970-1-1 ${shopStore.breakfast}`).getHours();
      shopStore.minutes = new Date(
        `19970-1-1 ${shopStore.breakfast}`
      ).getMinutes();
    } else if (mealTime === "lunch") {
      shopStore.hours = new Date(`19970-1-1 ${shopStore.lunch}`).getHours();
      shopStore.minutes = new Date(`19970-1-1 ${shopStore.lunch}`).getMinutes();
    } else if (mealTime === "dinner") {
      shopStore.hours = new Date(`19970-1-1 ${shopStore.dinner}`).getHours();
      shopStore.minutes = new Date(
        `19970-1-1 ${shopStore.dinner}`
      ).getMinutes();
    } else if (mealTime === "open_time") {
      mealtimeOrShoptime.value = false;
      shopStore.hours = new Date(`19970-1-1 ${shopStore.open_time}`).getHours();
      shopStore.minutes = new Date(
        `19970-1-1 ${shopStore.open_time}`
      ).getMinutes();
    } else if (mealTime === "close_time") {
      mealtimeOrShoptime.value = false;
      shopStore.hours = new Date(
        `19970-1-1 ${shopStore.close_time}`
      ).getHours();
      shopStore.minutes = new Date(
        `19970-1-1 ${shopStore.close_time}`
      ).getMinutes();
    }
  }

  function closeTimeChangeWindow() {
    timeDescription.value = null;
    shopStore.hours = 0;
    shopStore.minutes = 0;
    TimeChangeWindow.value = false;
  }

  return {
    // component visibility
    logoutPopupWindow,
    PasswordChangeWindow,
    CodeVerify,
    PasswordRest,
    TimeChangeWindow,

    timeDescription,
    mealtimeOrShoptime,

    // funciton
    openLogoutPopup,
    closeLogoutPopup,
    closeCodeVerifyPopup,
    openTimeChangeWindow,
    closeTimeChangeWindow,
  };
});
