<template>
  <div class="c1-level-one-container">
    <div class="c1-level-two-container">
      <div class="c1-level-three-container window-header">
        <h3 class="window-title">ADD NEW FOOD ITEM</h3>
      </div>
      <div class="c1-level-three-container window-content">
        <div class="field-section">
          <p class="field-name">Category :</p>
          <select class="user-input">
            <option
              v-for="item in showcase.categoryList"
              :key="item.id"
              :value="item.id"
              @click="showcase.processingFoodItem.category_id = item.id"
            >
              {{ item.name }}
            </option>
          </select>
        </div>
        <div class="field-section">
          <p class="field-name">Name :</p>
          <input
            type="text"
            id="name-input"
            v-model="showcase.processingFoodItem.name"
          />
        </div>
        <div class="field-section">
          <p class="field-name">Image :</p>
          <label for="file-upload" class="image-input">Upload image</label>
          <input type="file" id="file-upload" />
        </div>
        <div class="field-section">
          <p class="field-name">Description :</p>
          <div class="field-sub-section">
            <textarea
              cols="30"
              rows="10"
              id="description-input"
              maxlength="300"
              v-model="showcase.processingFoodItem.description"
            ></textarea>
            <p class="info">
              {{ 300 - showcase.processingFoodItem.description.length }}
              characters
            </p>
          </div>
        </div>
        <div class="section-divider">
          <p class="field-name">Price</p>
          <hr class="ruler" />
        </div>
        <div class="field-section">
          <table class="table-container">
            <thead class="table-head">
              <tr>
                <th class="column-title name-column">Name</th>
                <th class="column-title potion-column">Potion size</th>
                <th class="column-title price-column">Price</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>
                  <input
                    type="text"
                    class="table-data name-column name-column-data"
                    v-model="showcase.processingFoodItem.price[0].name"
                  />
                </td>
                <td>
                  <input
                    type="number"
                    class="table-data potion-column potion-column-data"
                    v-model="showcase.processingFoodItem.price[0].price"
                  />
                </td>
                <td>
                  <input
                    type="text"
                    class="table-data price-column price-column-data"
                    v-model="showcase.processingFoodItem.price[0].portion"
                  />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="button-section">
          <button
            class="action-button cancel-button"
            @click="uistore.closeAddFoodWindow()"
          >
            Cancel
          </button>
          <button class="action-button" @click="addNewFood">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import router from "@/router";
import { useAuthonticationStore } from "@/stores/authontication";
import { useShowCase } from "@/stores/showcase";
import { useUiStore } from "@/stores/ui";
import axios from "axios";
import { onBeforeMount, onBeforeUnmount } from "vue";
import { useToast } from "vue-toast-notification";

// pinia stores
const uistore = useUiStore();
const authontication = useAuthonticationStore();
const toast = useToast();
const showcase = useShowCase();

onBeforeUnmount(() => {
  if (uistore.logoutPopupWindow === true) {
    uistore.logoutPopupWindow = false;
  }
});

// add new items request
const addNewFood = () => {
  axios
    .post(
      `${import.meta.env.VITE_url}/addfooditem`,
      showcase.processingFoodItem,
      {
        headers: {
          Authorization: "Bearer " + authontication.cookies_token,
        },
      }
    )
    .then((response) => {
      if (response.status == 200) {
        showcase.processingFoodItem = null;
        showcase.getAllFoodItems();
        toast.success("new item added successfully");
        uistore.closeAddFoodWindow();
      }
    })
    .catch((response) => {
      showcase.processingFoodItem = null;
      uistore.closeAddFoodWindow();
      toast.error("something go wrong. try again.");
    });
};

// load first category item as a default
onBeforeMount(() => {
  showcase.processingFoodItem.category_id = showcase.categoryList[0].id;
})

</script>

<style scoped>
.c1-level-one-container {
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
.c1-level-two-container {
  width: 586px;
  height: 600px;
  border-radius: 6px;
  background: #fff;
}
.window-header {
  width: 100%;
  height: 50px;
  border-radius: 6px 6px 0px 0px;
  background: #41b06e;
  display: flex;
  justify-content: center;
  align-items: center;
}
.window-title {
  color: #fff;
  font-family: "Space Grotesk";
  font-size: 24px;
  font-weight: 700;
  text-transform: uppercase;
}
.window-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  margin-top: 10px;
}
.field-section {
  width: 90%;
  margin: 10px 0px;
  display: flex;
  justify-content: space-between;
}
.field-name {
  color: #000;
  font-family: "Space Grotesk";
  font-size: 18px;
  font-weight: 300;
}
.field-sub-section {
  display: flex;
  flex-direction: column;
  align-items: end;
}
.section-divider {
  width: 90%;
}
.ruler {
  width: 100%;
}
.table-container {
  width: 100%;
  margin: 20px 10px;
}
.column-title {
  text-align: left;
  font-family: "Space Grotesk";
  font-weight: 400;
}
.name-column {
  width: 220px;
  margin-right: 10px;
}
.name-column-data {
  height: 26px;
  border-radius: 4px;
  border: 0.5px solid #adadad;
  background: #fff;
  padding-left: 10px;
}
.potion-column {
  width: 80px;
  margin-right: 10px;
}
.potion-column-data {
  height: 26px;
  border-radius: 4px;
  border: 0.5px solid #adadad;
  background: #fff;
  padding-left: 10px;
}
.price-column {
  width: 150px;
  margin-right: 10px;
}
.price-column-data {
  height: 26px;
  border-radius: 4px;
  border: 0.5px solid #adadad;
  background: #fff;
  padding-left: 10px;
}
.table-data {
  font-family: "Space Grotesk";
  font-size: 17px;
}
.button-section {
  align-self: flex-end;
  /* margin-right: 30px; */
  width: 240px;
}
.action-button {
  margin: 0px 10px;
}
.cancel-button {
  border-radius: 4px;
  border: 1px solid #ff204e;
  background: #fff;
  color: #ff204e;
}
.cancel-button:hover {
  border: 1px solid #ff204e;
  background: #ff204e;
  color: #fff;
  font-family: "Space Grotesk";
}
#name-input {
  width: 323px;
  height: 34px;
  border-radius: 3px;
  border: 0.8px solid #41b06e;
  background: #fff;
  padding-left: 10px;
  font-size: 16px;
}
#description-input {
  width: 313px;
  height: 88px;
  border-radius: 3px;
  border: 0.8px solid #41b06e;
  background: #fff;
  resize: none;
  font-family: "Space Grotesk";
  padding: 10px;
}
input[type="file"] {
  display: none;
}
.image-input {
  margin-right: 205px;
  border: 0.8px solid #41b06e;
  font-family: "Space Grotesk";
  border-radius: 4px;
  padding: 6px 12px;
  color: #41b06e;
}
.image-input:hover {
  border: 0.8px solid #41b06e;
  background: #41b06e;
  color: #fff;
}
.user-input {
  width: 333px;
  font-family: "Space Grotesk";
  font-size: 16px;
  height: 30px;
  background-color: #fff;
  border-radius: 4px;
  border: 0.8px solid #41b06e;
  padding-left: 10px;
}
.info {
  margin-top: 10px;
  font-size: 14px;
  font-family: "Space Grotesk";
  color: #41b06e;
}
</style>
