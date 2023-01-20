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
  data: () => ({
    is_filter: true,
    value: false,
  }),
  computed: {
    props() {
      return this.$attrs;
    },
  },
  methods: {
    onVisualizationInit() {
      const initial_value = this.getFilterValue("checkbox");
      this.value = initial_value === "true";
      this.setFilterValue("checkbox", this.value);
    },
    toggled(value) {
      this.value = value;
      this.setFilterValue("checkbox", this.value);
    },
  },
};
</script>
