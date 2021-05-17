<template>
  <div id="adminInsertArea">
    <h1>회원추가</h1>

    <div class="inputArea">
      <img src="@/assets/icon/icon_home.png">
      <input type="text" v-model="adminName" id="inputName" placeholder="이름" maxlength="10" >
    </div>
    <div class="inputArea">
      <img src="@/assets/icon/icon_home.png">
      <input type="text" v-model="adminID" id="inputID" placeholder="아이디" maxlength="40">
    </div>
    <div class="inputArea">
      <img src="@/assets/icon/icon_home.png">
      <input type="password" v-model="adminPass" id="inputPass" placeholder="비밀번호" maxlength="20">
    </div>

    <div class="inputArea">
      <img src="@/assets/icon/icon_home.png">
      <input type="text" v-model="adminBelong" id="inputBelong" placeholder="소속" maxlength="30">
    </div>

    <div :style="{display : state.alertDisplay}">
      <h3  id="alertMessage"></h3>
    </div>
    <button id="inputBtn" v-on:click="adminInsert()">추가하기</button>

    <h2>©illo Corp. All rights reserved.</h2>

  </div>
</template>
<script>
/*eslint-disable*/

import {watch, ref, reactive} from 'vue'
import {baseURL} from "@/utils/BasicAxiosURL.ts"
import axios from "axios";
import Vue from 'vue'
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

    const adminName = ref("");
    const adminID = ref("");
    const adminPass = ref("");
    const adminBelong = ref("");


    const alertCloseEvent = () =>{
      state.alertDisplay = "none";
    }

    const adminInsert = () =>{
      clearTimeout(event1);
      if(adminName.value==''){
        document.getElementById("inputName").focus();
        document.getElementById("alertMessage").innerHTML = "<span style='font-weight: bold;'>이름</span>이 비어있습니다";
        state.alertDisplay = "block";
        event1 = setTimeout(alertCloseEvent,3000);
        return false;
      }
      if(adminID.value==''){
        document.getElementById("inputID").focus();
        document.getElementById("alertMessage").innerHTML = "아이디가 비어있습니다";
        state.alertDisplay = "block";
        event1 = setTimeout(alertCloseEvent,3000);
        return false;
      }
      if(adminPass.value==''){
        document.getElementById("inputPass").focus();
        document.getElementById("alertMessage").innerHTML = "비밀번호가 비어있습니다";
        state.alertDisplay = "block";
        event1 = setTimeout(alertCloseEvent,3000);
        return false;
      }
/*
      const reg = /^.*(?=.{8,10})(?=.*[a-zA-Z])(?=.*?[A-Z])(?=.*\d)(?=.+?[\W|_])[a-zA-Z0-9!@#$%^&*()-_+={}\|\\\/]+$/g;
      if(!reg.test(this.adminPass)){
        document.getElementById("alertMessage").innerHTML = "대문자,소문자,숫자,특수문자 포함하여 8글자 이상이여야 합니다.";
        this.alertDisplay = true;
        event1 = setTimeout(this.alertCloseEvent,3000);
        return false;
      }
*/
      if(adminBelong.value==''){
        document.getElementById("inputBelong").focus();
        document.getElementById("alertMessage").innerHTML = "소속이 비어있습니다";
        state.alertDisplay = "block";
        event1 = setTimeout(alertCloseEvent,3000);
        return false;
      }
      //db insert

      ai.post("/data/user", {
        userid : adminID.value,
        password : adminPass.value,
        username : adminName.value,
        company : adminBelong.value
      },
      {
        headers: {
          "Authorization": 'Bearer '+storage.getItem("access_token")
        }
      }
    ).then(res => {
        if(res.status === 201){
          Swal.fire({
              toast: true,
              position: 'top',
              icon: 'success',
              title: '회원가입 성공',
              showConfirmButton: false,
              timer: 3000
             })
          router.push('/mainPage/dashBoard');
        }else{
          alert("오류")
        }
      }).catch((e) =>{
        if(e.response.status === 409){
          Swal.fire({
            toast: true,
            position: 'top',
            icon: 'error',
            title: '아이디 중복',
            showConfirmButton: false,
            timer: 3000
          })
        }else{
          Swal.fire({
            toast: true,
            position: 'top',
            icon: 'error',
            title: '회원가입 실패2',
            showConfirmButton: false,
            timer: 3000
          })
        }
        //console.log("err : ",e)
      })

    }

    watch(adminName, ()=>{
      const reg = /[\{\}\[\]\/?,;:|\)*~`!^\-_+<>\#$%&\\\=\(\'\"]/gi;
      if(reg.test(adminName.value)){
      alert('22');
        clearTimeout(event1);
        document.getElementById("alertMessage").innerHTML = "특수문자는 입력이 불가능합니다.";
        state.alertDisplay = "block";
        event1 = setTimeout(alertCloseEvent,3000);
        return adminName.value = adminName.value.slice(0,-1);
      }
    })
    watch(adminID, ()=>{
      const reg = /[\{\}\[\]\/?,;:|\)*~`!^\-_+<>\#$%&\\\=\(\'\"]/gi;
      if(reg.test(adminID.value)){
        clearTimeout(event1);
        document.getElementById("alertMessage").innerHTML = "특수문자는 입력이 불가능합니다.";
        state.alertDisplay = "block";
        event1 = setTimeout(alertCloseEvent,3000);
        return adminID.value = adminID.value.slice(0,-1);
      }
    })
    watch(adminBelong, ()=>{
      const reg = /[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]/gi;
      if(reg.test(adminBelong.value)){
        clearTimeout(event1);
        document.getElementById("alertMessage").innerHTML = "특수문자는 입력이 불가능합니다.";
        state.alertDisplay = "block";
        event1 = setTimeout(alertCloseEvent,3000);
        return adminBelong.value = adminBelong.value.slice(0,-1);
      }
    })

    return {
      state,
      adminName,
      adminID,
      adminBelong,
      adminPass,
      adminInsert
    }
  }
}
</script>

<style lang="scss" scoped>

@import "@/styles/_mixins.scss";
@import "@/styles/_variables.scss";

#adminInsertArea{
  overflow: hidden;
  width: 100%;
  max-width: 500px;
  margin: 0 auto;
  margin-top: 30px;
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
