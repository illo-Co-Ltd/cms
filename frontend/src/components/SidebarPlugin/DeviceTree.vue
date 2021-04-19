<template>
  <div class="dt-container">
    <div class="dt-item-box"
         v-for="(item, i) in this.entry" :key="i">{{item}}</div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return{
      entry: Object,
    }
  },
  mounted() {
    this.init()
  },
  methods: {
    init() {
      axios.get('server/data/device_entry')
        .then((res)=>{
          this.entry = res.data.data
        })
    }
  }
}
</script>

<style scoped>
.dt-container{
  cursor: pointer;
}
.dt-item-box{
  margin-left: 15px;
}
</style>