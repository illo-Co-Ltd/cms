<template>
<div class="side-bar-parent">
  <div class="side-bar-div1">
    <button @click="fetchStructures">{{this.result}}</button>
    <my-comp :node="root"
             @onClick="nodeClicked"/>
  </div>
  <div class="side-bar-div2" >
    <thumbnail-card :node="selectedNodeTarget.children"/>
  </div>
</div>
</template>

<script>
import MyComp from '../MyComp.vue'
import ThumbnailCard from '../ThumbnailCard.vue';
import axios from 'axios';

export default {
  components: { MyComp, ThumbnailCard },

  data() {
    return {
      result: 'default',
      selectedNodeTarget: {},
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
    fetchStructures: function() {
      axios({
        methods: 'GET',
        url: '/api/',
      }).then((response) => {
        console.log(response);
        this.result = response.data;
      }).catch((e) => {
        console.log("err:",e)
      })
    },
    addStructures: function() {
      
    },
    upadateStructures: function() {
      
    },
    deleteStructures: function() {
      
    },
  },  
}
</script>

<style scoped>
.side-bar-parent {
  display: grid;
  width: 100%;
  height: 100%;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: 1fr;
  grid-column-gap: 0px;
  grid-row-gap: 0px;
}

.side-bar-div1 { 
  grid-area: 1 / 1 / 2 / 2; 
  background-color: rgb(255, 255, 255);
  overflow-x: auto;
}
.side-bar-div2 { 
  grid-area: 1 / 2 / 2 / 3; 
  background-color: rgb(255, 255, 255);
  overflow-x: auto;
}
</style>