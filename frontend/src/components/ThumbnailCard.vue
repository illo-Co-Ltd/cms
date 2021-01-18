<template>
<div>
<div class="card-item" v-for="item in node" :key="item.name"
     style="cursor: pointer;"
     @click="itemClicked(item.name)">
  <img class="card-img-top" 
       :src="item.name"
       alt="Card image cap"/>
  <h5 class="card-title">{{item.name}}</h5>
</div>
</div>
</template>

<script>
export default {
  data() {
    return {
      imgPath: '',
    }
  },
  props: {
    node: Array,
  },
  methods: {
   itemClicked(path) {
     this.imgPath = path;
     this.$emit('onClick', this.imgPath);
   }
  },
};
</script>

<style scoped>
.card-item {
  position: relative;
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  -webkit-box-orient: vertical;
  -webkit-box-direction: normal;
  -ms-flex-direction: column;
  flex-direction: column;
  min-width: 0;
  word-wrap: break-word;
  background-color: #fff;
  background-clip: border-box;
}
</style>