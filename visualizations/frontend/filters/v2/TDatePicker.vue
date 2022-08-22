<template>
    <div class="relative flex t-date-picker">
        <!-- Date Picker -->
        <base-date-picker
            read-only
            show-clear-button
            confirm
            confirm-text="Apply"
            v-model="date"
            ref="datePicker"
            :range="mode === 'range'"
            :format="dateFormat"
            :range-separator="seperator"
            @confirm="handleConfirm"
            @pick="setCustomPreset"
            @open="fetchLayerData"
        >
            <div class="presets-dropown" slot="sidebar">
                <button
                    v-for="preset in presets[mode]"
                    :key="preset.key"
                    :style="{ color: preset.key === selectedPreset.key ? '#1284e7' : '#73879c' }"
                    class="cursor-pointer"
                    @click="handlePreset(preset)"
                >
                    {{ preset.label }}
                </button>
            </div>

            <div slot="icon-clear"></div>
            <div slot="icon-calendar">
                <div class="flex items-center gap-1">
                    <button>
                        <reload-icon @click="handleReload" />
                    </button>
                    <button>
                        <close-icon @click="handleClear" />
                    </button>
                    <t-loading-spinner position="relative" slot="icon-calendar" v-if="loading" />
                    <span style="color: #1284e7" v-else>
                        <calendar-blank-outline-icon />
                    </span>
                </div>
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
    },
    computed: {
        mode() {
            if (this.$attrs['t-filter:start_date'] && this.$attrs['t-filter:end_date']) {
                return "range";
            }
            return "single";
        }
    },
    data: () => ({
        date: [],
        presets: {
            range: [
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
            ]
        },
        selectedPreset: {},
        is_filter: true,
    }),
    methods: {
        onVisualizationInit() {
            this.assignDatesFromFilters();
        },
        setCustomPreset() {
            this.selectedPreset = this.presets[this.mode].filter(p => p.key === "custom")[0];
        },
        handleConfirm(date) {
            // Url should always store date in a readable format to avoid failure on component load.
            if (this.mode === "range") {
                // Returns array
                const startDate = date[0];
                const endDate = date[1]
                this.setFilterValue("start_date", this.formatDate(startDate, "YYYY-MM-DD"));
                this.setFilterValue("end_date", this.formatDate(endDate, "YYYY-MM-DD"));
            } else {
                // Returns string
                this.setFilterValue("start_date", this.formatDate(date, "YYYY-MM-DD"));
            }
            this.setFilterValue("date_preset", this.selectedPreset.key);

        },
        handleReload() {
            this.assignDatesFromFilters();
            const preset = this.getFilterValue("date_preset");
            if (preset) {
                const presetObject = this.presets[this.mode].filter(p => p.key === preset)[0];
                this.selectedPreset = presetObject;
            }
        },
        assignDatesFromFilters() {
            if (this.mode === "range") {
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

            const preset = this.getFilterValue("date_preset");
            if (preset) {
                const presetObject = this.presets[this.mode].filter(p => p.key === preset)[0];
                this.selectedPreset = presetObject;
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
                    startDate = startDate.subtract(7, 'days');
					endDate = endDate.subtract(1, 'days');
                    break;
                
                case "lastmonth":
					startDate = startDate.subtract(1, 'months').startOf('month');
					endDate = endDate.subtract(1, 'months').endOf('month');
                    break;

                case "last30days":
					startDate = startDate.subtract(30, 'days');
					endDate = endDate.subtract(1, 'days');
                    break;
                
                case "last90days":
					startDate = startDate.subtract(90, 'days');
					endDate = endDate.subtract(1, 'days');
                    break;
                
                case "mtd":
                    startDate = startDate.startOf('month');
					endDate = endDate.subtract(1, 'days');
                    break;
                
                case "ytd":
					startDate = startDate.startOf('year');
					endDate = endDate.subtract(1, 'days');
                    break;
            }

            this.date = [
                startDate.toDate(),
                endDate.toDate(),
            ];
        },
        handleSingleDates(preset) {
            let date = window.Moment();
            switch(preset) {
                case "yesterday":
                    date = date.subtract(1, 'days');
                    break;

                case "7DaysAgo":
                    date = date.subtract(7, 'days');
                    break;

                case "30DaysAgo":
                    date = date.subtract(30, 'days')
                    break;
                
                case "90DaysAgo":
                    date = date.subtract(90, 'days')
                    break;
                
                case "yearAgo":
                    date = date.subtract(1, 'year')
                    break;
                
            }
            this.date = date.toDate();
        },
        handleClear() {
            this.date = [];
            this.selectedPreset = {};
            this.unsetFilterValue("start_date");
            this.unsetFilterValue("end_date");
            this.unsetFilterValue("date_preset");
        },
        formatDate(date, format=this.dateFormat) {
            return window.Moment(date).format(format);
        }
    },
}
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
</style>