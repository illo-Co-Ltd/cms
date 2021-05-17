<template>
  <section>
    <div id="deviceUpdateArea">
      <h1>추가 가능한 장비 리스트()</h1>

      <div id="deviceScroll">

        <div id="deviceListArea" v-for="(array, i) in props.arrDevice" v-bind:key="`B-${i}`">
          <div id="areaLeft">
            <h6>이름 : {{array.serial}}({{array.model}})</h6>
            <h6>담당 : {{array.owner}} : {{array.company}}</h6>
            <h6>IP : {{array.ip}}</h6>
          </div>
          <div id="areaRight" v-on:click="deviceDelete(array)">
            <img src="@/assets/icon/icon_sunny.png"/>
          </div>
        </div>

      </div>
    </div>
  </section>
</template>

<script>

import {reactive} from 'vue'
import {baseURL} from "@/utils/BasicAxiosURL.ts"
import axios from "axios";

const ai = axios.create({
  baseURL
});


export default {
  props : ['arrProjectDevice','arrDevice'],
  setup(props){
    const state = reactive({
    });


    const deviceDelete = (array) =>{
      console.log('11');
      array;
      ai;
    }

    return {
      state,
      deviceDelete,
      props
    }
  }
}
</script>

<style lang="scss" scoped>

@import "@/styles/_mixins.scss";
@import "@/styles/_variables.scss";

  #deviceUpdateArea{
    overflow: hidden;
    width: 100%;
    max-width: 500px;
    margin: 50px auto;

  }

  h1{
    font-size: 30px;
    font-weight: bold;
    margin: 30px 0px;
    text-align: center;
  }

  #deviceScroll{
    height: 400px;
    overflow-y:scroll;
    border: 1px solid #999;
  }

  #deviceScroll::-webkit-scrollbar {
    width: 10px;
  }
  #deviceScroll::-webkit-scrollbar-thumb {
    background-color: #dbdbdb;
    border-radius: 10px;
    background-clip: padding-box;
    border: 2px solid transparent;
  }
  #deviceScroll::-webkit-scrollbar-track {
    background-color: grey;
    border-radius: 10px;
    box-shadow: inset 0px 0px 5px white;
  }


  #deviceListArea{
    overflow: hidden;
    margin: 0 10px;
    border-bottom: 1px solid #ccc;
    >*{
      float: left;
      font-size: 18px;
      padding: 4px;
      height: 60px;
    }
    >#areaLeft{
      width: 85%;
      line-height: 21px;
      font-size: 15px;
    }
    >#areaRight{
      width: 10%;
      float: right;
      >img{
        width: 25px;
        margin-top: 19px;
        margin-left: 5px;
        background: #999;
      }
    }
  }

</style>
