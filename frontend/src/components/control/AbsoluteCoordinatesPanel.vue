<template>
    <section>
        
        <div id = "absoluteCoordinatesArea">
            <div class="displayControlTogleBtnArea">
                <h3 class = "btnText">절대 좌표 이동</h3>
                <img src="@/assets/icon/icon_home.png" v-on:click="DisplayTogleEvent('absoluteCoordinatesArea')"> <!-- 토글 버튼 -->
            </div>

            <div class="displayControlTogleMainArea">
            <div class="inputArea">
                <img src="@/assets/icon/icon_home.png">
                <input type="text"  id="absoluteCoordinatesX" placeholder="x" maxlength="6" >
            </div>
            <div class="inputArea">
                <img src="@/assets/icon/icon_home.png">
                <input type="text" id="absoluteCoordinatesY" placeholder="y" maxlength="6">
            </div>
            <div class="inputArea">
                <img src="@/assets/icon/icon_home.png">
                <input type="text"  id="absoluteCoordinatesZ" placeholder="z" maxlength="6">
            </div>
            <button  id="absoluteCoordinatesInputBtn" class="InputBtn" v-on:click="AbsoluteCoordinatesInsert()">시작</button>
            </div>
        </div>
    </section>
</template>


<script>


import {baseURL} from "@/utils/BasicAxiosURL.ts"
import axios from "axios";

const ai = axios.create({
  baseURL
});

export default {
  // DeviceControl.vue에서 파라미터(props) 받아오는 부분
  props : ['projectName','deviceId'],
  setup(props){
    ai; 

        // 토글 버튼 이벤트
    // param : 토글 하고자 하는 항목의 id
    const DisplayTogleEvent = (togleAreaId)=>{
      // 토글 버튼이 켜져있는지 판단.
      if(document.getElementById(togleAreaId).getElementsByClassName('displayControlTogleMainArea')[0].style.display == 'none')
      {
        // 활성화
        document.getElementById(togleAreaId).getElementsByClassName('displayControlTogleMainArea')[0].style.display ='block';
        document.getElementById(togleAreaId).getElementsByClassName('displayControlTogleBtnArea')[0].firstChild.style.color = '#033E5D';
      }
      else
      {
        // 비활성화
        document.getElementById(togleAreaId).getElementsByClassName('displayControlTogleMainArea')[0].style.display='none';
        document.getElementById(togleAreaId).getElementsByClassName('displayControlTogleBtnArea')[0].firstChild.style.color = '#AAA';
      }
    };

    // 절대 좌표 이동 메소드
    const AbsoluteCoordinatesInsert = () =>{
       ai.post("/control/pos", {
        serial : props.deviceId,
        x : document.getElementById("absoluteCoordinatesX").value,
        y : document.getElementById("absoluteCoordinatesY").value,
        z : document.getElementById("absoluteCoordinatesZ").value
      }).then(res => {
          console.log(res);
      })
    };

    return {
      props,                      // 시리얼, 프로젝트 명이 들어있는 파라미터
      AbsoluteCoordinatesInsert,  // 절대 좌표 이동 메소드
      DisplayTogleEvent           // 토글 이벤트
    }
  }
}

</script>

<style lang="scss" scoped>
  @import "@/styles/control.scss";
</style>