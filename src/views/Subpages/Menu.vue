<template>
  <div class="s-level-one-container">
    <div class="page-title-section">
      <h2 class="page-title">Todays' menu</h2>
    </div>
    <div class="s-level-two-container">
      <div class="s-level-three-container">
        <table class="table-outfit">
          <thead class="table-head">
            <tr class="table-title-row">
              <!-- <th class="table-row-title category">Nane</th> -->
              <th class="table-row-title name"></th>
              <!-- <th class="table-row-title code center-text">Item code</th> -->
              <th class="table-row-title breakfirst center-text">
                Breackfirst
              </th>
              <th class="table-row-title lunch center-text">Lunch</th>
              <th class="table-row-title dinner center-text">Dinner</th>
            </tr>
          </thead>
          <tbody v-for="(value, key) in showcase.sortedFood" :key="key">
            <!-- this is category sub title bars -->
            <tr class="category-title">
              <td colspan="6" class="category-title-text">{{ key }} category</td>
              <!-- <td colspan="6" class="category-title-text">{{ item[0]['category_id'] }} category</td> -->
            </tr> 
            <!-- this include all food data of above category -->
            <tr class="table-row" v-for="i in value" :key="i">
              <td class="table-row-data food-name">{{ i.name }}</td>
              <!-- <td class="table-row-data"></td> -->
              <!-- <td class="table-row-data center-text"></td> -->
              <td class="table-row-data center-text">
                <input type="checkbox" class="tikbox" v-model="i.breakfast" @click="changeMealtime(i.id, 'breakfast', i.breakfast)"/>
              </td>
              <td class="table-row-data center-text">
                <input type="checkbox" class="tikbox" v-model="i.lunch" @click="changeMealtime(i.id, 'lunch', i.lunch)"/>
              </td>
              <td class="table-row-data center-text">
                <input type="checkbox" class="tikbox" v-model="i.dinner" @click="changeMealtime(i.id, 'dinner', i.dinner)" />
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="button-section">
      <button class="action-button">CLEAR</button>
      <button class="action-button">CONFIRM</button>
    </div>
  </div>
</template>

<script setup>
import { useAuthonticationStore } from "@/stores/authontication";
import { useShowCase } from "@/stores/showcase";
import { onBeforeMount, ref } from "vue";

// pinia stores
const showcase = useShowCase();
const authontication = useAuthonticationStore();


// if categories not available(null), then fetch from server
onBeforeMount(() => {
  if(showcase.categoryList == null){
    if (
      authontication.cookies_token == null ||
      authontication.cookies_email == null
    ) {
      const credencials = authontication.restoreCredentials();
      if (credencials == false) {
        router.replace({ name: "login" });
      } else if (credencials == true) {
        showcase.getAllCategories();
      }
    }
    else{
      showcase.getAllCategories();
    }
  }
});

// if food items not availble(null), then fetch from server
onBeforeMount(() => {
  if(showcase.foodItemList == null){
    if (
      authontication.cookies_token == null ||
      authontication.cookies_email == null
    ) {
      const credencials = authontication.restoreCredentials();
      if (credencials == false) {
        router.replace({ name: "login" });
      } else if (credencials == true) {
        showcase.getAllFoodItems();
      }
    }
    else{
      showcase.getAllFoodItems();
    }
  }
});

const changeMealtime = (id, meal, availability) => {
  console.log(availability)
  showcase.shop_menu.find((item) => {
    if(item.id == id){
      item[meal] = !availability;
    }
  });
}

</script>

<style scoped>
.category-title{
  color: #41b06e;
  font-family: "Space Grotesk";
  height: 40px;
  background-color: rgba(207, 244, 206, 0.5);
  font-size: 16px;
  font-family: "Space Grotesk";
  font-weight: 900;
  text-transform: capitalize;
  border-radius: 4px;
}
.category-title-text{
  padding-left: 20px;
}
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
.table-head{
  height: 50px;
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
.table-row-data {
  font-size: 17px;
  padding: 12px 0px;
  font-family: "Space Grotesk";
  color: #000;
  border-top: 1px solid #7ac89a;
}
.center-text {
  text-align: center;
}
.category {
  width: 250px;
}
.name {
  width: 60%;
}
.code {
  width: 13%;
}
.tikbox {
  width: 30px;
  height: 30px;
  flex-shrink: 0;
  /* accent-color: #41b06e; */
  accent-color: rgba(207, 244, 206, 0.5);
}
.button-section {
  margin: 20px 10px 0px 10px;
  display: flex;
  justify-content: end;
  gap: 10px;
}
.food-name{
  padding-left: 40px;
}
</style>
