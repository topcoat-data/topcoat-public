<template>
  <t-dropdown @open="fetchLayerData" :is-active="barMinValue && barMaxValue">
    <div slot="handle" class="flex items-center gap-1 p-1 text-sm font-medium">
      <div class="pl-1">
        <slot name="icon"></slot>
      </div>
      <div class="flex items-center">
        <span>{{ label }}</span>
        <div
          v-if="barMinValue && barMaxValue"
          class="flex items-center gap-1 font-normal"
        >
          : {{ barMinValue }}-{{ barMaxValue }}
          <close-icon :size="12" @click="removeFilter" />
        </div>
      </div>
      <t-loading-spinner v-if="loading" position="relative" />
      <menu-down-icon v-else :size="20" />
    </div>
    <div class="flex flex-col overflow-x-hidden t-range-slider min-w-[294px]">
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
      <t-loading-spinner class="py-2" v-if="loading" position="relative" />
      <base-range-slider
        v-else
        :min="minValue"
        :max="maxValue"
        :step="step"
        :minValue="barMinValue"
        :maxValue="barMaxValue"
        @input="update"
      />
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
  data: () => ({
    is_filter: true,
  }),
  props: {
    label: {
      default: "",
    },
    tMaxColumn: {
      default: "",
    },
    tMinColumn: {
      default: "",
    },
    step: {
      default: 1,
    },
    isDeletable: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    minValue() {
      const item = this.rows.length ? this.rows[0] : null;
      if (item) {
        if (item[this.tMinColumn]) {
          return item[this.tMinColumn].value;
        }
      }
      return 0;
    },
    maxValue() {
      const item = this.rows.length ? this.rows[0] : null;
      if (item) {
        if (item[this.tMaxColumn]) {
          return item[this.tMaxColumn].value;
        }
      }
      return 100;
    },
    barMinValue: {
      get() {
        const minInternal = this.getFilterValue("min");
        return minInternal ? parseInt(minInternal) : this.minValue;
      },
      set(val) {
        this.setFilterValue("min", val, true);
        return val;
      },
    },
    barMaxValue: {
      get() {
        const maxInternal = this.getFilterValue("max");
        return maxInternal ? parseInt(maxInternal) : this.maxValue;
      },
      set(val) {
        this.setFilterValue("max", val, true);
        return val;
      },
    },
  },
  methods: {
    update: window._.debounce(function (e) {
      if (e.minValue === e.min && e.maxValue == e.max && !this.isDeletable) {
        this.removeFilter();
      } else {
        this.barMinValue = e.minValue;
        this.barMaxValue = e.maxValue;
      }
    }, 250),
    removeFilter() {
      this.unsetFilterValue("min");
      this.unsetFilterValue("max");
    },
  },
  mounted() {
    this.fetchLayerData();
  },
};
</script>

<style>
/* Override default look  */
.t-range-slider .ruler,
.labels {
  display: none !important;
}
.t-range-slider .multi-range-slider .bar .bar-inner {
  background-color: gray;
}
.t-range-slider .multi-range-slider {
  border: none;
  box-shadow: none;
  padding: 40px 20px 10px 14px;
}
.t-range-slider .multi-range-slider .bar-left,
.t-range-slider .multi-range-slider .bar-right {
  box-shadow: none;
  background: #cac8c8;
}
.t-range-slider .multi-range-slider .thumb::before {
  box-shadow: none;
}
.t-range-slider .multi-range-slider .caption {
  bottom: 31px;
}
</style>
