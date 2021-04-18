<template slot="links">
  <div>
    <div v-for="(item, i) in this.project.data" :key="i">
      <div class="pt-item-box">
        <i class="ni ni-bold-right pt-icon-box"></i>
        <a class="pt-text-box">{{item.name}}</a>
        <a class="pt-button-box">
          <button class="btn pt-button-style" @click="registDevice(i)">+</button>
          <button class="btn pt-button-style">-</button>
        </a>
      </div>
      <!-- <device-tree></device-tree> -->
    </div>
  </div>
</template>

<script>
import DeviceTree from './DeviceTree.vue'

export default {
  components: { DeviceTree },
  props: {
    project: Object
  },
  methods: {
    registDevice(i){
      this.$store.state.modals.selectedDevice = this.project.data[i].name
      this.$store.state.modals.rDevice = !this.$store.state.modals.rDevice
    }
  }
}
</script>

<style scoped>
.pt-item-box{
  width: 100%;
  cursor: pointer;
  /* border-top: 1px solid rgb(235, 235, 235);;
  border-bottom: 1px solid rgb(235, 235, 235); */
}
.pt-icon-box{
  margin: 0px 5px;
  margin-top: 6px;
}
.pt-button-box{
  position: absolute;
  right: 5px;
}
.pt-text-box{
  position: relative;
  bottom: 0.1rem;
}
.pt-button-style{
  padding: 0px 2px;
  color: rgb(45, 45, 45);
}
</style>