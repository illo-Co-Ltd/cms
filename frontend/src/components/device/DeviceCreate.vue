<template>
  <section>
    <div id="deviceInsertArea">
      <h1>디바이스 생성</h1>

      <div class="inputArea">
        <img src="@/assets/icon/icon_home.png">
        <select v-model="model" id="inputModel">
          <option value="" selected>모델 선택</option>
          <option value="j-ver1">JPEG STREAM MODEL VER1</option>
          <option value="h-ver1">H264 STREAM MODEL VER1</option>
        </select>
      </div>
      <div class="inputArea">
        <img src="@/assets/icon/icon_home.png">
        <input type="text" v-model="serial" id="inputShorthand" placeholder="ID" maxlength="20">
      </div>
      <div class="inputArea">
        <img src="@/assets/icon/icon_home.png">
        <input type="text" v-model="deviceIp" id="inputDeviceIp" placeholder="IP - EX) 192.168.0.1" maxlength="15">
      </div>

      <div :style="{display : state.alertDisplay}">
        <h3  id="alertMessage"></h3>
      </div>
      <button id="inputBtn" v-on:click="projectInsert()">추가하기</button>

      <h2>©liio Corp. All rights reserved.</h2>

    </div>
  </section>
</template>

<script>
/*eslint-disable*/

import {watch, ref, reactive} from 'vue'
import {baseURL} from "@/utils/BasicAxiosURL.ts"
import axios from "axios";
import Swal from 'sweetalert2/dist/sweetalert2.js'
import router from "@/routes/routes.js"

const storage = window.sessionStorage;

const ai = axios.create({
  baseURL
});


let event1;

export default {

  setup(){
    const state = reactive({
      alertDisplay : "none"
    })

    const model = ref("");
    const serial = ref("");
    const deviceIp = ref("");


    const alertCloseEvent = () =>{
      state.alertDisplay = "none";
    }

    const projectInsert = () =>{
      clearTimeout(event1);
      if(model.value==''){
        document.getElementById("inputModel").focus();
        document.getElementById("alertMessage").innerHTML = "<span style='font-weight: bold;'>모델</span>을 선택해주세요.";
        state.alertDisplay = "block";
        event1 = setTimeout(alertCloseEvent,3000);
        return false;
      }
      if(serial.value==''){
        document.getElementById("inputShorthand").focus();
        document.getElementById("alertMessage").innerHTML = "아이디를 설정해주세요.";
        state.alertDisplay = "block";
        event1 = setTimeout(alertCloseEvent,3000);
        return false;
      }
      if(deviceIp.value==''){
        document.getElementById("inputDeviceIp").focus();
        document.getElementById("alertMessage").innerHTML = "IP번호를 입력해주세요.";
        state.alertDisplay = "block";
        event1 = setTimeout(alertCloseEvent,3000);
        return false;
      }
      const reg = /^(?!.*\.$)((?!0\d)(1?\d?\d|25[0-5]|2[0-4]\d)(\.|$)){4}$/g;
      if(!reg.test(deviceIp.value)){
        clearTimeout(event1);
        document.getElementById("alertMessage").innerHTML = "형식이 잘못 되었습니다.";
        state.alertDisplay = "block";
        event1 = setTimeout(alertCloseEvent,3000);
        return false;
      }

      ai.post("/data/device", {
        serial : serial.value,
        model : model.value,
        ip : deviceIp.value,
        owner : storage.getItem("cms_userid"),
        company : storage.getItem("cms_company")
      }
    ).then(res => {
        if(res.status === 201){
          router.go(0);
        }else{
          alert("오류")
        }
      }).catch((e) =>{
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

    watch(serial, ()=>{
      const reg = /[\{\}\[\]\/?,;:|\)*~`!^\+<>\#$%&\\\=\(\'\"]/gi;
      if(reg.test(serial.value)){
        clearTimeout(event1);
        document.getElementById("alertMessage").innerHTML = "일부 특수문자는 입력이 불가능합니다.";
        state.alertDisplay = "block";
        event1 = setTimeout(alertCloseEvent,3000);
        return serial.value = serial.value.slice(0,-1);
      }
    })

    return {
      state,
      model,
      serial,
      deviceIp,
      projectInsert
    }
  }
}
</script>

<style lang="scss" scoped>

@import "@/styles/_mixins.scss";
@import "@/styles/_variables.scss";

  #deviceInsertArea{
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
      padding-left : 10px;
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
