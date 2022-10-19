<template>
  <div
    class="border-t border-b border-[#D3D3D9] w-full relative p-5 flex flex-col gap-2"
    style="font-family: 'Roboto'"
  >
    <!-- Header -->
    <div class="flex items-center gap-4 text-[#555463]">
      <div class="flex gap-1 hover:text-[#145DEB]">
        <filter-variant-icon :size="18" />
        Filters
      </div>
      <div class="flex gap-1 hover:text-[#145DEB]">
        <reload-icon :size="18" />
        Reset
      </div>
    </div>
    <div class="flex flex-wrap items-center gap-1">
      <component
        v-for="(visible, tag) in filterComponents"
        :key="tag"
        :is="tag"
        v-if="visible"
      />
      <t-filters-dropdown :items="items" />
    </div>
  </div>
</template>

<script>
export default {
  data: () => ({
    filterComponents: {},
  }),
  computed: {
    items() {
      let items = {};
      if (this.$slots.default) {
        this.$slots.default.forEach((element, index) => {
          if (element.data && element.componentOptions) {
            const attrs = element.data.attrs || {};
            const label =
              element?.componentOptions?.propsData?.label || attrs["label"];
            const type = attrs["dropdown-section"] || "Ungrouped";

            // Check active url filters
            let urlParams = [];
            let visible = false;
            for (let attribute of Object.keys(attrs)) {
              if (attribute.includes("t-filter")) {
                if (this.filters.hasOwnProperty(attrs[attribute])) {
                  urlParams = [];
                  visible = true;
                  break;
                }
                urlParams.push(attrs[attribute]);
              }
            }

            // Create component instance
            const componentTag = `${label}${index}`.replace(/\s/g, "");
            if (!this.filterComponents.hasOwnProperty(componentTag)) {
              window.Vue.component(componentTag, {
                render: function (c) {
                  return c("div", {}, [element]);
                },
              });
            }
            // Handle visibility state
            // If filter is used as url param, show the filter in active section.
            this.$set(this.filterComponents, componentTag, visible);

            // If filter is not used as url param, show in dropdown.
            if (urlParams.length) {
              if (items[type]) {
                items[type].items = [
                  ...items[type].items,
                  { label, filters: urlParams },
                ];
              } else {
                items[type] = {
                  label: type,
                  items: [{ label, filters: urlParams }],
                };
              }
            }
          }
        });
      }
      return items;
    },
  },
};
</script>
