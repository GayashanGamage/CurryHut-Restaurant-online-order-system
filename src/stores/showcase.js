import { ref, watch } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useAuthonticationStore } from "./authontication";

export const useShowCase = defineStore("showcase", () => {
  // pinia store reference
  const authontication = useAuthonticationStore();

  const unDeletable = [
    "uncategorize",
    "curry",
    "pilaw rice",
    "drinks",
    "deserts",
  ];
  const categoryList = ref(null);
  const processingCategory = ref(null); //this is for edit, new-adds and delete perpose

  const foodItemList = ref(null);
  const processingFoodItem = ref(null); //this is for edit, new-adds and delete perpose
  // const selectedFoodItem = ref();

  function getCategoryDetails() {
    axios
      .get(`${import.meta.env.VITE_url}/getcategories`, {
        headers: {
          Authorization: "Bearer " + authontication.authcookie,
        },
      })
      .then((response) => {
        categoryList.value = response.data;
      });
  }

  // get all foods
  const getAllFoods = () => {
    axios
      .get(`${import.meta.env.VITE_url}/getallfood`, {
        headers: {
          Authorization: "Bearer " + authontication.authcookie,
        },
      })
      .then((response) => {
        if (response.status == 200) {
          foodItemList.value = response.data;
        }
      })
      .catch((response) => {
        toast.error("something go wrong. refresh manualy");
      });
  };

  return {
    unDeletable,
    categoryList,
    foodItemList,
    processingCategory,
    processingFoodItem,
    // selectedFoodItem,

    getCategoryDetails,
    getAllFoods,
  };
});
