import { ref, computed } from "vue";
import { defineStore } from "pinia";

export const useUiStore = defineStore("ui", () => {
  const foodPopup = ref(false);
  const riceandcurryPopup = ref(false);

  // shop time related
  const shopOpen = ref(undefined);
  const shopClose = ref(undefined);
  const isShopClosed = ref(false);

  // product view
  const categorySection = ref(false)
  // const mainProductSection = ref(false)
  const budgetPackSection = ref(false)

  // componennt visibility
  const bugetPack = ref(false)

  // authonticate related
  const allowMobile = ref(false)
  const allowVerification = ref(false)

  return {
    foodPopup,
    riceandcurryPopup,
    shopOpen,
    shopClose,
    isShopClosed,
    categorySection,
    // mainProductSection,
    budgetPackSection,
    bugetPack,
    allowMobile,
    allowVerification,
  };
});
