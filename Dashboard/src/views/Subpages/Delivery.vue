<template>
  <div class="s-level-one-container">
    <div class="page-title-section">
      <h2 class="page-title">
        Delivery <span v-if="uiStore.deliveryChange">...</span>
      </h2>
      <button
        class="action-button add-new-button"
        @click="openAddNewDeliveryPopup"
      >
        Add new
      </button>
    </div>
    <div class="s-level-two-container">
      <div class="table-container">
        <div class="table-head">
          <div class="table-head-title">
            <p class="table-title" id="column1">Location</p>
            <p class="table-title" id="column2">Price</p>
            <p class="table-title" id="column3">Availability</p>
          </div>
          <hr class="column-devider" />
        </div>
        <div
          class="table-column"
          v-for="(item, index) in showcase.DeliveryLocationList"
          :key="item['_id']"
        >
          <div class="table-column-content">
            <p class="column-text" id="column1">{{ item.place }}</p>
            <p class="column-text" id="column2">{{ item.cost }}</p>
            <!-- set availability button -->
            <button
              :class="item.status == true ? 'available' : 'not-available'"
              id="column3"
              @click="setAvailability(index, item.status)"
            >
              {{ item.status == true ? "available" : "not available" }}
            </button>
            <div class="button-container" id="column4">
              <button
                class="action-button-edit"
                @click="openDeliveryEditPopup(index)"
              >
                Edit
              </button>
              <button
                class="action-button-delete"
                @click="removeDeliveryLocation(index)"
              >
                Delete
              </button>
            </div>
          </div>
          <hr class="column-devider" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthonticationStore } from "@/stores/authontication";
import { useShowCase } from "@/stores/showcase";
import { useUiStore } from "@/stores/ui";
import axios from "axios";
import { onBeforeMount, onUpdated } from "vue";
import { useToast } from "vue-toast-notification";
const notification = useToast();
const authontication = useAuthonticationStore();


// pinia stores
const showcase = useShowCase();
const uiStore = useUiStore();

// get delivery list
const getDeliveryList = () => {
  axios
    .get(`${import.meta.env.VITE_url}/delivery/get`)
    .then((response) => {
      showcase.DeliveryLocationList = response.data['data'];
    })
    .catch((error) => {
      console.log(error);
    });
};

// if the delivery list is not available, get the delivery list
onBeforeMount(() => {
  if (showcase.DeliveryLocationList == null) {
    authontication.restoreCredentials();
    getDeliveryList();
  }
});

// open delivery popup
const openDeliveryEditPopup = (id) => {
  uiStore.editDeliveryPopup = true;
  showcase.processingDeliveryLocation = JSON.parse(
    JSON.stringify(showcase.DeliveryLocationList[id])
  );
};

// when deliveryChange ( uiStore ) is true, get the delivery list again
onUpdated(() => {
  if (uiStore.deliveryChange == true) {
    getDeliveryList();
    uiStore.deliveryChange = false;
  }
});

// open remove delivery location popup
const removeDeliveryLocation = (index) => {
  showcase.processingDeliveryLocation = showcase.DeliveryLocationList[index];
  uiStore.removeDeliveryPopup = true;
};

// change availability of the delivery location
const setAvailability = (index, status) => {
  axios
    .post(`${import.meta.env.VITE_url}/delivery/set-status`, {
      _id: showcase.DeliveryLocationList[index].id,
      status: !status,
    }, 
    {
      headers: {
        Authorization: "Bearer " + authontication.cookies_token,
      },
    })
    .then((response) => {
      if (response.status == 200) {
        uiStore.deliveryChange = true;
        if (!status == true) {
          notification.success(
            `${showcase.DeliveryLocationList[index].place} is set to available`
          );
        } else if (!status == false) {
          notification.warning(
            `${showcase.DeliveryLocationList[index].place} is set to not available`
          );
        }
      }
    })
    .catch((error) => {
      notification.error("Failed to change availability");
    });
};

// open add new delivery location popup
const openAddNewDeliveryPopup = () => {
  showcase.processingDeliveryLocation = {
    place: "",
    cost: "",
    status: true,
  };
  uiStore.addDeliveryPopup = true;
};
</script>

<style scoped>
.page-title-section {
  display: flex;
  justify-content: space-between;
}
.add-new-button {
  margin: 54px 12px 0px 0px;
}
.table-container {
  margin-top: 25px;
  display: flex;
  width: calc(98% - 44px);
  padding: 19px 22px;
  flex-direction: column;
  align-items: flex-start;
  gap: 13px;
  border-radius: 6px;
  background: #fff;
}
.table-head {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 13px;
  align-self: stretch;
}
.table-head-title {
  display: flex;
  align-items: center;
  align-self: stretch;
}
#column1 {
  width: 28%;
}
#column2 {
  width: 24%;
}
#column3 {
  width: 30%;
}
#column4 {
  width: 18%;
}
.table-title {
  color: #41b06e;
  font-family: "Space Grotesk";
  font-size: 20px;
  font-weight: 400;
}
.column-devider {
  width: 100%;
  height: 0.6px;
  background: #7ac89a;
  border: none;
}
.table-column {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  align-self: stretch;
}
.table-column-content {
  display: flex;
  justify-content: center;
  align-items: center;
  align-self: stretch;
}
.column-text {
  color: #000;
  font-family: "Space Grotesk";
  font-size: 16px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
}
.available {
  padding: 5px 18px;
  flex: 1 0 0;
  border-radius: 4px;
  background: #41b06e;
  border: none;
  color: #fff;
  font-family: "Space Grotesk";
  font-size: 16px;
  font-weight: 400;
}
.available:hover {
  background: #67c08b;
}
.not-available {
  padding: 5px 18px;
  flex: 1 0 0;
  border-radius: 4px;
  background: #ff204e;
  border: none;
  color: #fff;
  font-family: "Space Grotesk";
  font-size: 16px;
  font-weight: 400;
}
.not-available:hover {
  background: #ff4d71;
}
.button-container {
  display: flex;
  padding-inline: 12px;
  justify-content: flex-end;
  align-items: center;
  gap: 13px;
  flex: 1 0 0;
}
.action-button-edit {
  width: 50%;
  padding: 4px 18px;
  border-radius: 4px;
  border: 1px solid #41b06e;
  background: #fff;
  color: #41b06e;
  font-family: "Space Grotesk";
  font-size: 16px;
  font-weight: 400;
}
.action-button-edit:hover {
  border: 1px solid #67c08b;
  background: #67c08b;
  color: #fff;
}
.action-button-edit:active {
  border: 1px solid #41b06e;
  background: #41b06e;
  color: #fff;
}

.action-button-delete {
  width: 50%;
  padding: 4px 18px;
  border-radius: 4px;
  border: 1px solid #ff204e;
  background: #fff;
  color: #ff204e;
  font-family: "Space Grotesk";
  font-size: 16px;
  font-weight: 400;
}
.action-button-delete:hover {
  border: 1px solid #ff4d71;
  background: #ff4d71;
  color: #fff;
}
.action-button-delete:active {
  border: 1px solid #ff204e;
  background: #ff204e;
  color: #fff;
}
</style>
