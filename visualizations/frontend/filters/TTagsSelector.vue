<template>
  <t-dropdown
    :is-active="selected.length ? true : false"
    @open="fetchLayerData"
  >
    <!-- Handle -->
    <div slot="handle" class="flex items-center gap-1 p-1 text-sm font-medium">
      <div class="pl-1">
        <slot name="icon"></slot>
      </div>
      <div class="flex items-center">
        <span>{{ label }}</span>
      </div>

      <t-loading-spinner v-if="loading" position="relative" />
      <menu-down-icon v-else :size="20" />
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
        <div class="search-input" @click="showList = true">
          <div
            class="rounded-full border border-[#145DEB] text-[#145DEB] flex items-center"
          >
            <plus-icon :size="12" v-if="!showList" />
            <close-icon v-else :size="12" @click.stop="close" />
          </div>
          <input
            class="bg-transparent outline-none !text-black w-full"
            v-model="search"
          />
        </div>
        <div v-if="showList" class="p-2">
          <div class="min-h-[200px] max-h-[500px] overflow-auto">
            <!-- Show values -->
            <div v-if="selectedKey" class="flex flex-col gap-1">
              <span
                class="sticky top-0 left-0 w-full m-auto font-semibold text-left bg-white"
                >Select a {{ selectedKey }}</span
              >
              <div
                v-for="value of tags[selectedKey]"
                class="p-1 hover:bg-[#F9F8FA]"
              >
                <div @click="selectValue(value)" class="p-1 hover:bg-[#F9F8FA]">
                  {{ value }}
                </div>
              </div>
              <div v-if="!tags[selectedKey].length">Tags not found</div>
            </div>

            <!-- Show keys -->
            <div v-else class="flex flex-col gap-1">
              <span
                class="sticky top-0 left-0 w-full m-auto font-semibold text-left bg-white"
                >Select a key</span
              >
              <div
                v-for="key in Object.keys(tags)"
                @click="selectKey(key)"
                class="p-1 hover:bg-[#F9F8FA]"
              >
                {{ key }}
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
            <span class="font-semibold">{{ selectedTag.key }}</span>
            {{ selectedTag.value }}
            <close-icon :size="12" @click="removeTag(selectedTag)" />
          </div>
        </div>
        <div v-else class="p-2">No tags selected</div>
      </div>
      <div
        v-if="isDeletable"
        class="flex justify-end items-center border-t border-[#E4E3E8] p-2"
      >
        <div
          class="w-[34px] h-[32px] border border-[#B3B2BD] rounded flex items-center justify-center"
          @click="removeFilter"
        >
          ?
        </div>
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
    isDeletable: {
      type: Boolean,
      default: false,
    },
  },
  data: () => ({
    selected: [],
    search: "",
    is_filter: true,
    showList: false,
    selectedKey: null,
  }),
  computed: {
    tags() {
      const tags = {};
      for (let row of this.rows) {
        const key = row[this.tKeyColumn];
        const value = row[this.tValueColumn];

        if (
          !this.selectedKey &&
          !key.value.toLowerCase().includes(this.search.toLowerCase())
        ) {
          continue;
        }

        if (!value.value.toLowerCase().includes(this.search.toLowerCase())) {
          continue;
        }

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

      const keys = Object.keys(tags);
      if (keys.length === 1) {
        this.selectedKey = keys[0];
      }
      return tags;
    },
    urlParam() {
      for (let key of Object.keys(this.$attrs)) {
        if (key === "t-filter:selected_items") {
          return this.$attrs[key];
          break;
        }
      }
      return "";
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
      }
      this.selected = selected;
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
      if (!this.selected.length) {
        if (this.urlParam) {
          // Prevent reset button from removing filter.
          return this.setFilter({
            name: this.urlParam,
            value: "",
          });
        }
      }
      for (let obj of this.selected) {
        if (urlObject[obj.key]) {
          urlObject[obj.key].push(obj.value);
        } else {
          urlObject[obj.key] = [obj.value];
        }
      }
      return this.setFilterValue("selected_items", JSON.stringify(urlObject));
    },
    removeFilter() {
      this.unsetFilterValue("selected_items");
    },
    close() {
      this.selectedKey = "";
      this.search = "";
      this.showList = false;
    },
  },
};
</script>
