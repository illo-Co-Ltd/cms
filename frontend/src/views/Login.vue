<template>
  <div class="col-lg-5 col-md-7 mt-9">
    <div>
      <card clsss="bg-white" shadow>
        <template>
          <div class="text-center text-muted mb-4">
            <h1>Login</h1>
            <small>welcome back</small>
          </div>
          <form role="form">
              <base-input alternative
                          class="mb-3"
                          placeholder="ID"
                          addon-left-icon="ni ni-circle-08">
              </base-input>
              <base-input alternative
                          type="password"
                          placeholder="Password"
                          addon-left-icon="ni ni-lock-circle-open">
              </base-input>
              <div class="text-center">
                  <base-button block type="success" class="my-4">Log In</base-button>
              </div>
          </form>
        </template>   
      </card>
      <div class="row mt-3">
        <div class="col-6">
          <router-link to="/" class="text-light">
            <small class="lic-text-gray">Forgot Password?</small>
          </router-link>
        </div>
        <div class="col-6 text-right">
          <router-link to="/register" class="text-light">
            <small class="lic-text-gray">Create new account</small>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import BaseButton from '../components/BaseButton.vue'

export default {
  components: {
    BaseButton,
  }
}
</script>
<style scoped>
.lic-text-gray{
  color: rgb(170, 170, 170);
}
</style>