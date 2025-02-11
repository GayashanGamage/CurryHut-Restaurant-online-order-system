<!-- if shopstore menu is true then load 'set availability talbe'. otherwise load set menu table -->

<template>
  <div class="s-level-one-container">
    <div class="page-title-section">
      <h2 class="page-title">Todays' menu</h2>
    </div>
    <div class="s-level-two-container">
      <div class="s-level-three-container">

        <!-- set menu table -->
        <table class="table-outfit" v-if="!shopstore.menu">
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
                <input type="checkbox" class="tikbox" v-model="i.breakfast"
                  @click="changeMealtime(i.id, 'breakfast', i.breakfast)" />
              </td>
              <td class="table-row-data center-text">
                <input type="checkbox" class="tikbox" v-model="i.lunch"
                  @click="changeMealtime(i.id, 'lunch', i.lunch)" />
              </td>
              <td class="table-row-data center-text">
                <input type="checkbox" class="tikbox" v-model="i.dinner"
                  @click="changeMealtime(i.id, 'dinner', i.dinner)" />
              </td>
            </tr>
          </tbody>
        </table>

        <!-- set menu table -->
        <table class="table-outfit" v-if="shopstore.menu">
          <thead class="table-head">
            <tr class="table-title-row">
              <!-- this is for show categroy name and food name. no need to column name -->
              <th class="table-row-title name"></th>
              <th class="table-row-title dinner center-text">Availability</th>
            </tr>
          </thead>
          <tbody v-for="(value, key) in showcase.availableFood" :key="key">
            <!-- this is category sub title bars -->
            <tr class="category-title">
              <td colspan="6" class="category-title-text">{{ key }} category</td>
              <!-- <td colspan="6" class="category-title-text">{{ item[0]['category_id'] }} category</td> -->
            </tr>
            <!-- this include all food data of above category -->
            <tr class="table-row" v-for="i in value" :key="i">
              <td class="table-row-data food-name">{{ i.name }}</td>
              <td class="table-row-data toggle-position">
                <!-- toggle button -->
                <div class="toggle-button" id="shop8">
                  <p class="toggle-text-not">Unavailable</p>
                  <label class="switch"><input type="checkbox" id="checkbox" :checked="i.availability"
                    @click="setAvailabilityStatus(i.id, i.name)" />
                    <div></div>
                  </label>
                  <p class="toggle-text">Available</p>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="button-section" v-if="!shopstore.menu">
      <button class="action-button">CLEAR</button>
      <button class="action-button" @click="setMenu">CONFIRM</button>
    </div>
    <div class="button-section" v-if="shopstore.menu">
      <button class="action-button" @click="backToMenu">New Item for menu</button>
    </div>
  </div>
</template>

<script setup>
import { useAuthonticationStore } from "@/stores/authontication";
import { useShopStore } from "@/stores/shop";
import { useShowCase } from "@/stores/showcase";
import axios from "axios";
import { onBeforeMount, ref } from "vue";
import { useToast } from "vue-toast-notification";
const notification =  useToast()

// pinia stores
const showcase = useShowCase();
const authontication = useAuthonticationStore();
const shopstore =  useShopStore()


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
        showcase.getAllCategories(authontication.cookies_token);
      }
    }
    else{
      showcase.getAllCategories(authontication.cookies_token);
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
        showcase.getAllFoodItems(authontication.cookies_token);
      }
    }
    else{
      showcase.getAllFoodItems(authontication.cookies_token);
    }
  }
});

// if shopstore.menu is null, then request shop data
onBeforeMount(() => {
  if(shopstore.menu == null){
    if (
      authontication.cookies_token == null ||
      authontication.cookies_email == null
    ) {
      const credencials = authontication.restoreCredentials();
      if (credencials == false) {
        router.replace({ name: "login" });
      } else if (credencials == true) {
        shopstore.requestSettingData(authontication.cookies_token)
      }
    }
    else {
      shopstore.requestSettingData(authontication.cookies_token)
    }
  }
})

// onBeforeMount(() => {
//   showcase.updateMenu(showcase.foodItemList)
// })


const changeMealtime = (id, meal, availability) => {
  // TODO: this should update availability also
  showcase.shop_menu.find((item) => {
    if(item.id == id) {
      item[meal] = !availability;
      if(item['breakfast'] == true || item['lunch'] == true || item['dinner'] == true){
        item['availability'] = true
      }else{
        item['availability'] = false
      }
    }
  });
}

//  set todays menu
const setMenuSub = () => {
  axios
  .patch(`${import.meta.env.VITE_url}/menu/update`, 
  { menu : showcase.shop_menu},
  {
      headers: {
        Authorization: "Bearer " + authontication.cookies_token,
      },
    })
    .then((responce) => {
      if (responce.status == 200) {
        notification.success('menu update sucssfully')
        shopstore.menu = true
        showcase.getAllFoodItems()
      }
    })
    .catch((error) => {
      notification.error('something go wrong')
    });
  }
  
  // base request for set today menu
  // this depend on setMenu 
const setMenu = () => {
    if (
      authontication.cookies_token == null ||
      authontication.cookies_email == null
    ) {
      const credencials = authontication.restoreCredentials();
      if (credencials == false) {
        router.replace({ name: "login" });
      } else if (credencials == true) {
        setMenuSub();
      }
    }
    else {
      setMenuSub();
    }
  }

const setAvailabilityStatus = (food_id, name) => {
  axios.patch(`${import.meta.env.VITE_url}/menu/set-availability`, null, {
    params : {id : food_id},
    headers : {
      Authorization: "Bearer " + authontication.cookies_token,
    }
  })
  .then((responce) => {
    if(responce.status == 200){
      notification.success(`availablity set sucssesfull in ${name}`)
    }
  })
  .catch((error) => {
    notification.error('something go wrong !')
  })
}

const backToMenu = () => {
  shopstore.menu = false;
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
.toggle-position{
  display: flex;
  justify-content: center;
  align-items: center;
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
/* toggle button styling */
.toggle-button{
  display: flex;
}
.toggle-text {
  color: #41b06e;
  font-family: "Space Grotesk";
  font-weight: 900;
  font-size: 14px;
}
.toggle-text-not {
  color: red;
  font-family: "Space Grotesk";
  font-weight: 900;
  font-size: 14px;
}
.switch input {
  position: absolute;
  opacity: 0;
}

.switch {
  display: inline-block;
  font-size: 20px;
  /* 1 */
  height: 20px;
  width: 40px;
  background: #bdb9a6;
  border-radius: 1em;
  margin: 0px 20px;
}

.switch div {
  height: 1em;
  width: 1em;
  border-radius: 1em;
  background: #fff;
  box-shadow: 0 0.1em 0.3em rgba(0, 0, 0, 0.3);
  /* -webkit-transition: all 300ms; */
  /* -moz-transition: all 300ms; */
  /* transition: all 300ms; */
}

.switch input:checked+div {
  /* -webkit-transform: translate3d(100%, 0, 0); */
  /* -moz-transform: translate3d(100%, 0, 0); */
  transform: translate3d(100%, 0, 0);
}
</style>
