<template>
  <div class="trendArrow"
    @mouseover="showTooltip = true"
    @mouseleave="showTooltip = false">
    <arrow-up-icon v-if="direction > 0" :size="size" />
    <minus-icon v-else-if="direction === 0" :size="size" />
    <arrow-down-icon v-else-if="direction < 0" :size="size" />
    <t-tooltip
      v-if="!!tooltip"
      position="bottom"
      :is-open="showTooltip"
    >
        {{ tooltip }}
    </t-tooltip>
  </div>
</template>

<script>
export default {
  name: "TTrendArrow",
  props: {
    direction: {
      type: Number,
      required: true,
    },
    size: {
      type: Number,
      default: 20,
      validator: function (value) {
        return value > 0;
      },
    },
    tooltip: {
        type: String,
    },
  },
  data: () => ({
    showTooltip: false,
  }),
};
</script>

<style scoped>
.trendArrow {
  color: #727184;
}
</style>
