<template>
  <button @click="handleClick">{{ text }}</button>
</template>

<script>
export default {
  props: {
    text: {
      type: String,
      default: 'Reset all Filters'
    },
  },
  methods: {
    handleClick(e) {
      this.unsetAllFilters()
    }
  }
}
</script>
