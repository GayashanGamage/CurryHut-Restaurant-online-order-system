<template>
  <main>
    <Menubar></Menubar>
    <div class="space"></div>
    <Foodsection :foodList = foodStore.extra_portion foodStoreVariable = 'extra_portion'></Foodsection>
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
// const orderStore = useOrderStore();


onMounted(() => {
  if(foodStore.extra_portion == null){
    axios.get(`${import.meta.env.VITE_url}/customer/category/67b1baa519f60cfa444a0afc`)
    .then((response) => {
      foodStore.extra_portion = response.data.data
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
