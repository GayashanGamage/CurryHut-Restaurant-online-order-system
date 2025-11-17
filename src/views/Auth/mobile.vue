<template>
  <main>
    <Menubar></Menubar>
    <div class="space"></div>
    <div class="auth-window">
      <div class="auth-head">Mobile Number</div>
      <div class="auth-content">
        <input
          type="text"
          class="auth-content-input"
          placeholder="071 xxx xxxx"
          @keyup="checkKeys"
          v-model="authStore.mobile"
        />
        <button class="auth-content-action" @click="codeVerification" :disabled="buttonStatus">
          Send Code
        </button>
      </div>
    </div>
    <div class="space"></div>
    <Footer></Footer>
  </main>
</template>

<script setup>
import Footer from "@/components/common/footer.vue";
import Menubar from "@/components/common/menubar.vue";
import router from "@/router";
import { useAuthonticationStore } from "@/stores/auth";
import axios from "axios";
import { computed, onMounted, ref, watch } from "vue";
import { useToast } from "vue-toast-notification";

// variables
// import pinia stores
const authStore =  useAuthonticationStore();
// other reactive variables
const buttonStatus = ref(true)
const notification = useToast();

// functions 
// send the mobile number to the server and get the verification code / check mobile number alredy in database
const codeVerification = () => {
  if(buttonStatus.value == false){
    axios.post(`${import.meta.env.VITE_url}/customer/auth/mobile`, {
      mobile: authStore.mobile
    }).then((response) => {
      if(response.status == 200){
        document.cookie = `customer= ${response.data.customer}; expires=Thu, 18 Dec 2040 12:00:00 UTC`;
        authStore.mobile = null
        notification.success("Check your messages on mobile for verification code")
        router.push({ name: "verification" }); 
      }
    }).catch((err) => {
      if(err.status == 422){
        notification.error("Enter valied mobile number")
      }else if(err.status == 500){
        notification.error("something went wrong - try again later")
      }
    })
  }
};

// check the input keys is number and length of the input
const checkKeys = () => {
  if(isNaN(authStore.mobile.at(-1))){
    authStore.mobile = authStore.mobile.slice(0, -1)
  }
  if(authStore.mobile.length > 10){
    authStore.mobile = authStore.mobile.slice(0, 10)
  }
}

// enabled or disabled the action button
watch(() => authStore.mobile, (newValue) => {
  if(newValue.length === 10){
    buttonStatus.value = false
  }else{
    buttonStatus.value = true
  }
})

// lifecycle hooks
onMounted(() => {
  authStore.mobile = ""
})

</script>

<style scoped>
.space {
  height: 15vh;
  width: 100vw;
}
.auth-window {
  display: flex;
  width: 415px;
  padding-bottom: 30px;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 50px;
  border-radius: 4px;
  background: #fff;
  margin-inline: auto;
}
.auth-head {
  display: flex;
  padding: 10px 0px;
  justify-content: center;
  align-items: center;
  gap: 8px;
  align-self: stretch;
  border-radius: 6px 6px 0px 0px;
  background: #ff5e5e;
  color: #fff;
  text-align: center;
  font-size: 18px;
  font-style: normal;
  font-weight: 300;
  line-height: normal;
  flex: 1 0 0;
}
.auth-content {
  display: flex;
  width: 80%;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
}
.auth-content-input {
  display: flex;
  padding: 6px;
  justify-content: center;
  align-items: center;
  align-self: stretch;
  border-radius: 4px;
  border: 1px solid #a7a6a6;
  color: #a7a6a6;
  font-size: 18px;
  font-style: normal;
  font-weight: 300;
  line-height: normal;
  flex: 1 0 0;
  outline: none;
}
a {
  text-decoration: none;
}
.auth-content-action {
  display: flex;
  padding: 5px 6px;
  justify-content: center;
  align-items: center;
  align-self: stretch;
  border-radius: 4px;
  background: #ff8f8f;
  color: #fff;
  font-size: 18px;
  font-weight: 300;
  border: none;
  cursor: pointer;
}
.auth-content-action:hover {
  background: #f57070;
}
.auth-content-action:disabled{
  background-color: #a7a6a6;
  cursor: not-allowed;
  color: #fff;
}
</style>
