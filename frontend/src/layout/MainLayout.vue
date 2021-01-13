<template>
  <div class="wrapper">
    <side-bar-custom></side-bar-custom>

    <div class="my-main-content">
      
    </div>
  </div>
</template>

<script>
import SideBarCustom from '../components/SidebarPlugin/SideBarCustom.vue';

export default {
  name: "app",
  data() {
    return {

    }
  },
  components: {
    SideBarCustom,
  },
};
</script>

<style scoped>
.card-wrapper {
  display: block;
  position: fixed;
  width: 250px;
  margin-left: 250px;
  top: 0;
  bottom: 0;
  background-color: rgb(255, 255, 255);
  overflow-x: auto;
}
.my-main-content {
  position: relative;
  margin-left: 500px;
}
</style>