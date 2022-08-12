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
                <div
                    v-for="preset in presets[mode]"
                    :key="preset.key"
                    :style="{ color: preset.key === selectedPreset.key ? '#1284e7' : '#73879c' }"
                    class="cursor-pointer"
                    @click="handlePreset(preset)"
                >
                    {{ preset.label }}
                </div>
            </div>

            <div slot="icon-clear"></div>
            <div slot="icon-calendar">
                <div class="flex items-center gap-1">
                    <reload-icon @click="handleReload" class="cursor-pointer" />
                    <close-icon @click="handleClear" class="cursor-pointer" />
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
            if (this.mode === "range") {
                const startDate = date[0];
                const endDate = date[1]
                this.setFilterValue("start_date", this.formatDate(startDate));
                this.setFilterValue("end_date", this.formatDate(endDate));
            } else {
                this.setFilterValue("date", this.formatDate(date));
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
                const date = [];
                const startDate = this.getFilterValue("start_date");
                const endDate = this.getFilterValue("end_date");

                if (startDate) {
                    date.push(new Date(startDate));
                }

                if (endDate) {
                    date.push(new Date(endDate));
                }

                this.date = date;
            } else {
                const date = this.getFilterValue("date");
                this.date = new Date(date);
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
            let startDate = new Date();
            let endDate = new Date();

            switch (preset) {
                case "last7days":
                    startDate = new Date(startDate.setDate(startDate.getDate() - 7));
                    endDate = new Date(endDate.setDate(endDate.getDate() - 1));
                    break;
                
                case "lastmonth":
                    const lastMonth = startDate.getMonth() - 1;
                    startDate.setMonth(lastMonth);
                    startDate.setDate(1); // First day of month
                    endDate.setMonth(lastMonth);

                    const lastDayOfMonth = new Date(endDate.getFullYear(), endDate.getMonth()+1, 0).getDate();
                    endDate.setDate(lastDayOfMonth); // Last day of month
                    break;
                
                case "last30days":
                    startDate = new Date(startDate.setDate(startDate.getDate() - 30));
                    endDate = new Date(endDate.setDate(endDate.getDate() - 1));
                    break;
                
                case "last90days":
                    startDate = new Date(startDate.setDate(startDate.getDate() - 90));
                    endDate = new Date(endDate.setDate(endDate.getDate() - 1));
                    break;
                
                case "mtd":
                    startDate.setDate(1);
                    break;
                
                case "ytd":
                    startDate.setMonth(0);
                    startDate.setDate(1);
                    break;
            }

            this.date = [startDate, endDate];
        },
        handleSingleDates(preset) {
            let date = new Date();
            switch(preset) {
                case "yesterday":
                    date.setDate(date.getDate() - 1);
                    break;

                case "7DaysAgo":
                    date.setDate(date.getDate() - 7);
                    break;

                case "30DaysAgo":
                    date.setDate(date.getDate() - 30);
                    break;
                
                case "90DaysAgo":
                    date.setDate(date.getDate() - 90);
                    break;
                
                case "yearAgo":
                    date.setDate(date.getDate() - 365);
                    break;
                
            }
            this.date = date;
        },
        handleClear() {
            this.date = [];
            this.selectedPreset = {};
            this.unsetFilterValue("start_date");
            this.unsetFilterValue("end_date");
            this.unsetFilterValue("date_preset");
            this.unsetFilterValue("date");
        },
        formatDate(dateValue) {
            const date = [];

            const dateObject = new Date(dateValue);
            let year = dateObject.getFullYear();

            let month = dateObject.getMonth() + 1;
            month = month < 10 ? ("0" + month) : month;

            let day = dateObject.getDate();
            day = day < 10 ? ("0" + day) : day;

            let formatItems = this.dateFormat.match(/(.)\1*/g);  // Formats the date-format like this ['YYYY', '-', 'MM', '-', 'DD']
            for (let item of formatItems) {
                if (item === "YYYY") {
                    date.push(year);
                } else if (item === "MM") {
                    date.push(month);
                } else if (item === "DD") {
                    date.push(day);
                } else {
                    // It's a seperator
                    date.push(item);
                }
            }
            return date.join("");
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