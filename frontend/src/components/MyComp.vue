<template slot="links">
  <div>
    <div @click="nodeClicked">
      <div v-if="hasChildren">
        <sidebar-item
          v-if="!expanded"
          :link="{
            name: node.name,
            icon: 'ni ni-bold-right text-primary',
            path: '#',
          }"
        />
        <sidebar-item
          v-else
          :link="{
            name: node.name,
            icon: 'ni ni-bold-down text-primary',
            path: '#',
          }"
        />
      </div>
      <div v-else>
        <sidebar-item :link="{ name: node.name, path: '#' }" />
      </div>
    </div>
    <div v-if="expanded">
      <my-comp
        v-for="child in node.children"
        :key="child.name"
        :node="child"
        :depth="depth + 1"
        @onClick="(node) => $emit('onClick', node)"
      />
    </div>
  </div>
</template>

<script>
import MyComp from "./MyComp.vue";
import SidebarItem from "./SidebarPlugin/SidebarItem.vue";
export default {
  components: {
    SidebarItem,
    MyComp,
  },
  name: "MyComp",
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
        this.$emit("onClick", this.node);
      }
    },
  },
  computed: {
    hasChildren() {
      return this.node.children;
    },
  },
};
</script>