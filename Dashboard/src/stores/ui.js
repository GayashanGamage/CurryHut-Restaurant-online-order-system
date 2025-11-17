import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useShopStore } from "./shop";
import { useShowCase } from "./showcase";

export const useUiStore = defineStore("ui", () => {
  // other pinia stors
  const refresh = ref(false);
  const shopStore = useShopStore();
  const showCase = useShowCase();

  // Passwordchange component
  const logoutPopupWindow = ref(false);
  const PasswordChangeWindow = ref(false);
  const CodeVerify = ref(true); //subwindow of CodeVerificationWindow
  const PasswordRest = ref(false); //subwindow of CodeVerificationWindow

  // Timechange popups
  const timeWindow = ref(false);
  const windowTitle = ref("");
  const timeDescription = ref("");

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

  // delivery place related popup window
  const addDeliveryPopup = ref(false);
  const editDeliveryPopup = ref(false);
  const removeDeliveryPopup = ref(false);
  const deliveryChange = ref(false);

  function openLogoutPopup() {
    logoutPopupWindow.value = true;
  }

  function closeLogoutPopup() {
    logoutPopupWindow.value = false;
  }

  function closeCodeVerifyPopup() {
    PasswordChangeWindow.value = false;
  }

  // this is for close all the time change window
  function closeTimeChangeWindow() {
    timeWindow.value = false;
    shopStore.hours = 0;
    shopStore.minutes = 0;
  }

  function openNewCategoryWindow() {
    // console.log("new category window open");
    NewCategoryWindow.value = true;
  }

  function closeNewCategoryWindow() {
    showCase.getAllCategories(); //update entire category list from database
    showCase.processingCategory = null; //clear the processing category
    NewCategoryWindow.value = false; //close the add new category window
  }

  function openDeleteCategoryWindow(id, name) {
    showCase.processingCategory = { _id: id, name: name };
    DeleteCategoryWindow.value = true;
  }

  function closeDeleteCategoryWindow() {
    showCase.processingCategory = null; // clear the processing category
    DeleteCategoryWindow.value = false; // close the delete category window
  }

  function openEditCategoryWindow(item_id) {
    // console.log("new category window open");
    showCase.processingCategory = item_id;
    EditCategoryWindow.value = true;
  }

  function closeEditCategoryWindow() {
    showCase.processingCategory = null; //clear the processing category
    EditCategoryWindow.value = false; //close the edit category window
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
    showCase.processingFoodItem = null;
  }

  function foodViewOpen(value) {
    for (let i = 0; i < showCase.foodItemList.length; i++) {
      if (showCase.foodItemList[i].id == value) {
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
    refresh,
    // component visibility
    logoutPopupWindow,
    PasswordChangeWindow,
    CodeVerify,
    PasswordRest,

    // time change - time related
    timeWindow,
    // time change - window related
    windowTitle,
    timeDescription,

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

    // delivery place related popup window
    addDeliveryPopup,
    editDeliveryPopup,
    removeDeliveryPopup,
    deliveryChange, // this is give a signal to the delivery component to update the delivery list

    // funciton
    openLogoutPopup,
    closeLogoutPopup,
    closeCodeVerifyPopup,
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
