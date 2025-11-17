import { ref, computed, watch } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useUiStore } from "./ui";
import router from "@/router";

export const useFoodStore = defineStore("food", () => {
  // other pinia stores
  const uiStore = useUiStore();
  
  const foodInfo = ref(null);
  const categories = ref(null);
  // const availableCategoryList = ref(null) // all category came with foods
  
  // undeletable section
  const drinks = ref(null)
  const decert = ref(null)
  const extra_portion = ref(null)
  
  const selectedCategory = ref(0); //this is for identify the selected category for styling ( css )
  const selectedCategoryId = ref(null); // this is use for load the selected category food items
  const selectedFood = ref(null); //this is for identify the selected food item. load product related data into this.
  const selectedPotion = ref(0); //this is for identify the selected potion
  // const allSelectedCategoryItems = ref([]);
  const selectedFoodCategoryList = ref(null) //this is for load data into 
  
  // data from food view popup
  const portion = ref(0)
  const price = ref(0)


  // rice and curry section
  const plainRice = ref(null)
  const curry = ref(null)
  const ricePack = ref(null)
  const selectedRicePack = ref(null)
  
  // functions
  // get all deletable foods accoring to timly manner
  function getAllDeletableFoods(){
    axios
    .get(`${import.meta.env.VITE_url}/customer/`)
    .then((response) => {
        foodInfo.value = response.data.data;
        categories.value = response.data.categories;
        selectedCategoryId.value = categories.value[0].id
        changeCategory(0, categories.value[0].id)
    })
    .catch((error) => {
      if (error.status === 403) {
        uiStore.shopClose = error.response.data["close_time"];
        uiStore.shopOpen = error.response.data["open_time"];
        router.push("/closed");
      }
    });
  }

  // get all rice and curry list
  function getFoodList(){
    axios.get(`${import.meta.env.VITE_url}/customer/riceAndCurry`)
    .then((response) => {
      plainRice.value = response.data.rice
      curry.value = response.data.curry 
      ricePack.value = response.data['rice&curry']
      uiStore.bugetPack = true
      console.log()
    })
    .catch((error) => {
      console.log(error)
    })
  }

  function changeCategory(index, id){
    selectedCategory.value = index
    selectedCategoryId.value = id
    selectedFoodCategoryList.value  = foodInfo.value.filter((food) => food.category_id === id)
  }

  watch(selectedCategoryId.value, (newId) => {
    console.log(newId)
    selectedDeletableFoodCategory.value = foodInfo.value.filter((food) => food.category_id === newId)
  })




  return {
    foodInfo,
    categories,
    selectedFood,
    selectedPotion,
    selectedCategoryId,
    selectedFoodCategoryList,

    // data from food view popup
    portion,
    price,

    // undeletable section
    drinks,
    decert,
    extra_portion,


    plainRice,
    curry,
    ricePack,
    selectedRicePack,

    // uniqueCategories,
    selectedCategory,
    // allSelectedCategoryItems,

    // functions
    getFoodList,
    getAllDeletableFoods,
    changeCategory,
  };
});
