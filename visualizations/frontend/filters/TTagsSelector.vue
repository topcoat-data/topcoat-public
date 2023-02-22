<template>
  <t-dropdown
    :is-active="selected.length ? true : false"
    :is-open="isOpen"
    @open="fetchLayerData"
    @closed="close"
  >
    <!-- Handle -->
    <div slot="handle" class="flex items-center gap-1 p-1 text-sm font-medium">
      <div class="pl-1">
        <slot name="icon"></slot>
      </div>
      <div class="flex flex-wrap items-center w-max">
        <span>{{ label }}</span>
        <div v-if="selected.length" class="flex flex-wrap gap-1">
          <span>:</span>
          <div
            v-for="selectedTag of selected.slice(0, selectedVisibleCount)"
            :key="selectedTag"
            class="bg-[#EAF1FF] rounded flex items-center gap-1 rounded"
          >
            <span v-if="!isSingleTag" class="font-semibold">
              {{ selectedTag.key }}
            </span>
            <span class="font-normal">
              {{ selectedTag.value }}
            </span>
            <span class="text-[#7FA7F5]">
              <close-icon :size="14" @click.stop="removeTag(selectedTag)" />
            </span>
          </div>
        </div>
      </div>
      <div class="flex items-center tracking-widest">
        <div
          v-if="selected.length > selectedVisibleCount"
          class="flex items-center gap-2"
        >
          <div class="border-r border-[#7FA7F5] py-2"></div>
          +{{ selected.length - selectedVisibleCount }}
        </div>
        <t-loading-spinner v-if="loading" position="relative" />
        <menu-down-icon v-else :size="20" />
      </div>
    </div>

    <!-- Popup Contents -->
    <div class="relative max-w-[300px]">
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

      <!-- Input -->
      <div class="relative w-full p-2 min-w-[300px]">
        <div class="search-input" @click="open">
          <div
            class="rounded-full border border-[#145DEB] text-[#145DEB] flex items-center"
          >
            <plus-icon v-if="!showList" :size="12" />
            <close-icon v-else :size="12" @click.stop="close" />
          </div>
          <input
            v-model="search"
            class="bg-transparent outline-none !text-black w-full"
            :class="loading && 'cursor-wait'"
          />
        </div>
        <div v-if="showList" class="p-2">
          <div class="min-h-[200px] max-h-[500px] overflow-auto">
            <!-- Show values -->
            <div v-if="selectedKey" class="flex flex-col gap-1">
              <span
                class="sticky top-0 left-0 w-full m-auto font-semibold text-left bg-white"
              >
                Select a {{ selectedKey }}
              </span>
              <div v-if="tags[selectedKey] && tags[selectedKey].length">
                <div
                  v-for="value of expanded.includes(selectedKey)
                    ? tags[selectedKey]
                    : tags[selectedKey].slice(0, valueLimit)"
                  :key="value"
                  class="p-1 hover:bg-[#F9F8FA]"
                >
                  <div
                    class="p-1 hover:bg-[#F9F8FA]"
                    @click.stop="selectValue(value)"
                  >
                    {{ displayValue(value) }}
                  </div>
                </div>
                <div
                  v-if="
                    tags[selectedKey] && tags[selectedKey].length > valueLimit
                  "
                  class="text-[#145DEB] text-sm px-2 py-1"
                  @click="handleExpanded(selectedKey)"
                >
                  <span v-if="expanded.includes(selectedKey)"> Show less </span>
                  <span v-else> Show more </span>
                </div>
              </div>
              <div v-else>Tags not found</div>
            </div>

            <!-- Show keys -->
            <div v-else class="flex flex-col gap-1">
              <span
                class="sticky top-0 left-0 w-full m-auto font-semibold text-left bg-white"
              >
                Select a key
              </span>
              <div
                v-for="key in Object.keys(tags)"
                :key="key"
                class="p-1 hover:bg-[#F9F8FA]"
                @click.stop="selectKey(key)"
              >
                {{ displayKey(key) }}
              </div>
            </div>
          </div>
        </div>
        <div v-else-if="selected.length" class="flex flex-wrap gap-1 p-2">
          <div
            v-for="selectedTag of selected"
            :key="selectedTag"
            class="bg-[#EAF1FF] rounded p-1 flex items-center gap-1 rounded"
          >
            <span v-if="!isSingleTag" class="font-semibold">
              {{ selectedTag.key }}
            </span>
            {{ selectedTag.value }}
            <close-icon :size="12" @click.stop="removeTag(selectedTag)" />
          </div>
        </div>
        <div v-else class="p-2">No values selected</div>
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
    placeholder: {
      type: String,
      default: "",
    },
    isSingleTag: {
      type: Boolean,
      default: false,
    },
    isOpen: {
      type: Boolean,
      default: false,
    },
    valueLimit: {
      type: Number,
      default: 30,
    },
    selectedVisibleCount: {
      type: Number,
      default: 5,
    },
    defaultValue: {
      type: Array,
      default: () => [],
    },
    searchFields: {
      type: Array,
      default: null,
    },
  },
  data: () => ({
    selected: [],
    search: "",
    is_filter: true,
    showList: false,
    selectedKey: null,
    expanded: [], // When 'Show more' is clicked inside values.
  }),
  computed: {
    tags() {
      const tags = {};
      for (let row of this.rows) {
        const key = row[this.tKeyColumn];
        const value = row[this.tValueColumn];
        if (this.search && !this.searchInObject(this.search, row)) continue;

        const selected = this.selected.filter((s) => {
          if (s.key === key.value) {
            return s.value === value.value;
          }
          return false;
        })[0];

        if (selected) {
          continue;
        }

        if (!tags[key.value]) {
          tags[key.value] = [value.value];
        } else {
          tags[key.value].push(value.value);
        }
      }

      return tags;
    },
  },
  methods: {
    onVisualizationInit() {
      const initial_value = this.getFilterValue("selected_items");
      let selected = [];
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
            selected = [...tags, ...selected];
          }
        } catch (error) {
          console.error(error);
          console.error("Failed to parse tags data");
        }
      } else if (this.defaultValue) {
        selected = [...this.defaultValue];
      }
      this.selected = selected;
      this.updateUrlValue();
    },
    selectValue(value) {
      this.selected.push({
        key: this.selectedKey,
        value,
      });
      this.close();
      this.updateUrlValue();
    },
    selectKey(key) {
      this.selectedKey = key;
      this.search = "";
    },
    removeTag(tag) {
      this.selected = this.selected.filter((s) => {
        if (s.key === tag.key) {
          return s.value !== tag.value;
        }
        return true;
      });
      this.updateUrlValue();
    },
    updateUrlValue() {
      const urlObject = {};
      for (let obj of this.selected) {
        if (urlObject[obj.key]) {
          urlObject[obj.key].push(obj.value);
        } else {
          urlObject[obj.key] = [obj.value];
        }
      }
      const urlValue = Object.keys(urlObject).length
        ? JSON.stringify(urlObject)
        : "";
      return this.setFilterValue("selected_items", urlValue);
    },
    removeFilter() {
      this.unsetFilterValue("selected_items");
    },
    open() {
      if (this.loading) {
        return false;
      }
      if (this.isSingleTag && !this.selectedKey) {
        const tagKeys = Object.keys(this.tags);
        if (tagKeys.length === 1) {
          this.selectedKey = tagKeys[0];
        }
      }
      this.showList = true;
    },
    close() {
      this.search = "";
      this.showList = false;
      this.expanded = [];
      if (!this.isSingleTag) {
        this.selectedKey = null;
      }
    },
    handleExpanded(key) {
      if (!this.expanded.includes(key)) {
        return this.expanded.push(key);
      }
      return (this.expanded = this.expanded.filter((k) => k !== key));
    },
    reset() {
      this.selected = [...this.defaultValue];
      this.updateUrlValue();
    },
    searchInObject(searchTerm, row) {
      const COLUMN_VALUE = "value";
      const lowercaseSearchFields = this.searchFields
        ? this.searchFields.map((field) => field.toLowerCase())
        : [];

      for (const column of Object.keys(row)) {
        if (
          !this.searchFields ||
          lowercaseSearchFields.includes(column.toLowerCase()) ||
          column.toLowerCase() === COLUMN_VALUE
        ) {
          const data = row[column];

          if (
            data?.value
              ?.toString()
              .toLowerCase()
              .includes(searchTerm.toLowerCase())
          ) {
            return true;
          }
        }
      }
      return false;
    },
    displayValue(value) {
      if (!value) {
        return "";
      }

      const row = this.rows.find((row) => {
        const columnValue = row[this.tValueColumn];
        return columnValue.value === value;
      });

      return row?.DISPLAYVALUE?.value || value;
    },

    displayKey(key) {
      if (!key) {
        return "";
      }

      const row = this.rows.find((row) => {
        const columnKey = row[this.tKeyColumn];
        return columnKey.value === key;
      });

      return row?.DISPLAYKEY?.value || key;
    },
  },
};
</script>
