<template>
  <div>
    <modal :show.sync="$store.state.modals.addDevice"
           size="sm">
      <card type="secondary"
            header-classes="bg-transparent pb-5"
            body-classes="px-lg-5 py-lg-5"
            class="border-0 mb-0">
        <template>
          <div>
            Add Device
          </div>
        </template>
      </card>
    </modal>
  </div>
</template>

<script>
export default {
  
}
</script>