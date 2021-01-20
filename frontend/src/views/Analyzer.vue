<template>
<div>
  <img :src="require(`../assets/data/${mainImage}`)" />
</div>
</template>
<script>
export default {
  props: {
    mainImage: String,
  },   
}
</script>
<style scoped>

</style>