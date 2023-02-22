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
          <reload-icon
            :size="12"
            @click="removeFilter"
            v-if="isReloadIconVisible"
          />
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
        @input="handleSlider"
      />
      <div class="flex items-center justify-between px-2">
        <small>Min: {{ minValue }}</small>
        <small>Max: {{ maxValue }}</small>
      </div>
      <div class="flex items-center justify-between gap-2 px-2 pb-2">
        <t-tooltip position="right" width="155px">
          <div
            slot="trigger"
            class="flex items-center justify-between gap-1 border rounded"
            :class="
              focusedInput === 'min'
                ? 'border-[#145DEB] text-[#145DEB]'
                : 'border-[#B3B2BD]'
            "
          >
            <input
              type="number"
              class="p-2 border-none outline-none h-full rounded text-[#555463]"
              :value="barMinValue"
              @keyup.enter="update($event, 'min')"
              @focus="focusedInput = 'min'"
              @blur="focusedInput = null"
            />
            <span
              class="px-2 pt-1"
              :class="focusedInput === 'min' ? 'opacity-100' : 'opacity-0'"
              >↵</span
            >
          </div>
          <span>Press enter to confirm</span>
        </t-tooltip>
        -
        <t-tooltip position="left" width="155px">
          <div
            slot="trigger"
            class="flex items-center justify-between gap-1 border rounded"
            :class="
              focusedInput === 'max'
                ? 'border-[#145DEB] text-[#145DEB]'
                : 'border-[#B3B2BD]'
            "
          >
            <input
              type="number"
              class="p-2 border-none outline-none h-full rounded text-[#555463]"
              :value="barMaxValue"
              @keyup.enter="update($event, 'max')"
              @focus="focusedInput = 'max'"
              @blur="focusedInput = null"
            />
            <span
              class="px-2 pt-1"
              :class="focusedInput === 'max' ? 'opacity-100' : 'opacity-0'"
              >↵</span
            >
          </div>
          <span>Press enter to confirm</span>
        </t-tooltip>
      </div>
    </div>
    <div v-if="$slots['footer']" class="p-2 border-t border-[#E4E3E8]">
      <slot name="footer"></slot>
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
    focusedInput: null,
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
        this.setFilterValue("min", val);
        return val;
      },
    },
    barMaxValue: {
      get() {
        const maxInternal = this.getFilterValue("max");
        return maxInternal ? parseInt(maxInternal) : this.maxValue;
      },
      set(val) {
        this.setFilterValue("max", val);
        return val;
      },
    },
    isReloadIconVisible() {
      if (
        this.barMinValue != this.minValue ||
        this.barMaxValue != this.maxValue
      ) {
        return true;
      }
      return false;
    },
  },
  mounted() {
    this.fetchLayerData();
  },
  methods: {
    handleSlider(e, type = null) {
      this.triggerCaption(true);
      this.update(e, type);
    },
    update: window._.debounce(function (e, type = null) {
      this.triggerCaption();
      if (type) {
        this.handleInputs(e.target.value, type);
        return;
      }

      this.barMinValue = e.minValue;
      this.barMaxValue = e.maxValue;
    }, 250),
    removeFilter() {
      this.unsetFilterValue("min");
      this.unsetFilterValue("max");
    },
    handleInputs(value, type) {
      if (!["max", "min"].includes(type)) {
        return;
      }

      if (type === "min") {
        if (value >= this.barMaxValue) {
          value = this.barMaxValue - 1;
        } else if (value < this.minValue) {
          value = this.minValue;
        }
        this.barMinValue = value;
        return;
      }

      if (value <= this.barMinValue) {
        value = this.barMinValue + 1;
      } else if (value > this.maxValue) {
        value = this.maxValue;
      }
      this.barMaxValue = value;
    },
    triggerCaption(show = false) {
      const element = document.querySelectorAll(".multi-range-slider .caption");
      element.forEach((e) => {
        e.style.display = show ? "flex" : "none";
      });
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

/* Hide input number arrows */
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type="number"] {
  -moz-appearance: textfield;
}
</style>
