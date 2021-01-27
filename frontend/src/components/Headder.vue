<template>
  <div class="headder-parent">
    <span class="hd-div1 d-flex justify-content-start">
      <span class="p-2">
        <img src="../assets/logo.png"
             class="logo-size"/>
      </span>
      <span class="p-3">Simple Logo</span>
      <span class="p-2">
        <base-button outline type="default"
                     @click="modals.keyControl=true">Control</base-button>
      </span>
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

    <modal :show.sync="modals.keyControl"
           size="sm">
      <card type="secondary"
          header-classes="bg-transparent pb-5"
          body-classes="px-lg-5 py-lg-5"
          class="border-0 mb-0">
        <template>
          <div class="modal-parent">
            <div class="modal-div1">
              <base-button outline block @click="upPressed">up</base-button>
            </div>
            <div class="modal-div2">
              <base-button outline block @click="downPressed">down</base-button>
            </div>
            <div class="modal-div3">
              <base-button outline block @click="leftPressed">left</base-button>
            </div>
            <div class="modal-div4">
              <base-button outline block @click="rightPressed">right</base-button>
            </div>
          </div>
        </template>
    </card>
  </modal>

  </div>
</template>
<script>
import BaseButton from './BaseButton.vue'
import Card from './Card.vue'
import Modal from './Modal.vue'
import axios from 'axios';

export default {
  components: { BaseButton, Card, Modal },
    data() {
    return {
      modals: {
        keyControl: false,
      },
      key: {
        up: false,
        down: false,
        left: false,
        right: false,
      },
    }
  },
  methods: {
    upPressed(){
      axios.get('server/api/camera/pos_offset?x=0&y=100&z=0')
      .then((response) => {
        console.log(response);
      }).catch((e) => {
        console.log("err:",e)
      })
    },
    downPressed(){
      axios.get('server/api/camera/pos_offset?x=0&y=-100&z=0')
      .then((response) => {
        console.log(response);
      }).catch((e) => {
        console.log("err:",e)
      })
    },
    leftPressed(){
      axios.get('server/api/camera/pos_offset?x=-6000&y=0&z=0')
      .then((response) => {
        console.log(response);
      }).catch((e) => {
        console.log("err:",e)
      })
    },
    rightPressed(){
      axios.get('server/api/camera/pos_offset?x=100&y=0&z=0')
      .then((response) => {
        console.log(response);
      }).catch((e) => {
        console.log("err:",e)
      })
    },
  },
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

.modal-parent {
display: grid;
grid-template-columns: repeat(3, 1fr);
grid-template-rows: repeat(3, 1fr);
grid-column-gap: 0px;
grid-row-gap: 0px;
}

.modal-div1 { grid-area: 1 / 2 / 2 / 3; }
.modal-div2 { grid-area: 3 / 2 / 4 / 3; }
.modal-div3 { grid-area: 2 / 1 / 3 / 2; }
.modal-div4 { grid-area: 2 / 3 / 3 / 4; }

</style>