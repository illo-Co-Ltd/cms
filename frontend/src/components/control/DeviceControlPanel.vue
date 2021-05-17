<template>
    <section>
        <!-- 디스플레이 컨트롤 영역 시작-->
        <div class="togleArea" >

            <!-- 상대 좌표 이동 영역 시작 -->
            <div class="displayControlTogleBtnArea" >
                <h3>상대 좌표 이동</h3>
                <img src="@/assets/icon/icon_home.png" v-on:click="DisplayTogleEvent('relativeCoordinates')"> <!-- 토글 버튼 -->
            </div>
            <div id = "relativeCoordinates" class="displayControlTogleMainArea">
                <div class="inputArea">
                    <img src="@/assets/icon/icon_home.png">
                    <input type="text"  id="relativeCoordinatesX" placeholder="x" maxlength="6" >
                </div>
                    <div class="inputArea">
                    <img src="@/assets/icon/icon_home.png">
                    <input type="text" id="relativeCoordinatesY" placeholder="y" maxlength="6">
                </div>
                    <div class="inputArea">
                    <img src="@/assets/icon/icon_home.png">
                    <input type="text"  id="relativeCoordinatesZ" placeholder="z" maxlength="6">
                </div>
                
                <button  id="relativeCoordinatesInputBtn" class="InputBtn" v-on:click="projectInsert()">시작</button>
            </div>
            <!-- 상대 좌표 이동 영역 끝 -->

            <!-- 절대 좌표 이동 영역 시작 -->
            <div class="displayControlTogleBtnArea" >
                <h3>절대 좌표 이동</h3>
                <img src="@/assets/icon/icon_home.png" v-on:click="DisplayTogleEvent('absoluteCoordinates')"> <!-- 토글 버튼 -->
            </div>
            <div id = "absoluteCoordinates" class="displayControlTogleMainArea">
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
                
                <button  id="absoluteCoordinatesInputBtn" class="InputBtn" v-on:click="projectInsert()">시작</button>
            </div>
            <!-- 절대 좌표 이동 영역 끝 -->

        </div>
    </section>
</template>


<script>

export default {
    setup(){
        // 토글 버튼 구현 함수
        // param : 토글 하고자 하는 항목의 id
        const DisplayTogleEvent = (id)=>{
            if(document.getElementById(id).style.display == 'none')
            {
                document.getElementById(id).style.display ='block';
            }
            else
            {
                document.getElementById(id).style.display='none';
            }
         };

         return {
             DisplayTogleEvent
         }
    }
}


</script>

<style lang="scss" scoped>
  .inputArea{
    width: 90%;
    height: 30px;
    margin: 10px 5%;
    outline: 1px solid #aaa;

    font-size: 13px;
    >img{
      width: 30px;
      height: 30px;
      float: left;
    }
    >input{
      width: calc(100% - 52px);
      height: 100%;
      border: none;
      margin: 0px;
      padding: 0px 10px;
      float: left;
    }
  }

  .togleArea{
    width: 100%;
    height: 100vh; // 화면의 100%
    border-left: 1px solid #aaa;

    .displayControlTogleBtnArea{
      width: 100%;
      height: 30px;
      border-bottom: 1px solid #aaa;
      border-top: 1px solid #aaa;
      text-align: center;
      >img{
        width: 30px;
        height: 30px;
        float: right;
        display: inline;
      }
      >h3{
        height: 30px;
        padding-left: 30px;
        color : #aaa;
        line-height:35px;
        display: inline;
      }
    }

    .displayControlTogleMainArea{
      border-bottom: 1px solid #aaa;
    }
  }

    .InputBtn{
    width: 90%;
    height: 30PX;
    margin: 10px 5%;

    color: #fff;
    background: #033E5D;
    border: none;
  }
</style>