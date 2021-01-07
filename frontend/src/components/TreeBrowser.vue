<template>
  <div>
    <div @click="nodeClicked"
         :style="{'margin-left': `${depth * 10}px`}"
         class="node"
    >
    <span v-if="hasChildren" 
          class="type">
          {{ expanded ? '&#9660;' : '&#9658;' }}
    </span>
    <span v-else>&#9671;</span>
    {{ node.name }}
    </div>
    <ul v-if="expanded">
        <tree-browser v-for="child in node.children"
                     :key="child.name"
                     :node="child"
                     :depth="depth + 1"
                     @onClick="(node) => $emit('onClick', node)">
        </tree-browser>
    </ul>
  </div>
</template>

<script>
export default {
  name: "TreeBrowser",
  props: {
    node: Object,
    depth: {
      type: Number,
      default: 0,
    },
  },
  data() {
    return {
      expanded: false,
    };
  },
  methods: {
      nodeClicked() {
          this.expanded = !this.expanded;
          if (!this.hasChildren()) {
              console.log('delete onclick');
              this.$emit('onClick', this.node);
          }
      }
  },
  computed: {
      hasChildren() {
          return this.node.children;
      }
  }
}
</script>

<style scoped>
.node {
  text-align: left;
  font-size: 14px;
}
</style>>