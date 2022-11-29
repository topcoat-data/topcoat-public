<template>
  <div class="relative flex t-date-picker">
    <!-- Date Picker -->
    <div class="flex items-center text-sm font-medium" v-if="label">
      {{ label }}: &nbsp;
    </div>
    <base-date-picker
      ref="datePicker"
      v-model="date"
      confirm
      confirm-text="Apply"
      :range="mode === 'range'"
      :format="dateFormat"
      :range-separator="seperator"
      :class="relativePreset && 'w-auto'"
      @confirm="handleConfirm"
      @pick="setCustomPreset"
      @open="fetchLayerData"
    >
      <div
        v-if="relativePreset"
        slot="input"
        class="border border-[#C3C2CB] py-1 px-2 bg-white cursor-pointer rounded-[4px] font-medium"
      >
        <div class="flex items-center gap-1 w-max">
          <calendar-blank-outline-icon class="text-[16px]" />
          {{ relativePreset.label }}
          <button v-if="!isRequired" @click="handleClear">
            <close-icon title="clear date selection" />
          </button>
          <menu-down-icon class="text-[20px]" />
        </div>
      </div>
      <div slot="sidebar" class="presets-dropown">
        <button
          v-for="preset in presets[mode]"
          :key="preset.key"
          :style="{
            color: preset.key === selectedPreset.key ? '#1284e7' : '#73879c',
          }"
          class="cursor-pointer"
          @click="handlePreset(preset)"
        >
          {{ preset.label }}
        </button>
      </div>

      <!-- To hide default clear icon -->
      <div slot="icon-clear"></div>

      <div v-if="!relativePreset" slot="icon-calendar">
        <div class="flex items-center gap-1">
          <t-loading-spinner v-if="loading" position="relative" />
          <button v-if="!isRequired" @click="handleClear">
            <close-icon />
          </button>
          <calendar-blank-outline-icon />
        </div>
      </div>

      <!-- To hide default calendar icon when preset is selected -->
      <div v-else slot="icon-calendar"></div>

      <div
        v-if="$slots['footer']"
        slot="footer"
        class="flex items-center h-max"
      >
        <slot name="footer"></slot>
      </div>
    </base-date-picker>
  </div>
</template>

<script>
export default {
  props: {
    dateFormat: {
      type: String,
      default: "YYYY-MM-DD",
      // Fromat tokens are inspired from moment.js style formatting.
    },
    placeholder: {
      type: String,
      default: "",
    },
    seperator: {
      type: String,
      default: " ~ ",
    },
    defaultStartDate: {
      type: String,
      default: "",
    },
    defaultEndDate: {
      type: String,
      default: "",
    },
    defaultDatePreset: {
      type: String,
      default: "",
    },
    isRequired: {
      type: Boolean,
      default: false,
    },
    label: {
      type: String,
      default: "",
    },
  },
  data: () => ({
    date: [],
    presets: {
      range: [
        { key: "last7days", label: "Last 7 Days" },
        { key: "lastmonth", label: "Last Month" },
        { key: "last30days", label: "Last 30 Days" },
        { key: "last90days", label: "Last 90 Days" },
        { key: "last365days", label: "Last 365 Days" },
        { key: "mtd", label: "Month to Date" },
        { key: "ytd", label: "Year to Date" },
        { key: "custom", label: "Custom Range" },
      ],
      single: [
        { key: "today", label: "Today" },
        { key: "yesterday", label: "Yesterday" },
        { key: "7DaysAgo", label: "7 Days Ago" },
        { key: "30DaysAgo", label: "30 Days Ago" },
        { key: "90DaysAgo", label: "90 Days Ago" },
        { key: "yearAgo", label: "A Year Ago" },
        { key: "custom", label: "Custom Date" },
      ],
    },
    selectedPreset: {},
    is_filter: true,
  }),
  computed: {
    mode() {
      if (
        this.$attrs["t-filter:start_date"] &&
        this.$attrs["t-filter:end_date"]
      ) {
        return "range";
      }
      return "single";
    },
    relativePreset() {
      const preset = this.getFilterValue("date_preset");
      if (preset === "custom") {
        return null;
      }
      return this.presets[this.mode].filter((p) => p.key === preset)[0];
    },
  },
  methods: {
    onVisualizationInit() {
      this.assignDatesFromFilters();
      this.handleDefaults();
    },
    setCustomPreset() {
      this.selectedPreset = this.presets[this.mode].filter(
        (p) => p.key === "custom"
      )[0];
    },
    handleConfirm(date) {
      // Url should always store date in a readable format to avoid failure on component load.
      if (this.mode === "range") {
        // Returns array
        const startDate = date[0];
        const endDate = date[1];
        this.setFilterValue(
          "start_date",
          this.formatDate(startDate, "YYYY-MM-DD")
        );
        this.setFilterValue("end_date", this.formatDate(endDate, "YYYY-MM-DD"));
      } else {
        // Returns string
        this.setFilterValue("start_date", this.formatDate(date, "YYYY-MM-DD"));
      }
      this.setFilterValue("date_preset", this.selectedPreset.key);
    },
    assignDatesFromFilters() {
      const preset = this.getFilterValue("date_preset");
      if (preset) {
        const presetObject = this.presets[this.mode].filter(
          (p) => p.key === preset
        )[0];
        this.selectedPreset = presetObject;

        if (presetObject.key !== "custom") {
          // If relative date, use the date assigned by preset.
          this.handlePreset(presetObject);
          this.handleConfirm(this.date);
          return;
        }
      }

      // If absolute date is set, use the date from url parameter.
      if (this.mode === "range") {
        this.date = [];

        const startDate = this.getFilterValue("start_date");
        const endDate = this.getFilterValue("end_date");

        if (startDate) {
          this.date.push(window.Moment(startDate).toDate());
        }

        if (endDate) {
          this.date.push(window.Moment(endDate).toDate());
        }
      } else {
        const date = this.getFilterValue("start_date");
        if (date) {
          this.date = window.Moment(date).toDate();
        }
      }
    },
    handlePreset(preset) {
      if (this.mode === "range") {
        this.handleRangeDates(preset.key);
      } else {
        this.handleSingleDates(preset.key);
      }
      this.selectedPreset = preset;
    },
    handleRangeDates(preset) {
      let startDate = window.Moment();
      let endDate = window.Moment();

      switch (preset) {
        case "last7days":
          startDate = startDate.subtract(7, "days");
          break;

        case "lastmonth":
          startDate = startDate.subtract(1, "months").startOf("month");
          endDate = endDate.subtract(1, "months").endOf("month");
          break;

        case "last30days":
          startDate = startDate.subtract(30, "days");
          break;

        case "last90days":
          startDate = startDate.subtract(90, "days");
          break;

        case "last365days":
          startDate = startDate.subtract(365, "days");
          break;

        case "mtd":
          startDate = startDate.startOf("month");
          break;

        case "ytd":
          startDate = startDate.startOf("year");
          break;
      }

      this.date = [startDate.toDate(), endDate.toDate()];
    },
    handleSingleDates(preset) {
      let date = window.Moment();
      switch (preset) {
        case "yesterday":
          date = date.subtract(1, "days");
          break;

        case "7DaysAgo":
          date = date.subtract(7, "days");
          break;

        case "30DaysAgo":
          date = date.subtract(30, "days");
          break;

        case "90DaysAgo":
          date = date.subtract(90, "days");
          break;

        case "yearAgo":
          date = date.subtract(1, "year");
          break;
      }
      this.date = date.toDate();
    },
    handleClear() {
      this.date = [];
      this.selectedPreset = {};
      for (const [attribute, name] of Object.entries(this.$attrs)) {
        if (attribute.includes("t-filter:")) {
          this.deleteFilter({ name });
        }
      }
    },
    formatDate(date, format = this.dateFormat) {
      return window.Moment(date).format(format);
    },
    handleDefaults() {
      const urlPreset = this.getFilterValue("date_preset");

      // Handle Preset, override dates.
      if (!urlPreset && this.defaultDatePreset) {
        // If preset used, skip start and end dates default
        return this.handleDefaultPreset();
      }

      return this.handleDefaultDates();
    },
    handleDefaultPreset() {
      const defaultPreset = this.presets[this.mode].filter((p) => {
        return (
          p.key === this.defaultDatePreset || p.label === this.defaultDatePreset
        );
      })[0];

      if (defaultPreset) {
        this.handlePreset(defaultPreset);
        this.handleConfirm(this.date);
      }
    },
    handleDefaultDates() {
      const urlStartDate = this.getFilterValue("start_date");
      const urlEndDate = this.getFilterValue("end_date");

      if (urlStartDate || urlEndDate) {
        return;
      }

      const defaultStartDate = this.defaultStartDate;
      const defaultEndDate = this.defaultEndDate || defaultStartDate; // If no end date default, set same as start to avoid error.

      if (defaultStartDate && defaultEndDate) {
        const date = [
          window.Moment(defaultStartDate).toDate(),
          window.Moment(defaultEndDate).toDate(),
        ];

        this.date = this.mode === "range" ? date : date[0];
        const preset = this.presets.range.filter((p) => p.key === "custom")[0];

        this.selectedPreset = preset;
        this.handleConfirm(this.date);
      }
    },
  },
};
</script>

<style>
.mx-datepicker-sidebar {
  width: 150px;
  text-align: left;
}

.mx-datepicker-sidebar .presets-dropown {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 10px;
}

.mx-datepicker-content {
  margin-left: 153px !important;
}

.mx-icon-calendar {
  display: block !important;
}

.mx-datepicker-footer {
  display: flex;
  justify-content: end;
  gap: 10px;
}

.mx-datepicker-btn-confirm {
  border-color: #b3b2bd !important;
}
</style>
