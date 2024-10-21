<template>
  <div class="c1-level-one-container">
    <div class="c1-level-two-container">
      <div class="c1-level-three-container window-header">
        <h3 class="window-title">Food item</h3>
      </div>
      <div class="c1-level-three-container window-content">
        <div class="content-section details">
          <div id="image"></div>
          <div id="name">
            <input type="text" class="user-input" />
          </div>
          <div id="category">
            <select name="" id="" class="category-input">
              <option value="" class="category-item">ojewofiow</option>
              <option value="" class="category-item">ojewofiow</option>
            </select>
          </div>
          <div id="code">
            <input type="text" class="user-input" />
          </div>
          <div id="description">
            <textarea
              name=""
              cols="30"
              rows="10"
              id="item-description"
            ></textarea>
            <p id="descrioption-info">300 charactor</p>
          </div>
        </div>
        <div class="content-section price">
          <p class="info">Price</p>
          <hr id="ruler" />
          <div class="price-table">
            <table class="table-container">
              <thead class="table-head">
                <tr>
                  <th class="column-title name-column">Name</th>
                  <th class="column-title potion-column">Potion size</th>
                  <th class="column-title price-column">Price</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>
                    <input
                      type="text"
                      class="table-data name-column name-column-data"
                    />
                  </td>
                  <td>
                    <input
                      type="number"
                      class="table-data potion-column potion-column-data"
                    />
                  </td>
                  <td>
                    <input
                      type="text"
                      class="table-data price-column price-column-data"
                    />
                  </td>
                </tr>
                <tr>
                  <td>
                    <input
                      type="text"
                      class="table-data name-column name-column-data"
                    />
                  </td>
                  <td>
                    <input
                      type="number"
                      class="table-data potion-column potion-column-data"
                    />
                  </td>
                  <td>
                    <input
                      type="text"
                      class="table-data price-column price-column-data"
                    />
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div class="content-section button-section">
          <button class="action-button" @click="uistore.foodViewClose">
            Close
          </button>
          <button class="action-button delete">Delete</button>
          <button class="action-button">Save</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useUiStore } from "@/stores/ui";

const uistore = useUiStore();
</script>

<style scoped>
/* main container */
.c1-level-one-container {
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
/* popup window */
.c1-level-two-container {
  width: 731px;
  height: auto;
  border-radius: 6px;
  background: #fff;
}
/* child container of popup window */
.window-content {
  padding: 30px;
}
/* sub section of the popup window */
.window-header {
  width: 731px;
  height: 60px;
  border-radius: 6px 6px 0px 0px;
  background: #41b06e;
  display: flex;
  justify-content: center;
  align-items: center;
}
.price {
  margin-top: 10px;
  height: auto;
}
.button-section {
  margin-top: 10px;
  height: 45px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 10px;
  margin-right: 15px;
}
.window-title {
  color: #fff;
  font-family: "Space Grotesk";
  font-size: 24px;
  font-weight: 700;
}
.details {
  width: 100%;
  height: 330px;
  display: grid;
  grid-template-columns: repeat(1fr, 2);
  grid-template-rows: repeat(1fr, 7);
  grid-gap: 10px;
  grid-template-areas:
    "img name"
    "img category"
    "img code"
    "img des"
    "img des"
    "img des";
}
#image {
  grid-area: img;
  width: 334px;
  height: 303px;
  border-radius: 4px;
  background: #d9d9d9;
}
#description {
  grid-area: des;
  display: flex;
  flex-direction: column;
  align-items: end;
  width: fit-content;
}
.info {
  color: #000;
  font-family: "Space Grotesk";
  font-size: 20px;
  font-style: normal;
  font-weight: 700;
  line-height: normal;
}
#ruler {
  background: #a0d8b7;
  border: 0px;
  height: 1px;
}
.price-table {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0px;
  padding: 0px;
}
.table-container {
  width: 100%;
  margin: 10px 10px;
}
.column-title {
  text-align: left;
  padding-left: 5px;
  font-family: "Space Grotesk";
  font-weight: 400;
}
.name-column {
  width: 375px;
  margin: 0px 5px;
}
.name-column-data {
  height: 26px;
  border-radius: 4px;
  border: 0.5px solid #adadad;
  background: #fff;
  padding-left: 10px;
}
.potion-column {
  width: 80px;
  margin: 0px 5px;
}
.potion-column-data {
  height: 26px;
  border-radius: 4px;
  border: 0.5px solid #adadad;
  background: #fff;
  padding-left: 10px;
}
.price-column {
  width: 150px;
  margin: 0px 5px;
  margin-right: 10px;
}
.price-column-data {
  height: 26px;
  border-radius: 4px;
  border: 0.5px solid #adadad;
  background: #fff;
  padding-left: 10px;
}
.table-data {
  font-family: "Space Grotesk";
  font-size: 17px;
}
.user-input {
  font-family: "Space Grotesk";
  width: 302px;
  height: 33px;
  border-radius: 4px;
  font-size: 18px;
  border: 1px solid #d9d9d9;
  padding-left: 10px;
  font-weight: 300;
}
#item-description {
  width: 292px;
  height: 146px;
  border-radius: 4px;
  border: 1px solid #d9d9d9;
  color: #000;
  font-family: "Space Grotesk";
  font-size: 18px;
  font-weight: 300;
  padding: 10px;
  resize: none;
}
#descrioption-info {
  color: #000;
  font-family: "Space Grotesk";
  font-size: 11px;
  font-weight: 300;
  margin-top: 6px;
}
.category-input {
  width: 312px;
  height: 33px;
  color: #000;
  font-family: "Space Grotesk";
  font-size: 18px;
  font-weight: 300;
  padding-left: 10px;
  border-radius: 4px;
  border: 1px solid #d9d9d9;
  background: #fff;
}
.category-item {
  font-family: "Space Grotesk";
  font-size: 18px;
  font-weight: 300;
  padding-left: 10px;
  /* background: #fff; */
}
.delete {
  border-radius: 4px;
  border: 1px solid #ff204e;
  background: #fff;
  color: #ff204e;
}
.delete:hover {
  border: 1px solid #ff204e;
  background: #ff204e;
  color: #fff;
}
</style>
