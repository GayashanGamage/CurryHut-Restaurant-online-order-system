<template>
  <div class="c-level-one-container">
    <div class="c-level-two-container" ref="addDeliveryWindow">
      <div class="c-level-three-container window-header">
        <h3 class="window-title">Remove Delivery place</h3>
      </div>
      <div class="c-level-three-container window-content">
        <div class="content">
          <p class="warning-message">
            You are going to delete
            <span class="location">{{
              showCase.processingDeliveryLocation.place
            }}</span>
            from your delivery location
          </p>
          <button class="action-btn" @click="deleteLocation">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthonticationStore } from "@/stores/authontication";
import { useShowCase } from "@/stores/showcase";
import { useUiStore } from "@/stores/ui";
import { onClickOutside } from "@vueuse/core";
import axios from "axios";
import { ref } from "vue";
import { useToast } from "vue-toast-notification";
const notification = useToast();

// pinia stores
const uiStore = useUiStore();
const showCase = useShowCase();
const authontication = useAuthonticationStore();

// click outside of the 'delete-window' to close itself
const addDeliveryWindow = ref(null);
onClickOutside(addDeliveryWindow, () => {
  uiStore.removeDeliveryPopup = false;
});

// delete delivery location
const deleteLocation = () => {
  axios
    .delete(
      `${import.meta.env.VITE_url}/delivery/delete/${
        showCase.processingDeliveryLocation.id
      }`, 
      {
        headers: {
          Authorization: 'Bearer ' + authontication.cookies_token,
        },
      }
    )
    .then((response) => {
      if (response.status == 200) {
        uiStore.deliveryChange = true;
        notification.success("Delivery location removed successfully");
        showCase.processingDeliveryLocation = null;
        uiStore.removeDeliveryPopup = false;
      }
    })
    .catch((error) => {
      notification.error("Failed to remove delivery location");
    });
};
</script>

<style scoped>
.c-level-one-container {
  background-color: rgba(24, 28, 20, 0.8);
  width: 100vw;
  height: 100vh;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  position: fixed;
  display: flex;
  justify-content: center;
  align-items: center;
}
.c-level-two-container {
  width: 466px;
  height: 253px;
  border-radius: 6px;
  background: #fff;
}
.window-header {
  height: 60px;
  border-radius: 6px 6px 0px 0px;
  background: #ff204e;
  display: flex;
  justify-content: center;
  align-items: center;
}
.window-content {
  height: 80%;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.window-title {
  display: inline;
  color: #fff;
  font-family: "Space Grotesk";
  font-size: 20px;
  font-weight: 400;
  text-transform: uppercase;
}
.content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  margin-block: auto;
  padding: 20px;
}
.warning-message {
  color: #ff204e;
  text-align: center;
  font-family: "Space Grotesk";
  font-size: 20px;
  font-weight: 400;
}
.location {
  font-weight: 900;
  color: white;
  text-transform: uppercase;
  background-color: #ff204e;
  padding: 4px;
  border-radius: 4px;
}
.action-btn {
  width: 50%;
  padding: 6px 8px;
  border-radius: 4px;
  border: 0.5px solid #ff204e;
  color: #ff204e;
  text-align: center;
  font-family: "Space Grotesk";
  font-size: 16px;
  font-weight: 500;
  background-color: #fff;
}
.action-btn:hover {
  background-color: #ff204e;
  color: #fff;
}
</style>
