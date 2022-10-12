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
      <!-- <t-active-filters> -->
      <slot></slot>
      <!-- </t-active-filters> -->

      <t-filters-dropdown :items="dropdownItems" />
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    dropdownItems() {
      let items = {};

      this.$slots.default.forEach((element) => {
        if (element.data && element.componentOptions) {
          const attrs = element.data.attrs || {};
          const label =
            element?.componentOptions?.propsData?.label || attrs["label"];
          const type = attrs["filter-type"] || "--";
          const urlParams = [];

          for (let attribute of Object.keys(attrs)) {
            if (attribute.includes("t-filter")) {
              if (!this.filters.hasOwnProperty(attrs[attribute])) {
                urlParams.push(attrs[attribute]);
              }
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
      return items;
    },
  },
};
</script>
