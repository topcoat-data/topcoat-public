<template>
  <div class="centerCheckOrX">
    <span v-if="value" class="text-[#2D9283] mr-[6px]">
      <i class="fas fa-check-circle"> </i>
    </span>
    <span v-else class="text-[#ba1515] mr-[6px]">
      <i class="fas fa-times-circle"> </i>
    </span>
  </div>
</template>
<script>
export default {
  name: "CheckOrX",
  props: {
    value: {
      type: Boolean,
      required: true,
    },
  },
};
</script>

<style scoped>
.centerCheckOrX {
  position: relative;
  top: 4px;
}
</style>