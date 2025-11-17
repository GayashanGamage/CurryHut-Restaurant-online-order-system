<template>
  <div class="s-level-one-container">
    <h3 class="page-title">
      Site setting <span v-if="uistore.refresh"></span>
    </h3>
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
          <p class="cell" id="shop2">{{ String(new Date(shop.open_time).getHours()).padStart(2, '0') }} : {{ String(new Date(shop.open_time).getMinutes()).padStart(2, '0') }}</p>
          <button
            class="action-button cell"
            id="shop3"
            @click="setTime('open_time')"
          >
            Edit
          </button>

          <p class="cell" id="shop4">Regular closing time :</p>
          <p class="cell" id="shop5">{{ String(new Date(shop.close_time).getHours()).padStart(2, '0') }} : {{ String(new Date(shop.close_time).getMinutes()).padStart(2, '0') }}</p>
          <button
            class="action-button cell"
            id="shop6"
            @click="setTime('close_time')"
          >
            Edit
          </button>

          <p class="cell" id="shop7">Operation status :</p>
          <!-- <button class="action-button cell" id="shop8">Pause</button> -->
          <div class="cell" id="shop8">
            <p class="shutdown-text">Open</p>
            <label class="switch"
              ><input
                type="checkbox"
                id="checkbox"
                @click="setShopStatuts"
                :checked="shop.shutdown"
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
          <p class="cell" id="meal2">{{ String(new Date(shop.breakfast).getHours()).padStart(2, '0') }} : {{ String(new Date(shop.breakfast).getMinutes()).padStart(2, '0') }}</p>
          <button
            class="cell action-button"
            id="meal3"
            @click="setTime('breakfast')"
          >
            Edit
          </button>
          <p class="cell" id="meal4">Lunch time</p>
          <p class="cell" id="meal5">{{ String(new Date(shop.lunch).getHours()).padStart(2, '0') }} : {{ String(new Date(shop.lunch).getMinutes()).padStart(2, '0') }}</p>
          <button
            class="cell action-button"
            id="meal6"
            @click="setTime('lunch')"
          >
            Edit
          </button>
          <p class="cell" id="meal7">Dinner</p>
          <p class="cell" id="meal8">{{ String(new Date(shop.dinner).getHours()).padStart(2, '0') }} : {{ String(new Date(shop.dinner).getMinutes()).padStart(2, '0') }}</p>
          <button
            class="cell action-button"
            id="meal9"
            @click="setTime('dinner')"
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
import { onBeforeMount, onMounted, onUpdated, ref, watch } from "vue";
import { useShopStore } from "@/stores/shop";
import router from "@/router";
import { useUiStore } from "@/stores/ui";
import { useToast } from "vue-toast-notification";

// toast messages initiating
const toast = useToast();

// pinia stores
const shopStore = useShopStore();

// import all pinia stores
const authontication = useAuthonticationStore();
const shop = useShopStore();
const uistore = useUiStore();

const requestData = () => {
  axios
    .get(`${import.meta.env.VITE_url}/shopdetails`, {
      headers: {
        Authorization: "Bearer " + authontication.cookies_token,
      },
    })
    .then((response) => {
      if (response.status == 200) {
        // assign response data in to variabl 
        let APIdata = response.data.data;

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
};

//  load shop details
onBeforeMount(() => {
  if (
    authontication.cookies_token == null ||
    authontication.cookies_email == null
  ) {
    const credencials = authontication.restoreCredentials();
    if (credencials == false) {
      router.replace({ name: "login" });
    } else if (credencials == true) {
      requestData();
    }
  }
});

const changePassword = () => {
  axios
    .get(`${import.meta.env.VITE_url}/secreatecode`, {
      params: {
        email_address: authontication.local_storage_email,
      },
    })
    .then((response) => {
      if (response.status == 200) {
        uistore.CodeVerify = true; //to open code verify window
        uistore.PasswordChangeWindow = true; //to open main window from home page
      }
    })
    .catch((error) => {
      if (error.status == 404 || error.status == 500) {
        toast.error("something went wrong. try agian shortly");
      }
    });
}


function openPasswordResetWindow() {
  // function : send email with 'secreate_code' to admin and open passwordChangeWindow
  // 1. check authontication
  // 2. if not available, then crean all credicials and direct to login page
  // 3. otherwise send request to 'secretecode'
  // 4. set CodeVerifyWindow visible
  // 5. if it is successfull, then open password reset popup
  // authontication.checkAuthontication();
  if (
    authontication.cookies_token == null ||
    authontication.local_storage_email == null
  ) {
    const credencials = authontication.restoreCredentials();
    if (credencials == false) {
      router.replace({ name: "login" });
    } else {
      changePassword();
    }
  } else {
    changePassword();
  }
}

// exrtact hours and minutes from selected time
const extractTime = (selecteTime) => {
  shopStore.hours = new Date(selecteTime).getHours();
  shopStore.minutes = new Date(selecteTime).getMinutes();
};

// open time chage window - common for all windows ---------
const setTime = (time_arg) => {
  uistore.timeDescription = time_arg;
  uistore.timeWindow = true;

  if (time_arg == "open_time") {
    extractTime(shopStore.open_time);
    uistore.windowTitle = "Open time";
  } else if (time_arg == "close_time") {
    extractTime(shopStore.close_time);
    uistore.windowTitle = "Close time";
  } else if (time_arg == "breakfast") {
    extractTime(shopStore.breakfast);
    uistore.windowTitle = "breakfast time";
  } else if (time_arg == "lunch") {
    extractTime(shopStore.lunch);
    uistore.windowTitle = "lunch time";
  } else if (time_arg == "dinner") {
    extractTime(shopStore.dinner);
    uistore.windowTitle = "dinner time";
  }
};

// page refresh and get new data
onUpdated(() => {
  if (uistore.refresh == true) {
    requestData();
    uistore.refresh = false;
  }
});

// came from - setShopStatus()
const requestShopStatus = () => {
  axios
    .patch(`${import.meta.env.VITE_url}/operationhold`, null, {
      headers: {
        Authorization: "Bearer " + authontication.cookies_token,
      },
    })
    .then((responce) => {
      toast.success("Shop status changed successfully");
      uistore.refresh = true; // this is do some critical changes in the page
    })
    .catch((error) => {
      if(error.status == 400){
        toast.error("while shop close you cannot change status of the shop");
        document.getElementById('checkbox').checked = shop.shutdown;
      }
    });
};

// set shop status - open or close
const setShopStatuts = () => {
  if (
    authontication.cookies_token == null ||
    authontication.local_storage_email == null
  ) {
    const credencials = authontication.restoreCredentials();
    if (credencials == false) {
      router.replace({ name: "login" });
    } else {
      requestShopStatus();
    }
  } else {
    requestShopStatus();
  }
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
