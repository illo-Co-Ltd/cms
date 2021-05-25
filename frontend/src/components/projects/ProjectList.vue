<template>
  <section>
    <div id="deviceUpdateArea">
      <h1>{{state.pageTitle}}({{state.arrProject.length}})</h1>

      <div id="deviceScroll">

        <div id="deviceListArea" v-for="(array, i) in state.arrProject" v-bind:key="`B-${i}`">
          <div id="areaLeft" @click="moveProjectManagement(array)">
            <h6>이름 : {{array.name}}</h6>
            <h6>담당 : {{array.created_by}}</h6>
            <h6>기간 : {{array.started}} ~
              <span v-if="props.projectState == 'close'">{{array.ended}}</span>
              <span v-if="props.projectState != 'close'">진행중</span>
            </h6>
          </div>
        </div>

      </div>
    </div>
  </section>
</template>

<script>
import router from "@/routes/routes.js"
import {reactive} from 'vue'
import {onMounted} from 'vue'
import {baseURL} from "@/utils/BasicAxiosURL.ts"
import axios from "axios";
const ai = axios.create({
  baseURL
});


export default {
  props : ['projectState'],
  setup(props){
    const state = reactive({
        arrProject : new Array(),
        pageTitle : ''
    });
    onMounted(()=>{
      if(props.projectState == 'close'){
        state.pageTitle = '종료된 프로젝트';
      }else{
        state.pageTitle = '진행중인 프로젝트';
      }


      ai.get('/data/project').then(res =>{

        for(let i = 0; i < res.data.data.length ; i++){
          let projectData = {};
          projectData.id = res.data.data[i].id;
          projectData.name = res.data.data[i].name;
          projectData.started = res.data.data[i].started+'';
          projectData.started = projectData.started.substr(0,10);
          projectData.ended = res.data.data[i].ended+'';
          projectData.ended = projectData.ended.substr(0,10);
          projectData.created_by = res.data.data[i].created_by;

          if(props.projectState == 'close'){
            if(res.data.data[i].ended != null){
              state.arrProject.push(projectData);
            }
          }else{
            if(res.data.data[i].ended == null){
              state.arrProject.push(projectData);
            }
          }

        }


      })
    })

    const moveProjectManagement = (array) =>{
      router.push('/mainPage/projectManagement/'+array.name)
    }



    return {
      state,
      props,
      moveProjectManagement
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
    margin: 50px auto;
    margin-top: 10px;
    max-width: 450px;
  }

  h1{
    font-size: 25px;
    font-weight: bold;
    margin: 30px 0px;
    text-align: center;
  }
  #deviceScroll{
    height: 400px;
    overflow-y:auto;
    border: 1px solid #999;
    @include border-radius(10px);
    margin: 0 10px;
    background: #dddddd88;
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
      padding: 4px;
      height: 60px;
    }
    >#areaLeft{
      width: 100%;
      line-height: 21px;
      font-size: 14px;
    }
  }

</style>
