<template>
  <div class="flex w-full" :class="!isVertical && 'flex-col'">
    <div
      class="flex items-center gap-2 bg-[#F9F8FA] px-6"
      :class="isVertical && 'flex-col'"
    >
      <div
        v-for="tab in tabs"
        :key="tab"
        class="cursor-pointer border-t-4"
        :class="
          activeTab === tab.slot
            ? 'bg-white border-[#145DEB]'
            : 'border-transparent'
        "
        @click="switchTab(tab)"
      >
        <slot :name="['tab_' + tab.slot]" :tab="tab">
          {{ tab.label }}
        </slot>
      </div>
    </div>
    <slot v-if="activeTab" :name="activeTab"></slot>
  </div>
</template>

<script>
export default {
  props: {
    tabs: {
      type: Array,
      default: () => [],
    },
    isVertical: {
      type: Boolean,
      default: false,
    },
  },
  data: () => ({
    activeTab: null,
    is_filter: true,
  }),
  methods: {
    switchTab(tab) {
      this.activeTab = tab.slot;
      this.setFilterValue("tab", tab.slot);
    },
    onVisualizationInit() {
      let value = this.getFilterValue("tab");
      value = value && value !== "undefined" ? value : this.tabs[0].slot;
      this.activeTab = value;
    },
  },
};
</script>
