<template>
  <main>
    <Menubar></Menubar>
    <div class="space"></div>
    <div class="auth-window">
      <div class="auth-head">Verification Code</div>
      <div class="auth-content">
        <div class="back" @click="router.push({ name: 'mobile' })">
          <span class="material-icons">keyboard_backspace</span>
          <p class="sub-action">Change mobile number</p>
        </div>
        <input type="text" class="auth-content-input" placeholder="xxxx" />
        <p class="sub-action">Send again</p>
        <button
          class="auth-content-action"
          @click="router.push({ name: 'checkout' })"
        >
          Verify number
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
.sub-action {
  color: #989898;
  font-size: 13px;
  cursor: pointer;
}
.back {
  display: flex;
  gap: 8px;
  align-items: center;
  cursor: pointer;
  margin-right: auto;
}
.material-icons {
  color: #989898;
  font-weight: 200;
}
.back:hover .material-icons {
  color: #ff5e5e;
}
.sub-action:hover {
  color: #ff5e5e;
  font-weight: 500;
}
</style>
