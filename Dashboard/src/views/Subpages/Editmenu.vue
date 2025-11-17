<template>
  <div class="s-level-one-container">
    <div class="page-title-section">
      <h2 class="page-title">Todays' menu - EDIT</h2>
      <button
        class="action-button add-button"
        @click="uistore.openAddNewAvailableFood()"
      >
        Add new
      </button>
    </div>
    <div class="s-level-two-container">
      <div class="s-level-three-container">
        <table class="table-outfit">
          <thead>
            <tr class="table-title-row">
              <th class="table-row-title category">Category</th>
              <th class="table-row-title name">Name</th>
              <th class="table-row-title code center-text">Item code</th>
              <th class="table-row-title code center-text">Availability</th>
              <th class="table-row-title meals center-text">Br.</th>
              <th class="table-row-title meals center-text">Lu.</th>
              <th class="table-row-title meals center-text">Din.</th>
              <th class="table-row-title action center-text"></th>
            </tr>
          </thead>
          <tbody>
            <!-- this include all category data -->
            <tr class="table-row">
              <td class="table-row-data"></td>
              <td class="table-row-data"></td>
              <td class="table-row-data center-text"></td>
              <td class="table-row-data center-text">
                <!-- <input type="checkbox" /> -->
                <!-- <div class="toggle-button-cover"> -->
                <div class="button-cover">
                  <div class="button r" id="button-1">
                    <input type="checkbox" class="checkbox" />
                    <div class="knobs"></div>
                    <div class="layer"></div>
                  </div>
                </div>
                <!-- </div> -->
              </td>
              <td class="table-row-data center-text">
                <input type="checkbox" class="tikbox" disabled />
              </td>
              <td class="table-row-data center-text">
                <input type="checkbox" class="tikbox" disabled />
              </td>
              <td class="table-row-data center-text">
                <input type="checkbox" class="tikbox" disabled />
              </td>
              <td class="table-row-data center-text">
                <button
                  class="action-button"
                  @click="uistore.openEditFoodTime()"
                >
                  EDIT
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="popup-background" v-if="uistore.foodAvailableTime">
      <div class="popup-box">
        <div class="popup-header">
          <p class="popup-header-text">select available time</p>
        </div>
        <div class="popup-content">
          <div class="brekfirst-check content-check-div">
            <label for="breakfist" class="checkbox-lable">Breakfirst</label>
            <input type="checkbox" id="breakfist" class="tikbox" />
          </div>
          <div class="luch-check content-check-div">
            <label for="lunch" class="checkbox-lable">Breakfirst</label>
            <input type="checkbox" id="lunch" class="tikbox" />
          </div>
          <div class="dinner-check content-check-div">
            <label for="dinner" class="checkbox-lable">Breakfirst</label>
            <input type="checkbox" id="dinner" class="tikbox" />
          </div>
        </div>
        <div class="popup-button">
          <button
            class="action-button cancel"
            @click="uistore.closeEditFoodTime()"
          >
            cancel
          </button>
          <button class="action-button">save</button>
        </div>
      </div>
    </div>
    <!-- add new food popup -->
    <div class="popup-background" v-if="uistore.addNewAvailableFood">
      <div class="popup-box-add-new">
        <div class="popup-header">
          <p class="popup-header-text">new food for today's menu</p>
        </div>
        <div class="popup-content-add-new">
          <div class="category-dropdown">
            <label for="category-dropdown" class="dropdown-name"
              >Category :</label
            >
            <select
              name="category-dropdown"
              id="category-dropdown"
              class="dropdown-box"
            >
              <option value="">One</option>
              <option value="">Two</option>
            </select>
          </div>
          <div class="category-dropdown">
            <label for="category-dropdown" class="dropdown-name">Food :</label>
            <select
              name="category-dropdown"
              id="category-dropdown"
              class="dropdown-box"
            >
              <option value="">One</option>
              <option value="">Two</option>
            </select>
          </div>
          <div class="food-time">
            <div class="brekfirst-check content-check-div">
              <label for="breakfist" class="checkbox-lable">Breakfirst</label>
              <input type="checkbox" id="breakfist" class="tikbox" />
            </div>
            <div class="luch-check content-check-div">
              <label for="lunch" class="checkbox-lable">Lunch</label>
              <input type="checkbox" id="lunch" class="tikbox" />
            </div>
            <div class="dinner-check content-check-div">
              <label for="dinner" class="checkbox-lable">Dinner</label>
              <input type="checkbox" id="dinner" class="tikbox" />
            </div>
          </div>
        </div>
        <div class="popup-button add-new-button">
          <button
            class="action-button cancel"
            @click="uistore.closeAddNewAvailableFood()"
          >
            cancel
          </button>
          <button class="action-button">save</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthonticationStore } from "@/stores/authontication";
import { useShowCase } from "@/stores/showcase";
import { useUiStore } from "@/stores/ui";

// pinia stores
const showcase = useShowCase();
const authontication = useAuthonticationStore();
const uistore = useUiStore();
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
  padding: 17px 0px;
  font-family: "Space Grotesk";
  color: #000;
  border-top: 1px solid #7ac89a;
}
.center-text {
  text-align: center;
}
.category {
  width: 200px;
}
.name {
  width: 240px;
}
.code {
  width: 100px;
}
.action {
  width: 100px;
}
.meals {
  width: 100px;
}
.tikbox {
  width: 30px;
  height: 30px;
  flex-shrink: 0;
  accent-color: rgba(207, 244, 206, 0.5);
}
/* toggle button */
.button-cover {
  margin-top: 16px;
  height: 36px;
  width: 76px;
  /* margin: 40px; */
  /* border: 1px solid black; */
  background-color: #cff4ce;
  /* box-shadow: 0 10px 20px x -8px #c5d6d6; */
  border-radius: 20px;
}
.button {
  position: relative;
  /* top: 50%; */
  width: 74px;
  height: 36px;
  margin: -20px auto 0 auto;
  overflow: hidden;
}
.button.r {
  border-radius: 100px;
}
.checkbox {
  position: relative;
  width: 100%;
  height: 100%;
  padding: 0;
  margin: 0;
  opacity: 0;
  cursor: pointer;
  z-index: 3;
}
.knobs {
  z-index: 2;
}

.layer {
  width: 100%;
  background-color: #ebf7fc;
  transition: 0.3s ease all;
  z-index: 1;
}
#button-1 .knobs:before {
  content: "YES";
  position: absolute;
  top: 4px;
  left: 4px;
  width: 20px;
  height: 10px;
  color: #fff;
  font-size: 10px;
  font-weight: bold;
  text-align: center;
  line-height: 1;
  padding: 9px 4px;
  background-color: #41b06e;
  border-radius: 50%;
  transition: 0.3s cubic-bezier(0.18, 0.89, 0.35, 1.15) all;
}

#button-1 .checkbox:checked + .knobs:before {
  content: "NO";
  left: 42px;
  background-color: #f44336;
}

#button-1 .checkbox:checked ~ .layer {
  background-color: #fcebeb;
}

#button-1 .knobs,
#button-1 .knobs:before,
#button-1 .layer {
  transition: 0.3s ease all;
}
.popup-background {
  width: 100vw;
  height: 100vh;
  top: 0;
  left: 0;
  position: absolute;
  background-color: rgba(26, 26, 29, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
}
.popup-box {
  width: 450px;
  height: 295px;
  border-radius: 6px;
  background-color: white;
}
.popup-header {
  width: 100%;
  height: 60px;
  flex-shrink: 0;
  border-radius: 6px 6px 0px 0px;
  background: #41b06e;
  display: flex;
  justify-content: center;
  align-items: center;
}
.popup-header-text {
  color: #fff;
  font-family: "Space Grotesk";
  font-size: 24px;
  font-style: normal;
  font-weight: 700;
  line-height: normal;
  text-transform: uppercase;
}
.content-check-div {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 20px;
}
.popup-content {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  height: 60%;
  gap: 20px;
}
.popup-content-add-new {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 300px;
  gap: 20px;
}

.checkbox-lable {
  color: #41b06e;
  font-family: "Space Grotesk";
  font-size: 20px;
  font-weight: 300;
}
.cancel {
  border: 1.5px solid red;
  background: #fff;
  color: red;
}
.cancel:hover {
  border: 1.5px solid red;
  background: red;
  color: white;
}
.popup-button {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  height: 19%;
  gap: 20px;
  margin-right: 20px;
}
.add-new-button {
  margin-block: 20px;
  margin-right: 60px;
}
.add-button {
  margin-top: 60px;
  margin-right: 12px;
}
.popup-box-add-new {
  width: 449px;
  height: auto;
  border-radius: 6px;
  background: #fff;
}
.food-time {
  display: flex;
  gap: 50px;
}
.category-dropdown {
  width: 72%;
  display: flex;
  flex-direction: column;
}
.dropdown-name {
  color: #000;
  font-family: "Space Grotesk";
  font-size: 20px;
  font-style: normal;
  font-weight: 300;
  line-height: normal;
}
.dropdown-box {
  margin-top: 8px;
  width: 100%;
  height: 34px;
  padding-inline: 10px;
  border-radius: 4px;
  border: 0.8px solid #41b06e;
  background: #fff;
  color: #000;
  font-family: "Space Grotesk";
  font-size: 16px;
  font-weight: 300;
}
</style>
