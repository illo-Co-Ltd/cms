<template>
  <div class="hd-fix navbar navbar-expand bg-white hd-shadow hd-p" ref="mheader">
    <a class="navbar-brand mr-0 mr-md-2" href="/">
     <img class="d-block" width="110" height="40" :src="logo"/>
    </a>
    <ul v-if="!this.login"
        class="navbar-nav flex-row ml-md-auto d-none d-md-flex">
      <router-link to="/login">
        <base-button outline type="secondary">Login</base-button>
      </router-link>
      <router-link to="/register">
        <base-button outline type="secondary">Register</base-button>
      </router-link>
    </ul>
    <ul v-if="this.login"
        class="navbar-nav flex-row ml-md-auto d-none d-md-flex">
      <base-button outline type="secondary"
                   @click="registDevice">Regist Device</base-button>
      <base-button @click="logOut" outline type="secondary">Logout</base-button>
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
      default: 'img/myimg/logo.jpg',
      description: 'Sidebar app logo'
    },
  },
  data() {
    return{
      login: false
    }
  },
  methods: {
    init() {
      this.$store.state.dimens.header=this.$refs.mheader.clientHeight;
      if(sessionStorage.getItem("access_token") != null)
        this.login=true
      else this.login=false
    },
    registDevice() {
      this.$store.state.modals.cDevice=true;
    },
    logOut() {
      this.$store.dispatch("logout")
      this.$router.push('/login')
    }
  },
  mounted() {
    this.init();
  },
}
</script>
<style scoped>
.hd-fix{
  position: fixed;
  left: 0;
  right: 0;
}
.hd-shadow{
  box-shadow: 0px 1px 5px rgb(223, 223, 223);
  z-index: 1;
}
.hd-ps{
  position: sticky;
}
.hd-p{
  padding: .5rem 1rem;
}
</style>