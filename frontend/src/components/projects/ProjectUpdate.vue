<template>
  <section>
    <div id="projectInsertArea">
      <h1>프로젝트 업데이트</h1>

      <div class="inputArea">
        <img src="@/assets/icon/icon_home.png">
        <input type="text" v-model="projectName" id="inputName" placeholder="이름" maxlength="10" >
      </div>
      <div class="inputArea">
        <img src="@/assets/icon/icon_home.png">
        <input type="text" v-model="shorthand" id="inputShorthand" placeholder="약자" maxlength="40">
      </div>
      <div class="inputArea">
        <img src="@/assets/icon/icon_home.png">
        <input type="text" v-model="description" id="inputDescription" placeholder="설명" maxlength="30">
      </div>
      <div class="inputArea">
        <img src="@/assets/icon/icon_home.png">
        <input type="text" v-model="started" id="inputStarted" placeholder="시작 날짜" maxlength="30">
      </div>


      <div :style="{display : state.alertDisplay}">
        <h3  id="alertMessage"></h3>
      </div>

      <button id="inputBtn" v-on:click="projectInsert()">수정하기</button>

      <h2>©liio Corp. All rights reserved.</h2>

    </div>
  </section>
</template>

<script>
/*eslint-disable*/

import {watch, ref, reactive, onMounted, inject} from 'vue'
import {baseURL} from "@/utils/BasicAxiosURL.ts"
import axios from "axios";
import Swal from 'sweetalert2/dist/sweetalert2.js'
import router from "@/routes/routes.js"
import {useRoute} from 'vue-router'

const storage = window.sessionStorage;

const ai = axios.create({
  baseURL
});


let event1;

export default {

  setup(){
    const emitter = inject("emitter");
    const {
      params : {originName}
    } = useRoute();

    const state = reactive({
      alertDisplay : "none"
    })

    const projectName = ref("");
    const shorthand = ref("");
    const description = ref("");
    const started = ref("2021-05-20T12:31:54.911+09:00");
    const ended = ref("2021-05-20T12:31:54.911+09:00");
    //2021-05-20T02:37:08.388089+00:00

    onMounted(()=>{

      ai.get('/data/project?name='+originName).then(res =>{
        console.log(res);
        projectName.value = res.data.data[0].name;
        shorthand.value = res.data.data[0].shorthand;
        description.value = res.data.data[0].description;
        started.value = res.data.data[0].started;
        ended.value = res.data.data[0].ended;

      })

    })


    const alertCloseEvent = () =>{
      state.alertDisplay = "none";
    }

    const projectInsert = () =>{
      clearTimeout(event1);
      if(projectName.value==''){
        document.getElementById("inputName").focus();
        document.getElementById("alertMessage").innerHTML = "<span style='font-weight: bold;'>이름</span>이 비어있습니다";
        state.alertDisplay = "block";
        event1 = setTimeout(alertCloseEvent,3000);
        return false;
      }
      if(shorthand.value==''){
        document.getElementById("inputShorthand").focus();
        document.getElementById("alertMessage").innerHTML = "아이디가 비어있습니다";
        state.alertDisplay = "block";
        event1 = setTimeout(alertCloseEvent,3000);
        return false;
      }
      if(description.value==''){
        document.getElementById("inputDescription").focus();
        document.getElementById("alertMessage").innerHTML = "소속이 비어있습니다";
        state.alertDisplay = "block";
        event1 = setTimeout(alertCloseEvent,3000);
        return false;
      }
      //db insert

      ai.put("/data/project", {
        shorthand : shorthand.value,
        name : originName,
        newname : projectName.value,
        description : description.value,
        started : started.value,
        //created : started.value,
        ended : ended.value
        //created_by : 'root'
      }).then(res => {
        if(res.status === 200){
          Swal.fire({
              toast: true,
              position: 'top',
              icon: 'success',
              title: '수정되었습니다.',
              showConfirmButton: false,
              timer: 3000
             })
          emitter.emit('header_Update');
          router.push('/mainPage/projectManagement/'+projectName.value);
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

    watch(projectName, ()=>{
      const reg = /[\{\}\[\]\/?,;:|\)*~`!^\-_+<>\#$%&\\\=\(\'\"]/gi;
      if(reg.test(projectName.value)){
        clearTimeout(event1);
        document.getElementById("alertMessage").innerHTML = "특수문자는 입력이 불가능합니다.";
        state.alertDisplay = "block";
        event1 = setTimeout(alertCloseEvent,3000);
        return projectName.value = projectName.value.slice(0,-1);
      }
    })
    watch(shorthand, ()=>{
      const reg = /[\{\}\[\]\/?,;:|\)*~`!^\-_+<>\#$%&\\\=\(\'\"]/gi;
      if(reg.test(shorthand.value)){
        clearTimeout(event1);
        document.getElementById("alertMessage").innerHTML = "특수문자는 입력이 불가능합니다.";
        state.alertDisplay = "block";
        event1 = setTimeout(alertCloseEvent,3000);
        return shorthand.value = shorthand.value.slice(0,-1);
      }
    })
    watch(description, ()=>{
      const reg = /[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]/gi;
      if(reg.test(description.value)){
        clearTimeout(event1);
        document.getElementById("alertMessage").innerHTML = "특수문자는 입력이 불가능합니다.";
        state.alertDisplay = "block";
        event1 = setTimeout(alertCloseEvent,3000);
        return description.value = description.value.slice(0,-1);
      }
    })



    return {
      state,
      projectName,
      shorthand,
      description,
      projectInsert,
      started
    }
  }
}
</script>

<style lang="scss" scoped>

@import "@/styles/_mixins.scss";
@import "@/styles/_variables.scss";

  #projectInsertArea{
    overflow: hidden;
    width: 100%;
    max-width: 500px;
    margin: 50px auto;

  }

  h1{
    font-size: 25px;
    font-weight: bold;
    margin: 30px 0px;
    text-align: center;
  }

  h2{
    font-size: 13px;
    text-align: center;
    margin-top: 10px;
  }

  #alertMessage{
    font-size: 15px;
    text-align: center;
    height: 37px;
    color : red;
  }



  .inputArea{
    width: 90%;
    height: 50px;
    margin: 25px 5%;
    outline: 1px solid #aaa;
    font-size: 13px;
    >img{
      width: 50px;
      height: 50px;
      border-right: 1px solid #aaa;
      float: left;
    }
    >input{
      width: calc(100% - 72px);
      height: 100%;
      border: none;
      margin: 0px;
      padding: 0px 10px;
      float: left;
    }
    > select{
      width: calc(100% - 52px);
      height: 100%;
      padding-left : 5px;
      border-radius: 0px; /* iOS 둥근모서리 제거 */
      cursor: pointer;
      float: left;
      border: none;
    }
  }

  #inputBtn{
    width: 90%;
    height: 55PX;
    margin: 0px 5%;

    @include border-radius(5px);
    color: #fff;
    background: #033E5D;
    border: none;
  }

</style>
