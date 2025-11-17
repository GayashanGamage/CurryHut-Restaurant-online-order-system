/* this include two basic auth (signin and signup) */
<template>
  <main>
    <Menubar></Menubar>
    <div class="space"></div>
    <div class="checkout-window">
      <div class="forms">
        <!-- this is for toggle button to switch between self order and oder for others -->
        <div class="checkout-toggle">
          <p class="toggle-text">For me</p>
          <!-- toggle button -->
          <div class="toggle">
            <span class="switch">
              <input id="switch-rounded" type="checkbox" @click="sender()" />
              <label for="switch-rounded"></label>
            </span>
          </div>
          <p class="toggle-text">For other</p>
        </div>
        <!-- customers data form 1 -->
        <div class="delivery-form" id="delivery-form1">
          <h3 class="delivery-form-title">Reciver delivery information</h3>
          <div class="form-content">
            <div class="section-title">
              <h4 class="title">Reciver name</h4>
              <hr class="devider" />
            </div>
            <div class="radio-button-container">
              <div class="radio-button">
                <input type="radio" id="mr" name="title" value="mr" />
                <label for="mr" class="radio-button-text">Mr.</label>
              </div>
              <div class="radio-button">
                <input type="radio" id="mrs" name="title" value="mrs" />
                <label for="mrs" class="radio-button-text">Mrs.</label>
              </div>
              <div class="radio-button">
                <input type="radio" id="miss" name="title" value="miss" />
                <label for="miss" class="radio-button-text">Miss</label>
              </div>
            </div>
            <div class="name-container">
              <input type="text" class="name-input" placeholder="First name" />
              <input type="text" class="name-input" placeholder="Last name" />
            </div>
            <div class="section-title">
              <h4 class="title">Hometown</h4>
              <hr class="devider" />
            </div>
            <!-- delivery locaiton -->
            <div class="radio-button-container">
              <div
                class="radio-button"
                v-for="(item, index) in shopStore.deliveryLocations"
                :key="item.id"
              >
                <input
                  type="radio"
                  :id="item.id"
                  name="town"
                  :value="item.place"
                  class="radio-button-text"
                  @click="changeDeliveryLocation(index)"
                />
                <label :for="item.id">{{ item.place }}</label>
              </div>
            </div>
            <div class="section-title">
              <h4 class="title">Reciver address</h4>
              <hr class="devider" />
            </div>
            <div class="address-container">
              <input
                type="text"
                class="address-input"
                placeholder="Resident Number"
              />
              <input
                type="text"
                class="address-input"
                placeholder="Apartment / Vanue"
              />
              <input type="text" class="address-input" placeholder="City" />
            </div>
            <!-- reciver contact numbr if sender is not a sender  -->
            <div class="section-title">
              <h4 class="title">Reciver Contact Number</h4>
              <hr class="devider" />
            </div>
            <div class="address-container">
              <input
                type="text"
                class="address-input"
                placeholder="Mobile Number"
              />
            </div>
          </div>
        </div>
        <!-- customers data form 2, this is for others' delivery -->
        <div class="delivery-form" v-show="sendForOther">
          <h3 class="delivery-form-title">Sender information</h3>
          <div class="form-content">
            <div class="section-title">
              <h4 class="title">Sender name</h4>
              <hr class="devider" />
            </div>
            <div class="radio-button-container">
              <div class="radio-button">
                <input type="radio" id="mr" name="title2" value="mr" />
                <label for="mr" class="radio-button-text">Mr.</label>
              </div>
              <div class="radio-button">
                <input type="radio" id="mrs" name="title2" value="mrs" />
                <label for="mrs" class="radio-button-text">Mrs.</label>
              </div>
              <div class="radio-button">
                <input type="radio" id="miss" name="title2" value="miss" />
                <label for="miss" class="radio-button-text">Miss</label>
              </div>
            </div>
            <div class="name-container">
              <input type="text" class="name-input" placeholder="First name" />
              <input type="text" class="name-input" placeholder="Last name" />
            </div>
            <div class="section-title">
              <h4 class="title">Sender contact number</h4>
              <hr class="devider" />
            </div>
            <div class="address-container">
              <input
                type="text"
                class="address-input"
                placeholder="Mobile number - 1"
              />
              <input
                type="text"
                class="address-input"
                placeholder="Mobile number -2"
              />
            </div>
          </div>
        </div>
      </div>
      <!-- cart information -->
      <div class="cart">
        <div class="cart-item" v-for="item in mergedOrder" :key="item.name">
          <img :src="item.image" :alt="item.name" class="cart-image" />
          <!-- <div class="cart-image"></div> -->
          <div class="cart-data">
            <div class="data">
              <p class="cart-text cart-title">{{ item.name }}</p>
              <p class="cart-text">{{ item.size }}</p>
              <p class="cart-text">{{ item.quantity }} items</p>
            </div>
            <p class="cart-text">Rs {{ item.quantity * item.price }}</p>
          </div>
        </div>
        <hr class="cart-devider" />
        <div class="cart-summery">
          <p class="delivery">Delivery</p>
          <p class="delivery">
            Rs
            {{
              shopStore.selectDeliveryLocation == null
                ? 0
                : shopStore.selectDeliveryLocation.cost
            }}
          </p>
        </div>
        <hr class="cart-devider" />
        <div class="cart-summery">
          <p class="total">Total</p>
          <p class="total">Rs {{ totalBill }}</p>
        </div>
        <hr class="cart-devider" />
        <div class="payment-type">
          <div class="radio-button">
            <input type="radio" id="cash" name="payment" value="cash" />
            <label for="cash" class="radio-button-text">Cash On Delivery</label>
          </div>
          <div class="radio-button">
            <input type="radio" id="card" name="payment" value="card" />
            <label for="card" class="radio-button-text">Card Payment</label>
          </div>
        </div>
        <button class="checkout-button" :disabled="checkout">Checkout</button>
      </div>
    </div>
    <div class="space"></div>
    <Footer></Footer>
  </main>
</template>

<script setup>
import Footer from "@/components/common/footer.vue";
import Menubar from "@/components/common/menubar.vue";
import { computed, onBeforeMount, ref, watch } from "vue";
import { useFoodStore } from "@/stores/food";
import { useOrderStore } from "@/stores/order";
import router from "@/router";
import { useShopStore } from "@/stores/shop";
import axios from "axios";

// use pinia stores
const foodStore = useFoodStore();
const orderStore = useOrderStore();
const shopStore = useShopStore();

const sendForOther = ref(false); // this is for toggle between self order and order for others
const checkout = ref(false); // this is for enable and disable checkout button

// toggle between self order and order for others
const sender = () => {
  const whoSend = document.getElementById("switch-rounded").checked;
  if (whoSend == false) {
    sendForOther.value = false;
  } else if (whoSend == true) {
    sendForOther.value = true;
  }
};

// merge order data ( merge order and product data )
const mergedOrder = computed(() => {
  return orderStore.order.map((orderItem) => {
    const productItem = foodStore.foodInfo.find(
      (p) => p.id === orderItem.foodid
    );
    return {
      categoryName: productItem.categoryName,
      image: productItem.image,
      name: productItem.name,
      price: orderItem.price,
      quantity: orderItem.quantity,
      size: orderItem.size,
    };
  });
});

// change delivery location
const changeDeliveryLocation = (index) => {
  shopStore.selectDeliveryLocation = shopStore.deliveryLocations[index];
};

// initialize total bill using computed
const totalBill = computed(() =>
  orderStore.order.reduce(
    (sum, orderItem) => sum + orderItem.price * orderItem.quantity,
    0
  )
);

// if no item in your cart - you cannot load this page and get delivery locations
onBeforeMount(() => {
  if (orderStore.order.length == 0) {
    router.push({ name: "home" });
  }
  if (shopStore.deliveryLocations == null) {
    axios
      .get(`${import.meta.env.VITE_url}/delivery/get`)
      .then((response) => {
        shopStore.deliveryLocations = response.data;
      })
      .catch((error) => {
        console.log(error);
      });
  }
});

// if cart is going to be empty - you cannot checkout
watch(orderStore.order, (newValue) => {
  if (newValue.length == 0) {
    checkout.value = true;
  }
});
</script>

<style scoped>
.space {
  height: 10vh;
  width: 100vw;
}
.checkout-window {
  display: flex;
  width: 70%;
  margin-inline: auto;
  align-items: flex-start;
  gap: 39px;
}
.forms {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 20px;
  flex: 3 0 0;
}
/* radio button style by checkout form radio button styling */
.name-container {
  display: flex;
  align-items: center;
  gap: 12px;
  align-self: stretch;
}
.name-input {
  display: flex;
  padding: 6px 8px;
  justify-content: center;
  align-items: center;
  gap: 8px;
  flex: 1 0 0;
  border-radius: 4px;
  border: 1px solid #dadada;
  font-size: 17px;
  outline: none;
}
.name-input::placeholder {
  color: #d6d6d6;
  font-size: 17px;
  font-style: normal;
  font-weight: 300;
  line-height: normal;
}
.address-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 14px;
  align-self: stretch;
}
.address-input {
  display: flex;
  padding: 6px 8px;
  justify-content: center;
  align-items: center;
  gap: 8px;
  align-self: stretch;
  width: 50%;
  border-radius: 4px;
  border: 1px solid #dadada;
  outline: none;
}
.address-input::placeholder {
  color: #d6d6d6;
  font-size: 16px;
  font-style: normal;
  font-weight: 300;
  line-height: normal;
}

/* chekout container styling */
.checkout-toggle {
  display: flex;
  padding: 8px 0px;
  justify-content: center;
  align-items: center;
  gap: 15px;
  align-self: stretch;
  border-radius: 4px;
  background: #fff;
}
.toggle-text {
  color: #000;
  font-size: 16px;
  font-style: normal;
  font-weight: 900;
  line-height: normal;
}
.toggle-button {
  width: 55px;
  height: 30px;
  border-radius: 25px;
  background: #ff8f8f;
}

/* form styling */
.delivery-form {
  display: flex;
  padding: 12px;
  flex-direction: column;
  align-items: flex-start;
  gap: 20px;
  align-self: stretch;
  border-radius: 4px;
  background: #fff;
}
.delivery-form-title {
  color: #000;
  font-size: 16px;
  font-style: normal;
  font-weight: 900;
  line-height: normal;
  align-self: stretch;
}
.form-content {
  display: flex;
  padding: 20px 15px;
  flex-direction: column;
  align-items: flex-start;
  gap: 21px;
  align-self: stretch;
  border-radius: 4px;
  border: 1px solid #ececec;
}
.section-title {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
  align-self: stretch;
}
.title {
  color: #959595;
  font-size: 16px;
  font-style: normal;
  font-weight: 900;
  line-height: normal;
  align-self: stretch;
}
.devider {
  width: 100%;
  height: 1px;
  background: #959595;
  border: none;
}
.radio-button-container {
  display: flex;
  align-items: center;
  gap: 14px;
  align-self: stretch;
  flex-wrap: wrap;
}
/* cart related style */
.cart {
  display: flex;
  padding: 16px 16px;
  flex-direction: column;
  align-items: flex-start;
  gap: 14px;
  flex: 1 0 0;
  background: #fff;
  border-radius: 4px;
  flex: 2 0 0;
}
.cart-item {
  display: flex;
  align-items: flex-end;
  gap: 17px;
  align-self: stretch;
}
.cart-image {
  width: 96px;
  height: 96px;
  background-color: #ff8f8f;
  border-radius: 4px;
  border: none;
}
.cart-data {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  flex: 1 0 0;
}
.data {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 5px;
  flex: 1 0 0;
}
/* .cart-text will not work expectedly */
.cart-text {
  text-align: right;
  color: #000;
  font-size: 16px;
  font-weight: 300;
  flex: 1 0 0;
}
.cart-title {
  font-size: 17px;
  font-weight: 600;
}
.cart-devider {
  width: 100%;
  height: 1px;
  background: #b8b3b3;
  border: 0px;
}
.cart-summery {
  display: flex;
  justify-content: space-between;
  align-items: center;
  align-self: stretch;
}
.delivery {
  color: #000;
  font-size: 20px;
  font-weight: 300;
}
.total {
  color: #000;
  font-size: 20px;
  font-weight: 900;
}
.payment-type {
  display: flex;
  align-items: flex-start;
  align-self: stretch;
}
.radio-button {
  display: flex;
  align-items: center;
  gap: 10px;
  width: fit-content;
  flex: 1 0 0;
  min-width: 150px;
}
.radio-button-text {
  color: #000;
  font-size: 18px;
  font-weight: 300;
}
.checkout-button {
  padding: 8px;
  align-self: stretch;
  border-radius: 4px;
  background: #ff5e5e;
  border: none;
  color: #fff;
  font-size: 20px;
  font-weight: 300;
}
/* toggle button styling */
.switch {
  display: inline-block;
}

.switch input {
  display: none;
}

.switch label {
  display: block;
  width: 50px;
  height: auto;
  padding: 3px;
  border-radius: 15px;
  border: 2px solid #ff5e5e;
  cursor: pointer;
  transition: 0.3s;
}

.switch label::after {
  content: "";
  display: inherit;
  width: 20px;
  height: 20px;
  border-radius: 12px;
  background: #ff5e5e;
  transition: 0.1s;
}

.switch input:checked ~ label {
  border-color: #ff5e5e;
}

.switch input:checked ~ label::after {
  translate: 30px 0;
  background: #ff5e5e;
}

.switch input:disabled ~ label {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
