import { ref, watch } from "vue";
import { defineStore } from "pinia";
import { useAuthonticationStore } from "./authontication";
// support for seperated functions
import axios from "axios";
import { useToast } from "vue-toast-notification";
import router from "@/router";
const toast = useToast();

export const useShowCase = defineStore("showcase", () => {
  // pinia store reference
  const authontication = useAuthonticationStore();
  
  const DeliveryLocationList = ref(null);
  const processingDeliveryLocation = ref(null); //this is for edit, new-adds and delete perpose
  
  const unDeletable = [
    "uncategorize",
    "curry",
    "pilaw rice",
    "drinks",
    "deserts",
  ];
  const categoryList = ref(null);
  const processingCategory = ref(null); //this is for edit, new-adds and delete perpose
  
  // only for views
  const sortedFood = ref(null) // this is use for showcase food under category name in menu page
  const availableFood = ref(null) // this is use for showcase food under category name in menu page
  const foodItemList = ref(null);
  // const selectedFoodItem = ref();
  
  // only for procesing
  const shop_menu = ref([]); //  this data structure for update shop menu ( for API request )
  const processingFoodItem = ref(null); //this is for edit, new-adds and delete perpose

  const preventCategories = ['670cbd156e6b240be2d189e6', '670cbd0e6e6b240be2d189e5']

  // common functions
  const getAllCategories = () => {
    axios
      .get(`${import.meta.env.VITE_url}/category/getcategories`, {
        headers: {
          Authorization: "Bearer " + authontication.cookies_token,
        },
      })
      .then((response) => {
        categoryList.value = response.data;
      })
      .catch((error) => {
        if (error.stataus == 404) {
          toast.error("No category found");
        } else if (error.stataus == 401) {
          authontication.removeCredentials();
          router.push({ name: "Login" });
        }
      });
  };

  const getAllDeliveryLocations = () => {
    axios
    .get(`${import.meta.env.VITE_url}/delivery/get`)
    .then((response) => {
      DeliveryLocationList.value = response.data['data'];
    })
    .catch((error) => {
      if(error.stataus == 400){
        toast.error("No delivery location found");
      }
    });
  }

  // get all foods
  const getAllFoodItems = () => {
    axios
    .get(`${import.meta.env.VITE_url}/getallfood`, {
      headers: {
        Authorization: "Bearer " + authontication.cookies_token,
      },
    })
    .then((response) => {
      foodItemList.value = response.data;
      // updateMenu(response.data)
      sortFoodList(response.data);
      setMenu();
      setAvailableFood(response.data);
    })
    .catch((error) => {
      if (error.status == 401) {
        authontication.removeCredentials();
        router.replace({ name: "login" });
      }
    });
  }

  // ---------------------- if you change sortFoodList then change setMenu function also ----------------------
  // sort food list accoring to the category name and remove uncatgory food items form this list
  // function sortFoodList(a){
  //   sortedFood.value = a.reduce((acc, item) => {
  //     if (item['category_id'] !== '670cbcf46e6b240be2d189e2') { // uncatgory's id
  //       let category_name = categoryList.value.find(category => category.id === item['category_id']).name;
  //         if (!acc[category_name]) {
  //             acc[category_name] = []; // Initialize the category array if it doesn't exist
  //         }
  //         // add availability of food item
  //         if(preventCategories.includes(item['category_id'])){
  //           item['breakfast'] = true;
  //           item['lunch'] = true;
  //           item['dinner'] = true;
  //           // itme['availability'] = false;
  //         }
  //         // else{
  //         //   item['breakfast'] = false;
  //         //   item['lunch'] = false;
  //         //   item['dinner'] = false;
  //         //   // itme['availability'] = false;
  //         // }
  //         acc[category_name].push(item); // Add the item to the corresponding category
  //     }
  //     return acc;
  // }, {});
  // }


  // sort food list accoring to the category name and remove uncatgory food items form this list
  function sortFoodList(a){
    sortedFood.value = a.reduce((acc, item) => {
      if (item['category_id'] !== '670cbcf46e6b240be2d189e2') { // uncatgory's id
        let category_name = categoryList.value.find(category => category.id === item['category_id']).name;
          if (!acc[category_name]) {
              acc[category_name] = []; // Initialize the category array if it doesn't exist
          }
          acc[category_name].push(item); // Add the item to the corresponding category
      }
      return acc;
  }, {});
  }

  // set available food list according to the category
  function setAvailableFood(a){
    availableFood.value = a.reduce((acc, item) => {
      console.log(item)
      if (item['category_id'] !== '670cbcf46e6b240be2d189e2' && (item['breakfast'] == true || item['lunch'] == true || item['dinner'] == true)) { // uncatgory's id
        let category_name = categoryList.value.find(category => category.id === item['category_id']).name;
        if (!acc[category_name]) {
            acc[category_name] = []; // Initialize the category array if it doesn't exist
        }
        acc[category_name].push({'id' : item.id, 'availability' : item.availability, 'name' : item.name}); // Add the item to the corresponding category
      }
      return acc;
  }, {});
  }

  // datastructure of send api request
  // function setMenu() {
  //   let temp_menu = []
  //   for(let a = 0; a < foodItemList.value.length; a++){
  //     if(preventCategories.includes(foodItemList.value[a].category_id))
  //       {
  //       temp_menu.push({
  //         id: foodItemList.value[a].id,
  //         breakfast: true,
  //         lunch: true,
  //         dinner: true,
  //         availability : true,
  //         name : foodItemList.value[a].name
  //       });
  //     }else
  //     {
  //       temp_menu.push({
  //         id: foodItemList.value[a].id,
  //         breakfast: foodItemList.value[a].breakfast,
  //         lunch: foodItemList.value[a].lunch,
  //         dinner: foodItemList.value[a].dinner,
  //         availability : foodItemList.value[a].availability,
  //         name : foodItemList.value[a].name
  //       });
  //     }
  //   }
  //   shop_menu.value = temp_menu;  
  // }


  // datastructure of send api request
  function setMenu() {
    let temp_menu = []
    for(let a = 0; a < foodItemList.value.length; a++){
        temp_menu.push({
          id: foodItemList.value[a].id,
          breakfast: foodItemList.value[a].breakfast,
          lunch: foodItemList.value[a].lunch,
          dinner: foodItemList.value[a].dinner,
          availability : foodItemList.value[a].availability,
          name : foodItemList.value[a].name
        });
      }
      shop_menu.value = temp_menu;  
    }


  return {
    unDeletable,
    categoryList,
    sortedFood,
    availableFood,
    foodItemList,
    shop_menu,
    processingCategory,
    processingFoodItem,
    DeliveryLocationList,
    processingDeliveryLocation,
    getAllCategories,
    getAllDeliveryLocations,
    getAllFoodItems,
    setAvailableFood
  };
});
