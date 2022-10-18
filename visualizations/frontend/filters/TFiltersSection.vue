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
        v-for="component in visibleComponents"
        :key="component"
        :is="component"
      />
      <t-filters-dropdown :items="items" />
    </div>
  </div>
</template>

<script>
export default {
  data: () => ({
    visibleComponents: [],
  }),
  computed: {
    items() {
      let items = {};
      const visibleComponents = [];
      this.$slots.default.forEach((element, index) => {
        if (element.data && element.componentOptions) {
          const attrs = element.data.attrs || {};
          const label =
            element?.componentOptions?.propsData?.label || attrs["label"];
          const type = attrs["dropdown-section"] || "--";
          let urlParams = [];
          for (let attribute of Object.keys(attrs)) {
            if (attribute.includes("t-filter")) {
              if (this.filters.hasOwnProperty(attrs[attribute])) {
                const componentTag = `${label}${index}`.replace(/\s/g, "");
                window.Vue.component(componentTag, {
                  render: function (c) {
                    return c("div", {}, [element]);
                  },
                });
                visibleComponents.push(componentTag);
                urlParams = [];
                break;
              }
              urlParams.push(attrs[attribute]);
            }
          }

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
      this.visibleComponents = visibleComponents;
      return items;
    },
  },
};
</script>
