<template>
    <div class="trendArrow">
        <arrow-up-icon v-if="direction >0" :size="size" />
        <minus-icon v-else-if="direction === 0" :size="size" />
        <arrow-down-icon v-else-if="direction < 0" :size="size" />
    </div>
</template>

<script>
export default {
  name: "TTrendArrow",
  props: {
    direction:{
      type: Number,
      required: true,
    },
    size:{
      type: Number,
      default: 20,
      validator: function(value) {
        return value > 0
      }
    }
  },
};
</script>

<style scoped>
    .trendArrow{
        color: #727184;
    }
</style>

