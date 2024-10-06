<template>
  <div class="level-one-container">
    <div class="level-two-container">
      <div class="dummy menu">
        <Menubar></Menubar>
      </div>
      <div class="dummy content">
        <router-view></router-view>
      </div>
    </div>
    <Logout v-if="uistore.logoutPopupWindow"></Logout>
    <Passwordchange v-if="uistore.PasswordChangeWindow"></Passwordchange>
  </div>
</template>

<script setup>
import Menubar from "@/components/Menubar.vue";
import Logout from "@/components/Logout.vue";
import { useUiStore } from "@/stores/ui";
import Passwordchange from "@/components/Passwordchange.vue";

const uistore = useUiStore();
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
  display: grid;
  grid-template-columns: 1fr 4fr;
  grid-template-rows: auto;
  grid-template-areas: "menu content";
  grid-gap: 10px;
}
.menu {
  grid-area: menu;
}
</style>
