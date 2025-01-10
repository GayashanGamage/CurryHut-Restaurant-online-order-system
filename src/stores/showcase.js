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

  return {
    unDeletable,
    categoryList,
    foodItemList,
    processingCategory,
    processingFoodItem,
  };
});
