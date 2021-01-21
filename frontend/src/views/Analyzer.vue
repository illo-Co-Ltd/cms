<template>
<div>
  <div v-if="hasImage">
  <img class="img-fluid"
       :src="require(`../assets/data/${mainImage}`)" />
  </div>
</div>
</template>
<script>
export default {
  props: {
    mainImage: String,
  }, 
   computed: {
    hasImage() {
      return this.mainImage;
    },
  },
}
</script>
<style scoped>

</style>