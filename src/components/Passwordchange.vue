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
          v-model="authontication.secrete_code"
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
          v-model="authontication.change_password1"
        />
        <input
          type="password"
          class="user-input"
          placeholder="Re enter password"
          v-model="authontication.change_password2"
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
  // function : check verification code available and send request to API to verify
  // 1. if 'secreate_code' is null send error
  // 2. else send request to 'codeverification'
  // 3. if it is successfull then clearn 'secreate_code' and open password-change window
  // 4. else send error code
  if (authontication.secrete_code != null) {
    axios
      .post(`${import.meta.env.VITE_url}/codeverification`, {
        email: authontication.email,
        code: authontication.secrete_code,
      })
      .then((successfull) => {
        if (successfull.status == 200) {
          //   set secreate_code as undefined
          authontication.secrete_code = undefined;
          uistore.CodeVerify = false;
          uistore.PasswordRest = true;
        }
      })
      .catch((error) => {
        if (error.status == 404) {
          toast.error("incorect secreate code");
        }
      });
  } else {
    toast.error("Enter Valied secreate code");
  }
};

const closePasswordResetWindow = () => {
  // fucntion : close password change popup windows
  uistore.PasswordRest = false;
  uistore.PasswordChangeWindow = false;
};

const confirmPassword = () => {
  // function : change password if authontication details are available and both password correct
  // 1.check authontication
  // 2.check borth password correct
  // 3.if incorrect show error message
  // 4. otherwise send API request
  // 5. if success close window
  // 6.otherwise show error
  authontication.checkAuthontication();
  if (authontication.change_password1 === authontication.change_password2) {
    axios
      .post(`${import.meta.env.VITE_url}/resetpassword`, {
        email: authontication.email,
        password: authontication.change_password1,
      })
      .then((successfull) => {
        if (successfull.status == 200) {
          toast.success("you update passsword successfully !");
          setTimeout(closePasswordResetWindow, 1000);
        }
      })
      .catch((error) => {
        console.log(error);
      });
  } else {
    toast.error("Passwords are not matched");
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
