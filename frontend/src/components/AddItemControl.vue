<template>
<div class="aic-parent">
  <div class="aic-div1">Project</div>

  <div class="aic-div2">
    <base-button type="primary" size="sm">Add</base-button>
  </div>

  <div class="aic-div3">
    <base-button type="primary" size="sm">Delete</base-button>
  </div>

  <div class="aic-div4">Target</div>

  <div class="aic-div5">
    <base-button type="primary" size="sm">Add</base-button>
  </div>

  <div class="aic-div6">
    <base-button type="primary" size="sm">Delete</base-button>
  </div>
</div>
</template>
<script>
import BaseButton from './BaseButton.vue'
export default {
  components: { BaseButton },
  name: 'AddItemControl',
  props: {
    
  },
}
</script>
<style scoped>
.aic-parent {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(2, 1fr);
  grid-column-gap: 0px;
  grid-row-gap: 0px;
  text-align: center;
  padding-top: 15px;
  padding-bottom: 15px;
  border-bottom: 2px solid rgb(241, 241, 241);;
}

.aic-div1 { 
  grid-area: 1 / 1 / 2 / 2; 
  margin-bottom: 10px;
}
.aic-div2 { grid-area: 1 / 2 / 2 / 3; }
.aic-div3 { grid-area: 1 / 3 / 2 / 4; }
.aic-div4 { grid-area: 2 / 1 / 3 / 2; }
.aic-div5 { grid-area: 2 / 2 / 3 / 3; }
.aic-div6 { grid-area: 2 / 3 / 3 / 4; }
</style>