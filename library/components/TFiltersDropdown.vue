<!-- migrated -->
<template>
  <t-dropdown :is-open="isOpen" @open="handleOpen" @close="isOpen = false">
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
          ref="filtersSearchInput"
          @focus="$event.target.select()"
        />
        <div class="w-5">
          <close-icon v-if="search" :size="18" @click="search = ''" />
        </div>
      </div>
    </div>

    <div class="flex flex-col gap-2 px-2 pb-2 tracking-widest roboto-fonts">
      <div v-if="!filteredItems.length">No filters found</div>
      <div v-for="(section, index) in filteredItems" :key="section">
        <div class="px-2 py-1 text-xs font-semibold">{{ section.label }}</div>
        <div class="text-sm">
          <div
            class="px-2 py-1 rounded hover:bg-[#F9F8FA]"
            v-for="item in expanded.includes(index)
              ? section.items
              : section.items.slice(0, itemLimit)"
            :key="item"
            @click="toggleFilter(item)"
          >
            {{ item.label }}
          </div>
        </div>
        <div
          @click="handleExpanded(index)"
          class="text-[#145DEB] text-sm px-2 py-1"
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
  name: "TFiltersDropdown",
  props: {
    items: {
      type: Array,
      default: [],
    },
    itemLimit: {
      type: Number,
      default: 4,
    },
  },
  data: () => ({
    search: "",
    expanded: [],
    isOpen: false,
  }),
  computed: {
    filteredItems() {
      // Show filters according to `search` & `filters` variables.
      const items = [];
      const usedFilters = [];
      for (let key of Object.keys(this.items)) {
        let filteredItems = [];
        const section = this.items[key];

        for (let item of section.items) {
          // Only include searched items.
          if (
            item.label &&
            !item.label.toLowerCase().includes(this.search.toLowerCase())
          ) {
            continue;
          }
          if (item.is_default) {
            this.toggleFilter(item);
            continue;
          }

          filteredItems.push(item);
        }
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
    toggleFilter(item) {
      this.$emit("opened", item);
      this.isOpen = false;
    },
    handleExpanded(index) {
      if (this.expanded.includes(index)) {
        return (this.expanded = this.expanded.filter((e) => e !== index));
      }
      return this.expanded.push(index);
    },
    handleOpen() {
      this.isOpen = true;
      const searchInput = this.$refs.filtersSearchInput;
      searchInput.focus();
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
