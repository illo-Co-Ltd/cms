<template>
<div class="aic-parent">
  <div class="aic-div1">
    <base-button @click="modals.newProject=true">New Project</base-button>
  </div>
  <div class="aic-div2">
    <base-button @click="modals.newTarget=true">New Target</base-button>
  </div>

  <modal :show.sync="modals.newProject"
         size="sm">
    <card type="secondary"
          header-classes="bg-transparent pb-5"
          body-classes="px-lg-5 py-lg-5"
          class="border-0 mb-0">
      <template>
        <div>
          <div class="text-muted text-left mt-2 mb-3">
            <h3>New Project</h3>
          </div>
          <b-form role="form">
            <div class="text-center text-muted mb-4">
              <small>Input project's information</small>
            </div>
            <base-input v-model="projectModal.name"
                        class="mb-3"
                        placeholder="Name">
            </base-input>
            <base-input v-model="projectModal.shorthand"
                        placeholder="Short hand">
            </base-input>
            <base-input v-model="projectModal.description"
                        placeholder="Description">
            </base-input>
            <base-button type="primary" @click="createProject">Create</base-button>
            <base-button type="link" @click="modals.newProject=false">close</base-button>
          </b-form>
        </div>
      </template>
    </card>
  </modal>

  <modal :show.sync="modals.newTarget"
         size="sm">
    <card type="secondary"
          header-classes="bg-transparent pb-5"
          body-classes="px-lg-5 py-lg-5"
          class="border-0 mb-0">
      <template>
        <div>
          <div class="text-muted text-left mt-2 mb-3">
            <h3>New Target</h3>
          </div>
          <b-form role="form">
            <div class="text-center text-muted mb-4">
              <small>Input target's information</small>
            </div>
            <base-input v-model="targetModal.name"
                        class="mb-3"
                        placeholder="Name">
            </base-input>
            <base-input v-model="targetModal.type"
                        placeholder="Type">
            </base-input>
            <base-input v-model="targetModal.detail"
                        placeholder="Detail">
            </base-input>
            <base-input v-model="targetModal.description"
                        placeholder="Description">
            </base-input>
            <base-button type="primary" @click="createTarget">Create</base-button>
            <base-button type="link" @click="modals.newTarget=false">close</base-button>
          </b-form>
        </div>
      </template>
    </card>
  </modal>
</div>
</template>
<script>
import BaseButton from './BaseButton.vue'
import axios from 'axios';

export default {
  components: { BaseButton },
  name: 'AddItemControl',
  data() {
    return {
      modals: {
        newProject: false,
        newTarget: false,
      },
      projectModal: {
        name: '',
        shorthand: '',
        description: '',
      },
      targetModal: {
        project: '',
        name: '',
        type: '',
        detail: '',
        description: '',
      },
    }
  },
  props: {
    node: String,
  },
  methods: {
    createProject: function() {
      axios.post('server/api/project', this.projectModal)
      .then((response) => {
        this.$parent.fetchStructures();
        console.log(response);
      }).catch((e) => {
        console.log("err:",e)
      })
      this.newProject = false;
    },
    createTarget: function () {
      this.targetModal.project = this.node;
      axios.post('server/api/target', this.targetModal)
      .then((response) => {
        this.$parent.fetchStructures();
        console.log(response);
      }).catch((e) => {
        console.log("err:",e)
      })
      this.newTarget = false;
    }
  }
}
</script>
<style scoped>
.aic-parent {
  display: grid;
  grid-template-columns: 1fr;
  grid-template-rows: repeat(2, 1fr);
  grid-column-gap: 0px;
  grid-row-gap: 0px;
  text-align: center;
  padding-top: 15px;
  padding-bottom: 15px;
  border-bottom: 2px solid rgb(241, 241, 241);
}

.aic-div1 { 
  grid-area: 1 / 1 / 2 / 2;
  margin-bottom: 10px;
}
.aic-div2 { grid-area: 2 / 1 / 3 / 2; }
</style>