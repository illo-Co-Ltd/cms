<template>
  <div>
    <modal :show.sync="$store.state.modals.cDevice"
           size="sm">
      <card type="secondary"
            header-classes="bg-transparent pb-5"
            body-classes="px-lg-5 py-lg-5"
            class="border-0 mb-0">
        <template>
          <div>
            <div class="text-muted text-left mt-2 mb-3">
              <h3>New Device</h3>
            </div>
          </div>
          <div role="form">
            <div class="text-center text-muted mb-4">
              <small v-if="!this.emptyValue">Input project's information</small>
              <h4 class="red-text" v-if="this.emptyValue">please input all elements</h4>
            </div>
            <base-input label="model"
                        v-model="model"
                        placeholder="model">
            </base-input>
            <base-input label="serial number"
                        v-model="serial"
                        placeholder="serial number">
            </base-input>
            <base-input label="ip"
                        v-model="ip"
                        placeholder="ip">
            </base-input>
            <base-input label="select owner">
              <select class="form-control" v-model="owner">
                <option v-for="(item, i) in this.userlist" :key="i">{{item.userid}}</option>
              </select>
            </base-input>
            <base-button type="primary" @click="createDeviceMSG">Create</base-button>
            <base-button type="link" @click="$store.state.modals.cDevice=false">close</base-button>
          </div>
        </template>
      </card>
    </modal>
  </div>
</template>

<script>
import BaseDropdown from '../BaseDropdown.vue'
import axios from 'axios';

export default {
  components: { BaseDropdown },
  data() {
    return {
      userlist: Object,
      model: '',
      serial: '',
      ip: '',
      owner: '',
      company: '',

      emptyValue: false,
    }
  },
  methods: {
    getUserList() {
      axios.get('/server/data/user')
        .then((res) => {
          this.userlist = res.data
          this.owner = this.userlist[0].userid
          this.company = this.userlist[0].company
        })
    },
    itemSelected() {

    },
    createDeviceMSG() {
      const model = this.model
      const serial = this.serial
      const ip = this.ip
      const owner = this.owner
      const company = this.company

      if(!model || !serial || !ip || !owner) {
        this.emptyValue = true
        return
      }

      this.$store.dispatch("createDevice", {model, serial, company, owner, ip})
      this.$store.state.modals.cDevice=false
    },
  },
  mounted() {
    this.getUserList()
  }
}
</script>
<style scoped>
.red-text{
  color:red;
}
</style>