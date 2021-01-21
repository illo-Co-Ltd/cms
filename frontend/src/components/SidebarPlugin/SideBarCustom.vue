<template>
<div class="side-bar-parent">
  <div class="side-bar-parent-div1">
    <add-item-control :node="this.selectedNodeProject.name"></add-item-control>
    <my-comp :node="result"
             @onClick="nodeClicked"/>
  </div>
  <div class="side-bar-parent-div2" >
    <thumbnail-card :node="selectedNodeTarget.children"
                    @onClick="imageClicked"/>
  </div>
</div>
</template>

<script>
import MyComp from '../MyComp.vue'
import ThumbnailCard from '../ThumbnailCard.vue';
import axios from 'axios';
import AddItemControl from '../AddItemControl.vue';
export default {
  components: { MyComp, ThumbnailCard, AddItemControl },
  data() {
    return {
      result: {},
      selectedNodeTarget: {},
      selectedImagePath: '',
      selectedNodeProject: {},
    }
  },  
  mounted() {
    this.fetchStructures();
  },
  methods: {
    nodeClicked(node) {
      if(node.type == 'project')
        this.selectedNodeProject = node;
      else if(node.type == 'target') {
        this.selectedNodeTarget = node;
        this.fetchStructures();
      }
      else
        this.selectedNodeTarget = {};
      console.log(node);
    },
    imageClicked(img_path) {
      this.selectedImagePath = img_path;
      this.$emit('onClick', this.selectedImagePath);
    },
    fetchStructures: function() {
      axios({
        methods: 'GET',
        url: '/server/api/image/tree',
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
.side-bar-parent-div1 { 
  grid-area: 1 / 1 / 2 / 2; 
  background-color: rgb(255, 255, 255);
  overflow-x: auto;
  box-shadow: 1px 2px rgb(241, 241, 241);
  z-index: 2;
}
.side-bar-parent-div2 { 
  grid-area: 1 / 2 / 2 / 3; 
  background-color: rgb(255, 255, 255);
  overflow-x: auto;
  box-shadow: 1px 2px rgb(241, 241, 241);
  z-index: 1;
}
</style>