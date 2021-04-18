import axios from 'axios'
import router from '../router'

const state = {
  project: false,
  cDevice: false,
  rDevice: false,
  selectedDevice: '',
}

const actions = {
  createProject({dispatch}, projectObj) {
    axios.post('server/data/project', projectObj)
      .then((res) => {
        console.log(res);
      }).catch((e) => {
        console.log("err:",e)
      })
      // this.project = false;
  },
  createDevice({dispatch}, cDeviceObj) {
    axios.post('server/data/device', cDeviceObj)
      .then((res) => {
        alert("new device model created!!")
      }).catch((e) => {
        console.log("err:",e)
      })
    this.cDevice = false
  },
  registDevice({dispatch}, rDeviceObj) {
    axios.post('server/data/device_entry', rDeviceObj)
      .then((res) => {console.log(res)})
  },
}

export default {
  state,
  actions
}