<template>
  <div class="flex flex-col date-filter-container w-max">
    <label v-if="label" class="pb-[7px] text-sm font-medium">
      {{ label }}
    </label>
    <div class="inline-flex w-max">
      <div v-if="!hidePresets" class="relative">
        <t-dropdown>
          <div
            slot="handle"
            class="flex items-center justify-center gap-1 p-1 text-sm"
            :style="{ width: pickerMode === 'range' ? '167px' : '155px' }"
            @click="openPicker"
          >
            {{ presetValue }}
            <t-loading-spinner v-if="loading" position="relative" />
            <menu-down-icon v-else :size="20" />
          </div>
        </t-dropdown>
        <div v-if="pickerOpened" class="absolute top-[32px] w-max z-[99999]">
          <base-card
            :condensed="true"
            :style="{
              height: pickerMode === 'range' ? '370px' : '313px',
              width: pickerMode === 'range' ? '167.17px' : '155px',
            }"
            legacy
          >
            <div v-for="preset in presets[pickerMode]" :key="preset.key">
              <base-dropdown-menu-item
                :value="preset.label"
                :style="{
                  color: preset.key === datePreset ? '#145DEB' : 'black',
                }"
                @click="presetChange(preset)"
              />
            </div>
          </base-card>
        </div>
      </div>
      <div class="inline-block" :class="{ 'full-picker': !hidePresets }">
        <!-- Range Picker -->
        <div v-if="pickerMode == 'range'" class="flex items-center h-full">
          <div class="h-full" @click="pickerOpened = !pickerOpened">
            <a-range-picker
              class="relative h-full ant-calendar-filter"
              :allow-clear="false"
              dropdown-class-name="wld-date-picker w-20"
              :open="pickerOpened"
              :separator="separator"
              :format="dateFormat"
              :value="[startDate, endDate]"
              @change="onDateChange"
            >
              <template slot="renderExtraFooter">
                <div
                  style="padding: 2rem; padding-right: 1rem"
                  class="flex items-center justify-end"
                >
                  <div
                    class="flex content-center justify-end h-full gap-1 ml-1"
                  >
                    <button
                      class="bg-white border-[#C3C2CB] text-[#1C1C21] text-sm px-2 py-[5px] rounded-[4px]"
                      style="float: right"
                      @click="close"
                    >
                      Cancel
                    </button>
                    <button
                      class="bg-[#145DEB] border-[#145DEB] text-white text-sm px-2 py-[5px] rounded-[4px]"
                      style="float: right"
                      @click="apply"
                    >
                      Apply
                    </button>
                  </div>
                </div>
              </template>
            </a-range-picker>
          </div>
        </div>

        <!-- Date Picker -->
        <div
          v-else-if="pickerMode == 'single'"
          class="flex items-center h-full"
        >
          <div class="h-full" @click="pickerOpened = !pickerOpened">
            <a-date-picker
              v-model="date"
              :show-today="false"
              class="h-full ant-calendar-filter date-picker"
              :allow-clear="false"
              dropdown-class-name="wld-date-picker w-20"
              :format="dateFormat"
              :separator="separator"
              :open="pickerOpened"
              @change="onDateChange"
            >
              <template slot="renderExtraFooter">
                <div
                  class="flex content-center justify-end h-full gap-1 pb-2 pr-1 ml-1"
                >
                  <button
                    class="bg-white border-[#C3C2CB] text-[#1C1C21] text-sm px-2 py-[5px] rounded-[4px]"
                    style="float: right"
                    @click="close"
                  >
                    Cancel
                  </button>
                  <button
                    class="bg-[#145DEB] border-[#145DEB] text-white text-sm px-2 py-[5px] rounded-[4px]"
                    style="float: right"
                    @click="apply"
                  >
                    Apply
                  </button>
                </div>
              </template>
            </a-date-picker>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    dateFormat: {
      type: String,
      default: "MM/DD/YYYY",
    },
    label: String,
    hidePresets: Boolean,
    pickerMode: {
      type: String,
      default: "single",
    },
    separator: {
      type: String,
      default: "-",
    },
  },
  data() {
    return {
      startDate: null,
      endDate: null,
      date: null,
      pickerOpened: false,
      datePreset: null,
      is_filter: true,
      presets: {
        range: [
          { key: "yesterday", label: "Yesterday" },
          { key: "last7days", label: "Last 7 Days" },
          { key: "lastmonth", label: "Last Month" },
          { key: "last30days", label: "Last 30 Days" },
          { key: "last90days", label: "Last 90 Days" },
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
    };
  },
  computed: {
    presetValue() {
      const { presets, pickerMode, datePreset } = this;
      if (presets[pickerMode] && datePreset) {
        const preset = presets[pickerMode].filter(
          (p) => p.key === datePreset
        )[0];
        if (preset) return preset.label;
      }
      return "";
    },
  },
  methods: {
    close() {
      this.pickerOpened = false;

      // Reset values
      this.datePreset = this.getFilterValue("date_preset");
      this.startDate = Moment(this.getFilterValue("start_date"));
      this.endDate = Moment(this.getFilterValue("end_date"));
      this.date = Moment(this.getFilterValue("date"));
    },
    apply() {
      this.pickerOpened = false;
      if (this.pickerMode == "single") {
        this.setFilterValue("date", this.date.format("YYYY-MM-DD"), false);
      } else {
        this.setFilterValue(
          "start_date",
          this.startDate.format("YYYY-MM-DD"),
          false
        );
        this.setFilterValue(
          "end_date",
          this.endDate.format("YYYY-MM-DD"),
          false
        );
      }
      this.setFilterValue("date_preset", this.datePreset, false);
    },
    presetChange(event) {
      this.datePreset = event.key;
      if (this.pickerMode == "single") {
        this.handleSingleDates();
      } else {
        this.handleRangeDates();
      }
    },
    handleSingleDates() {
      const key = this.datePreset;
      if (key == "today") {
        this.date = Moment();
      } else if (key == "yesterday") {
        this.date = Moment().subtract(1, "days");
      } else if (key == "7DaysAgo") {
        this.date = Moment().subtract(7, "days");
      } else if (key == "30DaysAgo") {
        this.date = Moment().subtract(30, "days");
      } else if (key == "90DaysAgo") {
        this.date = Moment().subtract(90, "days");
      } else if (key == "yearAgo") {
        this.date = Moment().subtract(1, "year");
      }
    },
    handleRangeDates() {
      const key = this.datePreset;
      if (key == "yesterday") {
        this.startDate = Moment().subtract(1, "days");
        this.endDate = Moment().subtract(1, "days");
      } else if (key == "last7days") {
        this.startDate = Moment().subtract(7, "days");
        this.endDate = Moment().subtract(1, "days");
      } else if (key == "lastmonth") {
        this.startDate = Moment().subtract(1, "months").startOf("month");
        this.endDate = Moment().subtract(1, "months").endOf("month");
      } else if (key == "last30days") {
        this.startDate = Moment().subtract(30, "days");
        this.endDate = Moment().subtract(1, "days");
      } else if (key == "last90days") {
        this.startDate = Moment().subtract(90, "days");
        this.endDate = Moment().subtract(1, "days");
      } else if (key == "mtd") {
        this.startDate = Moment().startOf("month");
        this.endDate = Moment().subtract(1, "days");
      } else if (key == "ytd") {
        this.startDate = Moment().startOf("year");
        this.endDate = Moment().subtract(1, "days");
      }
    },
    onDateChange(event) {
      if (this.pickerMode == "single") {
        this.date = event;
      } else {
        this.startDate = event[0];
        this.endDate = event[1];
      }
      this.datePreset = "custom";
    },
    onVisualizationInit() {
      if (this.pickerMode === "single") {
        this.date = this.getFilterValue("date")
          ? Moment(this.getFilterValue("date"))
          : Moment();
        this.handleUrlPreset("single");
      } else if (this.pickerMode === "range") {
        this.startDate = this.getFilterValue("start_date")
          ? Moment(this.getFilterValue("start_date"))
          : Moment().subtract(1, "days");
        this.endDate = this.getFilterValue("end_date")
          ? Moment(this.getFilterValue("end_date"))
          : Moment().subtract(1, "days");
        this.datePreset = this.getFilterValue("date_preset");
        this.handleUrlPreset("range");
      }
    },
    openPicker() {
      if (this.loading) return;
      this.pickerOpened = !this.pickerOpened;
    },
    handleUrlPreset(type) {
      let urlPreset = this.datePreset;
      if (urlPreset) {
        // If url preset matches with pickerMode.
        urlPreset = this.presets[type].filter(
          (preset) => preset.key === this.datePreset
        )[0];
        urlPreset = urlPreset ? urlPreset.key : null;
      }
      this.datePreset = urlPreset || this.presets[type][0].key;
    },
  },
};
</script>

<style>
.wld-date-picker .ant-calendar-range,
.wld-date-picker .ant-calendar-picker-container-content {
  @apply !absolute !top-[35px];
}

.date-filter-container input {
  @apply !outline-none;
}

.full-picker .ant-calendar-filter .ant-calendar-picker-input {
  @apply !rounded !h-[30px] !border-[#C3C2CB] !text-[#555463] !bg-white;
}

.ant-calendar-picker-input.ant-input,
.ant-calendar-picker-input.ant-input {
  @apply h-full border text-sm text-center;
}

.ant-calendar-range .ant-calendar-selected-start-date .ant-calendar-date,
.ant-calendar-range .ant-calendar-selected-end-date .ant-calendar-date,
.ant-calendar-selected-day .ant-calendar-date,
.ant-calendar-range .ant-calendar-selected-start-date .ant-calendar-date:hover,
.ant-calendar-range .ant-calendar-selected-end-date .ant-calendar-date:hover {
  background: #145deb;
  border-color: #145deb;
  color: white;
}

.ant-calendar-today .ant-calendar-date {
  border-color: #145deb;
  color: black;
}

.ant-calendar-picker-input {
  background: #fff;
  height: 44px !important;
}

.ant-calendar {
  box-shadow: inset 0 0 0 1px #e5e8ed;
}

.ant-calendar-range-picker-separator {
  color: black;
}
</style>
