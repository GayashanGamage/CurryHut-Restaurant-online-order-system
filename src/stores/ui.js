import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useShopStore } from "./shop";
import { useShowCase } from "./showcase";

export const useUiStore = defineStore("ui", () => {
  // other pinia stors
  const shopStore = useShopStore();
  const showCase = useShowCase();

  // Passwordchange component
  const logoutPopupWindow = ref(false);
  const PasswordChangeWindow = ref(false);
  const CodeVerify = ref(true); //subwindow of CodeVerificationWindow
  const PasswordRest = ref(false); //subwindow of CodeVerificationWindow

  // Timechange component
  const TimeChangeWindow = ref(false);
  const timeDescription = ref(null); // meal-time : breakfast, lunch, dinner, shop-time : open_time, close_time
  const mealtimeOrShoptime = ref(true); // true = mealtime, false = shoptime

  // food component
  const AddFoodWindow = ref(false);
  const FoodView = ref(false);

  // category page
  const NewCategoryWindow = ref(false);
  const DeleteCategoryWindow = ref(false);
  const EditCategoryWindow = ref(false);

  // side menu bar
  const currentTab = ref("");

  // food available time - edit-menu page
  const foodAvailableTime = ref(false);
  const addNewAvailableFood = ref(false);

  function openLogoutPopup() {
    logoutPopupWindow.value = true;
  }

  function closeLogoutPopup() {
    logoutPopupWindow.value = false;
  }

  function closeCodeVerifyPopup() {
    PasswordChangeWindow.value = false;
  }

  function openTimeChangeWindow(mealTime) {
    timeDescription.value = mealTime;
    TimeChangeWindow.value = true;
    if (mealTime === "breakfast") {
      shopStore.hours = new Date(`19970-1-1 ${shopStore.breakfast}`).getHours();
      shopStore.minutes = new Date(
        `19970-1-1 ${shopStore.breakfast}`
      ).getMinutes();
    } else if (mealTime === "lunch") {
      shopStore.hours = new Date(`19970-1-1 ${shopStore.lunch}`).getHours();
      shopStore.minutes = new Date(`19970-1-1 ${shopStore.lunch}`).getMinutes();
    } else if (mealTime === "dinner") {
      shopStore.hours = new Date(`19970-1-1 ${shopStore.dinner}`).getHours();
      shopStore.minutes = new Date(
        `19970-1-1 ${shopStore.dinner}`
      ).getMinutes();
    } else if (mealTime === "open_time") {
      mealtimeOrShoptime.value = false;
      shopStore.hours = new Date(`19970-1-1 ${shopStore.open_time}`).getHours();
      shopStore.minutes = new Date(
        `19970-1-1 ${shopStore.open_time}`
      ).getMinutes();
    } else if (mealTime === "close_time") {
      mealtimeOrShoptime.value = false;
      shopStore.hours = new Date(
        `19970-1-1 ${shopStore.close_time}`
      ).getHours();
      shopStore.minutes = new Date(
        `19970-1-1 ${shopStore.close_time}`
      ).getMinutes();
    }
  }

  function closeTimeChangeWindow() {
    timeDescription.value = null;
    shopStore.hours = 0;
    shopStore.minutes = 0;
    TimeChangeWindow.value = false;
  }

  function openNewCategoryWindow() {
    // console.log("new category window open");
    NewCategoryWindow.value = true;
  }

  function closeNewCategoryWindow() {
    // console.log("new category window close");
    showCase.getCategoryDetails();
    showCase.processingCategory = null;
    NewCategoryWindow.value = false;
  }

  function openDeleteCategoryWindow(id, name) {
    showCase.processingCategory = { _id: id, name: name };
    DeleteCategoryWindow.value = true;
  }

  function closeDeleteCategoryWindow() {
    showCase.processingCategory = null;
    DeleteCategoryWindow.value = false;
  }

  function openEditCategoryWindow(item_id) {
    // console.log("new category window open");
    showCase.processingCategory = item_id;
    EditCategoryWindow.value = true;
  }

  function closeEditCategoryWindow() {
    showCase.processingCategory = null;
    EditCategoryWindow.value = false;
  }

  function openAddFoodWindow() {
    showCase.processingFoodItem = {
      category_id: "",
      name: "",
      description: "",
      price: [
        {
          name: "",
          price: 0,
          portion: 0,
        },
      ],
    };
    AddFoodWindow.value = true;
  }

  function closeAddFoodWindow() {
    AddFoodWindow.value = false;
  }

  function foodViewOpen(value) {
    for (let i = 0; i < showCase.foodItemList.length; i++) {
      if (showCase.foodItemList[i]._id == value) {
        showCase.processingFoodItem = showCase.foodItemList[i];
      }
    }
    FoodView.value = true;
  }

  function foodViewClose() {
    showCase.processingFoodItem = null;
    FoodView.value = false;
  }

  // edit-menu page
  function openEditFoodTime() {
    foodAvailableTime.value = true;
  }

  function closeEditFoodTime() {
    foodAvailableTime.value = false;
  }

  function openAddNewAvailableFood() {
    addNewAvailableFood.value = true;
  }
  function closeAddNewAvailableFood() {
    addNewAvailableFood.value = false;
  }

  return {
    // component visibility
    logoutPopupWindow,
    PasswordChangeWindow,
    CodeVerify,
    PasswordRest,
    TimeChangeWindow,

    timeDescription,
    mealtimeOrShoptime,

    // category page
    NewCategoryWindow,
    DeleteCategoryWindow,
    EditCategoryWindow,

    // food page
    AddFoodWindow,
    FoodView,

    // menu bar
    currentTab,

    // menu page
    foodAvailableTime,
    addNewAvailableFood,

    // funciton
    openLogoutPopup,
    closeLogoutPopup,
    closeCodeVerifyPopup,
    openTimeChangeWindow,
    closeTimeChangeWindow,
    openNewCategoryWindow,
    closeNewCategoryWindow,
    openDeleteCategoryWindow,
    closeDeleteCategoryWindow,
    openEditCategoryWindow,
    closeEditCategoryWindow,
    openAddFoodWindow,
    closeAddFoodWindow,
    foodViewOpen,
    foodViewClose,
    openEditFoodTime,
    closeEditFoodTime,
    openAddNewAvailableFood,
    closeAddNewAvailableFood,
  };
});
