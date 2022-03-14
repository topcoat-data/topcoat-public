<script>
export default {
  name: "t-column-config",
  props: {
    columnConfig: {
      type: Array,
      default() {
        return [];
      },
    },
    setColumnConfig: {
      type: Function,
      default: null,
    },
  },
  created() {
    if (typeof this.setColumnConfig === "function") {
      this.setColumnConfig(this.columnConfig);
    }
  },
};
</script>
