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
            v-if="checked.length < modifiableColumns.length"
            @click="selectAll"
          >
            Select All
          </span>
          <span v-else @click="reset"> Reset </span>
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
          <small v-if="!modifiableColumns.length"> No items found </small>
        </ul>
      </div>
    </div>
  </t-dropdown>
</template>

<script>
export default {
  name: "TSelectColumns",
  props: {
    modifiableColumns: {
      type: Array,
      default() {
        return [];
      },
    },
    TLayer: {
      type: String,
    },
    urlFilter: {
      type: String,
    }
  },
  data: () => ({
    checked: [],
    search: "",
    isExpanded: false,
    internalColumns: [],
  }),
  watch: {
    urlFilter(){
      this.modifiableColumns.forEach((col) => {
        const label = col.displayColumn;
        const iCol = { label: label, sqlColumns: col.layerColumns };
        this.internalColumns.push(iCol);
        if (this.urlFilter && this.urlFilter.length > 0) {
          if (this.urlFilter.includes(label)) this.checked.push(iCol);
        } else if (col.displayByDefault) {
          this.checked.push(iCol);
        }
      });
      this.$emit("updateFilteredColumns", this.checked);
    },
    checked() {
      this.updateChecked()
    },
  },
  computed: {
    urlParamName() {
      return `${this.TLayer}_cols`;
    },
  },
  methods: {
    selectAll() {
      this.checked = [...this.internalColumns];
      const visibleColumnlabels = this.checked.map((c) => c.label);
    },
    reset() {
      this.checked = []
      this.modifiableColumns.forEach((col) => {
        const label = col.displayColumn;
        const iCol = { label: label, sqlColumns: col.layerColumns };
        this.internalColumns.push(iCol);
        if (col.displayByDefault) {
          this.checked.push(iCol);
        }
      });
      this.$emit("updateFilteredColumns", this.checked);
    },
    updateChecked: _.debounce(function(){
      this.$emit("updateFilteredColumns", this.checked);
      const selectColumnLabels = this.checked.map((c) => c.label);
      this.setFilter({
        name: this.urlParamName,
        value: selectColumnLabels.join("|"),
        persist: false,
      });
    }, 750),
  },
};
</script>

<style>
.nav-search .vue--search-input__field {
  @apply !rounded-3xl !bg-white !opacity-[0.5];
}
</style>