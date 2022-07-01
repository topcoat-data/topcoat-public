<template>
  <div class="centerCheckOrX">
    <span :class="value ? 'text-[#2D9283]' : 'text-[#ba1515]'" class="mr-[6px]">
      <i :class="value ? 'fa-check-circle' : 'fa-times-circle'" class="fas"></i>
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