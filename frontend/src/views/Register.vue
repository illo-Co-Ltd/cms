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
          <base-input v-model="userid" class="col-md-8"></base-input>
        </div>
        <div class="form-group row">
          <label class="col-md-3 col-form-label form-control-label">Password</label>
          <base-input v-model="password" type="password" class="col-md-8"></base-input>
        </div>
        <div class="form-group row">
          <label class="col-md-3 col-form-label form-control-label">Password Check</label>
            <base-input v-model="passwordCheck" type="password" class="col-md-8"></base-input>
        </div>
        <div class="password-msg" v-if="matchPassword()">password is not match</div><hr>
        <div class="form-group row">
          <label class="col-md-3 col-form-label form-control-label">User Name</label>
          <base-input v-model="username" class="col-md-8"></base-input>
        </div>
        <div class="form-group row">
          <label class="col-md-3 col-form-label form-control-label">Company</label>
          <base-input v-model="company" class="col-md-8"></base-input>
        </div>
      </template>   
    </card>
    <div class="mt-4">
      <base-button class="py-3" block type="primary"
                   @click="registUser">Join</base-button>
    </div>
    <div class="mt-2 text-center">
      <small class="r-text-gray">
        By joining, you agree to the Terms and Privacy Policy.
      </small>
    </div>
  </div>
</template>
<script>
import axios from 'axios';
import BaseButton from '../components/BaseButton.vue'

export default {
  components: {
    BaseButton
  },
  data() {
    return {
      userid: '',
      password: '',
      passwordCheck: '',
      username: '',
      company: '',

      unmatch_password: false,
      match_password_msg: '',
    }
  },
  methods: {
    matchPassword() {
      if(!this.password || !this.passwordCheck) return false;
      if(this.password != this.passwordCheck) return true
      else return false;
    },
    registUser() {
      const userid = this.userid;
      const password = this.password;
      const username = this.username;
      const company = this.company;

      if(this.matchPassword()) return false;

      if (!userid || !password || !username || !company) {
        return false;
      }

      this.$store.dispatch("register", {userid, password, username, company})

    }
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
.password-msg{
  text-align: center;
  color: rgb(255, 0, 0);
}
</style>
