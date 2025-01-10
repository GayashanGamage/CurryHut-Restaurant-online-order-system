import { ref, computed } from "vue";
import { defineStore } from "pinia";
import "vue-toast-notification/dist/theme-sugar.css";

export const useAuthonticationStore = defineStore("authontication", () => {
  // cookies data
  const cookies_token = ref(null);

  // local storage
  const local_storage_email = ref(null);

  // session storage - this is only use for password reset matter
  const session_storage_email = ref(null);

  // login data
  const login_email = ref(null);
  const login_password = ref(null);

  // change password data
  const secreate_code = ref(null);

  // loging functions
  const storeJTW = (token) => {
    /* store jwt token in local storage and pinia store */
    document.cookie = `token=${token}; expires=Thu, 18 Dec 2026 12:00:00 UTC`;
    cookies_token.value = token;
  };

  const removeJTW = () => {
    /* remove jwt token from local storage and pinia store */
    document.cookie = `token=; expires=Thu, 01 Jan 1970 00:00:00 UTC`;
    cookies_token.value = null;
  };

  const storeEmail = (email) => {
    /* store email in local storage and pinia store */
    localStorage.setItem("email", email);
    local_storage_email.value = email;
  };

  const removeEmail = () => {
    /* remove email from local storage and pinia store */
    localStorage.removeItem("email");
    local_storage_email.value = null;
  };

  const restoreCredentials = () => {
    /* restore credentials from cookies store and local storage to pinia store 
      if credentials are availabe - return true
      else - return false
    */

    // get all cookies and find the 'token' from that and restore to pinia
    const cookies = document.cookie.split("; ");
    for (const cookie of cookies) {
      const [key, value] = cookie.split("=");
      if (key === "token") {
        cookies_token.value = value;
      }
    }

    // restore email from local storage to pinia
    local_storage_email.value = localStorage.getItem("email");

    // if one of the data is not available then remove all from local store, cookies and pinia store
    if (cookies_token.value == null || local_storage_email.value == null) {
      removeJTW();
      removeEmail();
      return false;
    } else {
      return true;
    }
  };

  const storeCredencial = (email, token) => {
    /* store email and token in local storage and cookies */
    storeEmail(email);
    storeJTW(token);
  };

  const removeCredentials = () => {
    /* remove credentials from cookies store, local storage and pinia store */
    removeJTW();
    removeEmail();
  };

  return {
    cookies_token,
    local_storage_email,
    session_storage_email,
    login_email,
    login_password,
    secreate_code,
    storeCredencial,
    restoreCredentials,
    removeCredentials,
  };
});
