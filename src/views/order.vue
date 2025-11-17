/* this include two basic auth (signin and signup) */
<template>
  <main>
    <Menubar></Menubar>
    <div class="space"></div>
    <div class="order-window">
      <div class="order-head">
        <p class="head cell1">description</p>
        <p class="head cell2">quantity</p>
        <p class="head cell3">unit price</p>
        <p class="head cell4">sub total</p>
        <p class="head cell5"></p>
      </div>
      <hr class="devider" />
      <div class="order-item" v-for="(item, index) in orderStore.order" :key="index">
        <div class="item-details cell1">
          <img src="https://curryhut.blr1.cdn.digitaloceanspaces.com/sample-images/koththu.webp" alt="item.name" class="item-image" />
          <div class="item-details-data">
            <p class="item-title">{{ item.name }}</p>
            <p class="item-description">{{ item.size }}</p>
            <p class="item-description" v-if="item.rice"><span class="rice-tag">{{ getRice(item.rice) }}</span> with</p>
            <p class="item-description curry-bucket" v-if="item.curry"><span class="curry-tag" v-for="i in item.curry" :key="i">{{ getCurrry(i) }}</span></p>
          </div>
        </div>
        <div class="item-quantity cell2">
          <button
            class="item-quantity-action"
            @click="changeQuantity(index, 'up')"
          >
            +
          </button>
          <!-- if somethign go wrong in style of this change class name -->
          <p class="item-common">{{ item.quantity }}</p>
          <button
            class="item-quantity-action"
            @click="changeQuantity(index, 'down')"
          >
            -
          </button>
        </div>
        <p class="item-common cell3">Rs.{{ item.price }}</p>
        <p class="item-common cell4">
          Rs.{{ parseInt(item.price) * parseInt(item.quantity) }}
        </p>
        <span class="material-icons" @click="deleteItem(index)">delete</span>
      </div>
      <!-- special category promotion -->
      <div
        class="unavailable-category"
        v-if="decert"
        @click="router.push({ name: 'decert' })"
      >
        <p class="unavailable-category-title">DESERT</p>
        <p class="unavailable-category-description">
          FInd flavorable desert after your main meal...
        </p>
      </div>
      <div
        class="unavailable-category"
        v-if="drinks"
        @click="router.push({ name: 'drinks' })"
      >
        <p class="unavailable-category-title">DRINKS</p>
        <p class="unavailable-category-description">
          There are plenty of drinks you can choose...
        </p>
      </div>
      <div
        class="unavailable-category"
        v-if="extra"
        @click="router.push({ name: 'extra' })"
      >
        <p class="unavailable-category-title">EXTRA POTIONS</p>
        <p class="unavailable-category-description">
          with extra curries, you can enjoy your meal better...
        </p>
      </div>
      <hr class="devider" />
      <div class="total">
        <p class="total-text">TOTAL BILL</p>
        <p class="total-text">Rs. {{ totalBill }}</p>
      </div>
      <hr class="devider" />
      <button
        class="order-action-button"
        @click="checkoutCart"
        :disabled="checkoutButton"
      >
        CHECKOUT
      </button>
    </div>
    <div class="space"></div>
    <Footer></Footer>
  </main>
</template>

<script setup>
import Footer from "@/components/common/footer.vue";
import Menubar from "@/components/common/menubar.vue";
import router from "@/router";
import { useAuthonticationStore } from "@/stores/auth";
import { useFoodStore } from "@/stores/food";
// import { useFoodStore } from "@/stores/food";
import { useOrderStore } from "@/stores/order";
import { useUiStore } from "@/stores/ui";
import axios from "axios";
import { computed, onBeforeMount, onMounted, onUpdated, ref, watch } from "vue";
import { useToast } from "vue-toast-notification";
const authStore = useAuthonticationStore()
const uiStore = useUiStore()

// pinia stores
const orderStore = useOrderStore();
const foodstore = useFoodStore();

// toast notification
const notification = useToast()

// other reactive variables
const checkoutButton = ref(true);
const decert = ref(true)
const drinks = ref(true)
const extra = ref(true)

// update visibility of special category section in order page - according to the order
watch(orderStore.order, (newVal) => {
  newVal.find((item) => item.category_id === '670cbd0e6e6b240be2d189e5') ? drinks.value = false : drinks.value = true
  newVal.find((item) => item.category_id === '670cbd156e6b240be2d189e6') ? decert.value = false : decert.value = true
  newVal.find((item) => item.category_id === '67b1baa519f60cfa444a0afc') ? extra.value = false : extra.value = true
})


// enable or disable special category section in order page
onBeforeMount(() => {
  orderStore.order.find((item) => item.category_id === '670cbd0e6e6b240be2d189e5') ? drinks.value = false : drinks.value = true
  orderStore.order.find((item) => item.category_id === '670cbd156e6b240be2d189e6') ? decert.value = false : decert.value = true
  orderStore.order.find((item) => item.category_id === '67b1baa519f60cfa444a0afc') ? extra.value = false : extra.value = true
})

// change quantity of order items in order store
const changeQuantity = (index, arg) => {
  if (arg === "up") {
    orderStore.order[index].quantity += 1;
  } else if (arg === "down") {
    if(orderStore.order[index].quantity > 1) {
      orderStore.order[index].quantity -= 1;
    }
  }
};

// initialize total bill using computed
const totalBill = computed(() =>
  orderStore.order.reduce(
    (sum, orderItem) => sum + orderItem.price * orderItem.quantity,
    0
  )
);

// update total bill when order store updated
// onUpdated(() => {
//   totalBill.value = orderStore.order.reduce(
//     (sum, orderItem) => sum + orderItem.price * orderItem.quantity,
//     0
//   );
// });

function getRice(id) {
  console.log(id)
  return foodstore.plainRice.find((item) => item.id == id).name
}

function getCurrry(id){
  return foodstore.curry.find((item) => item.id == id).name
}

// delete item in order store
const deleteItem = (index) => {
  orderStore.order.splice(index, 1);
};

// action button 
const checkoutCart = () => {
  if(authStore.user_key != null){
    axios.get(`${import.meta.env.VITE_url}/customer/auth/customerKey/${authStore.user_key}`
    ).then((response) => {
      if(response.status.data.status == 1001){
        uiStore.allowMobile = true // this allow dirrect to checkout page while passing other steps
        router.push({ name: "checkout" });
      }else if(response.status.data.status == 1001){
        uiStore.allowVerification = true // this allow dirrect to checkout page while passing other steps
        router.push({ name: "verification" });
      }
    }).catch((err) => {
      if(err.status == 404){
        notification.error("something go wrong - try again later")        
      }else if(err.status == 422){
        notification.error("Enter valied user key")
      }
    })
  }
  else{
    uiStore.allowMobile = true
    router.push({ name: "mobile" });
  }
}

// check if order store is empty, then disable checkout button
watch(orderStore.order, (newValue) => {
  if (newValue.length === 0) {
    checkoutButton.value = true;
  } else {
    checkoutButton.value = false;
  }
});

// check the order length and enable or disable checkout button when page initialized
onBeforeMount(() => {
  if (orderStore.order.length === 0) {
    checkoutButton.value = true;
  } else {
    checkoutButton.value = false;
  }
});

// load user_key from cookies if available
onMounted(() => {
  authStore.loadUserKey()
})

</script>

<style scoped>
.space {
  height: 10vh;
  width: 100vw;
}
.order-window {
  display: flex;
  width: 50%;
  padding: 30px;
  flex-direction: column;
  justify-content: center;
  align-items: flex-end;
  gap: 16px;
  border-radius: 6px;
  background: #fff;
  margin-inline: auto;
}
.order-head {
  display: flex;
  align-items: center;
  align-self: stretch;
}
.head {
  display: flex;
  align-items: center;
}
.devider {
  width: 100%;
  height: 1px;
  background: #d5d5d5;
  border: none;
}
.order-item {
  display: flex;
  align-items: flex-end;
  /* gap: 30px; */
  align-self: stretch;
}
.item-details {
  display: flex;
  align-items: flex-end;
  gap: 10px;
}
.item-image {
  width: 90px;
  height: 90px;
  border-radius: 4px;
  background-color: cornflowerblue;
  border: none;
}
.item-title {
  color: #000;
  font-size: 17px;
  font-weight: 500;
  align-self: stretch;
}
.item-description {
  color: #000;
  font-size: 14px;
  font-weight: 300;
  align-self: stretch;
}
.item-quantity {
  display: flex;
  align-items: center;
  gap: 12px;
  justify-self: stretch;
}
.item-quantity-action {
  display: flex;
  padding: 3px 10px;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-radius: 4px;
  background: #ff8f8f;
  border: none;
  color: #fff;
  text-align: center;
  font-size: 20px;
  font-weight: 400;
  align-self: stretch;
  cursor: pointer;
}
.item-common {
  color: #000;
  font-size: 16px;
  font-style: normal;
  font-weight: 300;
  line-height: normal;
}
.material-icons {
  color: #d9d9d9;
  cursor: pointer;
}
.material-icons:hover {
  color: #ff8f8f;
}
.unavailable-category {
  display: flex;
  padding: 10px 8px;
  flex-direction: column;
  align-items: flex-start;
  gap: 12px;
  align-self: stretch;
  border-radius: 4px;
  border: 1px solid #ff8f8f;
  background: #fff;
  cursor: pointer;
}
.unavailable-category-title {
  color: #b2b2b2;
  font-size: 18px;
  font-weight: 900;
  align-self: stretch;
}
.unavailable-category-description {
  color: #ff8f8f;
  font-size: 16px;
  font-weight: 400;
  align-self: stretch;
}
.total {
  display: flex;
  padding: 0px 8px;
  justify-content: space-between;
  align-items: center;
  align-self: stretch;
}
.total-text {
  color: #000;
  font-size: 20px;
  font-weight: 900;
}
.order-action-button {
  display: flex;
  padding: 6px 40px;
  justify-content: center;
  align-items: center;
  border-radius: 4px;
  background: #ff8f8f;
  color: #fff;
  font-size: 18px;
  font-weight: 300;
  border: none;
  cursor: pointer;
}
.order-action-button:hover {
  background: #f78d8d;
}
.order-action-button:disabled {
  background: #d9d9d9;
  color: #fff;
  cursor: not-allowed;
}
.cell1 {
  width: 56%;
}
.cell2 {
  width: 15%;
}
.cell3 {
  width: 15%;
}
.cell4 {
  width: 10%;
}
.cell5 {
  width: 2%;
}
.rice-tag{
  background-color: #fb8500;
  color: #fff;
  padding: 1px 15px;
  border-radius: 20px;
  font-size: 12px;
}
.curry-bucket{
  margin-top: 4px;
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  gap: 2px;
}
.curry-tag{
  color: #fff;
  background-color: #335c67;
  padding: 2px 10px;
  border-radius: 20px;
  font-size: 12px;
}
</style>
