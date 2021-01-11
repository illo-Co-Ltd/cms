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
      <h5>{{directoryPath}}</h5>
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
      ],
    };
  },
  components: {
    ThumbnailCard,
    MyComp,
  },
  methods: {
    nodeWasClicked(node) {
      this.directoryPath = node.path;
    },
  },
};
</script>
