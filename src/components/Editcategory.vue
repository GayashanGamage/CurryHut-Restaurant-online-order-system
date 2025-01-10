<template>
  <div class="c-level-one-container">
    <div class="c-level-two-container">
      <div class="c-level-three-container window-header">
        <h3 class="window-title">RENAME CATEGORY</h3>
      </div>
      <div class="c-level-three-container window-content">
        <P class="info"
          >Current name :
          <span class="category-name">{{
            showcase.processingCategory["current_name"]
          }}</span></P
        >
        <input
          type="text"
          class="user-input"
          placeholder="New name"
          v-model="showcase.processingCategory['categoryName']"
        />
        <div class="button-container">
          <button
            id="cancel-button"
            class="action-button"
            @click="uistore.closeEditCategoryWindow()"
          >
            Cancel
          </button>
          <button
            id="confirm-button"
            class="action-button"
            @click="editeCategory"
          >
            Confirm
          </button>
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
import { useToast } from "vue-toast-notification";

// toast notification
const toast = useToast();

// pinia stores
const uistore = useUiStore();
const showcase = useShowCase();
const authontication = useAuthonticationStore();

const exsistingCategoryList = [];

for (let i = 0; i < showcase.categoryList.length; i++) {
  exsistingCategoryList.push(showcase.categoryList[i]["name"]);
}

const editeCategory = () => {
  // remove prefix & postfix space
  let userInput = showcase.processingCategory["categoryName"].trim();
  // check the user input - empty
  if (!userInput || userInput.length == 0) {
    toast.error("you cannot save empty string as a category !");
  }
  // check unDeletable values
  else if (showcase.unDeletable.includes(userInput.toLowerCase())) {
    toast.error("you cannot enter reserved categories !");
  }
  // check existing category name to duplicate
  else if (exsistingCategoryList.includes(userInput.toLowerCase())) {
    toast.error("you cannot insert existing categories !");
  }
  // else send request
  else {
    axios
      .patch(`${import.meta.env.VITE_url}/editcategory`, null, {
        headers: {
          Authorization: "Bearer " + authontication.cookies_token,
        },
        params: {
          id: showcase.processingCategory["id"],
          categoryName: showcase.processingCategory["categoryName"].trim(),
        },
      })
      .then((response) => {
        if (response.status == 200) {
          toast.success("you successfully update category");
          showcase.getCategoryDetails();
          uistore.closeEditCategoryWindow();
        }
      })
      .catch((response) => {
        toast.error(response.data);
        uistore.closeEditCategoryWindow();
      });
  }
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
  background: #41b06e;
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
  font-size: 24px;
  font-weight: 700;
  text-transform: uppercase;
}
.info {
  color: #41b06e;
  font-family: "Space Grotesk";
  font-size: 12px;
  font-style: normal;
  font-weight: 300;
  line-height: normal;
  align-self: flex-start;
  margin: 30px 0px 0px 70px;
}
.category-name {
  font-weight: 900;
}
.user-input {
  width: 290px;
  height: 35px;
  border-radius: 4px;
  border: 0.8px solid #7ac89a;
  background: #fff;
  padding: 0px 15px;
  color: #41b06e;
  font-family: "Space Grotesk";
  font-size: 20px;
  font-weight: 300;
  margin: 10px 0px 0px 0px;
}
.button-container {
  margin: 20px 0px 0px 0px;
  display: flex;
  gap: 20px;
}
#cancel-button {
  border: 1px solid #ff204e;
  color: #ff204e;
}
#cancel-button:hover {
  background: #ff204e;
  color: #fff;
}
</style>

<style></style>
