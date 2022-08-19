<template>
  <TTextButton @click="handleClick">Reset Filters</TTextButton>
</template>

<script>
export default {
  data: () => ({
    is_filter: true
  }),
  methods: {
    handleClick(e) {
      this.unsetAllFilters()
    }
  }
}
</script>
