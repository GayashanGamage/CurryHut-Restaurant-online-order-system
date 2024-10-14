<template>
  <div class="c-level-one-container">
    <div class="c-level-two-container">
      <div class="c-level-three-container window-header">
        <h3 class="window-title">DELETE CATEGORY</h3>
      </div>
      <div class="c-level-three-container window-content">
        <P class="info"
          >Are you sure you want to delete
          <span class="category-name">Fried Rice</span> category</P
        >
        <div class="button-container">
          <button
            id="cancel-button"
            class="action-button"
            @click="uistore.closeDeleteCategoryWindow()"
          >
            Cancel
          </button>
          <button
            id="confirm-button"
            class="action-button"
            @click="deleteAction"
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

// pinia store reference
const uistore = useUiStore();
const authontication = useAuthonticationStore();
const showcase = useShowCase();

const deleteAction = () => {
  // check unDeletable categories
  if (showcase.unDeletable.includes(showcase.processingCategory["name"])) {
    toast.error("you cannot remove reserved categories !");
  } else {
    axios
      .delete(
        `${import.meta.env.VITE_url}/deletecategory/${
          showcase.processingCategory["_id"]
        }`,
        {
          headers: {
            Authorization: "Bearer " + authontication.authcookie,
          },
        }
      )
      .then((response) => {
        if (response.status == 200) {
          toast.success("delete selecte category successfully");
          showcase.getCategoryDetails();
          uistore.closeDeleteCategoryWindow();
        }
      })
      .catch((response) => {
        toast.error(response.data);
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
  font-size: 22px;
  text-align: center;
  font-style: normal;
  font-weight: 300;
  line-height: normal;
  align-self: flex-start;
  margin: 30px 30px 10px 30px;
}
.category-name {
  font-weight: 900;
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
