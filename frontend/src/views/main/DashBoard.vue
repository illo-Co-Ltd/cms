<template lang="html">
  <section>
    <div id="introMainArea">

      <div id="titleArea">
        <h6 class="pageTitle">DashBoard</h6>
        <div class="pointLine"></div>
      </div>
      <div id="mainSection">
        <ProjectList :projectState="'proceeging'"></ProjectList>
        <ProjectList :projectState="'close'"></ProjectList>
        <NoticeList></NoticeList>
        <DeviceHorizontalList></DeviceHorizontalList>
      </div>
    </div>
  </section>
</template>

<script>

import router from "@/routes/routes.js"
import ProjectList from "@/components/projects/ProjectList.vue"
import NoticeList from "@/components/etc/NoticeList.vue"
import DeviceHorizontalList from "@/components/device/DeviceHorizontalList.vue"


export default {
  router,
  components : {
    ProjectList,
    DeviceHorizontalList,
    NoticeList
  },
  setup(){


  }
}
</script>
<style lang="scss" scoped>

  @import "@/styles/_mixins.scss";
  @import "@/styles/_variables.scss";



    #introMainArea{
      width: 100%;
      max-width: 1000px;
      min-width: 300px;
      min-height : 500px;
      margin-bottom: 20px;
      margin: 0 auto;
    }

    #titleArea{
      min-width: 350px;
      .pointLine{
        @include length(80px, 5px);
        background: #000;
        margin: 0 auto;
        margin-bottom: 10px;
      }
      .pageTitle{
        font-size: 19px;
        margin: 0 auto;
        padding-top: 20px;
        padding-bottom: 5px;
        text-align: center;
      }
    }

    #mainSection{
      overflow: hidden;
      > * {
        float: left;

        &:nth-child(1){
          width: 33%;
        }
        &:nth-child(2){
          width: 33%;
        }
        &:nth-child(3){
          width: 33%;
        }
        &:nth-child(4){
          width: 100%;
        }
      }
    }


    @media ( max-width: 1100px ) {
      #mainSection{
        > * {
          &:nth-child(1){
            width: 50%;
          }
          &:nth-child(2){
            width: 50%;
          }
          &:nth-child(3){
            width: 100%;
          }
        }
      }
    }

    @media ( max-width: 600px ) {
      #mainSection{
        > * {
          &:nth-child(1){
            width: 100%;
          }
          &:nth-child(2){
            width: 100%;
          }
          &:nth-child(3){
            width: 100%;
          }
        }
      }
    }

</style>
