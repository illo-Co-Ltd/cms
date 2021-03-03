<template>
  <div ref="msidebar">
    <div class="sb bg-white sb-shadow"
        v-bind:style="{top:this.$store.state.header+'px',width:this.$store.state.sidebar_w+'px'}">
    </div>
  </div>
</template>

<script>

export default {
  components: {  },
  data() {
    return{
      
    };
  },
  methods:{
    SidebarWidth() {
      
    }
  }
}
</script>

<style scoped>
.sb-shadow{
  box-shadow: 1px 0px 5px rgb(223, 223, 223);
}
.sb{
  position: fixed;
  bottom: 0;
}
</style>
