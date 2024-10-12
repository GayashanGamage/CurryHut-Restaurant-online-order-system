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
          <button
            class="action-button cell"
            id="account5"
            @click="openPasswordResetWindow"
          >
            Change
          </button>
        </div>
        <h4 class="sub-title">Shop time</h4>
        <hr class="ruller" />
        <div class="s-level-four-container shop">
          <p class="cell" id="shop1">Regular opening time :</p>
          <p class="cell" id="shop2">{{ shop.open_time }}</p>
          <button
            class="action-button cell"
            id="shop3"
            @click="uistore.openTimeChangeWindow('open_time')"
          >
            Edit
          </button>
          <p class="cell" id="shop4">Regular closing time :</p>
          <p class="cell" id="shop5">{{ shop.close_time }}</p>
          <button
            class="action-button cell"
            id="shop6"
            @click="uistore.openTimeChangeWindow('close_time')"
          >
            Edit
          </button>
          <p class="cell" id="shop7">Operation status :</p>
          <!-- <button class="action-button cell" id="shop8">Pause</button> -->
          <div class="cell" id="shop8">
            <!-- <label class="switch">
              <input type="checkbox" />
              <span class="slider"></span> -->
            <p class="shutdown-text">Open</p>
            <label class="switch"
              ><input
                type="checkbox"
                @click="shutdownAction(a)"
                id="checkbox"
                checked="true"
              />
              <div></div>
            </label>
            <p class="shutdown-text">Close</p>
            <!-- </label> -->
          </div>
        </div>
        <h4 class="sub-title">Meal time</h4>
        <hr class="ruller" />
        <div class="s-level-four-container meal">
          <p class="cell" id="meal1">Breakfarst time</p>
          <p class="cell" id="meal2">{{ shop.breakfast }}</p>
          <button
            class="cell action-button"
            id="meal3"
            @click="uistore.openTimeChangeWindow('breakfast')"
          >
            Edit
          </button>
          <p class="cell" id="meal4">Lunch time</p>
          <p class="cell" id="meal5">{{ shop.lunch }}</p>
          <button
            class="cell action-button"
            id="meal6"
            @click="uistore.openTimeChangeWindow('lunch')"
          >
            Edit
          </button>
          <p class="cell" id="meal7">Dinner</p>
          <p class="cell" id="meal8">{{ shop.dinner }}</p>
          <button
            class="cell action-button"
            id="meal9"
            @click="uistore.openTimeChangeWindow('dinner')"
          >
            Edit
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { useAuthonticationStore } from "@/stores/authontication";
import { onBeforeMount, ref } from "vue";
import { useShopStore } from "@/stores/shop";
import router from "@/router";
import { useUiStore } from "@/stores/ui";
import { useToast } from "vue-toast-notification";

// toast messages initiating
const toast = useToast();

// import all pinia stores
const authontication = useAuthonticationStore();
const shop = useShopStore();
const uistore = useUiStore();

onBeforeMount(() => {
  if (authontication.authontication == false) {
    authontication.restoreAuthonticationDataToPinia();
    authontication.redirectToLogin();
  }
  axios
    .get(`${import.meta.env.VITE_url}/shopdetails`, {
      headers: {
        Authorization: "Bearer " + authontication.authcookie,
      },
    })
    .then((response) => {
      if (response.status == 200) {
        let APIdata = response.data;
        shop.open_time = APIdata.open_time;
        shop.close_time = APIdata.close_time;
        shop.shutdown = APIdata.shutdown;
        shop.breakfast = APIdata.breakfast;
        shop.lunch = APIdata.lunch;
        shop.dinner = APIdata.dinner;
      }
    })
    .catch((error) => {
      if (error.response.status == 401) {
        router.replace({ name: "login" });
      }
    });
});

function openPasswordResetWindow() {
  // function : send email with 'secreate_code' to admin and open passwordChangeWindow
  // 1. check authontication
  // 2. if not available, then crean all credicials and direct to login page
  // 3. otherwise send request to 'secretecode'
  // 4. set CodeVerifyWindow visible
  // 5. if it is successfull, then open password reset popup
  authontication.checkAuthontication();
  axios
    .get(`${import.meta.env.VITE_url}/secreatecode`, {
      params: {
        email: authontication.email,
      },
    })
    .then((response) => {
      if (response.status == 200) {
        uistore.CodeVerify = true;
        uistore.PasswordChangeWindow = true;
      }
    })
    .catch((error) => {
      if (error.status == 404 || error.status == 500) {
        toast.error("something went wrong. try agian shortly");
      }
    });
}

const shutdownAction = () => {
  // function : sudden shutdown and open action for shop
  // 1. get checkbox status
  // 2. send API request
  // 3. if successfull then show successfull message
  // 4. else get acction accordingly

  let checkboxAction = document.getElementById("checkbox");
  axios
    .patch(`${import.meta.env.VITE_url}/operationhold`, null, {
      headers: {
        Authorization: `Bearer ${authontication.authcookie}`,
      },
    })
    .then((response) => {
      shop.shutdown = !shop.shutdown;
      toast.success(response.data);
    })
    .catch((error) => {
      if (error.status == 401) {
        authontication.checkAuthontication();
      } else if (error.status == 400) {
        toast.error(error.response.data);
        checkboxAction.checked = false;
      }
    });
};
</script>

<style scoped>
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
  font-family: "Space Grotesk";
  font-size: 18px;
  font-style: normal;
  font-weight: 300;
  line-height: normal;
  margin: 10px 0px;
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
.switch input {
  position: absolute;
  opacity: 0;
}
.switch {
  display: inline-block;
  font-size: 20px; /* 1 */
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

.switch input:checked + div {
  /* -webkit-transform: translate3d(100%, 0, 0); */
  /* -moz-transform: translate3d(100%, 0, 0); */
  transform: translate3d(100%, 0, 0);
}
#shop8 {
  display: flex;
  align-items: center;
}
.shutdown-text {
  color: #41b06e;
  font-family: "Space Grotesk";
}
</style>
