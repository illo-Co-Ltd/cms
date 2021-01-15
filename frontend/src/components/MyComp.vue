<template slot="links">
  <div>
    <!-- 호출시 표시될 하나의 노드 -->
    <div :style="{'margin-left': `${depth * 10}px`}"
         @click="nodeClicked"
         @onClick="(node) => $emit('onClick', node)">
      <div v-if="hasChildren">
        <div v-if="node.type!='target'">
          <sidebar-item v-if="!expanded"
                      :link="{
                          name: node.name,
                          icon: 'ni ni-bold-right text-primary',
                          path: '',
                      }"/>
          <sidebar-item v-else
                        :link="{
                          name: node.name,
                          icon: 'ni ni-bold-down text-primary',
                          path: '',
                        }"/>
        </div>
        <div v-else>
          <sidebar-item :link="{
                          name: node.name,
                          icon: 'ni ni-app text-yellow',
                          path: '',
                        }"/>
        </div>
      </div>
    </div>
    <!-- 확장시 자식 노드들 표시 -->
    <div v-if="expanded">
      <my-comp
        v-for="child in node.children"
        :key="child.name"
        :node="child"
        :depth="depth + 1"
        @onClick="(node) => $emit('onClick', node)"/>
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
      this.$emit("onClick", this.node);
    },
  },
  computed: {
    hasChildren() {
      return this.node.children;
    },
  },
};
</script>