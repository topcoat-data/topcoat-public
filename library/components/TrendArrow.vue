<template>
    <div class="trendArrow">
        <arrow-up-icon v-if="difference > 0" :size="iconSize" />
        <minus-icon v-else-if="difference === 0" :size="iconSize" />
        <arrow-down-icon v-else :size="iconSize" />
    </div>
</template>

<script>
export default {
  name: "TrendArrow",
  props: {
    firstNumber: {
      type: Number,
      required: true,
    },
    secondNumber: {
      type: Number,
      required: true,
    },
    iconSize:{
      type: String,
      default: '20'
    }
  },
  data: () => ({}),
  computed:{
      difference(){
          return this.firstNumber - this.secondNumber
      },
  },
};
</script>

<style scoped>
    .trendArrow{
        color: #727184;
    }
</style>