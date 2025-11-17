import { ref } from "vue";
import { defineStore } from "pinia";

export const useAuthonticationStore = defineStore("authontication", () => {
    const mobile = ref(null)
    const user_key = ref(null)
    const secreate_code= ref(null)

    function loadUserKey(){
    if(user_key.value == null){
        let cookie = document.cookie.split('; ').find(row => row.startsWith('customer'))
        user_key.value = cookie ? cookie.split('=')[1] : null
     }
    }

  return {
    mobile,
    user_key,
    secreate_code,
    loadUserKey,
  };
});
