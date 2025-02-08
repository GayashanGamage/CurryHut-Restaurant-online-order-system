<template>
  <div class="s-level-one-container">
    <div class="page-title-section">
      <h2 class="page-title">Food Items</h2>
      <button
        class="action-button add-new-button"
        @click="uistore.openAddFoodWindow"
      >
        Add new
      </button>
    </div>
    <div class="s-level-two-container">
      <div class="s-level-three-container">
        <table class="table-outfit">
          <thead>
            <tr class="table-title-row">
              <th class="table-row-title name">Category</th>
              <th class="table-row-title name">Name</th>
              <th class="table-row-title count center-text">Varieties</th>
              <th class="table-row-title added center-text">Aded date</th>
              <th class="table-row-title edited center-text">Last modified</th>
              <th class="table-row-title edited"></th>
            </tr>
          </thead>
          <tbody>
            <!-- this include all category data -->
            <tr
              class="table-row"
              v-for="item in showcase.foodItemList"
              :key="item.id"
            >
              <!-- category name -->
              <!-- <td class="table-row-data">{{ item.category_id   }}</td> -->
              <td class="table-row-data">{{ findCategoryName(item.category_id) }}</td>
            
              <!-- food name -->
              <td class="table-row-data">{{ item.name }}</td>
              
              <!-- variety count -->
              <td class="table-row-data center-text">
                {{ item.price.length }}
              </td>
              <td class="table-row-data center-text">
                {{
                  `${new Date(item["added_data"]).getFullYear()}-${new Date(
                    item["added_data"]
                  ).getMonth()}-${new Date(item["added_data"]).getDate()}`
                }}
              </td>
              <td class="table-row-data center-text">
                {{
                  `${new Date(item["modified_data"]).getFullYear()}-${new Date(
                    item["modified_data"]
                  ).getMonth()}-${new Date(item["modified_data"]).getDate()}`
                }}
              </td>
              <td c lass="table-row-data table-row-data-button">
                <button
                  class="action-button table-button"
                  @click="uistore.foodViewOpen(item.id)"
                >
                  View
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
import { useAuthonticationStore } from "@/stores/authontication";
import { useShowCase } from "@/stores/showcase";
import { useUiStore } from "@/stores/ui";
import axios from "axios";
import { onBeforeMount, onMounted } from "vue";
import { useToast } from "vue-toast-notification";
const uistore = useUiStore();

const toast = useToast();

const authontication = useAuthonticationStore();
const showcase = useShowCase();

onBeforeMount(() => {
  if(showcase.foodItemList === null){
    if (
      authontication.cookies_token == null ||
      authontication.local_storage_email == null
    ) {
      const credencial = authontication.restoreCredentials();
      if (credencial == false) {
        router.replace({ name: "login" });
      } else if (credencial == true) {
        axios
        .get(`${import.meta.env.VITE_url}/getallfood`, {
          headers: {
            Authorization: "Bearer " + authontication.cookies_token,
          },
        })
        .then((response) => {
            showcase.foodItemList = response.data;
          })
          .catch((response) => {
            if (response.status == 401) {
              authontication.removeCredentials();
              router.replace({ name: "login" });
            } else {
              toast.error("something go wrong");
            }
          });
        }
      }
    
  }
  });
  
// if category still not loaded to categoryList variable, load it
onBeforeMount(() => {
if (showcase.categoryList === null) {
  axios
    .get(`${import.meta.env.VITE_url}/category/getcategories`, {
      headers: {
        Authorization: "Bearer " + authontication.cookies_token,
      },
    })
    .then((response) => {
      if (response.status == 200) {
        showcase.categoryList = response.data;
      }
    })
    .catch((error) => {
      if (error.status == 401) {
        authontication.removeCredentials();
        router.replace({ name: "login" });
      } else {
        toast.error("something go wrong");
      }
    });
  }
});

// find category name from category id
const findCategoryName = (id) => {
  if(showcase.categoryList !== null){
    for(let i = 0; i <= showcase.categoryList.length; i++) {
      if(showcase.categoryList[i].id == id) {
        return showcase.categoryList[i].name;
      }
    }
    return "something wrong";
  }
}


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
.table-row-data-button {
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
