<template>
  <div class="wrapper" :class="{ 'nav-open': $sidebar.showSidebar }">
    <side-bar :background-color="sidebarBackground"
              short-title="Argon"
              title="Argon">
      <template slot="links">
        <my-comp :node="root" @onClick="nodeWasClicked" />
      </template>
    </side-bar>

    <div class="main-content">
      <thumbnail-card :node="imgroot"></thumbnail-card>
    </div>
  </div>
</template>

<script>
import ThumbnailCard from "../components/ThumbnailCard.vue";
import MyComp from "../components/MyComp.vue";

export default {
  name: "app",
  data() {
    return {
      root: {
        name: "/",
        children: [
          {
            name: "music",
            children: [
              {
                name: "song.mp3",
              },
            ],
          },
          {
            name: "workspace",
            children: [
              {
                name: "source.js",
              },
            ],
          },
        ],
      },
      imgroot: [
        {
          path: require("../images/blend-dst.jpg")
        },
        {
          path: require("../images/blend-src.jpg")
        },
      ],
    };
  },
  components: {
    ThumbnailCard,
    MyComp,
  },
  methods: {
    nodeWasClicked(node) {
      alert(node.name);
    },
  },
};
</script>

<style>
.container {
  width: 100%;
  height: 100%;
}
.dir_hierarchy {
  border-right: solid;
  border-right-width: thin;
  border-right-color: black;
  background-color: burlywood;
  width: 20%;
  height: 100%;
  min-height: 100vh;
  float: left;
}
.image_hierarchy {
  border-right: solid;
  border-right-width: thin;
  border-right-color: black;
  background-color: rgb(243, 235, 225);
  width: 20%;
  height: 100%;
  min-height: 100vh;
  float: left;
}
</style>
