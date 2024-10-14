<template>
  <div class="s-level-one-container">
    <div class="page-title-section">
      <h2 class="page-title">Food Items</h2>
      <button class="action-button add-new-button">Add new</button>
    </div>
    <div class="s-level-two-container">
      <div class="s-level-three-container">
        <table class="table-outfit">
          <thead>
            <tr class="table-title-row">
              <th class="table-row-title code">Code</th>
              <th class="table-row-title name">Name</th>
              <th class="table-row-title count center-text">Category</th>
              <th class="table-row-title added center-text">Aded date</th>
              <th class="table-row-title edited center-text">Last modified</th>
              <th class="table-row-title edited"></th>
            </tr>
          </thead>
          <tbody>
            <!-- this include all category data -->
            <tr class="table-row">
              <td class="table-row-data">2A34</td>
              <td class="table-row-data">Chicken Fired Rice</td>
              <td class="table-row-data center-text">Fried Rice</td>
              <td class="table-row-data center-text">2024-10-12</td>
              <td class="table-row-data center-text">2024-10-17</td>
              <td class="table-row-data table-row-data-button">
                <button class="action-button table-button">View</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup></script>

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
