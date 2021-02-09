<template>
  <div class="navbar navbar-expand bg-white hd-shadow hd-ps hd-p">
    <a class="navbar-brand mr-0 mr-md-2" href="/">
     <img class="d-block" width="200" height="40" :src="logo"/>
    </a>
    <ul class="navbar-nav flex-row ml-md-auto d-none d-md-flex">
      <router-link to="/">
        <base-button href="#" outline type="secondary">Login</base-button>
      </router-link>
      <router-link to="/register">
        <base-button href="#" outline type="secondary">Register</base-button>
      </router-link>
    </ul>
  </div>
</template>
<script>
import BaseButton from '../components/BaseButton.vue'

export default {
  components: {
    BaseButton
  },
  props: {
    logo: {
      type: String,
      default: 'img/myimg/logo.png',
      description: 'Sidebar app logo'
    },
  },
}
</script>
<style scoped>
.hd-shadow{
  box-shadow: 0px 1px 5px rgb(223, 223, 223);
}
.hd-ps{
  position: sticky;
}
.hd-p{
  padding: .5rem 1rem;
}
</style>