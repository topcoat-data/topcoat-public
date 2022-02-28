<script>
export default {
  name: "TColumnConfig",
  props: {
    columnConfig: {
      type: Array,
      default() {
        return {};
      },
    },
    setColumnConfig: {
      type: Function,
    },
  },
  created() {
    if (typeof this.setColumnConfig === "function") {
      this.setColumnConfig(this.columnConfig);
    }
  },
};
</script>