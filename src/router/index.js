import { useAuthonticationStore } from "@/stores/authontication";
import Home from "@/views/Home.vue";
import Email from "@/views/Authontication/Email.vue";
import Login from "@/views/Authontication/Login.vue";
import PasswordReset from "@/views/Authontication/PasswordReset.vue";
import Verification from "@/views/Authontication/Verification.vue";
import { createRouter, createWebHistory } from "vue-router";
import Setting from "@/views/Subpages/Setting.vue";
import Category from "@/views/Subpages/Category.vue";

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
      beforeEnter: (to, from) => {
        if (from.name == "login") {
          console.log("this is from login page");
          useAuthonticationStore().fromLogintoEmailDataClearing();
        }
      },
    },
    {
      path: "/verification",
      component: Verification,
      name: "verification",
    },
    {
      path: "/passwordreset",
      component: PasswordReset,
      beforeEnter: (to, from) => {
        if (from.name == "verification") {
          useAuthonticationStore().fromVerificationtoPasswordresetDataCleaning();
        }
      },
      name: "passwordreset",
    },
    {
      path: "/",
      component: Home,
      name: "home",
      beforeEnter: (to, from) => {
        if (from.name == "login") {
          useAuthonticationStore().fromLogintoHomeDataClearing();
        }
      },
      redirect: "setting",
      children: [
        {
          path: "setting",
          component: Setting,
          name: "setting",
        },
        {
          path: "catagory",
          component: Category,
          name: "category",
        },
      ],
    },
  ],
});

router.beforeEach((to, from, next) => {
  // foword guard
  if (
    from.name !== "login" &&
    to.name === "email" &&
    useAuthonticationStore().email_page === false
  )
    next({ name: "login" });

  // foword guard
  if (
    from.name !== "email" &&
    to.name === "verification" &&
    useAuthonticationStore().verification_page === false
  )
    next({ name: "login" });

  // if press back button then direct to login page - backword
  if (from.name === "verification" && to.name === "email")
    next({ name: "login" });

  // forword guard
  if (
    from.name !== "verification" &&
    to.name === "passwordreset" &&
    useAuthonticationStore().passwordRest_page === false
  )
    next({ name: "login" });

  // if press back button then direct to login page - backword
  if (from.name === "passwordreset" && to.name === "verification")
    next({ name: "login" });
  // subpage of the admin page
  // if (
  //   useAuthonticationStore().authontication === false &&
  //   to.name === "setting"
  // )
  // next({ name: "login" });
  else next();
});

export default router;
