<template>
  <span>
    {{ formattedDate }}
  </span>
</template>

<script>
export default {
  name: "DateFormatter",
  props: {
    date: {
      type: [String, Date],
      required: true,
    },
    formatOptions: {
      type: Object,
      default() {
        return { dateStyle: "medium" };
      },
    },
  },
  computed: {
    formattedDate() {
      let d;
      if (typeof this.date === "string") {
        d = new Date(this.date);
      } else if (this.date instanceof Date) {
        d = this.date;
      }
      if (!d) return "";

      // undefined tells the date to use the local timezone/locale
      return d.toLocaleDateString(undefined, this.formatOptions);
    },
  },
};
</script>

<style scoped></style>
