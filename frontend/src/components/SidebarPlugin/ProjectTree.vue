<template slot="links">
  <div>
    <div>{{this.node}}</div>
  </div>
</template>

<script>
export default {
  props: {
    node: Object,
  },
  data() {
    return {
      expanded: false,
    };
  },
  methods: {
    
  },
}
</script>

<style scoped>

</style>