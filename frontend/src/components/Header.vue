<template>
  <div class="navbar navbar-expand bg-white hd-shadow hd-ps hd-p" ref="mheader">
    <a class="navbar-brand mr-0 mr-md-2" href="/">
     <img class="d-block" width="200" height="40" :src="logo"/>
    </a>
    <ul v-if="!$store.state.auth.login"
        class="navbar-nav flex-row ml-md-auto d-none d-md-flex">
      <router-link to="/login">
        <base-button outline type="secondary">Login</base-button>
      </router-link>
      <router-link to="/register">
        <base-button outline type="secondary">Register</base-button>
      </router-link>
    </ul>
    <ul v-if="$store.state.auth.login"
        class="navbar-nav flex-row ml-md-auto d-none d-md-flex">
      <router-link to="/manage">
        <base-button outline type="secondary">Regist Device</base-button>
      </router-link>
      <base-button @click="logOut" outline type="secondary">Logout</base-button>
    </ul>
  </div>
</template>
<script>
import axios from 'axios';
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
  methods: {
    measureHeight() {
      this.$store.state.dimens.header=this.$refs.mheader.clientHeight;
    },
    registDevice() {
      this.$store.state.modals.registDevice=true;
    },
    logOut() {
      const userid = this.$store.state.auth.userid

      axios.post('server/auth/logout', userid)
      .then((response) => {
        console.log(response);
        this.$store.state.auth.login=false
        this.$store.state.auth.userid=''
      }).catch((e) => {
        console.log("err:",e)
      })
    }
  },
  mounted() {
    this.measureHeight();
  },
}
</script>
<style scoped>
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