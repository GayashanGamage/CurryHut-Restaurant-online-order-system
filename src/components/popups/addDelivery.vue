<template>
  <div class="c-level-one-container">
    <div class="c-level-two-container" ref="addDeliveryWindow">
      <div class="c-level-three-container window-header">
        <h3 class="window-title">Add new Delivery location</h3>
      </div>
      <div class="c-level-three-container window-content">
        <div class="user-input-section">
          <div class="user-input-column">
            <p class="info">Delivery place</p>
            <input type="text" class="user-input" placeholder="Nawal" />
          </div>
          <div class="user-input-column">
            <p class="info">Price</p>
            <input type="text" class="user-input" placeholder="100.00" />
          </div>
          <div class="button-container">
            <button class="action-btn">Confirm</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useUiStore } from "@/stores/ui";
import { onClickOutside } from "@vueuse/core";
import { ref } from "vue";
const uiStore = useUiStore();

const addDeliveryWindow = ref(null);

onClickOutside(addDeliveryWindow, () => {
  uiStore.addDeliveryPopup = false;
});
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
  width: 466px;
  height: 253px;
  border-radius: 6px;
  background: #fff;
}
.window-header {
  height: 60px;
  border-radius: 6px 6px 0px 0px;
  background: #41b06e;
  display: flex;
  justify-content: center;
  align-items: center;
}
.window-content {
  height: 80%;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.window-title {
  display: inline;
  color: #fff;
  font-family: "Space Grotesk";
  font-size: 20px;
  font-weight: 400;
  text-transform: uppercase;
}
.user-input-section {
  display: flex;
  width: 80%;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-block: auto;
}
.user-input-column {
  display: flex;
  align-items: center;
  gap: 10px;
  align-self: stretch;
}
.info {
  color: #000;
  text-align: right;
  font-family: "Space Grotesk";
  font-size: 16px;
  font-weight: 300;
  flex: 1 0 0;
}
.user-input {
  width: 50%;
  padding: 8px 8px;
  border-radius: 4px;
  border: 0.5px solid #41b06e;
}
.user-input::placeholder {
  color: #bababa;
  font-family: "Space Grotesk";
  font-size: 16px;
  font-style: normal;
  font-weight: 300;
  line-height: normal;
}
.button-container {
  width: 100%;
}
.action-btn {
  display: flex;
  width: 55%;
  padding: 6px 8px;
  justify-content: center;
  align-items: center;
  border-radius: 4px;
  border: 0.5px solid #41b06e;
  background: white;
  color: #41b06e;
  font-family: "Space Grotesk";
  font-size: 16px;
  font-weight: 500;
  margin-left: auto;
}
.action-btn:hover {
  background: #67c08b;
  color: white;
}
.action-btn:active {
  background: #41b06e;
  color: white;
}
</style>
