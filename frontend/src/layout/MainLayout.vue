<template>
  <div class="wrapper">
    <side-bar :background-color="sidebarBackground"
              short-title="Argon"
              title="Argon">
      <template slot="links">
        <my-comp :node="root" @onClick="nodeWasClicked" />
      </template>
    </side-bar>

    <div class="card-wrapper">
      <thumbnail-card :node="imgroot"></thumbnail-card>
    </div>

    <div class="my-main-content">
      <img class="card-img-top" 
       src="@/devices/test_animals/img3.jpg"
       alt="Card image cap"/>
    </div>
  </div>
</template>

<script>
import ThumbnailCard from "../components/ThumbnailCard.vue";
import MyComp from "../components/MyComp.vue";
import SideBar from '../components/SidebarPlugin/SideBar.vue';

export default {
  name: "app",
  data() {
    return {
      sidebarBackground: 'vue', //vue|blue|orange|green|red|primary
      root: {
        name: "devices",
        path: "@/devices/",
        children: [
          {
            name: "test_animals",
            path: "@/devices/test_animals/",
            children: [
              {
                name: "lion",
                path: "@/devices/test_animals/lion/",
              }
            ]
          },
          {
            name: "test_people",
            path: "@/devices/test_people/",
          },
        ],
      },
      directoryPath: "@/devices/",
      imgroot: [
        {
          name: 'img1',
          path: require("@/devices/test_people/img1.jpg")
        },
        {
          name: 'img2',
          path: require("@/devices/test_people/img2.jpg")
        },
        {
          name: 'img3',
          path: require("@/devices/test_people/img3.jpg")
        },
        {
          name: 'img4',
          path: require("@/devices/test_people/img4.jpg")
        },
        {
          name: 'img5',
          path: require("@/devices/test_people/img5.jpg")
        },
        {
          name: 'img6',
          path: require("@/devices/test_people/img6.jpg")
        },
        {
          name: 'img6',
          path: require("@/devices/test_people/img6.jpg")
        },
        {
          name: 'img6',
          path: require("@/devices/test_people/img6.jpg")
        },
      ],
    };
  },
  components: {
    ThumbnailCard,
    MyComp,
    SideBar,
  },
  methods: {
    nodeWasClicked(node) {
      this.directoryPath = node.path;
    },
  },
};
</script>

<style scoped>
.card-wrapper {
  display: block;
  position: fixed;
  width: 250px;
  margin-left: 250px;
  top: 0;
  bottom: 0;
  background-color: rgb(255, 255, 255);
  overflow-x: auto;
}
.my-main-content {
  position: relative;
  margin-left: 500px;
}
</style>