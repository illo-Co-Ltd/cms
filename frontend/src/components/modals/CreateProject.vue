<template>
  <div>
    <modal :show.sync="$store.state.modals.project"
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
          </div>
          <div role="form">
            <div class="text-center text-muted mb-4">
              <small>Input project's information</small>
            </div>
            <base-input v-model="project.name"
                        placeholder="Name">
            </base-input>
            <base-input v-model="project.shorthand"
                        placeholder="Short hand">
            </base-input>
            <base-input v-model="project.description"
                        placeholder="Description">
            </base-input>
            <base-button type="primary" @click="createProject">Create</base-button>
            <base-button type="link" @click="$store.state.modals.project=false">close</base-button>
          </div>
        </template>
      </card>
    </modal>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return{
      project: {
        name: '',
        shorthand: '',
        description: '',
      }
    };
  },
  methods: {
    createProject() {
      axios.post('server/api/project', this.project)
      .then((response) => {
        console.log(response);
      }).catch((e) => {
        console.log("err:",e)
      })
      this.$store.state.modals.project = false;
    }
  }
}
</script>