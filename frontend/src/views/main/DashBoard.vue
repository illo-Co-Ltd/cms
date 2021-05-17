<template lang="html">
  <section>
    <div id="introMainArea">

      <div id="titleArea">
        <h6 class="pageTitle">Calender</h6>
        <div class="pointLine"></div>
      </div>

    </div>
  </section>
</template>

<script>

import router from "@/routes/routes.js"


export default {
  router,
  setup(){


  }
}
</script>
<style lang="scss" scoped>

  @import "@/styles/_mixins.scss";
  @import "@/styles/_variables.scss";



    #introMainArea{
      width: calc(100%);
      min-height : 500px;
      margin-bottom: 20px;
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




</style>
