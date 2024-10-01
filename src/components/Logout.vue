<template>
  <div class="c1-level-one-container">
    <div class="c1-level-two-container">
      <p class="warning-message">
        Are you sure you want to Log out from CURRY HUT Admin pannel ?
      </p>
      <div class="button-list">
        <button class="action-button cancel" @click="uistore.closeLogoutPopup">
          Cancel
        </button>
        <button class="action-button confirm" @click="logout">Confirm</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import router from "@/router";
import { useUiStore } from "@/stores/ui";
import { onBeforeUnmount } from "vue";

const uistore = useUiStore();

const logout = () => {
  router.push("login");
};

onBeforeUnmount(() => {
  if (uistore.logoutPopupWindow === true) {
    uistore.logoutPopupWindow = false;
  }
});
</script>

<style scoped>
.c1-level-one-container {
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
.c1-level-two-container {
  width: 466px;
  height: 253px;
  border-radius: 6px;
  background: #fff;
}
.warning-message {
  color: #41b06e;
  text-align: center;
  font-family: "Space Grotesk";
  font-size: 24px;
  font-style: normal;
  font-weight: 700;
  line-height: normal;
  width: 342px;
  height: 86px;
  flex-shrink: 0;
  margin: 40px 62px;
}
.button-list {
  width: 303px;
  display: flex;
  justify-content: space-between;
  margin: 0px 80px;
}
.action-button {
  width: 132px;
  height: 40px;
  border-radius: 4px;
  background: #fff;
  font-family: "Space Grotesk";
  font-size: 20px;
  font-weight: 700;
}
.cancel {
  color: #41b06e;
  border: 1px solid #41b06e;
}
.cancel:hover {
  color: #fff;
  background-color: #41b064;
  border: 1px solid #41b06e;
}
.confirm {
  color: #ff204e;
  border: 1px solid #ff204e;
}
.confirm:hover {
  color: #fff;
  background-color: #ff204e;
  border: 1px solid #ff204e;
}
</style>
