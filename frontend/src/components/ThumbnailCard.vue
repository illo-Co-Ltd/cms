<template>
<div class="card-group">
  <card v-for="item in node" :key="item.path">
    <img class="card-img-top" 
         :src="item.path"
         alt="Card image cap"/>
    <h5 class="card-title">{{item.name}}</h5>
  </card>
</div>
</template>

<script>
export default {
  props: {
    node: Array,
  },
};
</script>
