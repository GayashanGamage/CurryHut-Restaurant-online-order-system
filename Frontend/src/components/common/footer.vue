<template>
  <div class="footer-container">
    <div class="sub-container">
      <p class="container-title">contact</p>
      <p class="content">Curry Hut restaurent,</p>
      <p class="content">Narahenpita</p>
      <p class="content">Colombo 05</p>
      <p class="content contact">
        <span class="material-icons">call</span>
        071 300 4000
      </p>
    </div>
    <div class="sub-container">
      <p class="container-title">are you hungry ?</p>
      <p class="content">
        <router-link to="/">Main menu</router-link>
      </p>
      <p class="content">
        <router-link to="/extra">Extra potion</router-link>
      </p>
      <p class="content">
        <router-link to="/decert">Decerts</router-link>
      </p>
      <p class="content">
        <router-link to="/drinks">Drinks</router-link>
      </p>
    </div>
    <div class="sub-container">
      <p class="container-title">Important links</p>
      <p class="content">About us</p>
      <p class="content">Refund policy</p>
      <p class="content">Payments</p>
      <p class="content">FAQs</p>
    </div>
    <div class="social">
      <img
        v-for="item in social_links"
        :key="item.id"
        :src="item.link"
        :alt="item.alt"
        class="social-icons"
      />
    </div>
  </div>
</template>

<script setup>
const social_links = [
  {
    id: 1,
    link: "https://curryhut.blr1.cdn.digitaloceanspaces.com/social-icons/facebook.png",
    alt: "facebook-icon",
  },
  {
    id: 2,
    link: "https://curryhut.blr1.cdn.digitaloceanspaces.com/social-icons/pickme.png",
    alt: "pickme-icon",
  },
  {
    id: 3,
    link: "https://curryhut.blr1.cdn.digitaloceanspaces.com/social-icons/tictok.png",
    alt: "tictok",
  },
  {
    id: 4,
    link: "https://curryhut.blr1.cdn.digitaloceanspaces.com/social-icons/uber_eats.png",
    alt: "ubereats-icon",
  },
];
</script>

<style scoped>
.footer-container {
  display: flex;
  width: auto;
  padding: 25px 155px;
  justify-content: space-between;
  align-items: flex-start;
  background: #fff;
}
.sub-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 17px;
  flex: 1 0 0;
}
.container-title {
  color: #000;
  font-family: Roboto;
  font-size: 20px;
  font-style: normal;
  font-weight: 900;
  line-height: normal;
  text-transform: uppercase;
  align-self: stretch;
}
.content {
  color: #000;
  font-family: Roboto;
  font-size: 16px;
  font-style: normal;
  font-weight: 300;
  line-height: normal;
  align-self: stretch;
}
a {
  text-decoration: none;
  color: #000;
}
.contact {
  display: flex;
  align-items: center;
  gap: 23px;
  align-self: stretch;
}
.social {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  flex: 1 0 0;
}
</style>
