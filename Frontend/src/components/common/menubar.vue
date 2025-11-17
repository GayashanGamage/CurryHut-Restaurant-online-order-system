<template>
  <div class="main-container">
    <h3 class="site-title">
      <router-link to="/">Curry Hut</router-link>
    </h3>
    <div class="menu">
      <p class="menu-item">
        <router-link to="/">Main dish</router-link>
      </p>
      <p class="menu-item">
        <router-link to="/extra">extra potion</router-link>
      </p>
      <p class="menu-item">
        <router-link to="/decert">decert</router-link>
      </p>
      <p class="menu-item">
        <router-link to="/drinks">drinks</router-link>
      </p>
      <router-link to="/mobile">
        <button class="action-button">Track order</button></router-link
      >
      <router-link to="/order">
        <span class="material-icons">local_mall</span>
        <span class="oreder-count" v-if="orderStore.orderCount">
        {{ orderStore.orderCount }}</span>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { useOrderStore } from "@/stores/order";
import { watch } from "vue";


const orderStore = useOrderStore(); 

watch(orderStore.order,(newVal) => {
  if(newVal.length > 0 && newVal.length < 10){
    orderStore.orderCount = newVal.length;
    orderStore.moreOrder = false;
  }else if(newVal.length >= 10){
    orderStore.orderCount = '+9';
  }else if(newVal.length === 0){
    orderStore.orderCount = 0;
  }
})


</script>

<style scoped>
.main-container {
  display: flex;
  width: auto;
  padding: 8px 60px;
  justify-content: space-between;
  align-items: center;
  background: #ff5e5e;
}
.site-title {
  color: #fff;
  font-size: 32px;
  font-style: normal;
  font-weight: 900;
  line-height: normal;
  flex: 1 0 0;
}
.menu {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex: 1 0 0;
}
.menu-item {
  color: #fff;
  font-size: 18px;
  font-style: normal;
  font-weight: 300;
  line-height: normal;
  text-transform: uppercase;
}
a {
  text-decoration: none;
  color: #fff;
}
.menu-item:hover {
  font-weight: 500;
  cursor: context-menu;
}
.action-button {
  display: flex;
  padding: 6px 19px;
  justify-content: center;
  align-items: center;
  gap: 8px;
  border-radius: 4px;
  border: 1.5px solid #fff;
  background: #ff5e5e;
  color: #fff;
  font-size: 16px;
  font-style: normal;
  font-weight: 500;
  line-height: normal;
  cursor: pointer;
}
.action-button:hover {
  border: 1.5px solid #fff;
  background: #fff;
  color: #ff5e5e;
}
.material-icons {
  color: #fff;
  cursor: pointer;
}
.oreder-count{
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 50px;
  border: 2px solid #fff;
}
</style>
