<template>
  <div class="s-level-one-container">
    <div class="page-title-section">
      <h2 class="page-title">Todays' menu</h2>
    </div>
    <div class="s-level-two-container">
      <div class="s-level-three-container">
        <table class="table-outfit">
          <thead>
            <tr class="table-title-row">
              <th class="table-row-title category">Category</th>
              <th class="table-row-title name">Name</th>
              <th class="table-row-title code center-text">Item code</th>
              <th class="table-row-title breakfirst center-text">
                Breackfirst
              </th>
              <th class="table-row-title lunch center-text">Lunch</th>
              <th class="table-row-title dinner center-text">Dinner</th>
            </tr>
          </thead>
          <tbody>
            <!-- this include all category data -->
            <tr class="table-row">
              <td class="table-row-data"></td>
              <td class="table-row-data"></td>
              <td class="table-row-data center-text"></td>
              <td class="table-row-data center-text">
                <input type="checkbox" class="tikbox" @click="checkValue" />
              </td>
              <td class="table-row-data center-text">
                <input type="checkbox" class="tikbox" />
              </td>
              <td class="table-row-data center-text">
                <input type="checkbox" class="tikbox" />
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
import { useUiStore } from "@/stores/ui";

// pinia stores
const showcase = useShowCase();
const authontication = useAuthonticationStore();

const checkValue = () => {
  console.log(document.getElementsByClassName("tikbox")[0].checked);
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
  width: 250px;
}
.name {
  width: 300px;
}
.code {
  width: 100px;
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
</style>
