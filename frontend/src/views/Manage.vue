<template>
  <div class="p-5">
    <base-input v-model="model"
                placeholder="model">
    </base-input>
    <base-input v-model="serial"
                placeholder="serial number">
    </base-input>
    <base-input v-model="owner"
                placeholder="owner">
    </base-input>
    <base-input v-model="created_by"
                placeholder="creater name">
    </base-input>
    <base-input v-model="edited_by"
                placeholder="editor name">
    </base-input>
    <base-button block type="primary" @click="registDevice">Regist Device</base-button>
  </div>
</template>

<script>
import BaseButton from '../components/BaseButton.vue'
import axios from 'axios';

export default {
  components: { BaseButton },
  data() {
    return{
      model: '',
      serial: '',
      owner: '',
      created_by: '',
      edited_by: ''
    }
  },
  methods: {
    registDevice() {
      const model = this.model;
      const serial = this. serial;
      const owner = this.owner;
      const created_by = this.created_by;
      const edited_by = this.edited_by;

      axios.post('server/api/device', {model, serial, owner, created_by, edited_by})
      .then((response) => {
        console.log(response);
      }).catch((e) => {
        console.log("err:",e)
      })
    }
  }
}
</script>