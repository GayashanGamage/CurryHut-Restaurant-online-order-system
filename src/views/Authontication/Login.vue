<template>
  <div class="level-one-container">
    <div class="level-two-container">
      <div class="level-three-container">
        <div class="level-four-container login-header">
          <p class="login-title">CURRY HUT</p>
        </div>
        <div class="level-four-container login-content">
          <input type="text" class="user-input" placeholder="E mail" />
          <input type="password" class="user-input" placeholder="Password" />
          <p id="password-text" @click="directto('email')">Forget Password ?</p>
          <button id="login-button" @click="directto('setting')">LOGIN</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import router from "@/router";

const directto = (routerName) => {
  router.push(routerName);
};
</script>

<style scoped>
.level-one-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100vw;
  height: 100vh;
  position: absolute;
  bottom: 0;
  top: 0;
  left: 0;
  right: 0;
}
.level-two-container {
  width: 98vw;
  height: 96vh;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 6px;
  background: rgba(207, 244, 206, 0.5);
}
.level-three-container {
  width: 412px;
  height: 336px;
  border-radius: 6px;
  background: #fff;
  box-shadow: 0px 0px 20px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.login-header {
  width: 100%;
  height: 18%;
  border-radius: 6px 6px 0px 0px;
  background: #41b06e;
  display: flex;
  justify-content: center;
  align-items: center;
}
.login-content {
  width: 100%;
  height: 82%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
.login-title {
  color: #fff;
  font-family: "Space Grotesk";
  font-size: 24px;
  font-weight: 700;
}
.user-input {
  font-family: "Space Grotesk";
  width: 305px;
  height: 35px;
  border-radius: 4px;
  border: 0.8px solid #7ac89a;
  background: #fff;
  margin-top: 10px;
  font-size: 20px;
  padding-left: 15px;
}
.user-input::placeholder {
  color: #a0d8b7;
  font-family: "Space Grotesk";
  font-size: 20px;
  font-weight: 300;
}
#password-text {
  font-family: "Space Grotesk";
  color: #41b06e;
  font-family: "Space Grotesk";
  font-size: 13px;
  font-weight: 300;
  align-self: flex-end;
  width: 150px;
  text-align: end;
  margin: 10px 43px 10px 0;
}
#password-text:hover {
  color: #000;
  cursor: pointer;
}
#login-button {
  width: 320px;
  height: 40px;
  flex-shrink: 0;
  color: #41b06e;
  font-family: "Space Grotesk";
  font-size: 20px;
  font-weight: 700;
  border-radius: 4px;
  border: 1px solid #41b06e;
  background: #fff;
}
#login-button:hover {
  background: #41b06e;
  color: #fff;
}
</style>
