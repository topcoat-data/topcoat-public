<template>
  <div class="t-tags-input max-w-max min-w-full min-h-[43px] relative">
    <div v-if="label" class="pb-2 font-bold tracking-widest">
      {{ label.toUpperCase() }}
    </div>
    <base-multiple-value-input
      v-if="isSingleTag"
      v-model="selectedTags"
      selection-only
      :data="tags.length ? tags : tempTags"
      :loading="loading"
      :placeholder="placeholder"
      display-key="value"
      value-key="value"
      @update="handleUpdate"
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
        try {
          const urlTags = JSON.parse(initial_value);
          for (const [key, value] of Object.entries(urlTags)) {
            let tags = value.map((v) => {
              return {
                key,
                value: v,
              };
            });
            if (this.isSingleTag) {
              // base-multiple-value-input is used for single tag filter.
              this.tempTags = [...tags, ...this.tempTags]; // Without defaults base-multiple-value-input cannot show selected tags.
              this.selectedTags = [...value, ...this.selectedTags]; // base-multiple-value-input needs exact value instead of key:val pairs.
            } else {
              this.selectedTags = [...tags, ...this.selectedTags];
            }
          }
        } catch (error) {
          console.error(error);
          console.error("Failed to parse tags data");
        }
      }
    },
    handleUpdate(items) {
      const values = {};
      for (let item of items) {
        if (this.isSingleTag) {
          if (!this.firstKey) {
            break;
          }
          values[this.firstKey] = [item, ...(values[this.firstKey] || [])];
        } else {
          values[item.key] = [item.value, ...(values[item.key] || [])];
        }
      }
      if (Object.keys(values).length) {
        this.setFilterValue("selected_items", JSON.stringify(values));
      } else {
        this.unsetFilterValue("selected_items");
      }
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
