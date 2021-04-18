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
            <base-input v-model="name"
                        placeholder="Name">
            </base-input>
            <base-input v-model="shorthand"
                        placeholder="Short hand">
            </base-input>
            <base-input v-model="description"
                        placeholder="Description">
            </base-input>
            <base-button type="primary" @click="createProjectMSG">Create</base-button>
            <base-button type="link" @click="$store.state.modals.project=false">close</base-button>
          </div>
        </template>
      </card>
    </modal>
  </div>
</template>

<script>
export default {
  data() {
    return{
      name: '',
      shorthand: '',
      description: '',
      
    };
  },
  methods: {
    createProjectMSG() {
      const name = this.name
      const shorthand = this.shorthand
      const description = this.description

      this.$store.dispatch("createProject", {name, shorthand, description})
      this.$store.state.modals.project=false
      this.$emit('update')
    }
  }
}
</script>