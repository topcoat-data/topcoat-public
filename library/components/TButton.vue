<template>
  <button class="text-[#145DEB]" @click="$emit('clicked')">{{ text }}</button>
</template>

<script>
export default {
  emits: ['clicked'],
  props: {
    text: {
      type: String,
    },
  },
}
</script>
