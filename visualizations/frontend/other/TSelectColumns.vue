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
    <div class="min-w-[294px] min-h-[200px]">
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
      <div class="relative w-full p-2">
        <div class="search-input">
          <div
            class="rounded-full border border-[#145DEB] text-[#145DEB] flex items-center"
            v-if="!showTags"
          >
            <plus-icon :size="12" />
          </div>
          <input
            class="bg-transparent outline-none !text-black w-full"
            v-model="search"
            @focus="showTags = true"
            @blue="showTags = false"
          />
        </div>
        <div v-if="Object.keys(tags).length && showTags" class="p-2">
          <span v-if="Object.keys(selected).length" @click="reset">
            Reset
          </span>

          <!-- Show values -->
          <div v-if="selectedKey" class="flex flex-col gap-1">
            <span class="font-semibold">Select a {{ selectedKey }}</span>
            <div
              v-for="value of tags[selectedKey]"
              v-if="value.toLowerCase().includes(search.toLowerCase())"
              @click="selectValue(value)"
              class="p-1 hover:bg-[#F9F8FA]"
            >
              {{ value }}
            </div>
          </div>

          <!-- Show keys -->
          <div v-else class="flex flex-col gap-1">
            <span class="font-semibold">Select a key</span>
            <div
              v-for="key in Object.keys(tags)"
              v-if="key.toLowerCase().includes(search.toLowerCase())"
              @click="selectedKey = key"
              class="p-1 hover:bg-[#F9F8FA]"
            >
              {{ key }}
            </div>
          </div>
        </div>
        <div v-else>No tags selected</div>
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
    selectedKey: "",
    showTags: false,
  }),
  computed: {
    tags() {
      const tags = {};
      if (this.rows.length) {
        for (let row of this.rows) {
          const key = row[this.tKeyColumn];
          const value = row[this.tValueColumn];

          if (!tags[key.value]) {
            tags[key.value] = [value.value];
          } else {
            tags[key.value].push(value.value);
          }
        }
      }
      const keys = Object.keys(tags);
      if (keys.length === 1) {
        this.selectedKey = keys[0];
      }
      return tags;
    },
  },
  methods: {
    reset() {},
    selectValue(value) {
      if (Object.keys(this.tags).length > 1) {
        this.selectedKey = "";
      }
    },
  },
};
</script>
