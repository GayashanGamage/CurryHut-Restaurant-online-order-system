import { ref, computed } from "vue";
import { defineStore } from "pinia";

export const useUiStore = defineStore("ui", () => {
  // component visibility
  const logoutPopupWindow = ref(false);

  function openLogoutPopup() {
    logoutPopupWindow.value = true;
  }

  function closeLogoutPopup() {
    logoutPopupWindow.value = false;
  }

  return {
    logoutPopupWindow,
    openLogoutPopup,
    closeLogoutPopup,
  };
});
