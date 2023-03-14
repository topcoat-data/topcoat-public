<template>
  <div
    class="find-me p-2 rounded-[2px] h-max t-checkbox-group"
    :class="{ 'is-outlined': isOutlined }"
  >
    <div class="flex justify-between gap-1">
      <div v-if="label" class="font-bold tracking-widest">
        {{ label.toUpperCase() }}
      </div>
      <div v-if="isSearchable" class="px-2 pt-2 nav-search">
        <base-search-input
          v-model="search"
          class="mt-0 mb-3 text-sm search-report !rounded-md"
          :placeholder="searchPlaceholder"
          size="small"
          :clearable="false"
        />
      </div>
    </div>
    <div
      ref="checkBoxesContainer"
      class="relative py-2 overflow-hidden transition"
      :style="{
        maxHeight: containerHeight,
        transition: '0.3s',
      }"
      :class="{ 'w-max': !isInline, 'px-3': label }"
    >
      <div>
        <t-loading-spinner v-if="!init || loading" position="relative" />
        <div
          v-for="key in Object.keys(items)"
          v-else-if="Object.keys(items).length"
          :key="key"
        >
          <div v-if="!hideLabels" class="pb-3 font-bold tracking-widest">
            {{ isLabelCapitalized ? key.toUpperCase() : key }}
          </div>
          <div
            class="flex flex-wrap gap-2 px-2 pb-3"
            :class="{ 'flex-col': !isInline }"
          >
            <div
              v-for="value in items[key].data"
              :key="value.value + '_' + key"
              class="tracking-widest"
            >
              <base-checkbox
                v-if="value.rendered && value.value"
                v-model="checked"
                :label="value.rendered"
                :value="value.value + '_' + key"
                @change="updateUrlParams"
              />
            </div>
          </div>
        </div>
        <small v-else> No data found </small>
      </div>
    </div>
    <div v-if="!isExpanded && init && canBeExpanded" class="mt-2 text-center">
      <base-button
        ghost
        :disabled="!init || loading"
        @click="expanded ? collapse() : expand()"
      >
        <span v-if="expanded">Show Less</span>
        <span v-else>Show More</span>
      </base-button>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    label: {
      type: String,
      default: "",
    },
    searchPlaceholder: {
      type: String,
      default: "Search",
    },
    isExpanded: {
      type: Boolean,
      default: false,
    },
    isLabelCapitalized: {
      type: Boolean,
      default: false,
    },
    isInline: {
      type: Boolean,
      default: false,
    },
    isOutlined: {
      type: Boolean,
      default: false,
    },
    isSearchable: {
      type: Boolean,
      default: false,
    },
    defaultHeight: {
      type: String,
      default: "200px",
    },
    tKeyColumn: {
      type: String,
      default: "",
    },
    tValueColumn: {
      type: String,
      default: "",
    },
    hideLabels: {
      type: Boolean,
      default: false,
    },
    onExpandable: {
      type: Boolean,
      default: false,
    },
  },
  data: () => ({
    canBeExpanded: true,
    checked: [],
    containerHeight: "200px",
    is_filter: true,
    init: false,
    slotHeight: 0,
    expanded: false,
    search: "",
  }),
  computed: {
    keyColumn() {
      return this.tKeyColumn ? this.tKeyColumn : this.findColumnByTag("keys");
    },
    valueColumn() {
      return this.tValueColumn
        ? this.tValueColumn
        : this.findColumnByTag("values");
    },
    items() {
      const items = {};
      this.slotHeight = 0;

      for (let row of this.rows) {
        const key = row[this.keyColumn];
        if (!key) continue;
        const value = row[this.valueColumn];
        if (value && value.rendered && this.search) {
          const text = value.rendered.toLowerCase();
          if (!text.includes(this.search.toLowerCase())) {
            continue;
          }
        }
        if (items[key.value]) {
          items[key.value].data.push(value);
        } else {
          this.slotHeight += 40;
          items[key.value] = { label: "", data: [] };
          items[key.value].label = key.rendered;
          items[key.value].data = [value];
        }
        this.slotHeight += 40;
      }
      this.handleHeight();
      return items;
    },
  },
  watch: {
    onExpandable: function (newVal, oldVal) {
      if (newVal) {
        this.fetchLayerData();
      }
    },
  },
  methods: {
    collapse() {
      this.containerHeight = this.defaultHeight;
      this.expanded = false;
    },
    expand() {
      this.containerHeight = this.slotHeight + "px";
      this.expanded = true;
    },
    handleHeight() {
      const containerHeight = parseInt(this.defaultHeight.replace(/\D+/g, ""));
      this.canBeExpanded = containerHeight < this.slotHeight;
      return (this.containerHeight = this.isExpanded
        ? this.slotHeight + "px"
        : this.defaultHeight);
    },
    onVisualizationInit() {
      const selected = this.getFilterValue("selected_items");

      if (selected) {
        this.checked = selected.split("|");
      }

      this.init = true;
    },
    updateUrlParams() {
      this.setFilterValue("selected_items", this.checked.join("|"));
    },
  },
};
</script>

<style scoped>
.t-checkbox-group .is-outlined {
  box-shadow: inset 0 0 0 1px hsl(244deg 8% 84%);
}
</style>
