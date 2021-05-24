<template>
    <section>
      <div id = "focusArea" class = "test">
        <div class="displayControlTogleBtnArea">
            <h3 class = "btnText">초점</h3>
            <img src="@/assets/icon/icon_home.png" v-on:click="DisplayTogleEvent('focusArea')"> <!-- 토글 버튼 -->
        </div>
        <div class="displayControlTogleMainArea">
          <input class = "rangeInput" id="focusValue" type="range" name="points" min="0" max="255" step="0" value="0" v-on:input="RangeValueInputEvent('focusArea'),FocusInsert()">
          <div class="rangeValue">0</div>
          
          <button  id="autoFocusInputBtn" class="InputBtn" v-on:click="AutoFocusInsert()">자동 초점</button>
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

    // Range 값 변경시 값을 출력해주는 이벤트
    const RangeValueInputEvent = (rengeInputId)=>{
      document.getElementById(rengeInputId).getElementsByClassName('rangeValue')[0].innerHTML = document.getElementById(rengeInputId).getElementsByClassName('rangeInput')[0].value;
    };

    // 포커스 조절 메소드
    const FocusInsert = () =>{
      ai.put("/control/focus", {
        serial : props.deviceId,
        value : document.getElementById("focusValue").value,
      }).then(res => {
          console.log(res);
      })
    };

    // 자동 포커스 메소드
    const AutoFocusInsert = () =>{
      ai.put("/control/autofocus", {
        serial : props.deviceId,
      }).then(res => {
          console.log(res);
      })
    };

    return {
      props,                // 시리얼, 프로젝트 명이 들어있는 파라미터
      FocusInsert,          // 포커스 제어 메소드
      AutoFocusInsert,      // 자동 포커스 메소드
      RangeValueInputEvent, // Range 값 출력 이벤트
      DisplayTogleEvent     // 토글 이벤트
    }
  }
}

</script>
<style lang="scss" scoped>
  @import "@/styles/control.scss";
</style>