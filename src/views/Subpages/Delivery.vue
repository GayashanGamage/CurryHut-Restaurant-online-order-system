<template>
  <div class="s-level-one-container">
    <div class="page-title-section">
      <h2 class="page-title">Delivery</h2>
      <button
        class="action-button add-new-button"
        @click="uistore.openNewCategoryWindow"
      >
        Add new
      </button>
    </div>
    <div class="s-level-two-container">
      <div class="table-container">
        <div class="table-head">
          <div class="table-head-title">
            <p class="table-title" id="column1">Location</p>
            <p class="table-title" id="column2">Price</p>
            <p class="table-title" id="column3">Availability</p>
          </div>
          <hr class="column-devider" />
        </div>
        <div class="table-column">
          <div class="table-column-content">
            <p class="column-text" id="column1">Nawala</p>
            <p class="column-text" id="column2">100</p>
            <button class="available" id="column3">Available</button>
            <div class="button-container" id="column4">
              <button class="action-button-edit">Edit</button>
              <button class="action-button-delete">Delete</button>
            </div>
          </div>
          <hr class="column-devider" />
        </div>
        <div class="table-column">
          <div class="table-column-content">
            <p class="column-text" id="column1">Nawala</p>
            <p class="column-text" id="column2">100</p>
            <button class="not-available" id="column3">Available</button>
            <div class="button-container" id="column4">
              <button class="action-button-edit">Edit</button>
              <button class="action-button-delete">Delete</button>
            </div>
          </div>
          <hr class="column-devider" />
        </div>
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
.add-new-button {
  margin: 54px 12px 0px 0px;
}
.table-container {
  margin-top: 25px;
  display: flex;
  width: calc(98% - 44px);
  padding: 19px 22px;
  flex-direction: column;
  align-items: flex-start;
  gap: 13px;
  border-radius: 6px;
  background: #fff;
}
.table-head {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 13px;
  align-self: stretch;
}
.table-head-title {
  display: flex;
  align-items: center;
  align-self: stretch;
}
#column1 {
  width: 28%;
}
#column2 {
  width: 24%;
}
#column3 {
  width: 30%;
}
#column4 {
  width: 18%;
}
.table-title {
  color: #41b06e;
  font-family: "Space Grotesk";
  font-size: 20px;
  font-weight: 400;
}
.column-devider {
  width: 100%;
  height: 0.6px;
  background: #7ac89a;
  border: none;
}
.table-column {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  align-self: stretch;
}
.table-column-content {
  display: flex;
  justify-content: center;
  align-items: center;
  align-self: stretch;
}
.column-text {
  color: #000;
  font-family: "Space Grotesk";
  font-size: 16px;
  font-style: normal;
  font-weight: 400;
  line-height: normal;
}
.available {
  padding: 5px 18px;
  flex: 1 0 0;
  border-radius: 4px;
  background: #41b06e;
  border: none;
  color: #fff;
  font-family: "Space Grotesk";
  font-size: 16px;
  font-weight: 400;
}
.available:hover {
  background: #67c08b;
}
.not-available {
  padding: 5px 18px;
  flex: 1 0 0;
  border-radius: 4px;
  background: #ff204e;
  border: none;
  color: #fff;
  font-family: "Space Grotesk";
  font-size: 16px;
  font-weight: 400;
}
.not-available:hover {
  background: #ff4d71;
}
.button-container {
  display: flex;
  padding-inline: 12px;
  justify-content: flex-end;
  align-items: center;
  gap: 13px;
  flex: 1 0 0;
}
.action-button-edit {
  width: 50%;
  padding: 5px 18px;
  border-radius: 4px;
  border: 1px solid #41b06e;
  background: #fff;
  color: #41b06e;
  font-family: "Space Grotesk";
  font-size: 16px;
  font-weight: 400;
}
.action-button-edit:hover {
  border: 1px solid #67c08b;
  background: #67c08b;
  color: #fff;
}
.action-button-edit:active {
  border: 1px solid #41b06e;
  background: #41b06e;
  color: #fff;
}

.action-button-delete {
  width: 50%;
  padding: 5px 18px;
  border-radius: 4px;
  border: 1px solid #ff204e;
  background: #fff;
  color: #ff204e;
  font-family: "Space Grotesk";
  font-size: 16px;
  font-weight: 400;
}
.action-button-delete:hover {
  border: 1px solid #ff4d71;
  background: #ff4d71;
  color: #fff;
}
.action-button-delete:active {
  border: 1px solid #ff204e;
  background: #ff204e;
  color: #fff;
}
</style>
