<template>
  <base-button variant="link" class="text-[#145DEB]" @click="handleClick">TEXT</base-button>
  <h1>urg</h1>
</template>

<script>
export default {
  methods: {
    handleClick(e) {
      console.log('handle the cliiiiick!')
      this.unsetAllFilters()
    }
  }
}
</script>
