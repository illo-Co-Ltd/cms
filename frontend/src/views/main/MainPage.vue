<template lang="html">
  <div>
    <MainHeader></MainHeader>
    <router-view id="mainpage" :key="$route.fullPath"></router-view>
    <MainFooter class="mainFooter"></MainFooter>
  </div>
</template>

<script>

import router from "@/routes/routes.js"
import MainHeader from "@/components/mainFrame/MainHeader.vue"
import MainFooter from "@/components/mainFrame/MainFooter.vue"
// 안녕 3333
export default {
  router,
  components : {
    MainHeader,
    MainFooter
  }

}
</script>

<style lang="scss" scoped>

@import "@/styles/_mixins.scss";
@import "@/styles/_variables.scss";

  #mainpage{
    padding-top: 66px;
    margin-left: 200px;
    background: $main-background;
  }
  .mainFooter{
    margin-left: 200px;
  }

  // 1000 이하가 되면 aside 감춤
  @media ( max-width: 1000px ) {
    #mainpage{
      padding-top: 46px;
    }
    .mainFooter{
      margin-left: 20%;
    }
  }


  // 800 이하가 되면 aside 감춤
  @media ( max-width: 800px ) {
      #mainpage{
        margin-left: 0px;
      }
      .mainFooter{
        margin-left: 0px;
      }
  }



</style>
