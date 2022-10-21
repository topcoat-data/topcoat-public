<template>
  <t-dropdown
    :is-expanded="onExpandable"
    :is-active="checked.length ? true : false"
    :is-open="isOpen"
    @open="onDropdownOpen"
  >
    <!-- Handle -->
    <div
      slot="handle"
      class="flex items-center gap-1 p-1 text-sm font-medium"
      v-if="!isExpanded"
    >
      <div class="pl-1">
        <slot name="icon"></slot>
      </div>
      <div
        class="flex items-center"
        :class="!canShowSelected && 'flex-row-reverse gap-1'"
      >
        <span>{{ label }}</span>
        <div v-if="checked.length" class="flex items-center font-normal">
          {{ canShowSelected ? ": " + checked.join(", ") : checked.length }}
        </div>
      </div>

      <t-loading-spinner v-if="loading" position="relative" />
      <menu-down-icon v-else :size="20" />
    </div>

    <!-- Popup Contents -->
    <div class="min-w-[294px]" v-bind="popupAttrs">
      <div
        v-if="label"
        class="px-[12px] pt-[16px] flex justify-between items-center w-full"
      >
        <h6
          class="text-[10px] text-[#727184] font-semibold uppercase leading-[15px] tracking-widest flex gap-1 items-center"
        >
          <filter-variant-icon :size="18" />
          {{ label }}
        </h6>
      </div>

      <!-- Search input -->
      <div class="w-full p-2" v-if="isSearchable">
        <div class="search-input">
          <magnify-icon :size="18" />
          <input
            class="bg-transparent outline-none !text-black w-full"
            :placeholder="searchPlaceholder"
            v-model="search"
          />
          <div class="w-5">
            <close-icon v-if="search" :size="18" @click="search = ''" />
          </div>
        </div>
      </div>
      <div
        @click="selectUnselect"
        class="px-[12px] text-[#145DEB] text-[13px] cursor-pointer font-normal leading-[18px] inline-flex items-center justify-end"
        :class="checked.length ? 'text-[#145DEB]' : 'text-[#727184]'"
      >
        <t-loading-spinner v-if="isExpanded && loading" position="relative" />
        <span v-else>
          {{ checked.length < ids.length ? "Select All" : "Reset" }}
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
      <slot name="footer"></slot>
    </div>
  </t-dropdown>
</template>

<script>
const ItemComponent = Vue.component("item-component", {
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
    canShowSelected: {
      type: Boolean,
      default: false,
    },
    isOpen: {
      type: Boolean,
      default: false,
    },
  },
  data: () => ({
    checked: [],
    is_filter: true,
    search: "",
    itemComponent: ItemComponent,
  }),
  components: {
    ItemComponent,
  },
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
    urlParam() {
      for (let key of Object.keys(this.$attrs)) {
        if (key === "t-filter:selected_items") {
          return this.$attrs[key];
        }
      }
      return "";
    },
  },
  methods: {
    onVisualizationInit() {
      const initial_value = this.getFilterValue("selected_items");

      if (initial_value) {
        this.checked = initial_value.split("|");
      } else if (this.defaultValue) {
        this.checked = this.defaultValue.split("|");
        this.setFilterValue("selected_items", this.defaultValue);
      }
    },
    selectUnselect() {
      if (this.checked.length === this.ids.length) {
        this.checked = [];
      } else {
        // Only select what is visible, search can affect this.
        this.checked = this.menu.map((i) => i.value);
      }
      this.updateUrlParam();
    },
    updateUrlParam(value) {
      if (value) {
        this.checked = [...value];
      }

      if (this.urlParam) {
        // Prevent reset button from removing filter.
        return this.setFilter({
          name: this.urlParam,
          value: this.checked.join("|"),
        });
      }
      return this.setFilterValue("selected_items", this.checked.join("|"));
    },
    onDropdownOpen() {
      this.fetchLayerData();
    },
    removeFilter() {
      this.unsetFilterValue("selected_items");
    },
  },
};
</script>

<style>
.nav-search .vue--search-input__field {
  @apply !rounded-3xl !bg-white !opacity-[0.5] h-[32px];
}
</style>
