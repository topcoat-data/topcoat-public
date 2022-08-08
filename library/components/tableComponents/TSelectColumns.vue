<template>
  <t-dropdown
    :disable-handle-class="isExpanded"
    :is-active="checked.length ? true : false"
  >
    <!-- Handle -->
    <div
      slot="handle"
      class="flex items-center gap-1 p-1 text-sm font-medium"
      v-if="!isExpanded"
    >
      <view-column-outline size="20" />
      <span> Modify Columns </span>
      <menu-down-icon size="20" />
    </div>

    <!-- Popup Contents -->
    <div class="min-w-[294px]" attrs.slot="outside">
      <div
        class="
          px-[12px]
          pt-[16px]
          pb-[8px]
          flex
          justify-between
          items-center
          w-full
        "
      >
        <h6
          class="
            text-[10px] text-[#727184]
            font-semibold
            uppercase
            leading-[15px]
            tracking-widest
          "
        >
          Columns
        </h6>
        <span
          class="
            text-[#145DEB] text-[13px]
            cursor-pointer
            font-normal
            leading-[18px]
          "
          :class="checked.length ? 'text-[#145DEB]' : 'text-[#727184]'"
        >
          <span
            v-if="checked.length < filterableColumns.length"
            @click="selectAll"
          >
            Select All
          </span>
          <span v-else @click="deselectAll"> Reset </span>
        </span>
      </div>
      <div class="px-[8px] pt-[4px] pb-[6px] w-full">
        <ul class="max-h-[320px] overflow-auto">
          <li
            class="
              flex
              justify-between
              px-[8px]
              pb-[1px]
              text-sm
              cursor-pointer
              text-[#555463]
            "
            v-for="(item, index) in internalColumns"
            :key="index"
          >
            <div
              class="
                flex
                items-center
                justify-between
                w-full
                hover:text-[#1C1C21]
                leading-[16.41px]
              "
            >
              <base-checkbox
                class="!min-w-[200px]"
                :label="item.label"
                :value="item"
                v-model="checked"
              />
            </div>
          </li>
          <small v-if="!filterableColumns.length"> No items found </small>
        </ul>
      </div>
    </div>
  </t-dropdown>
</template>

<script>
export default {
  props: {
    filterableColumns: {
      type: Array,
      default() {
        return [];
      },
    },
    TLayer: {
      type: String,
    },
  },
  data: () => ({
    checked: [],
    search: "",
    isExpanded: false,
    internalColumns: [],
  }),
  mounted() {
    let initialSelection = this.getFilterState(this.urlParamName);
    if (initialSelection) initialSelection = initialSelection.split("|");

    this.filterableColumns.forEach((col) => {
      const label = col[0];
      let sqlColumns;
      if (typeof col[1] === "string") sqlColumns = [col[1]];
      else sqlColumns = col[1];
      const iCol = { label: label, sqlColumns: sqlColumns };
      this.internalColumns.push(iCol);
      if (initialSelection) {
        if (initialSelection.includes(label)) this.checked.push(iCol);
      } else if (col.length === 3 && col[2]) {
        this.checked.push(iCol);
      }
    });

    this.$emit("updateFilteredColumns", this.checked);
  },
  watch: {
    checked() {
      this.$emit("updateFilteredColumns", this.checked);
      if (this.checked.length === 0) {
        this.deleteFilter({ name: this.urlParamName });
      } else {
        const selectColumnLabels = this.checked.map((c) => c.label);
        this.setFilter({
          name: this.urlParamName,
          value: selectColumnLabels.join("|"),
          persist: false,
        });
      }
    },
  },
  computed: {
    urlParamName() {
      return this.TLayer + "cols";
    },
  },
  methods: {
    selectAll() {
      this.checked = [...this.internalColumns];
      const visibleColumnlabels = this.checked.map((c) => c.label);
    },
    deselectAll() {
      this.checked = [];
    },
  },
};
</script>

<style>
.nav-search .vue--search-input__field {
  @apply !rounded-3xl !bg-white !opacity-[0.5];
}
</style>