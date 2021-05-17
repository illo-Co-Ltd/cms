<template>
  <div>
    <section id="deviceMain">
      <DeviceCreate></DeviceCreate>
      <DeviceDelete></DeviceDelete>
    </section>
  </div>
</template>

<script>
import DeviceCreate from "@/components/device/DeviceCreate.vue"
import DeviceDelete from "@/components/device/DeviceDelete.vue"

export default{
  components : {
    DeviceCreate,
    DeviceDelete
  }
}
</script>

<style lang="scss" scoped>

@import "@/styles/_mixins.scss";
@import "@/styles/_variables.scss";

  #deviceMain{
    margin: 0 auto;
    width: 800px;
    min-height: 600px;
    overflow: hidden;
    > * {
      width: 400px;
      float: left;
    }
  }

</style>
