<template>
  <div class="food-container">
    <!-- <h3 class="container-title" v-if="titleToggle">
      {{ foodstore.uniqueCategories[foodstore.selectedCategory] }}
    </h3>
    <h3 class="container-title" v-if="!titleToggle">
      {{ sectionTitile }}
    </h3>
    <hr class="container-devider" /> -->
    <div class="food-section">
      <div
        class="food-item"
        v-for="(item, index) in foodList"
        :key="item.id"
      >
        <img src="https://curryhut.blr1.cdn.digitaloceanspaces.com/sample-images/koththu.webp" alt="image-name" class="food-image" />
        <h4 class="food-title">{{ item.name }}</h4>
        <p class="food-price">
          Rs. {{ item.price[0].price }}
        </p>
        <button class="action-button" @click="selectFood(item.id, index)">
          view
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
/*
HOW THIS WORK
  1. this is common component to drinks, decerts, extra potions and deletable other categories ( koththu, biriyani )
  2. load data from this parent component 
  3. onece user click on the 'action button', it should open the 'foodview' popup
  4. to open food item view popup, data get from foodstore - selectedFood ( entire food items' data should be store there )
  5. this item also should load to orderStore - temparyOrderItem ( this is the item that user going to add to the cart )
  6. foodstore.selectedPotion - this is for track witch price & size select by customer
*/

// import necesary packages --------------------------------
import { useFoodStore } from "@/stores/food";
import { useOrderStore } from "@/stores/order";
import { useUiStore } from "@/stores/ui";

// define props --------------------------------------------
const props = defineProps({
  // TODO: add defalt value as a empty array - []
  foodList : Array,
  foodStoreVariable : String // this is indicate where original dataset locate in foodStore - drinks, decerts, extra, deletable
})


// pinia stores
const orderStore = useOrderStore();
const uiStore = useUiStore();
const foodstore = useFoodStore();

// functions -----------------------------------------------
// select the food item
const selectFood = (item, index) => {
  foodstore.selectedFood = foodstore[props.foodStoreVariable].find((food) => food.id === item )
  orderStore.temparyOrderItem = {
    'id' : foodstore.selectedFood.id,
    'category_id' : foodstore.selectedFood.category_id,
    'name' : foodstore.selectedFood.name,
    'price' : foodstore.selectedFood.price[foodstore.selectedPotion].price,
    'quantity' : 1,
    'size' : foodstore.selectedFood.price[foodstore.selectedPotion].name,
    'availability' : foodstore.selectedFood.price[foodstore.selectedPotion].availability
  }
  foodstore.portion = foodstore.selectedFood.price[foodstore.selectedPotion].portion
  foodstore.price = foodstore.selectedFood.price[foodstore.selectedPotion].price
  uiStore.foodPopup = true;
};

</script>

<style scoped>
.food-container {
  display: flex;
  width: 76%;
  padding: 16px 16px;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 13px;
  border-radius: 4px;
  background: #fff;
  margin-inline: auto;
}
.container-title {
  color: #000;
  font-size: 30px;
  font-style: normal;
  font-weight: 900;
  line-height: normal;
  align-self: stretch;
}
.container-devider {
  width: 100%;
  height: 1.221px;
  background: #dadada;
  border: 0px;
}
.food-section {
  display: flex;
  align-items: center;
  align-content: center;
  gap: 12px;
  align-self: stretch;
  flex-wrap: wrap;
}
.food-item {
  flex: 1;
  align-self: stretch;
  display: flex;
  gap: 6px;
  align-self: stretch;
  min-width: 200px;
  max-width: 250px;
  height: auto;
  padding: 6px;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-radius: 4px;
  border: 1px solid #dbdbdb;
}
.food-item:hover {
  box-shadow: rgba(99, 99, 99, 0.2) 0px 2px 8px 0px;
}
.food-image {
  /* width: 80%; */
  height: auto;
  flex-shrink: 0;
  align-self: stretch;
  border-radius: 4px;
}
.food-title {
  color: #000;
  text-align: center;
  font-size: 20px;
  font-style: normal;
  font-weight: 600;
  line-height: normal;
  align-self: stretch;
}
.food-price {
  color: #000;
  text-align: center;
  font-size: 18px;
  font-style: normal;
  font-weight: 300;
  line-height: normal;
  align-self: stretch;
}
.action-button {
  display: flex;
  padding: 8px 0px;
  justify-content: center;
  align-items: center;
  align-self: stretch;
  border-radius: 4px;
  background: #ff8f8f;
  border: 0px;
  color: #fff;
  text-align: center;
  font-size: 18px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
  cursor: pointer;
}
.food-item:hover .action-button {
  background-color: #ff5e5e;
}
</style>
