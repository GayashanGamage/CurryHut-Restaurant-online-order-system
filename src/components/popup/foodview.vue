<template>
  <div class="main-popup" v-if="uiStore.foodPopup">
    <div class="popup-window" ref="target">
      <img
        alt="rice and curry"
        src="https://curryhut.blr1.cdn.digitaloceanspaces.com/sample-images/koththu.webp"
        class="image"
      />
      <div class="popup-content">
        <h3 class="window-title">
          {{ foodStore.selectedFood.name }}
        </h3>
        <p class="description">
          {{ foodStore.selectedFood.description }}
        </p>
        <div class="sub-section-portion">
          <div class="sub-sub-section">
            <h4 class="section-title">Size</h4>
            <hr class="sub-section-devider" />
            <div class="button-container">
              <button
                v-for="(item, index) in foodStore.selectedFood.price"
                :key="item.name"
                @click="changeFoodSize(item, index)"
                :class="[
                  'action-button',
                  foodStore.selectedPotion === index
                    ? 'action-button-select'
                    : '',
                ]"
                >
                {{ item.name }}
              </button>  
            </div>
          </div>
          <div class="sub-sub-section">
            <h4 class="section-title">Enought</h4>
            <hr class="sub-section-devider" />
            <p class="portion">
              for {{ foodStore.portion }} person
            </p>
          </div>
        </div>
        <div class="sub-section">
          <h4 class="section-title">Price</h4>
          <hr class="sub-section-devider" />
          <p class="price">
            Rs.{{ foodStore.price }}
          </p>
        </div>
        <div class="sub-section">
          <h4 class="section-title">Quantity</h4>
          <hr class="sub-section-devider" />
          <div class="sub-section-container">
            <button class="quntity-change" @click="quntityChange('add')">
              +
            </button>
            <p class="quantity">{{ orderStore.temparyOrderItem.quantity }}</p>
            <button class="quntity-change" @click="quntityChange('sub')">
              -
            </button>
          </div>
        </div>
        <div class="sub-section">
          <p class="red-notice" v-if="!foodStore.selectedFood.availability">out of stock</p>
          <button class="cart-button" @click="addtocart" :disabled="!foodStore.selectedFood.availability">Add to cart</button>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
/*
HOW THIS WORK
  1. load data from food store - selectedFood
  2. load same data to order store - temparyOrderItem
  3. price and size change in order store - temparyOrderItem
  4. all ui designs base on food store - selectedFood
*/
console.log('try to fetch')
// import necesary packages
import { useFoodStore } from "@/stores/food";
import { useOrderStore } from "@/stores/order";
import { useUiStore } from "@/stores/ui";
import { onClickOutside } from "@vueuse/core";
import { ref } from "vue";
import { useToast } from "vue-toast-notification";

// reactive variables ---------------------------------
// define pinia stores
const foodStore = useFoodStore();
const orderStore = useOrderStore();
const uiStore = useUiStore();

// define notification
const toast = useToast();

// outside click refference
const target = ref(null);

const portion = ref(0)
const price = ref(0)

// functions ------------------------------------------
// remove tempary order item when popup closed
const removeTemparyOrderItem = () => {
  orderStore.temparyOrderItem = undefined;
  foodStore.selectedFood = null;
  foodStore.selectedPotion = 0;
};

// outside click and close the popup
onClickOutside(target, (onclick) => {
  uiStore.foodPopup = false;
  foodStore.portion = 0
  foodStore.price = 0
  removeTemparyOrderItem();
});

// this is for add item to cart and close the popup
const addtocart = () => {
  orderStore.order.push(orderStore.temparyOrderItem);
  removeTemparyOrderItem();
  toast.open({
    message: "Item added to cart successfully",
    type: "success",
  });
  uiStore.foodPopup = false;
};

// quntity change - set min for 1
const quntityChange = (type) => {
  if (type === "add") {
    orderStore.temparyOrderItem.quantity += 1;
  } else if (type === "sub") {
    if (orderStore.temparyOrderItem.quantity === 1) {
      orderStore.temparyOrderItem.quantity = 1;
    } else {
      orderStore.temparyOrderItem.quantity -= 1;
    }
  }
};

const changeFoodSize = (item, index) => {
  console.log(index)
  // set css animation of the selected portion
  foodStore.selectedPotion = index;

  // change the price and poortion in the popup window
  foodStore.price = item.price
  foodStore.portion = item.portion

  // change the price and poortion in the order store
  orderStore.temparyOrderItem.price = item.price
  orderStore.temparyOrderItem.size = item.name
};

</script>

<style scoped>
.main-popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  z-index: 10;
}
.popup-window {
  display: flex;
  width: calc(60% - 24px);
  padding: 12px;
  justify-content: flex-start;
  align-items: center;
  gap: 30px;
  border-radius: 6px;
  background: #fff;
  margin-inline: auto;
  margin-top: 100px;
}
.image {
  width: 50%;
  height: auto;
  object-fit: cover;
  border-radius: 4px;
}
.popup-content {
  display: flex;
  width: 45%;
  height: auto;
  flex-direction: column;
  align-items: center;
  gap: 30px;
}
.window-title {
  color: #000;
  font-size: 22px;
  font-weight: 900;
  text-transform: uppercase;
  align-self: stretch;
}
.description {
  color: #000;
  font-size: 18px;
  font-style: normal;
  font-weight: 300;
  align-self: stretch;
}
.sub-section {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 6px;
  align-self: stretch;
}
/* efected */
.sub-section-portion {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  gap: 40px;
  align-self: stretch;
}
.sub-section-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
  align-self: stretch;
}
.section-title {
  color: #c6c2c2;
  font-size: 14px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
  align-self: stretch;
}
.sub-section-devider {
  width: 100%;
  height: 1px;
  background: #c6c2c2;
  border: 0px;
}
.sub-section-container {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 14px;
}
.action-button {
  display: flex;
  padding: 6px 14px;
  justify-content: center;
  align-items: center;
  border-radius: 4px;
  border: 1px solid #ff5e5e;
  background: #fff;
  color: #ff5e5e;
  font-size: 16px;
  font-weight: 400;
  line-height: normal;
}
.action-button-select {
  border: 1px solid #ff5e5e;
  background: #ff5e5e;
  color: #fff;
}
.portion {
  color: #ff5e5e;
  font-size: 16px;
  font-style: normal;
  font-weight: 600;
  line-height: 50px;
}
.price {
  color: #000;
  font-size: 24px;
  font-style: normal;
  font-weight: 600;
  line-height: normal;
  text-transform: capitalize;
}
.sub-section-container {
  display: flex;
  align-items: center;
  gap: 13px;
}
.quntity-change {
  width: 35px;
  height: 35px;
  border-radius: 4px;
  background: #fff;
  border: 0px;
  color: #000;
  font-size: 27.031px;
  font-weight: 400;
  color: #ff5e5e;
  border: 1px solid #ff5e5e;
}
.quntity-change:hover {
  background: #ff5e5e;
  color: #fff;
}
.quantity {
  color: #000;
  font-size: 24px;
  font-style: normal;
  font-weight: 600;
  line-height: normal;
}
.cart-button {
  display: flex;
  height: 36px;
  padding: 5px 85px;
  justify-content: center;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
  align-self: stretch;
  border-radius: 4px;
  background: #ff8f8f;
  color: #fff;
  font-size: 18px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
  border: 0px;
}
.cart-button:hover {
  background: #ff7878;
}
.cart-button:active {
  background: #ff5e5e;
}
.cart-button:disabled{
  background: #d5d5d5;
  color: #fff;
  font-weight: 400;
  cursor: not-allowed;
}
.button-container{
  margin-block: 8px;
  display: flex;
  flex-direction: row;
  gap: 6px;
}
.red-notice{
  background-color: var(--notice-red);
  color: #FFF;
  padding: 2px 20px;
  font-size: 12px;
  border-radius: 10px;
}
</style>
