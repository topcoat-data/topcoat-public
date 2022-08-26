<template>
    <div class="trendArrow">
        <arrow-up-icon v-if="arrowDirection === 'up'" :size="iconSize" />
        <minus-icon v-else-if="arrowDirection === 'neutral'" :size="iconSize" />
        <arrow-down-icon v-else-if="arrowDirection === 'down'" :size="iconSize" />
    </div>
</template>

<script>
export default {
  name: "TTrendArrow",
  props: {
    direction:{
      type: [Number, String],
      required: true,
      validator: function (value) {
        // The value must match one of these strings
        if(typeof value === "String"){
          return ['up', 'down', 'neutral'].includes(value)
        }
        // Note: if it isn't a string or number vue will already print a warning
        return true;
      }
    },
    iconSize:{
      type: String,
      default: '20'
    }
  },
  data: () => ({}),
  computed:{
      arrowDirection(){
        if(typeof this.direction === "String"){
          return this.direction
        }
        if(this.direction > 0){
          return 'up'
        }
        if(this.direction === 0){
          return 'neutral'
        }
        if(this.direction < 0){
          return 'down'
        }
      },
  },
};
</script>

<style scoped>
    .trendArrow{
        color: #727184;
    }
</style>