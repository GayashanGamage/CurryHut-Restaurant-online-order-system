import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import router from "@/router";
import { useToast } from "vue-toast-notification";
import "vue-toast-notification/dist/theme-sugar.css";

const tost = useToast();

export const useAuthonticationStore = defineStore("authontication", () => {
  const email = ref(null);
  const authcookie = ref(null);
  const authontication = ref(null);
  const reset_email = ref(undefined);
  const passsword = ref(undefined); //this is for login password
  const role = ref(undefined);
  const secrete_code = ref(undefined);

  // this is for change password
  const change_password1 = ref();
  const change_password2 = ref();

  // page direct validation
  const email_page = ref(false);
  const verification_page = ref(false);
  const passwordRest_page = ref(false);

  // all HTTPS requests
  // login functionality
  function login() {
    axios
      .post(`${import.meta.env.VITE_url}/login`, {
        email: email.value,
        password: passsword.value,
        role: "admin",
      })
      .then((response) => {
        if (response.status == 200) {
          authontication.value = true;
          // store email in local storange
          localStorage.setItem("email", email.value);
          // store cookie in cookie store
          document.cookie = `user=${response.data.token}; expires=Thu, 18 Dec 2024 12:00:00 UTC`;
          router.push({ name: "home" });
        }
      })
      .catch((error) => {
        if (error.status == 406) {
          tost.error("incorect password.");
        } else if (error.status == 404) {
          tost.error("incorect E-mail. please enter correct email");
        }
      });
  }

  // email verification
  function emailVerification() {
    axios
      .get(`${import.meta.env.VITE_url}/secreatecode`, {
        params: {
          email: reset_email.value,
        },
      })
      .then((response) => {
        if (response.status == 200) {
          email_page.value = true;
          router.push({ name: "verification" });
        }
        console.log(response);
      })
      .catch((error) => {
        if (error.status == 401) {
          tost.error("email not found");
        } else if (error.status == 500) {
          tost.info(
            "Verification code cannot send via email due to server error"
          );
        } else if (error.status == 404) {
          tost.info("something went wrong");
        }
      });
  }

  // code verification
  function codeVerification() {
    axios
      .post(`${import.meta.env.VITE_url}/codeverification`, {
        email: reset_email.value,
        code: parseInt(secrete_code.value),
      })
      .then((response) => {
        secrete_code.value = undefined;
        verification_page.value = true;
        router.push({ name: "passwordreset" });
      })
      .catch((error) => {
        if (error.status == 404) {
          tost.error("Validation code is incorect.");
        }
      });
  }

  // change password
  function chnagePassword() {
    if (change_password1.value !== change_password2.value) {
      tost.error("passwords are not mached");
    } else {
      axios
        .post(`${import.meta.env.VITE_url}/resetpassword`, {
          email: reset_email.value,
          password: change_password1.value,
        })
        .then((response) => {
          if (response.status == 200) {
            router.push({ name: "login" });
          }
        })
        .catch((error) => {
          if (error.status == 404) {
            tost.error("something went wrong. try again !");
          } else if (error.status == 400) {
            tost.error("YOU ARE LOOKS BOT. WE NOT ALLOWED FOR YOU !");
          }
        });
    }
  }

  function removeLoginDetails() {
    // reset selected variables
    email.value = undefined;
    passsword.value = undefined;
  }

  function removeEmail() {
    // reset selected variables
    email.value = undefined;
  }
  function removeSecretecode() {
    // reset selected variables
    secrete_code.value = undefined;
  }

  function removePasswords() {
    // reset selected variables
    change_password1.value = undefined;
    change_password2.value = undefined;
    reset_email.value = undefined;
  }

  function checkAuthontication() {
    // functionality : this is mainly for check all authontication details (email, token)

    // this is for update pinia store from local store and cookie storage
    email.value = localStorage.getItem("email");
    checkCookie();

    // 1. check loged email and cookies and authontication status
    // 2. if one or three not available then redirect to loging page with removing all available values

    if (
      email.value === null ||
      authcookie.value === null ||
      authontication.value === null
    ) {
      email.value = null;
      localStorage.removeItem("email");
      authontication.value = null;
      deleteCookie();
      router.push({ name: "login" });
    }
  }

  function checkCookie() {
    // functionality : check the availability of the token in cookies store and store in pinia store
    // 1. get all cookies
    // 2. select authontication token using key 'user'
    // 3. asign authontication value
    // 4. get authontication token to pinia store
    // 5. if token is not available then, 'authontication' and 'authcookie' set to null
    let allCookei = document.cookie.split("; ");
    let cookieAvailable = ref(false);
    for (let i = 0; i < allCookei.length; i++) {
      if (allCookei[i].startsWith("user")) {
        cookieAvailable.value = true;
        authontication.value = true;
        authcookie.value = allCookei[i].slice(5);
        break;
      }
    }
    if (cookieAvailable.value == false) {
      authontication.value = null;
      authcookie.value = null;
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
        authcookie.value = false;
        break;
      }
    }
  }

  function cleanCredencials() {
    // function : remove all authontication redated data from browser and pinia store
    deleteCookie();
    localStorage.removeItem("email");
    email.value = null;
    authontication.value = null;
  }

  return {
    // all variables
    email,
    reset_email,
    passsword,
    authontication,
    role,
    login,
    secrete_code,
    change_password1,
    change_password2,

    // page direct validation
    email_page,
    verification_page,
    passwordRest_page,

    // HTTPS request
    login,
    emailVerification,
    codeVerification,
    chnagePassword,

    // reset variables due to page chnages
    removeLoginDetails,
    removeEmail,
    removeSecretecode,
    removePasswords,

    // cookies
    checkCookie,
    authcookie,
    deleteCookie,
    checkAuthontication,
    cleanCredencials,
  };
});
