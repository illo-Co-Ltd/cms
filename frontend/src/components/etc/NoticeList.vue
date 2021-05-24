<template>
  <section>
    <div id="deviceUpdateArea">
      <h1>NOTICE</h1>

      <div id="deviceScroll">
        <h2>1. 경찰소는 112 입니다.</h2>
        <h2>2. 소방소는 119 입니다.</h2>
        <h2>3. 해병대 모집번호 02-820-4652 입니다.</h2>
        <h2>4. 재입대 문의 1588-9090</h2>
        <h2>5. 무료봉사 문의 1588-9090</h2>
      </div>
    </div>
  </section>
</template>

<script>
import {reactive} from 'vue'
import {onMounted} from 'vue'


export default {
  setup(){
    const state = reactive({

    });
    onMounted(()=>{


    })




    return {
      state
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
  }

  h1{
    font-size: 25px;
    font-weight: bold;
    margin: 30px 0px;
    text-align: center;
  }
  h2{
    line-height: 25px;
    margin-left: 7px;
  }
  #deviceScroll{
    height: 400px;
    border: 1px solid #999;
    overflow-y:auto;
    @include border-radius(10px);
    margin: 0 10px;
    >h2:nth-child(1){
      margin-top: 7px;
    }
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


</style>
