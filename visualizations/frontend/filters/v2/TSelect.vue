<template>
  <t-dropdown @open="onDropdownOpen">

    <!-- Handle -->
    <div slot="handle" class="flex items-center gap-1 p-1 text-sm font-medium">
      <div class="pl-1">
        <slot name="icon"></slot>
      </div>
      <span>{{ selectedItemLabel || label }}</span>

      <t-loading-spinner v-if="loading" position="relative" />
      <menu-down-icon v-else :size="20" />
    </div>

    <!-- Popup Contents -->
    <template>
      <div class="min-w-[254px]">
        <div class="px-[12px] pt-[16px] pb-[8px] flex justify-between items-center w-full" v-if="label">
          <h6 class="text-[10px] text-[#727184] font-semibold uppercase leading-[15px] tracking-widest">
            {{ label }}
          </h6>
        </div>
        <div class="px-[8px] pt-[4px] pb-[6px] w-full">
          <ul class="max-h-[200px] overflow-auto">
            <li class="flex justify-between px-[8px] py-[6px] text-sm cursor-pointer text-[#555463]"
              v-for="(item, index) in menu" :key="index" @click="selectItem(item)">
              <div class="flex items-center justify-between w-full hover:text-[#1C1C21] leading-[16.41px]">
                {{ item.title }}
                <div style="color: #0F47C6" class="relative flex items-center h-1 h-full"
                  v-show="selected_internal === item.value">
                  <check-icon />
                </div>
              </div>
            </li>
            <small v-if="!options.length && !loading">
              No items found
            </small>
          </ul>
        </div>
      </div>
    </template>
  </t-dropdown>
</template>

<script>
export default {
  props: {
    defaultValue: {
      type: String,
      default: '',
    },
    label: {
      type: String,
      default: 'Select'
    },
    tKeyColumn: {
      type: String,
      default: '',
    },
    tValueColumn: {
      type: String,
      default: '',
    },
    isUnselectable: {
      type: Boolean,
      default: false,
    }
  },
  data: () => ({
    is_filter: true,
    selected_internal: '',
  }),
  computed: {
    labels() {
      const column_name = this.tValueColumn ? this.tValueColumn : this.findColumnByTag("labels");
      return this.getColumn(column_name);
    },
    options() {
      const column_name = this.tKeyColumn ? this.tKeyColumn : this.findColumnByTag("options");
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
          menu.push({ value, title });
        }
      }
      return menu;
    },
    selectedItemLabel() {
      const selected = this.menu.filter(item => item.value === this.selected_internal)[0]

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
      // const initial_value = this.getFilterValue("dropdown");
      const initial_value = this.getFilterValueNew("dropdown");

      if (initial_value) {
        this.selected_internal = initial_value;
      } else if (this.defaultValue) {
        console.log('this.defaultValue in TSelect', this.defaultValue)
        this.selected_internal = this.defaultValue;
        // Here we set the default value because we are setting it for the first time.
        this.setFilterValueAsObject({ name: "dropdown", value: this.defaultValue, defaultValue: this.defaultValue });
        // this.setFilterValue("dropdown", this.defaultValue);
      }
    },
    selectItem(item) {
      if (this.selected_internal === item.value && this.isUnselectable) {
        this.selected_internal = '';
      } else {
        this.selected_internal = item.value;
      }
      console.log('selectItem Tselect this.selected_internal:', this.selected_internal)
      // Here we do not need to set the default Value as it would already have been set
      this.setFilterValueAsObject({ name: "dropdown", value: this.selected_internal });
      // this.setFilterValue("dropdown", this.selected_internal, true);
    },
    onDropdownOpen() {
      this.fetchLayerData();
    }
  }
}
</script>
