<template>
  <t-dropdown
    :is-expanded="onExpandable"
    :is-active="checked.length ? true : false"
    :is-open="isOpen"
    @open="onDropdownOpen"
  >
    <!-- Handle -->
    <div
      v-if="!isExpanded"
      slot="handle"
      class="flex items-center gap-1 p-1 text-sm font-medium"
    >
      <div class="pl-1">
        <slot name="icon"></slot>
      </div>
      <div
        class="flex items-center"
        :class="!canShowSelected && 'flex-row-reverse gap-1'"
      >
        <span>{{ label }}</span>
        <div v-if="checked.length">
          <div v-if="canShowSelected" class="flex items-center font-normal">
            :
            <div
              v-for="(item, index) in checked.slice(0, selectedVisibleCount)"
              :key="item"
              class="flex items-center pl-1"
            >
              {{ item }}
              <span v-if="!defaultValue" class="text-[#7FA7F5] pl-1">
                <close-icon :size="14" @click.stop="removeItem(item)" />
              </span>
              <span v-else-if="checked.length - 1 != index">, </span>
            </div>
            <div
              v-if="checked.length > selectedVisibleCount"
              class="flex items-center gap-2 font-medium pl-1"
            >
              <div class="border-r border-[#7FA7F5] py-2"></div>
              +{{ checked.length - selectedVisibleCount }}
            </div>
          </div>
          <div v-else>
            {{ checked.length }}
          </div>
        </div>
      </div>

      <t-loading-spinner v-if="loading" position="relative" />
      <menu-down-icon v-else :size="20" />
    </div>

    <!-- Popup Contents -->
    <div class="min-w-[294px]" v-bind="popupAttrs">
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

      <!-- Search input -->
      <div v-if="isSearchable" class="w-full p-2 pt-2 t-multi-nav-search">
        <base-search-input
          v-model="search"
          class="mt-0 text-sm !rounded-md"
          :placeholder="searchPlaceholder"
          size="small"
          :clearable="false"
        />
      </div>

      <div
        class="px-[12px] text-[#145DEB] text-[13px] cursor-pointer font-normal leading-[18px] flex justify-between items-center"
      >
        <span
          class="inline-flex items-center justify-end"
          :class="checked.length ? 'text-[#145DEB]' : 'text-[#727184]'"
        >
          <t-loading-spinner v-if="isExpanded && loading" position="relative" />
          <span
            v-else-if="checked.length < menu.length"
            @click="selectUnselect"
          >
            Select All
          </span>
          <button v-else @click="reset">Reset</button>
        </span>
        <span @click="showSelected = !showSelected">
          {{ showSelected ? "Show all" : "Only show selected" }}
        </span>
      </div>
      <div class="px-[12px] pt-[4px] pb-[6px] w-full">
        <virtual-list
          :style="{
            height: Math.min(menu.length * 30, 320) + 'px',
            'overflow-y': 'auto',
          }"
          :estimate-size="32"
          :extra-props="{ checked, updateUrlParam }"
          :data-key="'index'"
          :data-sources="menu"
          :data-component="itemComponent"
        />
        <small v-if="!menu.length && !loading"> No items found </small>
      </div>
      <div v-if="$slots['footer']" class="p-2 border-t border-[#E4E3E8]">
        <slot name="footer"></slot>
      </div>
    </div>
  </t-dropdown>
</template>

<script>
const ItemComponent = window.Vue.component("ItemComponent", {
  props: {
    index: {
      type: Number,
    },
    source: {
      type: Object,
      default() {
        return {};
      },
    },
    checked: {
      type: Array,
      default() {
        return [];
      },
    },
    updateUrlParam: {
      type: Function,
    },
    model: {
      prop: "checked",
    },
  },
  template: `
			<div class="flex items-center justify-between w-full hover:text-[#1C1C21] leading-[16.41px]">
				<base-checkbox
					class="!min-w-[200px]"
					:label="source.title"
					:value="source.value"
					v-model="checked"
					@change="updateUrlParam"
				/>
			</div>
		`,
});

export default {
  components: {
    ItemComponent,
  },
  props: {
    defaultValue: {
      type: String,
      default: "",
    },
    hasCheckedAll: {
      type: Boolean,
      default: false,
    },
    label: {
      type: String,
      default: "",
    },
    isSearchable: {
      type: Boolean,
      default: false,
    },
    searchPlaceholder: {
      type: String,
      default: "Search",
    },
    isExpanded: {
      type: Boolean,
      default: false,
    },
    tKeyColumn: {
      type: String,
      default: "",
    },
    tValueColumn: {
      type: String,
      default: "",
    },
    onExpandable: {
      type: Boolean,
      default: false,
    },
    isOpen: {
      type: Boolean,
      default: false,
    },
    canShowSelected: {
      type: Boolean,
      default: false,
    },
    selectedVisibleCount: {
      type: Number,
      default: 5,
    },
  },
  data: () => ({
    checked: [],
    is_filter: true,
    search: "",
    itemComponent: ItemComponent,
    showSelected: false,
  }),
  computed: {
    names() {
      const column_name = this.tValueColumn
        ? this.tValueColumn
        : this.findColumnByTag("names");
      return this.getColumn(column_name);
    },
    ids() {
      const column_name = this.tKeyColumn
        ? this.tKeyColumn
        : this.findColumnByTag("ids");
      return this.getColumn(column_name, "value");
    },
    menu() {
      const menu = [];
      const names = this.tValueColumn
        ? this.tValueColumn
        : this.findColumnByTag("names");
      const ids = this.tKeyColumn
        ? this.tKeyColumn
        : this.findColumnByTag("ids");
      const columns = this.getColumnsByNameAndAttribute([
        { name: names },
        { name: ids, attribute: "value" },
      ]);

      if (Object.keys(columns).length) {
        for (let index in columns[ids]) {
          const value = columns[ids][index] && columns[ids][index].toString();
          const title = columns[names][index];

          if (
            !value ||
            !title ||
            (this.showSelected && !this.checked.includes(value))
          ) {
            continue;
          }
          if (
            this.isSearchable &&
            !title.toLowerCase().includes(this.search.toLowerCase())
          ) {
            continue;
          }

          if (value && title) {
            menu.push({ value, title, index });
          }
        }
      }
      return menu;
    },
    popupAttrs() {
      let attrs = {};
      if (this.isExpanded) {
        attrs.slot = "outside";
      }
      return attrs;
    },
  },
  methods: {
    onVisualizationInit() {
      const initial_value = this.getFilterValue("selected_items");

      if (initial_value) {
        this.checked = initial_value.split("|");
      } else if (this.defaultValue) {
        this.checked = this.defaultValue.split("|");
        this.setFilterValue(
          "selected_items",
          this.defaultValue,
          this.defaultValue
        );
      }
    },
    selectUnselect: _.debounce(function () {
      if (this.checked.length === this.menu.length) {
        this.checked = [];
      } else {
        // Only select what is visible, search can affect this.
        this.checked = this.menu.map((i) => i.value);
      }
      this.updateUrlParam();
    }, 750),
    reset() {
      if (this.defaultValue) {
        this.checked = this.defaultValue.split("|");
      } else {
        this.checked = [];
      }
      this.setFilterValue(
        "selected_items",
        this.checked.join("|"),
        this.defaultValue
      );
    },
    updateUrlParam(value) {
      if (value) {
        this.checked = [...value];
      }

      this.setFilterValue(
        "selected_items",
        this.checked.join("|"),
        this.defaultValue
      );
    },
    onDropdownOpen() {
      this.fetchLayerData();
    },
    removeFilter() {
      this.unsetFilterValue("selected_items");
    },
    removeItem(id) {
      this.checked = this.checked.filter((c) => c !== id);
      this.updateUrlParam();
    },
    onFiltersUpdated() {
      if (this.getFilterValue("selected_items")) {
        this.onVisualizationInit();
      } else {
        this.reset();
      }
    },
  },
};
</script>

<style>
.t-multi-nav-search .vue--search-input__field {
  @apply !rounded-3xl !bg-white !opacity-[0.5] !h-[34px];
}
</style>
