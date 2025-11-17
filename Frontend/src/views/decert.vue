<template>
  <main>
    <Menubar></Menubar>
    <div class="space"></div>
    <Foodsection :foodList = foodStore.decert foodStoreVariable = 'decert'></Foodsection>
    <div class="space"></div>
    <Footer></Footer>
    <Foodview></Foodview>
  </main>
</template>

<script setup>
import Footer from "@/components/common/footer.vue";
import Menubar from "@/components/common/menubar.vue";
import Foodsection from "@/components/home_page/foodsection.vue";

// popup import
import Foodview from "@/components/popup/foodview.vue";
import { useFoodStore } from "@/stores/food";
import { useOrderStore } from "@/stores/order";
import axios from "axios";
import { onMounted, ref, watch } from "vue";

// use stors
const foodStore = useFoodStore();
const orderStore = useOrderStore();

onMounted(() => {
  if(foodStore.decert == null){
    axios.get(`${import.meta.env.VITE_url}/customer/category/670cbd156e6b240be2d189e6`)
    .then((response) => {
      foodStore.decert = response.data.data
    })
    .catch((error) => {
      console.log(error)
    })
  }
});

</script>

<style scoped>
.space {
  height: 30px;
  width: 100vw;
}
</style>
