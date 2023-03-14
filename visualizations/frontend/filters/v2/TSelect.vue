<template>
  <t-dropdown :is-open="isOpen" @open="onDropdownOpen">
    <!-- Handle -->
    <div slot="handle" class="flex items-center gap-1 p-1 text-sm font-medium">
      <div class="pl-1">
        <slot name="icon"></slot>
      </div>

      <div class="flex items-center gap-1">
        <div v-if="label">{{ label }}{{ selected_internal ? ":" : "" }}</div>
        <div class="font-normal">
          {{ selected_internal }}
        </div>
      </div>

      <t-loading-spinner v-if="loading" position="relative" />
      <menu-down-icon v-else :size="20" />
    </div>

    <!-- Popup Contents -->
    <div class="min-w-[254px]">
      <div
        v-if="label"
        class="px-[12px] pt-[16px] pb-[8px] flex justify-between items-center w-full"
      >
        <h6
          class="text-[10px] text-[#727184] font-semibold uppercase leading-[15px] tracking-widest flex gap-1 items-center"
        >
          <filter-variant-icon :size="18" />
          {{ label }}
        </h6>
      </div>
      <div v-if="isSearchable" class="pt-2 t-select-nav-search w-full p-2">
        <base-search-input
          v-model="search"
          class="mt-0 text-sm !rounded-md"
          :placeholder="searchPlaceholder"
          size="small"
          :clearable="false"
        />
      </div>
      <div class="px-[8px] pt-[4px] pb-[6px] w-full">
        <ul class="max-h-[200px] overflow-auto">
          <li
            v-for="(item, index) in menu"
            :key="index"
            class="flex justify-between px-[8px] py-[6px] text-sm cursor-pointer text-[#555463]"
            @click="selectItem(item)"
          >
            <div
              class="flex items-center justify-between w-full hover:text-[#1C1C21] leading-[16.41px]"
            >
              {{ item.title }}
              <div
                v-show="selected_internal === item.value"
                style="color: #0f47c6"
                class="relative flex items-center h-1 h-full"
              >
                <check-icon />
              </div>
            </div>
          </li>
          <small v-if="!options.length && !loading"> No items found </small>
        </ul>
        <small v-if="!menu.length && !loading"> No items found </small>
      </div>
      <div v-if="$slots['footer']" class="p-2 border-t border-[#E4E3E8]">
        <slot name="footer"></slot>
      </div>
    </div>
  </t-dropdown>
</template>

<script>
export default {
  props: {
    defaultValue: {
      type: String,
      default: "",
    },
    label: {
      type: String,
      default: "Select",
    },
    tKeyColumn: {
      type: String,
      default: "",
    },
    tValueColumn: {
      type: String,
      default: "",
    },
    isUnselectable: {
      type: Boolean,
      default: false,
    },
    isSearchable: {
      type: Boolean,
      default: false,
    },
    searchPlaceholder: {
      type: String,
      default: "Search",
    },
    isOpen: {
      type: Boolean,
      default: false,
    },
  },
  data: () => ({
    is_filter: true,
    selected_internal: "",
    search: "",
  }),
  computed: {
    labels() {
      const column_name = this.tValueColumn
        ? this.tValueColumn
        : this.findColumnByTag("labels");
      return this.getColumn(column_name);
    },
    options() {
      const column_name = this.tKeyColumn
        ? this.tKeyColumn
        : this.findColumnByTag("options");
      return this.getColumn(column_name);
    },
    menu() {
      const values = this.options;
      const titles = this.labels;
      const menu = [];

      if (values && titles) {
        for (let index in values) {
          const value = values[index];
          const title = titles[index];

          if (
            this.isSearchable &&
            !title.toLowerCase().includes(this.search.toLowerCase())
          ) {
            continue;
          }

          menu.push({ value, title });
        }
      }
      return menu;
    },
    selectedItemLabel() {
      const selected = this.menu.filter(
        (item) => item.value === this.selected_internal
      )[0];

      if (selected) {
        return selected.title;
      }

      if (this.selected_internal) {
        return this.selected_internal;
      }

      return null;
    },
  },
  methods: {
    onVisualizationInit() {
      const initial_value = this.getFilterValue("dropdown");

      if (initial_value) {
        this.selected_internal = initial_value;
      } else if (this.defaultValue) {
        this.selected_internal = this.defaultValue;
        this.setFilterValue("dropdown", this.defaultValue, this.defaultValue);
      }
    },
    onFiltersUpdated() {
      this.selected_internal = "";
      this.onVisualizationInit();
    },
    selectItem(item) {
      if (this.selected_internal === item.value && this.isUnselectable) {
        this.selected_internal = "";
      } else {
        this.selected_internal = item.value;
      }

      this.setFilterValue(
        "dropdown",
        this.selected_internal,
        this.defaultValue
      );
    },
    onDropdownOpen() {
      this.fetchLayerData();
    },
  },
};
</script>

<style>
.t-select-nav-search .vue--search-input__field {
  @apply !rounded-3xl !bg-white !opacity-[0.5] !h-[34px];
}
</style>
