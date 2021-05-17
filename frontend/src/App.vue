<template>
  <div id="app" class="jg">
    <router-view></router-view>
  </div>
</template>

<script>
import request from "request"
import {onMounted} from 'vue'
import {baseURL} from "@/utils/BasicAxiosURL.ts"

export default {


  setup(){

    onMounted(()=>{
      request(baseURL+'hello', function(error, respones, body){
        window.console.log(body);
      });

    })


  }
}
</script>


<style lang="scss">

@import "@/styles/_reset.scss";
@import "@/styles/_variables.scss";

  body{
    background: $app-background;
  }
</style>
