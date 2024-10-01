import Home from "@/views/Home.vue";
import Email from "@/views/Authontication/Email.vue";
import Login from "@/views/Authontication/Login.vue";
import PasswordReset from "@/views/Authontication/PasswordReset.vue";
import Verification from "@/views/Authontication/Verification.vue";
import { createRouter, createWebHistory } from "vue-router";
import Setting from "@/views/Subpages/Setting.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/login",
      component: Login,
      name: "login",
    },
    {
      path: "/email",
      component: Email,
      name: "email",
    },
    {
      path: "/verification",
      component: Verification,
      name: "verification",
    },
    {
      path: "/passwordreset",
      component: PasswordReset,
      name: "passwordreset",
    },
    {
      path: "/",
      component: Home,
      name: "home",
      children: [
        {
          path: "setting",
          component: Setting,
          name: "setting",
        },
      ],
    },
  ],
});

export default router;
