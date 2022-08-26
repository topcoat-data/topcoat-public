<template>
    <div class="trendArrow">
        <arrow-up-icon v-if="arrowDirection === 'up'" :size="size" />
        <minus-icon v-else-if="arrowDirection === 'neutral'" :size="size" />
        <arrow-down-icon v-else-if="arrowDirection === 'down'" :size="size" />
    </div>
</template>

<script>
export default {
  name: "TTrendArrow",
  props: {
    direction:{
      type: [Number, String],
      required: true,
      validator(value) {
        if(typeof value === "string"){
          return ['up', 'down', 'neutral'].includes(value)
        }
        // Note: if it isn't a string or number vue will already print a warning
        return true;
      }
    },
    size:{
      type: Number,
      default: 20,
    }
  },
  data: () => ({}),
  computed:{
      arrowDirection(){
        if(typeof this.direction === "string"){
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