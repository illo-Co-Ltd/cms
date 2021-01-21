<template>
  <div class="headder-parent">
    <span class="hd-div1 d-flex justify-content-start">
      <span class="p-2">
        <img src="../assets/logo.png"
             class="logo-size"/>
      </span>
      <span class="p-3">Simple Logo</span>
    </span>
    <div class="hd-div3">
      <div class="d-flex justify-content-end">
        <div class="p-2">
          <base-button type="link">Login</base-button>
        </div>
        <div class="p-2">
          <base-button type="link">Register</base-button>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import BaseButton from './BaseButton.vue'
export default {
  components: { BaseButton },
  
}
</script>
<style scoped>
.headder-parent {
  width: 100%;
  height: 100%;
  background-color: rgb(255, 255, 255);
  box-shadow: 1px 2px rgb(241, 241, 241);
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  grid-template-rows: 1fr;
  grid-column-gap: 0px;
  grid-row-gap: 0px;
  padding-left: 15px !important;
}

.hd-div1 { grid-area: 1 / 1 / 2 / 5; }
.hd-div3 { grid-area: 1 / 5 / 2 / 6; }

.logo-size {
  width: auto; height: auto;
  max-width: 40px;
  max-height: 40px;
}
</style>