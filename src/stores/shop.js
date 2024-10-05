import { ref, computed } from "vue";
import { defineStore } from "pinia";

export const useShopStore = defineStore("shop", () => {
  const open_time = ref(null);
  const close_time = ref(null);
  const shutdown = ref(false);
  const breakfast = ref(null);
  const lunch = ref(null);
  const dinner = ref(null);

  return { open_time, close_time, shutdown, breakfast, lunch, dinner };
});
