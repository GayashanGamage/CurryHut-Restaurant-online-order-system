import { ref, computed } from "vue";
import { defineStore } from "pinia";

export const useUiStore = defineStore("ui", () => {
  const logoutPopupWindow = ref(false);
  const PasswordChangeWindow = ref(false);
  const CodeVerify = ref(true); //subwindow of CodeVerificationWindow
  const PasswordRest = ref(false); //subwindow of CodeVerificationWindow

  function openLogoutPopup() {
    logoutPopupWindow.value = true;
  }

  function closeLogoutPopup() {
    logoutPopupWindow.value = false;
  }

  function closeCodeVerifyPopup() {
    PasswordChangeWindow.value = false;
  }

  return {
    // component visibility
    logoutPopupWindow,
    PasswordChangeWindow,
    CodeVerify,
    PasswordRest,

    // funciton
    openLogoutPopup,
    closeLogoutPopup,
    closeCodeVerifyPopup,
  };
});
