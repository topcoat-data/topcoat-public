<template>
  <div class="flex flex-col w-full relative">
    <div class="flex items-center gap-2 bg-[#F9F8FA] px-6">
      <div
        v-for="tab in tabs"
        :key="tab"
        class="pb-2 cursor-pointer border-t-4"
        :class="
          activeTab === tab.slot
            ? 'bg-white border-[#145DEB]'
            : 'border-transparent'
        "
        @click="switchTab(tab)"
      >
        <div
          class="p-6 min-w-[240px] border-2 rounded-md border-transparent"
          :class="
            activeTab === tab.slot
              ? 'text-[#1c1c21]'
              : 'hover:border-[#d3d3d980] hover:bg-[#F2F1F4] hover:text-[#1c1c21] text-[#555463]'
          "
        >
          <slot :name="['tab_' + tab.slot]" :tab="tab">
            {{ tab.label }}
          </slot>
        </div>
      </div>
    </div>
    <div :key="activeTab">
      <slot v-if="activeTab" :name="activeTab"></slot>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    tabs: {
      type: Array,
      default: () => [],
    },
  },
  data: () => ({
    activeTab: null,
    is_filter: true,
  }),
  mounted() {
    if (!this.layer && this.tabs.length && !this.activeTab) {
      this.switchTab(this.tabs[0]);
    }
  },
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
