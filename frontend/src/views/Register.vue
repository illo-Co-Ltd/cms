<template>
  <div class="col-md-9 col-lg-7 mt-9">
    <card clsss="bg-white" shadow>
      <template>
        <!-- banner -->
        <div class="text-center text-muted mb-4">
          <h1>Register</h1>
          <small>Already have account? </small>
          <router-link to="/" class="text-light">
            <small>Login</small>
          </router-link>
        </div><hr>
        <!-- Information -->
        <div class="form-group row">
          <label class="col-md-3 col-form-label form-control-label">ID</label>
          <base-input class="col-md-8"></base-input>
        </div>
        <div class="form-group row">
          <label class="col-md-3 col-form-label form-control-label">Password</label>
          <base-input type="password" class="col-md-8"></base-input>
        </div>
        <div class="form-group row">
          <label class="col-md-3 col-form-label form-control-label">Password Check</label>
          <base-input type="password" class="col-md-8"></base-input>
        </div><hr>
        <div class="form-group row">
          <label class="col-md-3 col-form-label form-control-label">User Name</label>
          <base-input class="col-md-8"></base-input>
        </div>
        <div class="form-group row">
          <label class="col-md-3 col-form-label form-control-label">Company</label>
          <base-input class="col-md-8"></base-input>
        </div>
        <div class="form-group row">
          <label class="col-md-3 col-form-label form-control-label">Address</label>
          <base-input class="col-md-8"></base-input>
        </div>
      </template>   
    </card>
    <div class="mt-4">
      <base-button class="py-3" block type="primary">Join</base-button>
    </div>
    <div class="mt-2 text-center">
      <small class="r-text-gray">
        By joining, you agree to the Terms and Privacy Policy.
      </small>
    </div>
  </div>
</template>
<script>
import BaseButton from '../components/BaseButton.vue'

export default {
  components: {
    BaseButton
  }
}
</script>
<style>
.form-group{
  margin-bottom: .8rem;
}
.r-text-gray{
  color: rgb(170, 170, 170);
}
</style>
