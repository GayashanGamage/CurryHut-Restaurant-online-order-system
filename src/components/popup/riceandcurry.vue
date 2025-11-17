<template>
  <div class="background" v-if="uistore.riceandcurryPopup">
    <div class="popup-window" ref="target">
      <div class="content">
        <h3 class="popup-title">{{ foodstore.selectedRicePack.name }}</h3>
        <div class="sub-section">
          <div class="section-head">
            <h4 class="section-title">rice section</h4>
            <hr class="section-head-devider">
            <div class="item-container">
              <div class="item" v-for="i in foodstore.plainRice" :key="i.id">
                <p class="item-name">{{ i.name }}</p>
                <p class="red-notice" v-if="!i.availability">out of stock</p>
                <button class="rice-button" :id="i.id" :disabled="!i.availability" @click="addRice(i.id)">Add</button>
              </div>
            </div>
          </div>
        </div>
        <div class="sub-section">
          <div class="section-head">
            <h4 class="section-title">curry section</h4>
            <hr class="section-head-devider">
            <div class="item-container">
              <div class="item" v-for="i in foodstore.curry" :key="i.id">
                <p class="item-name">{{ i.name }}</p>
                <p class="red-notice"  v-if="!i.availability">out of stock</p>
                <button class="curry-button" :id="i.id" :disabled="!i.availability" @click="addCurry(i.id)">Add</button>
              </div>
            </div>
          </div>
        </div>
        <div class="sub-section">
          <div class="section-head">
            <h4 class="section-title">summery</h4>
            <hr class="section-head-devider">
            <!-- TODO: load size of food -->
            <!-- column 01 -->
            <!-- <div class="summery-column">
              <p class="column-title">Porsion size</p>
              <div class="column-data">
                  <button class="column-button" v-for="(item, index) in foodstore.selectedRicePack.price" :key="item.index" @click="verityOptionNumber = index">{{ item.name }}</button>
              </div>
            </div> -->
            <!-- column 02 -->
            <div class="summery-column">
              <p class="column-title">Plate count</p>
              <div class="column-data">
                <button class="column-button" @click="changeQuntity('up')">+</button>
                <p>{{ orderstore.temparyOrderItem.quantity }}</p>
                <button class="column-button" @click="changeQuntity('down')">-</button>
              </div>
            </div>
            <!-- TODO: load total price -->
            <!-- column 03 -->
            <!-- <div class="summery-column">
              <p class="column-title">Total Price</p>
              <div class="column-data">
                <p>{{ packCount * foodstore.selectedRicePack.price[verityOptionNumber].price }}</p>
              </div>
            </div> -->
          </div>
        </div>
        <hr class="section-head-devider">
        <div class="button-section">
          <button class="action-button"  @click="closePopup">Cancel</button>
          <button class="action-button" @click="confirm">Confirm</button>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
// imports
import { useFoodStore } from '@/stores/food';
import { useOrderStore } from '@/stores/order';
import { useUiStore } from '@/stores/ui';
import { onClickOutside } from '@vueuse/core';
import { onBeforeMount, onBeforeUnmount, ref } from 'vue';
import { useToast } from 'vue-toast-notification';

// reactive variables
const target = ref(null)
const uistore = useUiStore()
const foodstore =  useFoodStore()
const maxCurry = ref(4);
const minCurry = ref(3);
const verityOptions = ref(null)
// const packCount = ref(1)
const orderstore = useOrderStore()
const notification = useToast()

onBeforeUnmount(() => {
  orderstore.temparyOrderItem = null
})

// function
const closePopup = () => {
  uistore.riceandcurryPopup = false
}

onClickOutside(target, (onclick) => {
  closePopup()
})

// add rice fucntionality -------- supportives
function removeAllSelectedRice(){
  const allButtons = document.getElementsByClassName('rice-button') // all rice buttons
  for(let i = 0; i < allButtons.length; i++){
    allButtons[i].classList.remove('select') // remove select class
    allButtons[i].textContent = 'Add' // change text 
  }
}

// add rice functionality -------- main 
const addRice = (id) => {
  removeAllSelectedRice()
  const element = document.getElementById(id) // selected element
  element.textContent = 'Selected' // change text content
  element.classList.add('select') // add select class
  orderstore.temparyOrderItem.rice = id // add selected rice
}

// add curry fucntionality -------- supportives
function removeAllSelectedCurry(){
  const allButtons = document.getElementsByClassName('curry-button')
  for(let i = 0; i < allButtons.length; i++){
    allButtons[i].classList.remove('select') // remove select class
    allButtons[i].textContent = 'Add' // change text 
  }
}

function checkCurryList(id){
  const allredyIn = ref(false)
  for(let i = 0; i < orderstore.temparyOrderItem.curry.length; i++){
    if(orderstore.temparyOrderItem.curry[i] == id){
      orderstore.temparyOrderItem.curry.splice(i, 1)
      allredyIn.value = true
    }
  }
  if(allredyIn.value == false){
    if(orderstore.temparyOrderItem.curry.length >= maxCurry.value){
      orderstore.temparyOrderItem.curry.shift()
      orderstore.temparyOrderItem.curry.push(id)
    }else{
      orderstore.temparyOrderItem.curry.push(id)
    }
  }
}

function showSelectedCurries(){
  for(let i = 0; i < orderstore.temparyOrderItem.curry.length; i++){
    const element = document.getElementById(orderstore.temparyOrderItem.curry[i])
    element.textContent = 'Selected'
    element.classList.add('select')
  }
}

// add curry functionality -------- main
const addCurry = (id) => {
  removeAllSelectedCurry() // remove all selected curry style and text content of the button 
  checkCurryList(id) // check 'id' currry is already in the list
  showSelectedCurries()  
}

function changeQuntity(action){
  if(action == 'up'){
    orderstore.temparyOrderItem.quantity += 1
  }else if(action == 'down'){
    if(orderstore.temparyOrderItem.quantity > 1){
      orderstore.temparyOrderItem.quantity -= 1
    }
  }
}

// confirm the order
function confirm (){
  if(orderstore.temparyOrderItem.rice != null && orderstore.temparyOrderItem.curry.length == maxCurry.value){
    orderstore.order.push(orderstore.temparyOrderItem)
    notification.success('Order added to the cart')
    uistore.riceandcurryPopup = false
  }else{
    notification.error('Please select rice and 4 curries')
  }
}


</script>

<style scoped>
.background{
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  z-index: 10;
  display: flex;
  justify-content: center;
  align-items: center;
}
.popup-window{
  display: flex;
  border-radius: 4px;
  background: #FFF;
  width: 60%;
  padding: 24px 26px;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 17px;
}
.content{
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  gap: 15px;
  align-self: stretch;
}
.popup-title{
  color: #000;
  text-align: center;
  font-size: 20px;
  font-style: normal;
  font-weight: 700;
  line-height: normal;
  text-transform: uppercase;
  width: 100%;
}
.sub-section{
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 15px;
  align-self: stretch;
}
.section-head{
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 5px;
  align-self: stretch;
}
.section-title{
  color: #000;
  font-size: 16px;
  font-style: normal;
  font-weight: 700;
  line-height: normal;
  text-transform: uppercase;
  align-self: stretch;
}
.section-head-devider{
  height: 1px;
  background-color: #D2D2D2;
  border: 0px;
  width: 100%;
}
.item-container{
  display: flex;
  align-items: flex-start;
  align-content: flex-start;
  gap: 20px;
  align-self: stretch;
  flex-wrap: wrap;
}
.item{
  display: flex;
  width: 234px;
  height: auto;
  padding: 7px 8px;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  border-radius: 4px;
  background: #EFEFEF;
  gap: 10px;
}
.item-name{
  color: #000;
  font-size: 18px;
  font-style: normal;
  font-weight: 300;
  line-height: normal;
  margin-top: 10px;
}
/* curry action button */
.curry-button{
  display: flex;
  width: 98%;
  height: 35%;
  padding: 6px 83px;
  justify-content: center;
  align-items: center;
  flex-shrink: 0;
  border-radius: 4px;
  background-color: var(--button-default);
  border: 0px;
  color: #FFF;
  font-size: 14px;
  font-weight: 400;
}
.curry-button:hover{
  background-color: var(--button-hover);
}
.curry-button:active{
  background-color: var(--button-select);
}
.curry-button:disabled{
  background-color: var(--button-deactivate);
  cursor: not-allowed;
}
/* rice action button */
.rice-button{
  display: flex;
  width: 98%;
  height: 35%;
  padding: 6px 83px;
  justify-content: center;
  align-items: center;
  flex-shrink: 0;
  border-radius: 4px;
  background-color: var(--button-default);
  border: 0px;
  color: #FFF;
  font-size: 14px;
  font-weight: 400;
}
.rice-button:hover{
  background-color: var(--button-hover);
}
.rice-button:active{
  background-color: var(--button-select);
}
.rice-button:disabled{
  background-color: var(--button-deactivate);
  cursor: not-allowed;
}
.red-notice{
  background-color: var(--notice-red);
  color: #FFF;
  padding: 2px 20px;
  font-size: 12px;
  border-radius: 10px;
}
.summery-column{
  display: flex;
  justify-content: space-between;
  align-items: center;
  align-self: stretch;
}
.column-data{
  display: flex;
  align-items: center;
  gap: 15px;
}
.column-button{
  display: flex;
  padding: 4px 12px;
  justify-content: center;
  align-items: center;
  gap: 8px;
  border-radius: 4px;
  background: #FFF;
  border: 1px solid var(--text-color-defalut-button);
  color: var(--text-color-defalut-button);
  font-size: 15px;
}
.column-button:hover{
  background-color: var(--button-default);
  border: 1px solid var(--button-default);
  color: var(--text-color-primary);
}
.column-button:active{
  background-color: var(--button-select);
  border: 1px solid var(--button-select);
}
.button-section{
  display: flex;
  align-items: flex-start;
  gap: 20px;
}
.action-button{
  border-radius: 4px;
  border: 1.5px solid var(--button-select);
  background: #FFF;
  width: 121px;
  height: 33px;
  flex-shrink: 0;
  color: var(--text-color-defalut-button);
  font-size: 14px;
  font-weight: 400;
}
.action-button:hover{
  background-color: var(--button-default);
  border: 1px solid var(--button-default);
  color: var(--text-color-primary);
}
.action-button:active{
  background-color: var(--button-select);
  border: 1px solid var(--button-select);
}
.action-button:disabled{
  background-color: var(--button-deactivate);
  cursor: not-allowed;
  color: var(--text-color-primary);
  border: 1px solid var(--button-deactivate);
}
.select {
  background-color: var(--button-select);
}

</style>


































<!-- <template>
  <div class="main-popup" v-if="uiStore.riceandcurryPopup">
    <div class="popup-window" ref="target">
      <h3 class="window-title">Select curries for your meal</h3>
      <hr class="section-devider" />
      <div class="common-section">
        <p class="description">efwefw</p>
        <div class="toggle">
          <span class="switch">
            <input id="switch-rounded" type="checkbox" @click="selectRice()" />
            <label for="switch-rounded"></label>
          </span>
        </div>
        <p class="description">Red rice</p>
      </div>
      <hr class="section-devider" />
      <div class="curry-section">
        <div class="curry" v-for="item in foodStore.curry" :key="item.id">
          <p class="description">{{ item.name }}</p>
          <button class="action-button" :id="item.id" @click="addCurry(item)">
            Add
          </button>
        </div>
      </div>
      <hr class="section-devider" />
      <div class="common-section">
        <p class="description">Quantity</p>
        <input
          min="1"
          type="number"
          class="quantity"
        />
      </div>
      <hr class="section-devider" />
      <div class="action-section">
        <button class="action" @click="closePopup">Cancel</button>
        <button
          class="action"
          @click="orderStore.addToOrder"
          :disabled="!buttonActive"
        >
          Add to cart
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
console.log('try to print')
import { useFoodStore } from "@/stores/food";
import { useOrderStore } from "@/stores/order";
import { useUiStore } from "@/stores/ui";
import { onClickOutside } from "@vueuse/core";
import { computed, ref, watch } from "vue";


const orderStore = useOrderStore();
const foodStore = useFoodStore();
const uiStore = useUiStore();


// this is for closing the popup when clicked outside
const target = ref(null);

// enable and disable the add to cart button
const buttonActive = ref(false);

const rice = computed(() =>
  foodStore.foodInfo.filter((item) => item.categoryName === "rice")
);

const curry = computed(() =>
  foodStore.foodInfo.filter((item) => item.categoryName === "curry")
);

// close the popup window and reset the tempary order item
const closePopup = () => {
  uiStore.riceandcurryPopup = false;
  orderStore.temparyOrderItem = {};
};

// close the popup when clicked outside
onClickOutside(target, (onclick) => {
  closePopup();
});

// // enable and disable the add to cart button
// const buttonActiveAction = (value) => {
//   if (orderStore.curryCount >= 3) {
//     buttonActive.value = true;
//   } else {
//     buttonActive.value = false;
//   }
// };

// const addCurry = (item) => {
//   const element = document.getElementById(item.id);
//   if (orderStore.temparyOrderItem.curry.includes(item)) {
//     orderStore.curryCount -= 1;
//     buttonActiveAction();

//     // change the button style
//     element.classList.add("action-button");
//     element.classList.remove("action-button-select");

//     // change the button text
//     element.innerHTML = "add";

//     // remove item from curry
//     orderStore.temparyOrderItem.curry =
//       orderStore.temparyOrderItem.curry.filter((curry) => curry !== item);
//   } else {
//     orderStore.curryCount += 1;
//     buttonActiveAction();

//     // change the button style
//     element.classList.add("action-button-select");
//     element.classList.remove("action-button");

//     // change the button text
//     element.innerHTML = "remove";

//     // add item to currylist
//     orderStore.temparyOrderItem.curry.push(item);
//   }
// };

// // this is for changing the rice type
// const selectRice = () => {
//   const element = document.getElementById("switch-rounded");
//   if (element.checked) {
//     orderStore.temparyOrderItem.rice = "red rice";
//   } else {
//     orderStore.temparyOrderItem.rice = "white white";
//   }
// };
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
  width: 70%;
  padding: 13px 41px;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 16px;
  border-radius: 6px;
  background: #fff;
  margin-inline: auto;
  margin-top: 150px;
}
.window-title {
  color: #000;
  font-size: 20px;
  font-style: normal;
  font-weight: 700;
  line-height: normal;
  text-transform: uppercase;
  align-self: stretch;
}
.section-devider {
  width: 100%;
  height: 1px;
  background: #d2d2d2;
  border: 0px;
}
.common-section {
  display: flex;
  align-items: center;
  gap: 30px;
}
.description {
  color: #000;
  font-size: 18px;
  font-style: normal;
  font-weight: 300;
  line-height: normal;
}
.curry-section {
  display: flex;
  align-items: flex-start;
  align-content: flex-start;
  gap: 20px;
  align-self: stretch;
  flex-wrap: wrap;
}
.curry {
  display: flex;
  width: 234px;
  height: 98px;
  padding: 0px 8px;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 20px;
  border-radius: 4px;
  background: #efefef;
}
.action-button {
  display: flex;
  height: 33px;
  padding: 6px 83px;
  justify-content: center;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
  align-self: stretch;
  border-radius: 4px;
  background: #ff8f8f;
  border: 0px;
  color: #fff;
  font-size: 15px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
}
.action-button:hover {
  background: #ff7a7a;
}
.action-button-select {
  display: flex;
  height: 33px;
  padding: 6px 83px;
  justify-content: center;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
  align-self: stretch;
  border-radius: 4px;
  font-size: 15px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
  background: #fff;
  color: #fb6262;
  border: 2px solid #fb6262;
}
.action-button:disabled {
  background: #d5d5d5;
  color: #fff;
}
.action-button-select:hover {
  background: #fff;
  color: #fb6262;
}
.action-section {
  display: flex;
  justify-content: flex-end;
  align-items: flex-end;
  gap: 38px;
}
.action {
  width: 210px;
  height: 33px;
  flex-shrink: 0;
  border-radius: 4px;
  background: #ff8f8f;
  border: 0px;
  color: #fff;
  font-size: 15px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
}
.action:hover {
  background: #ff7a7a;
}
.action:disabled {
  background: #d5d5d5;
  color: #fff;
}
.quantity {
  width: 50px;
  height: 20px;
  padding: 4px 6px;
  border-radius: 4px;
  border: 1px solid #d5d5d5;
  background: #fff;
  color: #000;
  font-size: 16px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
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
  border: 2px solid brown;
  cursor: pointer;
  transition: 0.3s;
}

.switch label::after {
  content: "";
  display: inherit;
  width: 20px;
  height: 20px;
  border-radius: 12px;
  background: brown;
  transition: 0.3s;
}

.switch input:checked ~ label {
  border-color: brown;
}

.switch input:checked ~ label::after {
  translate: 30px 0;
  background: brown;
}

.switch input:disabled ~ label {
  opacity: 0.5;
  cursor: not-allowed;
}
</style> -->
