import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import router from "@/router";
import { useToast } from "vue-toast-notification";
import "vue-toast-notification/dist/theme-sugar.css";

const tost = useToast();

export const useAuthonticationStore = defineStore("authontication", () => {
  const email = ref(undefined);
  const reset_email = ref(undefined);
  const passsword = ref(undefined);
  const authontication = ref(false);
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
      })
      .then((response) => {
        if (response.status == 200) {
          authontication.value = true;
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
    email.value = undefined;
    passsword.value = undefined;
  }

  function removeEmail() {
    email.value = undefined;
  }
  function removeSecretecode() {
    secrete_code.value = undefined;
  }

  function removePasswords() {
    change_password1.value = undefined;
    change_password2.value = undefined;
    reset_email.value = undefined;
  }

  function checkCookie() {
    console.log("this is for cookies");
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
  };
});
