<template lang="html">
  <section>
    <form @submit.prevent="onSubmit(state.id, state.pass)">
      <input v-model="state.id" type="text" placeholder="아이디" maxlength="20">
      <input v-model="state.pass" type="password" placeholder="비밀번호" maxlength="20">

      <div id="checkbox_area">
        <div id="checkbox_idSave">
          <input type="checkbox" v-model="state.idSave" value="save" id="chk">
          <label for="chk">아이디 저장</label>
        </div>
      </div>

      <h6>안녕하세요 집갈께요.</h6>
      <h6>문의 : 112</h6>
      <input type="submit" value="로그인">
      <input type="button" value="회원가입">
    </form>
  </section>
</template>

<script>

import axios from "axios";
import {reactive} from 'vue'
import router from "@/routes/routes.js"
import {baseURL} from "@/utils/BasicAxiosURL.ts"
import {useRoute} from 'vue-router'
import {onMounted} from 'vue'
import Swal from 'sweetalert2/dist/sweetalert2.js'

const storage = window.sessionStorage;

const ai = axios.create({
  baseURL
});




export default {

  setup () {

    const {
      query : {redirect}
    } = useRoute()

    const state = reactive({
      id: "",
      pass: "",
      idSave : ['save']
    })

    onMounted(()=>{

      //초기화시 쿠키 내용으로 id 값 확인
      if(getCookie('m2_auto_id')==null){
        state.idSave = [];
      }else{
        state.id=getCookie('m2_auto_id');
        state.idSave = ['save'];
      }
    })


    const onSubmit = (id, pass) => {

      storage.setItem("access_token", "");
      storage.setItem("cms_username", "");
      storage.setItem("cms_company", "");
      storage.setItem("cms_userid", "");

      const userid = id;
      const password = pass;

      ai.post("/auth/login?",{userid,password},{withCredentials: true})
      .then(res => {
        if(res.status == 200){
          //storage.setItem("access_token", res.headers["access_token"]);
          storage.setItem("access_token", res.data.access_token);


          ai.get("/auth/whoami").then(res =>{
            storage.setItem("cms_username", res.data.username);
            storage.setItem("cms_company", res.data.company);
            storage.setItem("cms_userid", res.data.userid);
          })


          //쿠키 자동저장 진행한다
          if(state.idSave == 'save'){
            setCookie('m2_auto_id',state.id,2);
          }else{
            deleteCookie('m2_auto_id');
          }

          if(redirect == null){
            router.push('/mainPage/dashBoard');
          }else{
            router.push(redirect)
          }

          Swal.fire({
              toast: true,
              position: 'top',
              icon: 'success',
              title: '로그인 성공',
              showConfirmButton: false,
              timer: 3000
             })
        }

      }).catch(e => {
        e;
        Swal.fire({
          toast: true,
          position: 'top',
          icon: 'error',
          title: '로그인 실패',
          showConfirmButton: false,
          timer: 3000
        })
      });

    }


    const setCookie = (name, value, exp) => {
      let date = new Date();
      date.setTime(date.getTime() + exp*24*60*60*1000);
      document.cookie = name + '=' + value + ';expires=' + date.toUTCString() + ';path=/';
    }

    const deleteCookie = (name) => {
      document.cookie =  name + '=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    }

    const getCookie = (name) => {
      let value = document.cookie.match('(^|;) ?' + name + '=([^;]*)(;|$)');
      return value? value[2] : null;
    }

    return {
      state,
      onSubmit
    }
  }
}
</script>



<style lang="scss" scoped>

  @import "@/styles/_mixins.scss";
  @import "@/styles/_variables.scss";

  section{
    overflow: hidden;
    width: 100%;
    max-width: 500px;
    margin: 0 auto;
    margin-top: 200px;
  }
  section > form > input[type=text], section > form > input[type=password]{
    width: calc(100% - 24px);
    height: 45px;
    margin: 10px 0px;
    padding-left: 10px;
    padding-right: 10px;
    float: left;
    font-size: 15px;

  }
  section > form > input[type=submit], section > form > input[type=button]{
    @include length(100%, 55px);
    margin-top: 10px;
    background: #033E5D;
    border: none;
    color: #fff;
    @include border-radius(5px);
  }

  section > form > input[type=button]{
    background: #366e8e;
  }


  section > form > h6 {
    margin: 4px;
    text-align: center;
    font-size: 13px;
  }

  #checkbox_area{
    float: left;
    width: 100%;
    padding-bottom: 25px;
  }


  #checkbox_idSave{
    padding-top: 5px;
    padding-bottom: 15px;

    @include checkbox(25px);
    border-bottom: $frame-border;
  }

  @media ( max-width: 600px ) {
    section > form > input[type=text], section > form > input[type=password]{
      margin: 7px 0px;
    }

    #checkbox_area{
      padding-bottom: 15px;
    }

    section > form > input[type=submit], section > form > input[type=button]{
      margin-top: 7px;
    }
  }

</style>
