<template>
  <div class="relative flex w-full gap-2 p-5" style="font-family: 'Roboto'">
    <filter-variant-icon class="relative top-[5px]" :size="18" />
    <div class="flex flex-col items-start justify-start gap-2">
      <div class="flex flex-wrap items-center gap-1">
        <slot name="defaultFilter"></slot>
        <component
          :is="tag"
          v-for="(data, tag) in visibleFilters"
          :key="tag"
          :ref="tag"
        >
          <div class="flex items-center justify-end cursor-pointer">
            <t-tooltip position="right" width="100px">
              <div
                slot="trigger"
                class="w-[34px] h-[32px] border border-[#B3B2BD] hover:border-[#555463] rounded flex items-center justify-center"
                @click="removeFilter(data.filters)"
              >
                <!-- Limitation: Using icon component as <delete-icon /> does not work with $slots manipulation -->
                <!-- Svg of icon is used directly -->
                <svg
                  width="16"
                  height="16"
                  viewBox="0 0 16 16"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    d="M10.6667 6V12.6667H5.33337V6H10.6667ZM9.66671 2H6.33337L5.66671 2.66667H3.33337V4H12.6667V2.66667H10.3334L9.66671 2ZM12 4.66667H4.00004V12.6667C4.00004 13.4 4.60004 14 5.33337 14H10.6667C11.4 14 12 13.4 12 12.6667V4.66667Z"
                    fill="#555463"
                  />
                </svg>
              </div>
              Remove filter
            </t-tooltip>
          </div>
        </component>
        <t-filters-dropdown :items="menuItems" @opened="handleFilterOpen" />


        <div class="flex gap-1 text-[#145DEB] cursor-pointer" @click="resetAllFilters">
            <backup-restore-icon :size="18" />
            Reset all filters
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "TFiltersSection",
  data: () => ({
    initialisedComponents: [],
    menuItems: [],
    visibleFilters: {},
    lastAddedFilter: null,
    selectedFilters: {},
  }),
  computed: {
    slotItems() {
      return this.$slots.default || [];
    },
  },
  mounted() {
    this.selectedFilters = this.filters;
    this.handleItems();
  },
  methods: {
    handleItems() {
      this.handleMenuItems();
      this.handleVisibleFilters();
    },
    handleMenuItems() {
      let items = {};
      this.slotItems.forEach((element, index) => {
        if (element.data && element.componentOptions) {
          const attrs = element.data.attrs || {};
          const props = element?.componentOptions?.propsData;
          const label =
            attrs["item-label"] || attrs["itemLabel"] || props.label;
          const type =
            attrs["dropdown-section"] ||
            attrs["dropdownSection"] ||
            "UNGROUPED";
          const unusedFilters = this.getFilters(attrs, true);

          const tag = `${element.tag}${index}`;
          if (unusedFilters.length) {
            let itemObject = { label, filters: unusedFilters, tag };
            if (items[type]) {
              items[type].items = [...items[type].items, itemObject];
            } else {
              items[type] = {
                label: type,
                items: [itemObject],
              };
            }
          }
        }
      });
      this.menuItems = items;
    },
    handleVisibleFilters() {
      // To preserve original add order for filter
      // this loop is required again.
      let assignedFilters = [];
      const visibleFilters = {};
      for (let filter in this.selectedFilters) {
        if (assignedFilters.includes(filter)) {
          continue;
        }

        this.slotItems.forEach((element, index) => {
          if (element.tag) {
            const tag = `${element.tag}${index}`;
            const urlFilters = this.getFilters(element.data.attrs);
            if (urlFilters.includes(filter) || element.isDefault) {
              assignedFilters = [...assignedFilters, ...urlFilters];
              if (!this.initialisedComponents.includes(tag)) {
                window.Vue.component(tag, {
                  render: () => {
                    return element;
                  },
                });
                this.initialisedComponents.push(tag);
              }

              visibleFilters[tag] = {
                filters: urlFilters,
              };
            }
          }
        });
      }
      this.visibleFilters = visibleFilters;

      // Better approach?
      // This is the only way (so far) to avoid glitched and broken behaviour.
      // The point of this is to push parent's delete button to every filter,
      // because Vue.component function wraps the component with a div,
      // Alternate is to manually add delete button to every filter file.
      for (let activeTag of Object.keys(this.visibleFilters)) {
        this.addDeleteButton(activeTag);
      }
    },
    handleFilterOpen(item) {
      this.lastAddedFilter = item.tag;
      for (let filter of item.filters) {
        if (!this.selectedFilters[filter]) {
          this.selectedFilters[filter] = "";
        }
      }
      this.handleItems();
    },
    getFilters(attrs, unusedOnly = false) {
      let urlFilters = [];
      for (let attribute of Object.keys(attrs)) {
        const param = attrs[attribute];
        if (attribute.includes("t-filter")) {
          if (
            Object.prototype.hasOwnProperty.call(this.selectedFilters, param) &&
            unusedOnly
          ) {
            urlFilters = [];
            break;
          } else {
            urlFilters.push(param);
          }
        }
      }
      return urlFilters;
    },
    removeFilter(urlFilters) {
      for (let filter of urlFilters) {
        this.deleteFilter({ name: filter });
        if (
          Object.prototype.hasOwnProperty.call(this.selectedFilters, filter)
        ) {
          this.$delete(this.selectedFilters, filter);
        }
      }
      this.handleItems();
    },
    resetAllFilters(){
        Object.keys(this.visibleFilters).forEach((vfname)=>{
            this.removeFilter(this.visibleFilters[vfname].filters)
        })
        this.resetAllFilters
    },
    addDeleteButton(tag) {
      this.$nextTick(() => {
        const parent = this.$refs[tag][0];
        const child = parent.$children[0];
        if (child && parent) {
          child.$slots.footer = parent.$slots.default;
          if (tag === this.lastAddedFilter) {
            child.isOpen = true;
          }
        }
      });
    },
  },
};
</script>
