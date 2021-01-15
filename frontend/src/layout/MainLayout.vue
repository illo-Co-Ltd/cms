<template>
  <div class="parent">
    <div class="div1">
      <headder></headder>
    </div>
    <div class="div2">
      <side-bar-custom></side-bar-custom>
    </div>
    <div class="main-fragment">
        <h5>hello</h5>
      </div>
  </div>
</template>

<script>
import Headder from '../components/Headder.vue';
import SideBarCustom from '../components/SidebarPlugin/SideBarCustom.vue';

export default {
  name: "app",
  data() {
    return {

    }
  },
  components: {
    Headder,
    SideBarCustom,
  },
};
</script>

<style scoped>
.parent {
  display: grid;
  width: 100%;
  height: 100%;
  grid-template-columns: repeat(2, 250px) 1fr;
  grid-template-rows: 56px 1fr;
  grid-column-gap: 0px;
  grid-row-gap: 0px;
}

.div1 { 
  grid-area: 1 / 1 / 2 / 4; 
  z-index: 2;
}
.div2 { 
  grid-area: 2 / 1 / 3 / 3; 
  z-index: 1;
}
.main-fragment { grid-area: 2 / 3 / 3 / 4; }
</style>