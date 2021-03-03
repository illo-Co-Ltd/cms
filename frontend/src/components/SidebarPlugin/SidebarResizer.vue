<template>
    <div class="sbr">
        {{ width }}, {{ height }}
    </div>
</template>

<script>
export default {
    data() {
        return {
            width: 0,
            height: 0
        }
    },
    mounted() {
        // console.log("ready...");
        window.addEventListener('resize', this.handleResize);
	},
    beforeDestroy() {
        // console.log("beforeDestroy...");
        window.removeEventListener('resize', this.handleResize);
    },
    methods: {
        handleResize() {
            this.width = window.innerWidth;
            this.height = window.innerHeight;
        }
    }
}
</script>
<style scoped>
.sbr-active{
  position: fixed;
  width: 2px;
  bottom: 0;
  background: rgb(136, 154, 255);
}
.sbr{
  position: fixed;
  width: 200px;
  top: 60px;
  bottom: 0;
  cursor: e-resize;
}
</style>