<template lang="html">
  <footer id="mainFooterArea">
    <div>
      <img src="@/assets/icon/icon_x.png">
      <p>
        Copyright © kr<br>
        DEVELOPER SITE<br>
        운영자 : OOO / 소재지 : OOO
      </p>
      <div>
        <h5>개인정보처리방침 ｜ </h5>
        <h5>이용 약관 ｜ </h5>
        <h5>정책</h5>
        <h6>@ COM</h6>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
}
</script>

<style lang="scss" scoped>

  @import "@/styles/_mixins.scss";
  @import "@/styles/_variables.scss";

  #mainFooterArea{
    height: 180px;
    min-width: 350px;
    background: $footer-background;
    color: white;
    > div{
      font-family: -apple-system, BlinkMacSystemFont,"Malgun Gothic","맑은 고딕",helvetica,"Apple SD Gothic Neo",sans-serif;
      width: 100%;
      margin: 0 auto;
      text-align: center;
      position: relative;
      > p {
        line-height: 20px;
        font-size: 12px;
        padding-top: 10px;
        color: #999;
      }
      >div{
        overflow: hidden;
        padding-top: 13px;
        position: absolute;
        left: 50%;
        margin-left: -130px;
        >h5{
          float: left;
          font-size: 13px;
          color: #999;
          cursor: pointer;
        }
        >h6{
          float: left;
          font-size: 13px;
          padding-left: 15px;
        }
      }

      >img{
        width: 40px;
        margin-top: 20px;
      }
    }
  }


</style>
