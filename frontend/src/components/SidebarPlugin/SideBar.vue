<template>
  <div class="sb bg-white sb-shadow"
       v-bind:style="{top:this.$store.state.header+'px'}">
    DashBoard SideBar
  </div>
</template>
<script>
export default {
  data () {
    return {
     
    }
  },
  methods: {
    logheaderHeight: function(){
     console.log(this.$store.state.header)
    },
  },
  mounted() {
    this.logheaderHeight();
  },
}
</script>
<style scoped>
.sb-shadow{
  box-shadow: 1px 0px 5px rgb(223, 223, 223);
}
.sb{
  position: fixed;
  width: 250px;
  bottom: 0;
}
</style>
