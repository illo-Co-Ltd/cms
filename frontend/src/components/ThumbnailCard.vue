<template>
<div class="card-deck">
  <card v-for="item in node" :key="item.path">
    <img class="card-img-top" 
         :src="item.path"
         alt="Card image cap">
    <h5 class="card-title">Card title</h5>
  </card>
</div>
</template>

<script>
export default {
  props: {
    node: Object,
  },
  computed: {
    hasChildren() {
      return this.node.children;
    }
  }
};
</script>

<style scoped>
.card_size {
  width: 100%;
  padding: 50px;
}
</style>