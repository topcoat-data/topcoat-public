<template>
  <t-dropdown
    :is-open="isOpen"
    :is-active="barMinValue && barMaxValue"
    @open="fetchLayerData"
  >
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
      <t-loading-spinner v-if="loading" class="py-2" position="relative" />
      <base-range-slider
        v-else
        :min="minValue"
        :max="maxValue"
        :step="step"
        :min-value="barMinValue"
        :max-value="barMaxValue"
        @input="update"
      />
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
    tMaxColumn: {
      type: String,
      default: "",
    },
    tMinColumn: {
      type: String,
      default: "",
    },
    step: {
      type: Number,
      default: 1,
    },
    isOpen: {
      type: Boolean,
      default: false,
    },
  },
  data: () => ({
    is_filter: true,
  }),
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
  mounted() {
    this.fetchLayerData();
  },
  methods: {
    update: window._.debounce(function (e) {
      if (e.minValue === e.min && e.maxValue == e.max) {
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
