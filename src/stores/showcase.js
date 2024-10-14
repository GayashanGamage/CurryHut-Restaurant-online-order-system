import { ref } from "vue";
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

  const foodItemList = ref();
  const selectedFoodItem = ref();

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

  return {
    unDeletable,
    categoryList,
    foodItemList,
    processingCategory,
    selectedFoodItem,

    getCategoryDetails,
  };
});
