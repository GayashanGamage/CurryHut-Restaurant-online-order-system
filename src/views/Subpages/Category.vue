<template>
  <div class="s-level-one-container">
    <div class="page-title-section">
      <h2 class="page-title">Category</h2>
      <button
        class="action-button add-new-button"
        @click="uistore.openNewCategoryWindow"
      >
        Add new
      </button>
    </div>
    <div class="s-level-two-container">
      <div class="s-level-three-container">
        <table class="table-outfit">
          <thead>
            <tr class="table-title-row">
              <!-- <th class="table-row-title code">Code</th> -->
              <th class="table-row-title name">Name</th>
              <th class="table-row-title count center-text">Item count</th>
              <th class="table-row-title added center-text">Aded date</th>
              <th class="table-row-title edited center-text">Last modified</th>
              <th class="table-row-title edited"></th>
              <th class="table-row-title edited"></th>
            </tr>
          </thead>
          <tbody>
            <tr
              class="table-row"
              v-for="item in showcase.categoryList"
              :key="item['_id']"
            >
              <td class="table-row-data">{{ item["name"].charAt(0).toUpperCase() + item["name"].slice(1).toLowerCase() }}</td>
              
              <!-- food item count  -->
              <td class="table-row-data center-text">
                {{ foodItemCount(item['id']) }}
                <!-- 0 -->
              </td>
              <td class="table-row-data center-text">
                {{
                  `${new Date(item["aded_date"]).getFullYear()}-${new Date(
                    item["aded_date"]
                  ).getMonth()}-${new Date(item["aded_date"]).getDate()}`
                }}
              </td>
              <td class="table-row-data center-text">
                {{
                  `${new Date(
                    item["last_modify_date"]
                  ).getFullYear()}-${new Date(
                    item["last_modify_date"]
                  ).getMonth()}-${new Date(item["last_modify_date"]).getDate()}`
                }}
              </td>
              <td class="table-row-data table-row-data-button">
                <button
                  class="action-button table-button"
                  v-if="item['deletable']"
                  @click="
                    uistore.openEditCategoryWindow({
                      id: item['id'],
                      current_name: item['name'],
                      categoryName: null,
                    })
                  "
                >
                  Edit
                </button>
              </td>
              <td class="table-row-data table-row-data-button">
                <button
                  class="action-button table-button delete-button"
                  v-if="item['deletable']"
                  @click="
                    uistore.openDeleteCategoryWindow(item['id'], item['name'])
                  "
                >
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
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
import { onBeforeMount } from "vue";
import { useToast } from "vue-toast-notification";

// toast notification
const toast = useToast();

// pinia stores
const showcase = useShowCase();
const authontication = useAuthonticationStore();
const uistore = useUiStore();

onBeforeMount(() => {
  if (
    authontication.cookies_token == null ||
    authontication.cookies_email == null
  ) {
    const credencials = authontication.restoreCredentials();
    if (credencials == false) {
      router.replace({ name: "login" });
    } else if (credencials == true) {
      showcase.getAllCategories(); // get all category details
    }
  }
});

onBeforeMount(() => {
  if (showcase.foodItemList === null) {
    showcase.getAllFoodItems();
  }
})


const foodItemCount = (id) => {
  console.log('called' + showcase.foodItemList)
  if(showcase.foodItemList !== null){
    
    var foodCount = 0
    for(let i = 0; i < showcase.foodItemList.length; i++){
      if(showcase.foodItemList[i].category_id == id){
        console.log('counted ')
        foodCount += 1
      }
    }
    return foodCount
  }
};


</script>

<style scoped>
.page-title-section {
  display: flex;
  justify-content: space-between;
}
.s-level-three-container {
  display: flex;
  justify-content: center;
  align-items: center;
}
.table-outfit {
  margin-top: 16px;
  width: 96%;
}
.code {
  width: 100px;
}
.name {
  width: 250px;
}
.table-title-row {
  text-align: left;
}
.table-row-title {
  color: #41b06e;
  font-family: "Space Grotesk";
  font-size: 20px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
}
.delete-button {
  border: 1px solid #ff204e;
  background: #fff;
  color: #ff204e;
}
.delete-button:hover {
  border: 1px solid #ff204e;
  background: #ff204e;
  color: #fff;
}
.table-row-data {
  font-size: 17px;
  padding: 17px 0px;
  font-family: "Space Grotesk";
  color: #000;
  border-top: 1px solid #7ac89a;
}
.add-new-button {
  margin: 54px 12px 0px 0px;
}
.center-text {
  text-align: center;
}
</style>
