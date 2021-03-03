<template>
  <div>
    <my-header></my-header>
    <div class="container">
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
import { FadeTransition } from 'vue2-transitions'

export default {
  components: {
    MyHeader,
    FadeTransition,
  },
}
</script>