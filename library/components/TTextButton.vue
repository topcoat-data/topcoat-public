<template>
  <button class="
    rounded
    text-[#145deb]" v-on="$listeners">
    <slot></slot>
  </button>
</template>
<script>
export default {
  props: {
    text: {
      type: String,
      required: true
    }
  }
}
</script>