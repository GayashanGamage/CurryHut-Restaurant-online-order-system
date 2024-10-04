<template>
  <div class="s-level-one-container">
    <h3 class="page-title">Site setting</h3>
    <div class="s-level-two-container">
      <div class="s-level-three-container">
        <h4 class="sub-title">Account credencials</h4>
        <hr class="ruller" />
        <div class="s-level-four-container account">
          <p id="account1" class="cell">E-mail</p>
          <p id="account2" class="cell">info@curryhut.lk</p>
          <p id="account3" class="cell">password</p>
          <p id="account4" class="cell">***********</p>
          <button class="action-button cell" id="account5">Change</button>
        </div>
        <h4 class="sub-title">Shop time</h4>
        <hr class="ruller" />
        <div class="s-level-four-container shop">
          <p class="cell" id="shop1">Regular opening time :</p>
          <p class="cell" id="shop2">6.00 a.m</p>
          <button class="action-button cell" id="shop3">Edit</button>
          <p class="cell" id="shop4">Regular closing time :</p>
          <p class="cell" id="shop5">11:00 a.m</p>
          <button class="action-button cell" id="shop6">Edit</button>
          <p class="cell" id="shop7">Operation hold :</p>
          <button class="action-button cell" id="shop8">Pause</button>
        </div>
        <h4 class="sub-title">Meal time</h4>
        <hr class="ruller" />
        <div class="s-level-four-container meal">
          <p class="cell" id="meal1">Brek first time</p>
          <p class="cell" id="meal2">6:00 a.m</p>
          <button class="cell action-button" id="meal3">Edit</button>
          <p class="cell" id="meal4">Lunch time</p>
          <p class="cell" id="meal5">11:00 a.m</p>
          <button class="cell action-button" id="meal6">Edit</button>
          <p class="cell" id="meal7">Dinner</p>
          <p class="cell" id="meal8">5:00 p.m</p>
          <button class="cell action-button" id="meal9">Edit</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthonticationStore } from "@/stores/authontication";
import { onBeforeMount, onBeforeUnmount } from "vue";

const authontication = useAuthonticationStore();

onBeforeMount(() => {
  authontication.checkCookie();
});

onBeforeUnmount(() => {
  authontication.checkCookie();
});
</script>

<style scoped>
.s-level-one-container {
  background: rgba(207, 244, 206, 0.5);
  width: 100%;
  height: auto;
  border-radius: 6px;
}

.page-title {
  color: #41b06e;
  font-family: "Space Grotesk";
  font-size: 32px;
  font-weight: 700;
  padding: 53px 0px 0px 19px;
}
.s-level-two-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: auto;
}
.s-level-three-container {
  width: 98%;
  height: auto;
  border-radius: 6px;
  background: #fff;
  margin-top: 26px;
  margin-bottom: 15px;
}
.sub-title {
  color: #000;
  font-family: "Space Grotesk";
  font-size: 20px;
  font-weight: 700;
  margin: 22px 0px 10px 32px;
}
.ruller {
  width: 1045px;
  height: 0.6px;
  background-color: rgb(172, 172, 172);
  border: 0px;
  margin-left: 31px;
}
.account {
  width: 1045px;
  margin-left: 31px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(2, 1fr);
  grid-template-areas:
    "email emailData . "
    "password passwordData actionButton";
}

#account1 {
  grid-area: email;
}
#account2 {
  grid-area: emailData;
}
#account3 {
  grid-area: password;
}
#account4 {
  grid-area: passwordData;
}
#account5 {
  grid-area: actionButton;
}
.cell {
  color: #000;
  font-family: "Space Grotesk";
  font-size: 18px;
  font-style: normal;
  font-weight: 300;
  line-height: normal;
  margin: 10px 0px;
}
.action-button {
  font-size: 18px;
  border-radius: 4px;
  border: 1.5px solid #41b06e;
  background: #fff;
  color: #41b06e;
  font-family: "Space Grotesk";
  font-size: 18px;
  font-weight: 400;
  padding: 4px 18px;
  width: fit-content;
}
.action-button:hover {
  background: #41b06e;
  color: #fff;
}
.shop {
  width: 1045px;
  margin-left: 31px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(3, 1fr);
  grid-template-areas:
    "open open-time open-button"
    "close close-time close-button"
    "hold . hold-button";
}
#shop8 {
  grid-area: hold-button;
}
.meal {
  width: 1045px;
  margin-left: 31px;
  padding-bottom: 80px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
}
</style>
