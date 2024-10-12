import { ref, computed } from "vue";
import { defineStore } from "pinia";
import router from "@/router";
import "vue-toast-notification/dist/theme-sugar.css";

export const useAuthonticationStore = defineStore("authontication", () => {
  const email = ref(null);
  const authcookie = ref(null);
  const authontication = ref(false);

  const reset_email = ref(undefined);
  const passsword = ref(undefined); //this is for login password
  const role = ref(undefined);
  const secrete_code = ref(undefined);

  // router protection variables
  const email_page = ref(false);
  const verification_page = ref(false);
  const passwordRest_page = ref(false);

  // this is for change password
  const change_password1 = ref(null);
  const change_password2 = ref(null);

  // authontication related functions ------------------------------------------------
  function restoreAuthonticationDataToPinia() {
    // functionality : check the availability of the token in cookies store and email, then store in pinia store
    email.value = localStorage.getItem("email");
    let allCookei = document.cookie.split("; ");
    for (let i = 0; i < allCookei.length; i++) {
      if (allCookei[i].startsWith("user")) {
        authontication.value = true;
        authcookie.value = allCookei[i].slice(5);
        break;
      }
    }
    if (authontication.value == false) {
      email.value = null;
      authcookie.value = null;
    }
  }

  function checkAuthontication() {
    // functionality : this is mainly for check all authontication details (email, token) and directed to login page
    if (
      email.value === null ||
      authcookie.value === null ||
      authontication.value === false
    ) {
      restoreAuthonticationDataToPinia();
    }
  }

  function deleteCookie() {
    // functionality : remove cookies from cookies store and pinia store
    // 1. get all cookes
    // 2. select authontication tokon cookie using 'user'
    // 3. assign previous day and expire cookie
    let allCookei = document.cookie.split("; ");
    for (let i = 0; i < allCookei.length; i++) {
      if (allCookei[i].startsWith("user")) {
        document.cookie = `${allCookei[i]}; expires=Thu, 18 Dec 2000 12:00:00 UTC;`;
        authcookie.value = null;
        break;
      }
    }
  }

  function logoutAction() {
    deleteCookie();
    authontication.value = false;
    localStorage.removeItem("email");
    email.value = null;
    router.push({ name: "login" });
  }

  function redirectToLogin() {
    if (authontication.value === false) {
      logoutAction();
    }
  }

  // variables data crearing from page changing - from_to_DataCleaign ---------------
  function fromEmailtoLoginDataClearing() {
    reset_email.value = undefined;
  }

  function fromLogintoEmailDataClearing() {
    email.value = null;
    passsword.value = null;
  }

  function fromLogintoHomeDataClearing() {
    passsword.value = undefined;
  }

  function fromVerificationtoPasswordresetDataCleaning() {
    secrete_code.value = undefined;
  }

  function fromPasswordresettoLoginDataCleaning() {
    change_password1.value = null;
    change_password2.value = null;
  }

  return {
    // all variables
    email,
    reset_email,
    passsword,
    authontication,
    role,
    secrete_code,
    change_password1,
    change_password2,

    // page direct validation
    email_page,
    verification_page,
    passwordRest_page,

    // HTTPS request
    // codeVerification,

    // cookies
    restoreAuthonticationDataToPinia,
    redirectToLogin,
    authcookie,
    deleteCookie,
    checkAuthontication,
    logoutAction,

    // variables data crearing from page changing
    fromEmailtoLoginDataClearing,
    fromLogintoEmailDataClearing,
    fromLogintoHomeDataClearing,
    fromVerificationtoPasswordresetDataCleaning,
    fromPasswordresettoLoginDataCleaning,
  };
});
