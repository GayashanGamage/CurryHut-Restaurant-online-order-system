import Home from "@/views/Home.vue";
import Email from "@/views/Authontication/Email.vue";
import Login from "@/views/Authontication/Login.vue";
import PasswordReset from "@/views/Authontication/PasswordReset.vue";
import Verification from "@/views/Authontication/Verification.vue";
import { createRouter, createWebHistory } from "vue-router";
import Setting from "@/views/Subpages/Setting.vue";
import Category from "@/views/Subpages/Category.vue";
import Food from "@/views/Subpages/Food.vue";
import { useUiStore } from "@/stores/ui";
import Orders from "@/views/Subpages/Orders.vue";
import Menu from "@/views/Subpages/Menu.vue";
import Statistics from "@/views/Subpages/Statistics.vue";
import Editmenu from "@/views/Subpages/Editmenu.vue";
import Delivery from "@/views/Subpages/Delivery.vue";

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
      redirect: "setting",
      children: [
        {
          path: "setting",
          component: Setting,
          name: "setting",
        },
        {
          path: "delivery",
          component: Delivery,
          name: "delivery",
        },
        {
          path: "catagory",
          component: Category,
          name: "category",
        },
        {
          path: "food",
          component: Food,
          name: "food",
        },
        {
          path: "orders",
          component: Orders,
          name: "orders",
        },
        {
          path: "menu",
          component: Menu,
          name: "menu",
        },
        {
          path: "statistics",
          component: Statistics,
          name: "statistics",
        },
        {
          path: "edit-menu",
          component: Editmenu,
          name: "editmenu",
        },
      ],
    },
  ],
});

router.beforeEach((to, from, next) => {
  useUiStore().currentTab = to.name;

  // foword guard
  if (from.name !== "login" && to.name === "email") next({ name: "login" });

  // foword guard
  if (from.name !== "email" && to.name === "verification")
    next({ name: "login" });

  // if press back button then direct to login page - backword
  if (from.name === "verification" && to.name === "email")
    next({ name: "login" });

  // forword guard
  if (from.name !== "verification" && to.name === "passwordreset")
    next({ name: "login" });

  // if press back button then direct to login page - backword
  if (from.name === "passwordreset" && to.name === "verification")
    next({ name: "login" });
  else next();
});

export default router;
