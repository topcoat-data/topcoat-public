<template>
  <div class="t-tags-input max-w-max min-w-full min-h-[43px] relative">
    <div class="pb-2 font-bold tracking-widest" v-if="label">
      {{ label.toUpperCase() }}
    </div>
    <base-multiple-value-input
      v-if="isSingleTag"
      v-model="selectedTags"
      selection-only
      :data="tags.length ? tags : tempTags"
      :loading="loading"
      :placeholder="placeholder"
      @update="handleUpdate"
      display-key="value"
      value-key="value"
      @opened="handleOpen"
    />
    <base-tags-input
      v-else
      v-model="selectedTags"
      selection-only
      :data="tags"
      :loading="loading"
      :placeholder="placeholder"
      @update="handleUpdate"
      @opened="handleOpen"
    />
  </div>
</template>

<script>
export default {
  props: {
    label: {
      type: String,
      default: "",
    },
    tKeyColumn: {
      type: String,
      default: "KEY",
    },
    tValueColumn: {
      type: String,
      default: "VALUE",
    },
    isSingleTag: {
      type: Boolean,
      default: false,
    },
    placeholder: {
      type: String,
      default: "",
    },
  },
  data: () => ({
    is_filter: true,
    selectedTags: [],
    tempTags: [], // base-multiple-value-input does not show selected items if `tags` is empty because data is fetched on open.
  }),
  computed: {
    tags() {
      const items = [];

      if (this.rows.length) {
        for (let row of this.rows) {
          const key = row[this.tKeyColumn];
          const value = row[this.tValueColumn];
          if (key && value) {
            items.push({
              key: key.value,
              value: value.value,
            });
          }
        }
      }
      return items;
    },
    firstKey() {
      // Used for single tag
      if (this.tags.length) {
        return this.tags[0].key;
      }

      if (this.tempTags) {
        return this.tempTags[0].key;
      }

      return null;
    },
  },
  methods: {
    onVisualizationInit() {
      const initial_value = this.getFilterValue("selected_items");

      if (initial_value) {
        const selectedTags = [];
        const tempTags = [];
        const urlTags = initial_value.split("|");

        for (let item of urlTags) {
          const splitPair = item.split("_");
          const key = splitPair.length > 1 ? splitPair[1] : splitPair[0];
          const value = splitPair[0];

          if (key && value) {
            if (this.isSingleTag) {
              selectedTags.push(value);
              tempTags.push({ key, value });
            } else {
              selectedTags.push({ key, value });
            }
          }
        }

        this.tempTags = tempTags;
        this.selectedTags = selectedTags;
      }
    },
    onFiltersUpdated() {
      this.tempTags = [];
      this.selectedTags = [];
      this.onVisualizationInit();
    },
    handleUpdate(items) {
      const values = [];
      for (let item of items) {
        if (this.isSingleTag) {
          if (!this.firstKey) {
            break;
          }
          values.push(`${item}_${this.firstKey}`);
        } else {
          values.push(`${item.value}_${item.key}`);
        }
      }
      this.setFilterValue("selected_items", values.join("|"));
    },
    handleOpen() {
      this.fetchLayerData();
    },
  },
};
</script>

<style>
.t-tags-input .vue--multiple-value-input__body {
  position: relative !important;
  min-width: 100% !important;
}
</style>
