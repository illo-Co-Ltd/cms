<template>
  <transition>
    <div v-if="$store.state.dimens.thumbnailbarShow" ref="mthumbnailbar">
      <div class="tb bg-white tb-shadow"
          v-bind:style="{top:this.$store.state.dimens.header+'px',
                        width:this.$store.state.dimens.thumbnailbarWidth+'px',
                        marginLeft:this.$store.state.dimens.sidebarWidth+'px'}">
      </div>
    </div>
  </transition>
</template>

<script>
export default {
  
}
</script>

<style scoped>
.tb-shadow{
  box-shadow: 1px 0px 5px rgb(223, 223, 223);
}
.tb{
  position: fixed;
  bottom: 0;
}
.slide-fade-enter-active {
  transition: all .1s ease;
}
.slide-fade-leave-active {
  transition: all .8s ;
}
.slide-fade-enter, .slide-fade-leave-to
/* .slide-fade-leave-active below version 2.1.8 */ {
  transform: translateX(-250px);
  opacity: 0;
}
.test{
  margin-left: 400px;
  margin-top: 400px;
}
</style>