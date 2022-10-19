<template>
  <base-search-input
    v-bind="props"
    v-model="value"
    @change="
      () => {
        props.type && props.type === 'date' && updateUrlParam();
      }
    "
    @enter="updateUrlParam"
    size="small"
    class="base-search-input"
    :class="{ 'base-search-input-rounded': rounded }"
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
  computed: {
    props() {
      return this.$attrs;
    },
  },
  data: () => ({
    is_filter: true,
    value: "",
  }),
  methods: {
    onVisualizationInit() {
      const initial_value = this.getFilterValue("query");
      if (initial_value) {
        // Value from url param.
        this.value = initial_value;
      } else if (this.config.default_value) {
        // Default value from layer
        this.value = this.config.default_value;
        this.setFilterValue("query", this.value, true);
      } else if (this.defaultValue) {
        // Default value from prop
        this.value = this.defaultValue;
        this.setFilterValue("query", this.value, true);
      } else {
        return;
      }
    },
    updateUrlParam() {
      this.setFilterValue("query", this.value, true);
    },
  },
};
</script>

<style>
.base-search-input-rounded .vue--search-input__field {
  @apply !rounded-3xl;
}
</style>
