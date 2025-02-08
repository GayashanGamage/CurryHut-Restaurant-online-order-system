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

  const foodItemList = ref(null);
  const processingFoodItem = ref(null); //this is for edit, new-adds and delete perpose
  // const selectedFoodItem = ref();

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
      DeliveryLocationList.value = response.data;
    })
    .catch((error) => {
      if(error.stataus == 400){
        toast.error("No delivery location found");
      }
    });
  }

  return {
    unDeletable,
    categoryList,
    foodItemList,
    processingCategory,
    processingFoodItem,
    DeliveryLocationList,
    processingDeliveryLocation,
    getAllCategories,
    getAllDeliveryLocations,
  };
});
