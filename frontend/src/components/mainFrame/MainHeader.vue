<template lang="html">
  <div>
    <div id="mainHeaderArea">
      <img src="@/assets/icon/icon_menu.png" v-on:click="menuEvent()">
      <img src="@/assets/icon/icon_x.png">
      <div>
        <img id="weatherImg" src="@/assets/icon/icon_sunny.png">
        <p><span>현재 5℃</span></p>
      </div>
    </div>
    <div id="mainAsideArea" class="box">

      <div id="asideTitle">
        <button v-on:click="moveProjectInsert()">프로젝트 추가</button>
      </div>
      <ul>
        <div class="menuBigTitle">
          <img src="@/assets/icon/icon_home.png">
          <li>PROJECT (2)</li>
          <div class="menuSmallTitle" id="smallTitle">
            <h5>· data</h5>
            <h5>· prediction</h5>
          </div>
        </div>

        <div class="menuBigTitle" v-for="(array, i) in state.arrProject" v-bind:key="`B-${i}`">
          <img src="@/assets/icon/icon_home.png">
          <li>{{array.name}}(3)</li>
          <span>+</span>
        </div>

      </ul>
    </div>


    <div id="mobileMainAsideArea" class="box" v-bind:style="{'-webkit-transform' : state.menuAnimation, 'transform' : state.menuAnimation}">

        <div id="asideHeader">
          <img src="@/assets/icon/icon_x.png" v-on:click="menuEvent()">
        </div>

        <div id="asideTitle">
          <button v-on:click="moveProjectInsert()">프로젝트 추가</button>
        </div>

        <ul>
          <div class="menuBigTitle">
            <img src="@/assets/icon/icon_home.png">
            <li>PROJECT (2)</li>
            <div class="menuSmallTitle" id="smallTitle">
              <h5>· data</h5>
              <h5>· prediction</h5>
            </div>
          </div>

          <div class="menuBigTitle" v-for="(array, i) in state.arrProject" v-bind:key="`B-${i}`">
            <img src="@/assets/icon/icon_home.png">
            <li>{{array.name}}(3)</li>
            <span>+</span>
          </div>

        </ul>
    </div>



  </div>

</template>

<script>
import router from "@/routes/routes.js"
import {onMounted} from 'vue'
import {reactive} from 'vue'
import {baseURL} from "@/utils/BasicAxiosURL.ts"
import axios from "axios"
//const storage = window.sessionStorage;
const ai = axios.create({
  baseURL
});

export default {

  setup(){

    const state = reactive({
        arrProject : new Array(),
        menuAnimation : 'translate(-400px, 0)'
    });

    const menuEvent = () => {
      if(state.menuAnimation=='translate(-400px, 0)'){
        state.menuAnimation='translate(0, 0)';
      }else{
        state.menuAnimation='translate(-400px, 0)';
      }
    }
    router;

    onMounted(()=>{

      ai.get('/data/project').then(res =>{

        for(let i = 0; i < res.data.data.length ; i++){
            let projectData = {};
            projectData.id = res.data.data[i].id;
            projectData.name = res.data.data[i].name;
            projectData.shorthand = res.data.data[i].shorthand;
            projectData.description = res.data.data[i].description;
            state.arrProject.push(projectData);
        }
      });


    })

    const moveProjectInsert = () => {
      state.menuAnimation='translate(-400px, 0)';
      router.push('/mainPage/projectInsert');
    }

    return {
      state,
      menuEvent,
      moveProjectInsert
    }
  }
}
</script>

<style lang="scss" scoped>

@import "@/styles/_mixins.scss";
@import "@/styles/_variables.scss";

  #mainHeaderArea{
    @include length(100%, 65px);
    min-width: 600px;
    position: fixed;
    top: 0px;
    left: 0px;
    z-index: 400;
    overflow: hidden;
    border-bottom: $frame-border;
    background: $header-background;
    box-shadow: 0px 0px 7px 0px rgba(12,13,14,0.15);
    > img:nth-of-type(1){
      display: none;
      @include length(30px, auto);
      margin-top: 10px;
      margin-left: 17px;
      vertical-align: middle;
      float: left;
      cursor: pointer;
    }
    > img:nth-of-type(2){
      @include length(170px, auto);
      margin-top: 9px;
      margin-left: 29px;
      vertical-align: middle;
      float: left;
      cursor: pointer;
    }
    > div{
      @include length(300px, 70px);
      float: right;
      margin-top: 3px;
      margin-right: 30px;
      >#weatherImg{
        float: right;
        @include length(45px, 45px);
        @include border-radius(25px);
        margin-top: 8px;
        cursor: pointer;
      }
      >p{
        float: right;
        cursor: pointer;
        line-height: 60px;
        font-size: 14px;
        > span{
          @include overtext();
          max-width : 110px;
          display:inline-block;
          margin-right: 10px;
        }
      }
    }
  }



  #mainAsideArea{
    //visibility: hidden;
    @include length(199px, 100%);
    @include scroll-hide();
    @include drag-provention();
    overflow: auto;
    position: fixed;
    top: 66px;
    left: 0px;
    z-index: 300;
    background: $aside-background;
    border-right: $frame-border;
    >#asideTitle{
      border: 1px solid #acacac;
      background: #dedede;
      @include border-radius(5px);
      position: relative;
      width: 90%;
      margin: 15px 5%;
      height: 0;
      overflow: hidden;
      padding-bottom: 22.5%;
      >button{
        border: none;
        background: #dedede;
        position: absolute;
        width: 100%;
        height: 100%;
        left: 0;
        top: 0;
      }
    }
    > ul {
      width: 85%;
      max-width : 170px;
      margin-left: 20px;
      >.menuBigTitle{
        overflow: hidden;
        margin: 13px 0px 1px 0px;
        > *{
          float: left;
        }
        > img{
          border: 1px solid #cacaca;
          @include length(25px, 25px);
          @include border-radius(15px);
          cursor: pointer;
        }
        > li{
          font-size: 15px;
          line-height: 30px;
          margin-left: 5px;
          cursor: pointer;
          width: calc(100% - 50px);
          @include overtext();
        }
        > span{
          width: 15px;
          float: right;
          font-weight: bold;
          line-height: 30px;
          cursor: pointer;
        }
        >.menuSmallTitle{
          padding-left: 40px;
          line-height: 16px;
          cursor: pointer;
          text-transform: lowercase;
          >h5{
            padding: 3px 0px;
          }
        }
      }
    }
  }


    #mobileMainAsideArea{
      //visibility: hidden;
      @include length(200px, 100%);
      @include scroll-hide();
      overflow: auto;
      position: fixed;
      left: 0px;
      z-index: 450;
      background: $aside-background;
      border-right: $frame-border;
      display: none;
      box-shadow: 0px 0px 10px 5px rgba(12,13,14,0.15);

      -webkit-transform: translate(0, 0);
      -webkit-transition: -webkit-transform 400ms;
      transform: translate(0, 0);
      transition: transform 400ms;

      > #asideHeader{
        height: 54px;
        border-bottom: $frame-border;
        overflow: hidden;
        >img{
          float: left;
          @include length(30px, auto);
          margin-top: 12px;
          margin-left: 17px;
        }
      }
      >#asideTitle{
        @include length(90%, 50px);
        @include border-radius(5px);
        margin-top: 15px;
        margin-left: calc(5% - 2px);
        border: 1px solid #acacac;
        background: #dedede;
        >button{
          border: none;
          background: #dedede;
          width: 100%;
          height: 100%;
        }
      }
      > ul {
        width: 150px;
        margin-left: 20px;
        >.menuBigTitle{
          overflow: hidden;
          margin: 13px 0px 1px 0px;
          > *{
            float: left;
          }
          > img{
            border: 1px solid #cacaca;
            @include length(25px, 25px);
            @include border-radius(15px);
            cursor: pointer;
          }
          > li{
            font-size: 17px;
            line-height: 35px;
            margin-left: 10px;
            cursor: pointer;
          }
          > span{
            float: right;
            font-weight: bold;
            line-height: 35px;
            cursor: pointer;
          }
          &:last-child{
            margin-bottom: 100px;
          }
          >.menuSmallTitle{
            font-size: 16px;
            padding-left: 40px;
            line-height: 20px;
            cursor: pointer;
            text-transform: lowercase;

            >h5{
              padding: 5px 0px;
            }
          }
        }

      }
    }



  // 1000 이하가 되면 aside 감춤
  @media ( max-width: 1000px ) {

    #mainAsideArea{
      top: 46px;
      @include length(20%, 100%);
      > ul{
        margin-left: 10%;
      }
    }




    #mainHeaderArea{
      @include length(100%, 49px);
      min-width: 350px;
      >img:nth-of-type(2){
        @include length(120px, auto);
        margin-top: 8px;
      }
      > div{
        @include length(165px, 70px);
        float: right;
        margin-top: 3px;
        >#weatherImg{
          @include length(30px, 30px);
          margin-top: 5px;
        }
        >p{
          line-height: 45px;
          > span{
            @include overtext();
            max-width : 120px;
          }
        }
      }
    }
  }
  @media ( max-width: 800px ) {
        #mainAsideArea{
          display: none;
        }

        #mobileMainAsideArea{
          display: inline;
        }


        #mainHeaderArea{
          >img:nth-of-type(1){
            display: inline;
            margin-left: 10px;
          }
          >img:nth-of-type(2){
            margin-left: 10px;
          }
        }
  }

  // 800 이하가 되면 aside 감춤
  @media ( max-width: 600px ) {

    #mainHeaderArea{
      >div{
        margin-right: 15px;
        >p{
          margin-right: 5px;
          >span{
            margin-right: 5px;
          }
        }
      }
    }
  }



</style>
