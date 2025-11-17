import { ref } from "vue";
import { defineStore } from "pinia";

export const useShopStore = defineStore("shop", () => {
  const deliveryLocations = ref(null);
  const selectDeliveryLocation = ref(null);

  return {
    deliveryLocations,
    selectDeliveryLocation,
  };
});
