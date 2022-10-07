<template>
  <div class="relative w-max">
    <base-loading-spinner v-if="loading" />
    <base-checkbox-switch
      v-else
      v-bind="props"
      v-model="value"
      @toggled="toggled"
    />
  </div>
</template>

<script>
export default {
  computed: {
    props() {
      return this.$attrs;
    },
  },
  data: () => ({
    is_filter: true,
    value: false,
  }),
  methods: {
    onVisualizationInit() {
      const initial_value = this.getFilterValue("checkbox");
      this.value = initial_value === "true";
      this.setFilterValue("checkbox", this.value, true);
    },
    onFiltersUpdated() {
      this.onVisualizationInit;
    },
    toggled(value) {
      this.value = value;
      this.setFilterValue("checkbox", this.value, true);
    },
  },
};
</script>
