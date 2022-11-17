<template>
  <div class="relative flex w-full gap-2 p-5" style="font-family: 'Roboto'">
    <filter-variant-icon class="relative top-[5px]" :size="18" />
    <div class="flex flex-col items-start justify-start gap-2">
      <div class="flex flex-wrap items-center gap-1">
        <slot name="defaultFilter"></slot>
        <component
          v-for="(data, tag) in visibleFilters"
          :key="tag"
          :is="tag"
          :ref="tag"
        >
          <div
            v-if="!data.isDefault"
            class="flex items-center justify-end cursor-pointer"
          >
            <div
              class="w-[34px] h-[32px] border border-[#B3B2BD] rounded flex items-center justify-center"
              @click="removeFilter(data.filters)"
            >
              X
            </div>
          </div>
        </component>
        <t-filters-dropdown :items="menuItems" @opened="handleFilterOpen" />
      </div>

      <!-- Todo: add reset filters functionality -->
      <!-- <div class="flex gap-1 hover:text-[#145DEB] cursor-pointer">
        <backup-restore-icon :size="18" />
        Reset all filters
      </div> -->
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
    defaultFilters: {},
    selectedFilters: {},
  }),
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
          const label = attrs["item-label"] || attrs["itemLabel"] || props.label;
          const type =
            attrs["dropdown-section"] ||
            attrs["dropdownSection"] ||
            "UNGROUPED";
          const unusedFilters = this.getFilters(attrs, true);
          element.isDefault = this.hasDefaultValue(props);

          if (element.isDefault) {
            // If has default value, extract all url filters from component.
            const defaultFilters = unusedFilters.reduce(
              (a, key) => Object.assign(a, { [key]: "" }),
              {}
            );
            this.defaultFilters = { ...this.defaultFilters, ...defaultFilters };
            return;
          }

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
      for (let filter in { ...this.selectedFilters, ...this.defaultFilters }) {
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
                  render: (c) => {
                    return element;
                  },
                });
                this.initialisedComponents.push(tag);
              }

              visibleFilters[tag] = {
                filters: urlFilters,
                isDefault: element.isDefault,
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
          if (this.selectedFilters.hasOwnProperty(param) && unusedOnly) {
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
        if (this.selectedFilters.hasOwnProperty(filter)) {
          this.$delete(this.selectedFilters, filter);
        }
      }
      this.handleItems();
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
    hasDefaultValue(props) {
      // Better solution?
      for (let key in props) {
        if (key.includes("default")) {
          return true;
        }
      }
      return false;
    },
  },
  computed: {
    slotItems() {
      return this.$slots.default || [];
    },
  },
};
</script>