<!-- migrated 2023-08-08 -->
<script>
export default {
  name: "TColumnConfig",
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
