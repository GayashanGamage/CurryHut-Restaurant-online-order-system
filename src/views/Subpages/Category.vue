<template>
  <div class="s-level-one-container">
    <div class="page-title-section">
      <h2 class="page-title">Category</h2>
      <button class="action-button" @click="uistore.openNewCategoryWindow">
        Add new
      </button>
    </div>
    <div class="s-level-two-container">
      <div class="s-level-three-container">
        <table class="table-outfit">
          <thead>
            <tr class="table-title-row">
              <th class="table-row-title code">Code</th>
              <th class="table-row-title name">Name</th>
              <th class="table-row-title count">Item count</th>
            </tr>
          </thead>
          <tbody>
            <tr class="table-row">
              <td class="table-row-data">FR001</td>
              <td class="table-row-data">Fried Rice</td>
              <td class="table-row-data">07</td>
              <td class="table-row-data table-row-data-button">
                <button class="action-button table-button">Edit</button>
              </td>
              <td class="table-row-data table-row-data-button">
                <button class="action-button table-button delete-button">
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
import { useUiStore } from "@/stores/ui";

const uistore = useUiStore();
</script>

<style scoped>
.page-title-section {
  display: flex;
  justify-content: space-between;
}
.action-button {
  margin: 47px 21px 0px 0px;
}
/* .s-level-one-container {
  padding-bottom: 1px;
} */
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
  width: 150px;
}
.name {
  width: 600px;
}
.table-title-row {
  /* background-color: yellow; */
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
  color: #000;
  font-family: "Space Grotesk";
  font-size: 18px;
  font-weight: 400;
  border-top: 1px solid #7ac89a;
}
.table-row-data-button {
  border: 0px;
  float: right;
  margin: 10px 0px 10px 10px;
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
.table-button {
  margin: 0px;
}
</style>
