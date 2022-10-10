<template>
  <t-dropdown>
    <!-- Handle button -->
    <div slot="handle" class="flex items-center gap-1 p-1 text-sm font-medium">
      <plus-icon :size="18" />
      Add filter
      <menu-down-icon :size="18" />
    </div>

    <!-- Search input -->
    <div class="p-2 filters-search roboto-fonts">
      <div class="search-input">
        <magnify-icon :size="18" />
        <input
          class="bg-transparent outline-none !text-black"
          placeholder="Filters by..."
          v-model="search"
        />
        <div class="w-5">
          <close-icon v-if="search" :size="18" @click="search = ''" />
        </div>
      </div>
    </div>

    <!-- Filters section  -->
    <div class="flex flex-col gap-2 px-4 pb-2 tracking-widest roboto-fonts">
      <div v-if="!filteredItems.length">No filters found</div>
      <div v-for="(section, index) in filteredItems" :key="section">
        <div class="py-2 text-xs font-semibold">{{ section.label }}</div>
        <div class="text-sm">
          <div
            class="pb-2"
            v-for="filter in expanded.includes(index)
              ? section.items
              : section.items.slice(0, 4)"
            :key="filter"
            @click="toggleFilter(filter.url_param)"
          >
            {{ filter.label }}
          </div>
        </div>
        <div
          @click="handleExpanded(index)"
          class="text-[#145DEB] text-sm"
          v-if="section.items.length > 4"
        >
          <span v-if="expanded.includes(index)"> Show less </span>
          <span v-else>
            Show all {{ section.label.toLowerCase() }} filters
          </span>
        </div>
      </div>
    </div>
  </t-dropdown>
</template>

<script>
export default {
  props: {
    items: {
      type: Array,
      default: [],
    },
  },
  data: () => ({
    search: "",
    is_filter: true,
    expanded: [],
  }),
  computed: {
    filteredItems() {
      // Show filters according to `search` & `filters` variables.
      let items = [];
      for (let section of this.items) {
        let filteredItems = section.items.filter((s) => {
          return (
            s.label.toLowerCase().includes(this.search.toLowerCase()) &&
            !this.filters.hasOwnProperty(s.url_param)
          );
        });
        if (!filteredItems.length) {
          continue;
        }
        items.push({
          label: section.label,
          items: filteredItems,
        });
      }
      return items;
    },
  },
  methods: {
    toggleFilter(name) {
      if (this.filters[name]) {
        return this.deleteFilter({ name });
      }
      return this.setFilter({
        name,
        value: "",
      });
    },
    handleExpanded(index) {
      if (this.expanded.includes(index)) {
        return (this.expanded = this.expanded.filter((e) => e !== index));
      }
      return this.expanded.push(index);
    },
  },
};
</script>

<style>
.search-input {
  @apply border text-[#A2A1AF] border-[#B3B2BD] flex gap-3 items-center bg-white p-2 rounded-3xl h-8 tracking-widest;
}

.search-input:hover {
  @apply text-[#145DEB] border-[#145DEB];
}

.roboto-fonts {
  font-family: "Roboto";
}
</style>
