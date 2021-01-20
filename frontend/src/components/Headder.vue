<template>
  <div class="headder-parent">
    <div class="d-flex justify-content-end mb-3">
      <div class="p-2">
        <base-button>Login</base-button>
      </div>
      <div class="p-2">
        <base-button>Register</base-button>
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
  box-shadow: 1px 2px rgb(241, 241, 241)
}
</style>