<template>
  <div>
    <my-header></my-header>
    <div>
      <side-bar></side-bar>
      <div class="row justify-content-center">
        <fade-transition :duration="100" origin="center top" mode="out-in">
          <router-view></router-view>
        </fade-transition>
      </div>
    </div>
  </div>
</template>
<script>
import MyHeader from '../components/Header.vue'
import SideBar from '../components/SidebarPlugin/SideBar.vue'
import { FadeTransition } from 'vue2-transitions'

export default {
  mounted() {
    window.addEventListener("keypress", e => {
      console.log(String.fromCharCode(e.keyCode));
    });
  },
  components: {
    MyHeader,
    SideBar,
    FadeTransition,
  },
}
</script>