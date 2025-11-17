<template>
  <main>
    <Menubar></Menubar>
    <div class="space"></div>
    <p>order type</p>
    <div class="space"></div>
    <Footer></Footer>
  </main>
</template>

<script setup>
import Footer from "@/components/common/footer.vue";
import Menubar from "@/components/common/menubar.vue";
</script>

<style scoped>
.space {
  height: 15vh;
  width: 100vw;
}
</style>
