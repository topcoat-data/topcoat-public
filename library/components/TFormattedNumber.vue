<template>
  <div>{{ formattedNumber }}</div>
</template>

<script>
export default {
  props: {
    value: {
      type: Number,
      required: true,
    },
    truncationLimit: {
      type: Number,
      default: 999999,
    },
  },
  computed: {
    formattedNumber() {
      if (this.value > this.truncationLimit) {
        return Intl.NumberFormat("en", { notation: "compact" }).format(
          this.value
        );
      }

      return Intl.NumberFormat("en").format(this.value);
    },
  },
};
</script>
