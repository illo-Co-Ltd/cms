<template lang="html">
  <div>

    <section id="projectInfomationArea">
      <h1>프로젝트 Infomation</h1>
      <div id="dataArea">
        <div id="infoArea" style="margin-top : 5px;">
          <h3>Name</h3>
          <h4>: {{state.name}}</h4>
        </div>
        <div id="infoArea">
          <h3>Shorthand</h3>
          <h4>: {{state.shorthand}}</h4>
        </div>
        <div id="infoArea">
          <h3>Description</h3>
          <h4>: {{state.description}}</h4>
        </div>
        <div id="infoArea">
          <h3>Progress status</h3>
          <h4>: {{state.present}}</h4>
        </div>
        <div id="buttonArea">
          <button id="update" @click="projectUpdate()">수정</button>
          <button id="close" v-if="state.present == '진행중'" @click="projectClose()">종료</button>
          <button id="close" v-if="state.present == '종료'" @click="projectResume()">재개</button>
          <button id="delete" @click="projectDelete()">삭제</button>
        </div>
      </div>
    </section>

  </div>
</template>

<script>

import {onMounted, reactive, inject} from 'vue'
import {baseURL} from "@/utils/BasicAxiosURL.ts"
import axios from "axios"
import {useRoute} from 'vue-router'
import router from "@/routes/routes.js"
import Swal from 'sweetalert2/dist/sweetalert2.js'

const ai = axios.create({
  baseURL
});


export default {


  setup(){
    const emitter = inject("emitter");
    const {
      params : {projectName}
    } = useRoute();

    const state = reactive({
      name : '',
      shorthand : '',
      description : '',
      started : '',
      ended : '',
      present : ''
    });

    onMounted(()=>{
      ai.get('/data/project?name='+projectName).then(res =>{
        console.log(res);
        state.name = res.data.data[0].name;
        state.shorthand = res.data.data[0].shorthand;
        state.description = res.data.data[0].description;
        state.started = res.data.data[0].started;
        state.ended = res.data.data[0].ended;
        if(state.ended == null || state.ended == ''){
          state.present = '진행중';
        }else{
          state.present = '종료';
        }
      })
    })


    const projectDelete = () => {

      ai.delete('/data/project?name='+projectName+'&shorthand='+state.shorthand).then(res=> {
        if(res.status == 200){
          Swal.fire({
              toast: true,
              position: 'top',
              icon: 'success',
              title: '삭제',
              showConfirmButton: false,
              timer: 3000
            });
          emitter.emit('header_Update');
          router.push('/mainPage/dashBoard');
        }
      })
    }
    const projectUpdate = () => {
      router.push({
        name : 'projectUpdate',
        params : {
          originName : state.name
        }
      });
    }
    const projectClose = () => {
      ai.put('/data/project',{
        name : state.name,
        shorthand : state.shorthand,
        description : state.description,
        started : state.started,
        ended : new Date().toISOString().replace("Z", "+09:00")
      }).then(res => {
        if(res.status == 200){
          Swal.fire({
              toast: true,
              position: 'top',
              icon: 'success',
              title: '프로젝트가 종료되었습니다.',
              showConfirmButton: false,
              timer: 3000
            });
          state.present = '종료';
          emitter.emit('header_Update');
        }
      })
    }

    const projectResume = () => {

        ai.put("/data/project", {
          shorthand : state.shorthand,
          name : state.name,
          description : state.description,
          started : state.started,
          //created : started.value,
          ended : null
          //created_by : 'root'
        }).then(res => {
          if(res.status === 200){
            Swal.fire({
                toast: true,
                position: 'top',
                icon: 'success',
                title: '재개 되었습니다.',
                showConfirmButton: false,
                timer: 3000
               })
               state.present = '진행중';
               emitter.emit('header_Update');
          }else{
            alert("오류")
          }
        }).catch((e) =>{
          console.log(e);
            Swal.fire({
              toast: true,
              position: 'top',
              icon: 'error',
              title: '생성 실패',
              showConfirmButton: false,
              timer: 3000
            })
          //console.log("err : ",e)
        })
    }

    return{
      state,
      projectUpdate,
      projectDelete,
      projectClose,
      projectResume
    }
  }

}
</script>

<style lang="scss" scoped>

  @import "@/styles/_mixins.scss";
  @import "@/styles/_variables.scss";


  #projectInfomationArea{
    width: 100%;
  }

  h1{
    font-size: 23px;
    font-weight: bold;
    text-align: left;
    margin: 30px 0px 10px 30px;
  }

  #dataArea{
    border: 1px solid #999;
    margin: 0 10px;
    @include border-radius(10px);
  }

  #infoArea{
    overflow: hidden;
    > * {
      float: left;
      line-height: 20px;
    }
    >h3{
      margin-left: 10px;
      width: 120px;
      line-height: 23px;
    }
  }
  #buttonArea{
    >button{
      height: 45px;

      border: none;
      color: #fff;
      margin-top: 5px;

      &:nth-of-type(1) {
        width: 33.3%;
        background: #0000ff;
        @include border-radius(0 0 0 10px);
      }
      &:nth-of-type(2) {
        width: 33.3%;
        background: #666;
      }
      &:nth-of-type(3) {
        width : calc(100% - 66.6%);
        background: #ff0000;
        @include border-radius(0 0 10px 0);
      }
    }
  }
</style>
