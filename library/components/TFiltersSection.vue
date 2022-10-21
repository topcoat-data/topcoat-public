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
        <backup-restore-icon :size="18" />
        Reset
      </div>
    </div>
    <div class="flex flex-wrap items-center gap-1">
      <component
        v-for="(data, tag) in visibleFilters"
        :key="tag"
        :is="tag"
        :ref="tag"
      >
        <div
          v-if="!data.isDefault"
          class="flex justify-end items-center border-t border-[#E4E3E8] p-2"
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
  </div>
</template>

<script>
export default {
  data: () => ({
    initialisedComponents: [],
    menuItems: [],
    visibleFilters: {},
    lastAddedFilter: null,
    defaultFilters: {},
  }),
  mounted() {
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
          const label =
            element?.componentOptions?.propsData?.label || attrs["label"];
          const type =
            attrs["dropdown-section"] ||
            attrs["dropdownSection"] ||
            "Ungrouped";
          const unusedFilters = this.getFilters(attrs, true);
          const isDefault = this.isDefault(attrs);

          element.isDefault = isDefault;
          if (isDefault) {
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
      for (let filter in { ...this.filters, ...this.defaultFilters }) {
        if (assignedFilters.includes(filter)) {
          continue;
        }

        this.slotItems.forEach((element, index) => {
          if (element.tag) {
            const urlFilters = this.getFilters(element.data.attrs);
            if (urlFilters.includes(filter) || element.isDefault) {
              assignedFilters = [...assignedFilters, ...urlFilters];
              const tag = `${element.tag}${index}`;
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
      // The point of this is to push parent's delete button to every filter.
      // Alternate is to manually add delete button to every filter file.
      for (let activeTag of Object.keys(this.visibleFilters)) {
        this.addDeleteButton(activeTag);
      }
    },
    handleFilterOpen(tag) {
      this.lastAddedFilter = tag;
      this.handleItems();
    },
    getFilters(attrs, unusedOnly = false) {
      let urlFilters = [];
      for (let attribute of Object.keys(attrs)) {
        if (attribute.includes("t-filter")) {
          if (this.filters.hasOwnProperty(attrs[attribute]) && unusedOnly) {
            urlFilters = [];
            break;
          } else {
            urlFilters.push(attrs[attribute]);
          }
        }
      }
      return urlFilters;
    },
    removeFilter(urlFilters) {
      for (let filter of urlFilters) {
        this.deleteFilter({ name: filter });
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
    isDefault(attrs) {
      // Attribute is used to avoid adding this prop to every single filter, not good for scalability.
      for (let key of Object.keys(attrs)) {
        if (key === "is-default" || key === "isDefault") {
          const value = attrs[key] !== false;
          return value;
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
