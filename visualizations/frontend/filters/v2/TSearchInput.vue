<template>
  <base-search-input
    v-bind="props"
    v-model="value"
    size="small"
    class="base-search-input"
    :class="{ 'base-search-input-rounded': rounded }"
    @change="
      () => {
        props.type && props.type === 'date' && updateUrlParam();
      }
    "
    @enter="updateUrlParam"
  />
</template>

<script>
export default {
  props: {
    defaultValue: {
      type: String,
      default: "",
    },
    rounded: {
      type: Boolean,
      default: true,
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
      } else if (this.config.default_value) {
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
  },
};
</script>

<style>
.base-search-input-rounded .vue--search-input__field {
  @apply !rounded-3xl;
}
</style>
