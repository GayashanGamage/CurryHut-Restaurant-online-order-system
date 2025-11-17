/* this include two basic auth (signin and signup) */
<template>
  <main>
    <Menubar></Menubar>
    <div class="space"></div>
    <div class="summery-window">
      <div class="order-section">
        <h3 class="section-title">Pending orders</h3>
        <hr class="section-devider" />
        <div class="section-content">
          <div class="section-row">
            <p class="head" id="cell1">Oder number</p>
            <p class="head" id="cell2">Oder time</p>
            <p class="head" id="cell3">Payment</p>
            <p class="head" id="cell4">Payment</p>
          </div>
          <div
            class="section-row"
            v-for="(order, index) in pending"
            :key="index"
          >
            <p class="data" id="cell1">{{ order.id }}</p>
            <p class="data" id="cell2">{{ order.orderdate }}</p>
            <p class="data" id="cell3">{{ order.payment }}</p>
            <button class="section-data-button" id="cell4">More</button>
          </div>
        </div>
      </div>
      <div class="order-section">
        <h3 class="section-title">Completed orders</h3>
        <hr class="section-devider" />
        <div class="section-content">
          <div class="section-row">
            <p class="head" id="cell1">Oder number</p>
            <p class="head" id="cell2">Oder time</p>
            <p class="head" id="cell3">Payment</p>
            <p class="head" id="cell4">Payment</p>
          </div>
          <div
            class="section-row"
            v-for="(order, index) in completed"
            :key="index"
          >
            <p class="data" id="cell1">{{ order.id }}</p>
            <p class="data" id="cell2">{{ order.orderdate }}</p>
            <p class="data" id="cell3">{{ order.payment }}</p>
            <button class="section-data-button" id="cell4">More</button>
          </div>
        </div>
      </div>
    </div>
    <div class="space"></div>
    <Footer></Footer>
  </main>
</template>

<script setup>
import Footer from "@/components/common/footer.vue";
import Menubar from "@/components/common/menubar.vue";
import { useOrderStore } from "@/stores/order";
import { computed } from "vue";
const orderStore = useOrderStore();

const pending = computed(() => {
  return orderStore.summery.filter((order) => order.status === "pending");
});

const completed = computed(() => {
  return orderStore.summery.filter((order) => order.status === "complete");
});
</script>

<style scoped>
.space {
  height: 10vh;
  width: 100vw;
}
.summery-window {
  display: flex;
  width: 45%;
  padding: 20px;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 30px;
  border-radius: 6px;
  background: #fff;
  margin-inline: auto;
}
.order-section {
  display: flex;
  gap: 6px;
  height: fit-content;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  align-self: stretch;
}
.section-title {
  color: #b2b2b2;
  font-size: 16px;
  font-style: normal;
  font-weight: 900;
  line-height: normal;
  align-self: stretch;
}
.section-devider {
  width: 100%;
  height: 1px;
  background: #ddd;
  border: none;
}
.section-content {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 15px;
  align-self: stretch;
}
.section-row {
  display: flex;
  /* justify-content: space-between; */
  align-items: center;
  align-self: stretch;
}
.head {
  color: #000;
  font-size: 16px;
  font-style: normal;
  font-weight: 900;
  line-height: normal;
}
#cell1 {
  width: 20%;
}
#cell2 {
  width: 30%;
}
#cell3 {
  width: 30%;
}
#cell4 {
  width: 20%;
}
.data {
  color: #000;
  font-size: 18px;
  font-style: normal;
  font-weight: 300;
  line-height: normal;
}
.section-data-button {
  display: flex;
  padding: 8px 30px;
  justify-content: center;
  align-items: center;
  border-radius: 4px;
  background: #ff9e9e;
  color: #fff;
  font-size: 16px;
  font-weight: 400;
  border: none;
}
.section-data-button:hover {
  background: #ff7e7e;
}
.section-data-button:active {
  background: #ff5e5e;
}
</style>
