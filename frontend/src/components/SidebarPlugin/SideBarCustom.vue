<template>
<div>
  <div class="sidebar-left">
    <my-comp :node="root"
             @onClick="nodeClicked"/>
  </div>
  <div class="sidebar-right" >
    <thumbnail-card :node="selectedNodeTarget.children"/>
  </div>
</div>
</template>

<script>
import MyComp from '../MyComp.vue'
import ThumbnailCard from '../ThumbnailCard.vue';
export default {
  components: { MyComp, ThumbnailCard },

  data() {
    return {
      selectedNodeTarget: {
        
      },
      root: {
        type: 'root',
        name: 'root',
        children: [
          {
            type: 'project',
            name: 'animal',
            children: [
              {
                type: 'target',
                name: 'lion',
                children: [
                  {
                    type: 'image',
                    name: require("@/devices/img4.jpg"),
                  },
                  {
                    type: 'image',
                    name: require("@/devices/img5.jpg"),
                  },
                ]
              },
              {
                type: 'target',
                name: 'dog',
                children: [
                  {
                    type: 'image',
                    name: require("@/devices/img1.jpg"),
                  },
                  {
                    type: 'image',
                    name: require("@/devices/img2.jpg"),
                  },
                ]
              },
              {
                type: 'target',
                name: 'cat',
                children: [
                  {
                    type: 'image',
                    name: require("@/devices/img3.jpg"),
                  }
                ]
              }
            ]
          },
          {
            type: 'project',
            name: 'people',
            children: [
              {
                type: 'target',
                name: 'people',
                children: [
                  {
                    type: 'image',
                    name: require("@/devices/img6.jpg"),
                  },
                  {
                    type: 'image',
                    name: require("@/devices/img7.jpg"),
                  },
                  {
                    type: 'image',
                    name: require("@/devices/img8.jpg"),
                  },
                  {
                    type: 'image',
                    name: require("@/devices/img9.jpg"),
                  },
                  {
                    type: 'image',
                    name: require("@/devices/img10.jpg"),
                  },
                ]
              }
            ]
          }
        ]
      },
    }
  }, //data() end
  methods: {
    nodeClicked(node) {
      if(node.type == 'target')
        this.selectedNodeTarget = node;
      else
        this.selectedNodeTarget = {};
    },
  },  
}
</script>

<style scoped>
.sidebar-left {
  display: block;
  position: fixed;
  top: 0;
  bottom: 0;
  width: 100%;
  max-width: 250px;
  padding-left: 0.3rem;
  padding-right: 0.3rem;
  background-color: rgb(255, 255, 255);
  overflow-x: auto;
}
.sidebar-right {
  display: block;
  position: fixed;
  width: 100%;
  max-width: 250px;
  margin-left: 250px;
  top: 0;
  bottom: 0;
  background-color: rgb(255, 255, 255);
  border-left: 2px;
  border-left-color: rgb(248, 249, 254);
  overflow-x: auto;
}
</style>