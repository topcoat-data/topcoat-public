<template>
  <div class="t-input-container">
    <base-input
      v-bind="props"
      v-model="value"
      @change="
        () => {
          props.type && props.type === 'date' && updateUrlParam();
        }
      "
      @keyup.enter="updateUrlParam"
    />
  </div>
</template>

<script>
export default {
  props: {
    defaultValue: {
      type: String,
      default: "",
    },
  },
  data: () => ({
    is_filter: true,
    value: "",
  }),
  computed: {
    props() {
      return this.$attrs;
    },
  },
  methods: {
    onVisualizationInit() {
      const initial_value = this.getFilterValue("query");
      if (initial_value) {
        // Value from url param.
        this.value = initial_value;
      } else if (this.config?.default_value) {
        // Default value from layer
        this.value = this.config.default_value;
        this.setFilterValue("query", this.value, this.defaultValue);
      } else if (this.defaultValue) {
        // Default value from prop
        this.value = this.defaultValue;
        this.setFilterValue("query", this.value, this.defaultValue);
      } else {
        return;
      }
    },
    updateUrlParam() {
      this.setFilterValue("query", this.value, this.defaultValue);
    },
    reset() {
      this.value = this.defaultValue;
      this.updateUrlParam();
    },
  },
};
</script>

<style>
.t-input-container .vue--input__field {
  height: 30px;
}
</style>
