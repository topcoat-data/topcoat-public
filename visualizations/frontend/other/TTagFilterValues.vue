<template>
  <t-loading-spinner v-if="loading && !tUrlParam" position="relative" />
  <div v-else-if="Object.keys(items).length">
    <t-grids v-if="isList" column-count="4" gap-x="8">
      <div
        v-if="label"
        class="flex-wrap text-base font-semibold whitespace-nowrap h-max"
      >
        {{ label }}
      </div>
      <div
        class="relative flex flex-col flex-wrap items-start w-full col-span-3 text-base gap-x-1 whitespace-nowrap"
        :style="{ color: textColor }"
      >
        <div
          v-for="(key, index) in Object.keys(items)"
          :key="key"
          class="border-b border-[#D3D3D9] w-full text-sm flex gap-1 items-center"
          :class="index == 0 ? 'pb-2' : 'py-2'"
        >
          <b>{{ key }}: </b>
          <div class="flex flex-wrap items-center gap-1">
            <base-chip v-for="tItem of items[key]" :key="tItem" :text="tItem" />
          </div>
        </div>
        <span v-if="truncatedItemsCount" class="text-[#A2A1AF] py-2 text-sm">
          &nbsp;+ {{ truncatedItemsCount }} more {{ label }}
        </span>
      </div>
    </t-grids>

    <t-grids v-else column-count="2" gap-x="8">
      <div
        v-if="label"
        class="flex-wrap text-base font-semibold whitespace-nowrap h-max"
      >
        {{ label }}
      </div>
      <div
        class="relative flex flex-col flex-wrap items-start justify-start gap-1 text-base whitespace-nowrap"
        :style="{ color: textColor }"
      >
        <div
          v-for="(key, index) in Object.keys(items)"
          :key="key"
          class="flex gap-1"
        >
          <b>{{ key }}:</b>
          <div class="flex flex-wrap items-center gap-1">
            <base-chip
              v-for="(tItem, tIndex) of items[key]"
              :key="tItem"
              :text="tItem"
            />
          </div>
        </div>
        <span v-if="truncatedItemsCount" class="text-[#A2A1AF] py-2">
          &nbsp;+ {{ truncatedItemsCount }} more {{ label }}
        </span>
      </div>
    </t-grids>
  </div>
  <div v-else>-</div>
</template>

<script>
export default {
  props: {
    label: String,
    tKeyColumn: {
      type: String,
      default: "",
    },
    tValueColumn: {
      type: String,
      default: "",
    },
    visibleItemsCount: {
      type: Number,
      default: -1,
    },
    textColor: {
      type: String,
      default: "#555463",
    },
    isList: {
      type: Boolean,
      default: false,
    },
    tUrlParam: {
      type: String,
      default: "",
    },
  },
  data: () => ({
    is_filter: true,
    truncatedItemsCount: 0,
  }),
  computed: {
    keys() {
      if (this.tKeyColumn) {
        return this.getColumn(this.tKeyColumn);
      }
      return [];
    },
    items() {
      // If direct values from url are needed (good for cases where id===label inside url)
      // This approach is way faster as it does not require t-layer.

      // Todo: Clean code and make it simple
      let keys = [...new Set(this.keys)];
      const urlVal = new URLSearchParams(window.location.search).get(
        this.tUrlParam
      );
      const urlItems = urlVal ? urlVal.split("|") : [];
      if (this.tUrlParam) {
        if (urlVal) {
          let urlKeys = urlItems.map((item) => {
            let split = item.split("_");
            return split.length > 1 ? split[1] : split[0];
          });
          keys = [...new Set(urlKeys)];
        }
      }
      const items = {};
      const selectedItems = this.tUrlParam
        ? urlItems
        : this.urlValue.split("|");

      let truncatedItems = 0;
      let addedItems = 0;

      for (let key of keys) {
        if (
          this.visibleItemsCount > -1 &&
          Object.keys(items).length === this.visibleItemsCount
        ) {
          truncatedItems = selectedItems.length - addedItems;
          break;
        }

        for (let sItem of selectedItems) {
          const split = sItem.split("_");
          const k = split.length > 1 ? split[1] : split[0];
          if (k === key) {
            if (items[key]) {
              items[key].push(split[0]);
            } else {
              items[key] = [split[0]];
            }
          }
        }

        addedItems += 1;
      }
      this.truncatedItemsCount = truncatedItems;
      return items;
    },
    urlValue() {
      return this.getFilterValue("selected_items");
    },
  },
};
</script>
