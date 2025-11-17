import { ref, computed, watch } from "vue";
import { defineStore } from "pinia";
import { useUiStore } from "./ui";
import { useToast } from "vue-toast-notification";

export const useOrderStore = defineStore("order", () => {
  const curryCount = ref(0); //get how many couries selected

  // this is for the tempary selected item before add to the order list - rice and curry
  const temparyOrderItem = ref();

  // this is for the order list
  const order = ref([]);

  // controll order count 
  const orderCount = ref(0); 

  const summery = ref([
    {
      id: 101,
      orderdate: "2021-09-01",
      payment: "cash",
      status: "pending",
    },
    {
      id: 111,
      orderdate: "2021-09-21",
      payment: "card",
      status: "complete",
    },
    {
      id: 103,
      orderdate: "2021-11-01",
      payment: "card",
      status: "complete",
    },
  ]);

  // check curryCount and disable curry availability
  watch(curryCount, (newCount) => {
    if (newCount == 4 || newCount >= 4) {
      const allEnabledActionButton =
        document.getElementsByClassName("action-button");
      for (let i = 0; i < allEnabledActionButton.length; i++) {
        allEnabledActionButton[i].disabled = true;
      }
    } else {
      const allEnabledActionButton =
        document.getElementsByClassName("action-button");
      for (let i = 0; i < allEnabledActionButton.length; i++) {
        allEnabledActionButton[i].disabled = false;
      }
    }
  });


  const addToOrder = () => {
    order.value.push(temparyOrderItem.value);
    temparyOrderItem.value = undefined;
    useUiStore().riceandcurryPopup = false;
    useOrderStore().curryCount = 0;
    useToast().open({
      message: "Item added to the order list",
      type: "success",
    });
  };
  
  function cookieExireationTime(){
    let a = new Date().getTime() + 900000
    return new Date(a).toUTCString();
  }

  watch(
    () => order.value, 
    (newValue) => {
      console.log(newValue);
      if (newValue.length > 0) {
        document.cookie = `order=${JSON.stringify(newValue)}; expires=${cookieExireationTime()}; path=/`;
      } else {
        document.cookie = "order=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/";
      }
    },
    { deep: true } 
  );

  // load order cookie to order variable - when change pages
  function getOrderFromCookies() {
    const cookies = document.cookie.split('; ');
    const orderCookie = cookies.find(cookie => cookie.startsWith('order=')); 

    if (orderCookie) {
      const orderString = orderCookie.split('=')[1]; 
      order.value =  JSON.parse(orderString); 
      orderCount.value = order.value.length;
    }else{
      order.value = [];
    }
  }


  return {
    curryCount,
    // curryAvailability,
    order,
    orderCount,
    temparyOrderItem,
    summery,
    addToOrder,
    getOrderFromCookies,
  };
});
