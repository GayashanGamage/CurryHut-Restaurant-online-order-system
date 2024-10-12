<template>
  <div class="c-level-one-container">
    <h2 class="shop-title">CURRY HUT</h2>
    <div
      class="menu-item select"
      id="menu-one"
      @click="changePage('menu-one', 'select-text-one')"
    >
      <p class="menu-text select-text" id="select-text-one">Orders</p>
    </div>
    <div
      class="menu-item"
      id="menu-two"
      @click="changePage('menu-two', 'select-text-two')"
    >
      <p class="menu-text" id="select-text-tow">Menu</p>
    </div>
    <div
      class="menu-item"
      id="menu-three"
      @click="changePage('menu-three', 'select-text-three')"
    >
      <p class="menu-text" id="select-text-three">Food item</p>
    </div>
    <div
      class="menu-item"
      id="menu-four"
      @click="changePage('menu-four', 'select-text-four', 'category')"
    >
      <p class="menu-text" id="select-text-four">Category</p>
    </div>
    <div
      class="menu-item"
      id="menu-five"
      @click="changePage('menu-five', 'select-text-five')"
    >
      <p class="menu-text" id="select-text-five">Statistics</p>
    </div>
    <div
      class="menu-item"
      id="menu-six"
      @click="changePage('menu-six', 'select-text-six', 'setting')"
    >
      <p class="menu-text" id="select-text-six">Site setting</p>
    </div>
    <p class="logout" @click="uistore.openLogoutPopup">Sign out</p>
    <div class="message-container" v-if="shopstore.shutdown">
      <p class="message-text">Shop is currently closed</p>
    </div>
  </div>
</template>

<script setup>
import router from "@/router";
import { useShopStore } from "@/stores/shop";
import { useUiStore } from "@/stores/ui";

const uistore = useUiStore();
const shopstore = useShopStore();

const changePage = (divElementID, textElementID, url) => {
  // select all list from menu
  var all = document.getElementsByClassName("menu-item");
  var alltext = document.getElementsByClassName("menu-text");

  // remove all existing style from previose selected items
  for (let i = 0; i < all.length; i++) {
    all[i].classList.remove("select");
  }

  for (let j = 0; j < alltext.length; j++) {
    alltext[j].classList.remove("select-text");
  }

  // add style to newly selected items
  document.getElementById(divElementID).classList.add("select");
  document.getElementById(textElementID).classList.add("select-text");

  // load sub-page
  router.push({ name: url });
};
</script>

<style scoped>
.c-level-one-container {
  background-color: #41b06e;
  width: 100%;
  height: 96vh;
  border-radius: 6px;
  position: sticky;
  top: 0;
  display: flex;
  flex-direction: column;
}
.shop-title {
  color: #fff;
  font-family: Spartan;
  font-size: 24px;
  font-style: normal;
  font-weight: 300;
  line-height: normal;
  font-family: "Space Grotesk";
  margin: 68px 0px 60px 78px;
}
.select {
  width: 358px;
  height: 49px;
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.39);
}
.menu-text {
  color: #fff;
  font-family: "Space Grotesk";
  font-size: 20px;
  font-weight: 300;
  line-height: normal;
  text-transform: capitalize;
  margin: 9px 0px 9px 78px;
}
.select-text {
  font-weight: 700;
}
.logout {
  color: #fff;
  font-family: "Space Grotesk";
  font-size: 24px;
  font-weight: 700;
  margin: 124px 0px 0px 78px;
}
.menu-item:hover {
  background-color: rgba(245, 239, 255, 0.2);
  cursor: pointer;
}
.message-container {
  background-color: #000;
  height: 40px;
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  border-radius: 0px 0px 8px 8px;
  display: flex;
  align-items: center;
}
.message-text {
  color: #fff;
  font-family: "Space Grotesk";
  font-size: 16px;
  font-weight: 700;
  margin-left: 78px;
}
</style>
