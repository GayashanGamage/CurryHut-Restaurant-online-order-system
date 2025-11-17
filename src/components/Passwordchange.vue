<template>
  <div class="c-level-one-container">
    <div class="c-level-two-container" v-if="uistore.CodeVerify">
      <div class="c-level-three-container window-header">
        <p class="window-title">VERIFY CODE</p>
      </div>
      <div class="c-level-three-container login-content">
        <P class="info">Check your email</P>
        <input
          type="text"
          class="user-input"
          placeholder="Code"
          v-model="authontication.secreate_code"
        />
        <button id="login-button" @click="verifyCode">VERIFY</button>
      </div>
    </div>
    <div class="c1-level-two-container" v-if="uistore.PasswordRest">
      <div class="c1-level-three-container window-header">
        <p class="window-title">change password</p>
      </div>
      <div class="c1-level-three-container window-content">
        <input
          type="password"
          class="user-input"
          placeholder="New password"
          v-model="authontication.login_password.one"
        />
        <input
          type="password"
          class="user-input"
          placeholder="Re enter password"
          v-model="authontication.login_password.two"
        />
        <button id="login-button" @click="confirmPassword">Set password</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthonticationStore } from "@/stores/authontication";
import { useUiStore } from "@/stores/ui";
import axios from "axios";
import { useToast } from "vue-toast-notification";

const toast = useToast();

// pinia stors
const uistore = useUiStore();
const authontication = useAuthonticationStore();

const verifyCode = () => {
  axios.post(`${import.meta.env.VITE_url}/codeverification`, {
    email: authontication.local_storage_email,
    code: authontication.secreate_code,
  }).then((res) => {
    console.log(res);
    if (res.status == 200) {
      uistore.PasswordRest = true;
      uistore.CodeVerify = false;
      authontication.login_password = {
        'one' : null,
        'two' : null
      }
    }
  }).catch((err) => {
    toast.error("Invalid token");
    uistore.PasswordChangeWindow = false; // this is for close the window
  });
};

const confirmPassword = () => {
  if(authontication.login_password.one == authontication.login_password.two){
    axios.post(`${import.meta.env.VITE_url}/resetpassword`, {
      email: authontication.local_storage_email,
      password: authontication.login_password.one,
    }).then((res) => {
      if (res.status == 200) {
        uistore.PasswordRest = false;
        toast.success("Password changed successfully");
        uistore.PasswordChangeWindow = false; // this is for close the window
        authontication.login_password = null; 
      }
    }).catch((err) => {
      toast.error("something go wrong");
      uistore.PasswordChangeWindow = false; // this is for close the window
      authontication.login_password = null;
    });
  }
  else{
    toast.error("Password not match");
  }
};
</script>

<style scoped>
.c-level-one-container {
  background-color: rgba(24, 28, 20, 0.8);
  width: 100vw;
  height: 100vh;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  position: fixed;
  display: flex;
  justify-content: center;
  align-items: center;
}
.c-level-two-container {
  width: 448px;
  height: 313px;
  border-radius: 6px;
  background: #fff;
}
.window-header {
  width: 448px;
  height: 60px;
  border-radius: 6px 6px 0px 0px;
  background: #41b06e;
  display: flex;
  justify-content: center;
  align-items: center;
}
.window-title {
  display: inline;
  color: #fff;
  font-family: "Space Grotesk";
  font-size: 24px;
  font-weight: 700;
  text-transform: uppercase;
}
.info {
  color: #41b06e;
  font-family: "Space Grotesk";
  font-size: 12px;
  font-style: normal;
  font-weight: 300;
  line-height: normal;
  align-self: flex-start;
  margin: 0px 0px 10px 63px;
}
.c-level-three-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.login-content {
  height: 250px;
}
.user-input {
  width: 290px;
  height: 35px;
  border-radius: 4px;
  border: 0.8px solid #7ac89a;
  background: #fff;
  margin-bottom: 10px;
  padding: 0px 15px;
  color: #41b06e;
  font-family: "Space Grotesk";
  font-size: 20px;
  font-weight: 300;
}
.user-input::placeholder {
  color: #a0d8b7;
  font-family: "Space Grotesk";
  font-size: 20px;
  font-weight: 300;
}
#login-button {
  width: 320px;
  height: 40px;
  border-radius: 4px;
  border: 1px solid #41b06e;
  background: #fff;
  color: #41b06e;
  font-family: "Space Grotesk";
  font-size: 20px;
  font-weight: 700;
  margin-top: 20px;
}
#login-button:hover {
  border: 1px solid #41b06e;
  background: #41b06e;
  color: #fff;
}
/* password reset window */
.c1-level-two-container {
  width: 448px;
  height: 312px;
  border-radius: 6px;
  background: #fff;
}
.window-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding-top: 40px;
}
</style>
