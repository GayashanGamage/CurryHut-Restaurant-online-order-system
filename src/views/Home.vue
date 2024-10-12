<template>
  <div class="level-one-container">
    <div class="level-two-container">
      <div class="menu">
        <Menubar></Menubar>
      </div>
      <div class="content">
        <router-view></router-view>
      </div>
    </div>
    <Logout v-if="uistore.logoutPopupWindow"></Logout>
    <Passwordchange v-if="uistore.PasswordChangeWindow"></Passwordchange>
    <Timechange v-if="uistore.TimeChangeWindow"></Timechange>
    <Newcategory v-if="uistore.NewCategoryWindow"></Newcategory>
    <Deletecategory v-if="uistore.DeleteCategoryWindow"></Deletecategory>
    <Editcategory v-if="uistore.EditCategoryWindow"></Editcategory>
  </div>
</template>

<script setup>
import Menubar from "@/components/Menubar.vue";
import Logout from "@/components/Logout.vue";
import { useUiStore } from "@/stores/ui";
import Passwordchange from "@/components/Passwordchange.vue";
import Timechange from "@/components/Timechange.vue";
import Newcategory from "@/components/Newcategory.vue";
import Deletecategory from "@/components/Deletecategory.vue";
import Editcategory from "@/components/Editcategory.vue";

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

<style>
.page-title {
  color: #41b06e;
  font-family: "Space Grotesk";
  font-size: 32px;
  font-weight: 700;
  padding: 53px 0px 0px 19px;
}
.s-level-one-container {
  background: rgba(207, 244, 206, 0.5);
  width: 100%;
  height: auto;
  border-radius: 6px;
  padding-bottom: 12px;
}
.s-level-two-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: auto;
}
.s-level-three-container {
  width: 98%;
  height: auto;
  border-radius: 6px;
  background: #fff;
  margin-top: 26px;
}
.action-button {
  font-size: 18px;
  border-radius: 4px;
  border: 1.5px solid #41b06e;
  background: #fff;
  color: #41b06e;
  font-family: "Space Grotesk";
  font-size: 18px;
  font-weight: 400;
  padding: 4px 18px;
  width: fit-content;
  height: 34px;
}
.action-button:hover {
  background: #41b06e;
  color: #fff;
}
</style>
