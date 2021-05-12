<template>
  <div>
    <my-header></my-header>
    <div>
      <side-bar></side-bar>
      <thumbnailbar></thumbnailbar>
      <div>
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
import Thumbnailbar from '../components/SidebarPlugin/Thumbnailbar.vue'

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
    Thumbnailbar,
  },
  methods: {
    test() {
     this.$store.state.dimens.thumbnailbarShow=!this.$store.state.dimens.thumbnailbarShow
      console.log(this.$store.state.dimens.thumbnailbarShow)
    }
  }
}
</script>