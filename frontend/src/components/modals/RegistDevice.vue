<template>
  <div>
    <modal :show.sync="$store.state.modals.rDevice"
           size="sm">
      <card type="secondary"
            header-classes="bg-transparent pb-5"
            body-classes="px-lg-5 py-lg-5"
            class="border-0 mb-0">
        <template>
          <div>
            <div class="text-muted text-left mt-2 mb-3">
              <h3>Regist Device</h3>
            </div>
          </div>
          <div role="form">
            <div class="text-center text-muted mb-4">
              <small>regist device on project</small>
            </div>
            <base-input label="select device">
              <select class="form-control" v-model="this.deviceEntryObj.serial">
                <option v-for="(item, i) in this.deviceEntry" :key="i">{{item.serial}}</option>
              </select>
            </base-input>
            <base-input label="target project">
              <base-input :placeholder=getSelectedProject() disabled alternative></base-input>
            </base-input>
            <base-button type="primary" @click=registDevice>Regist</base-button>
            <base-button type="link" @click="$store.state.modals.rDevice=false">close</base-button>
          </div>
        </template>
      </card>
    </modal>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  components: {  },
  data() {
    return {
      deviceEntry: Object,
      deviceEntryObj: {
        serial: '',
        project: '',
      }
    }
  },
  methods: {
    getDeviceEntry() {
      axios.get('/server/data/device')
      .then((res) => {
        this.deviceEntry = res.data.data
        this.deviceEntryObj.serial = this.deviceEntry[0].serial
      })
    },
    getSelectedProject() {
      this.deviceEntryObj.project = this.$store.state.modals.selectedDevice
      return this.$store.state.modals.selectedDevice
    },
    registDevice() {
      const serial = this.deviceEntryObj.serial
      const project = this.deviceEntryObj.project

      this.$store.dispatch("registDevice", {serial, project})
      this.$emit('update')
    }
  },
  mounted() {
    this.getDeviceEntry()
  }
}
</script>