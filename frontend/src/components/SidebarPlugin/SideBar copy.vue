<template>
  <div ref="msidebar">
    <div class="sb bg-white sb-shadow"
        v-bind:style="{top:this.$store.state.dimens.header+'px',width:this.$store.state.dimens.sidebarWidth+'px'}">
      <!-- content -->
      <div>
        <div class="c-p"
             @click="onClickCP">Create Project + </div>
        <project-tree :project="this.projectList"></project-tree>
      </div>
    </div>
    <!-- modal content -->
    <create-project @update="refreshTree"></create-project>
    <add-device></add-device>
  </div>
</template>

<script>
import axios from 'axios'
import AddDevice from '../modals/AddDevice.vue';
import CreateProject from '../modals/CreateProject.vue';
import ProjectTree from './ProjectTree.vue';

export default {
  components: { ProjectTree, CreateProject, AddDevice },
  data() {
    return {
      projectList: {},
    }
  },
  methods:{
    onClickCP() {
      this.$store.state.modals.project = !this.$store.state.modals.project
    },
    refreshTree() {
      axios.get('server/data/project')
      .then((res) => {
        this.projectList = res.data
      })
    }
  },
  mounted() {
    this.refreshTree()
  }
}
</script>

<style scoped>
.sb-shadow{
  box-shadow: 1px 0px 5px rgb(223, 223, 223);
}
.sb{
  position: fixed;
  bottom: 0;
}
.c-p{
  cursor: pointer;
  color: rgb(255, 255, 255);
  background-color: rgb(175, 175, 175);
}
</style>
