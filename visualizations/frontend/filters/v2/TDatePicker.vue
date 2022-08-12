<template>
    <div class="relative flex t-date-picker">
        <!-- Date Picker -->
        {{ selectedPreset }}
        <base-date-picker
            show-clear-button
            confirm
            confirm-text="Apply"
            v-model="date"
            ref="datePicker"
            :range="true"
            :format="dateFormat"
            :range-separator="seperator"
            @confirm="handleConfirm"
            @close="handleClose"
            @pick="handleDateButtonsClicked"
            @open="fetchLayerData"
        >
            <div class="presets-dropown" slot="sidebar">
                <div
                    v-for="preset in presets[mode]"
                    :key="preset.key"
                    :style="{ color: preset.key === selectedPreset.key ? '#1284e7' : '#73879c' }"
                    class="cursor-pointer"
                    @click="changePreset(preset)"
                >
                    {{ preset.label }}
                </div>
            </div>

            <t-loading-spinner slot="icon-calendar" v-if="loading" />
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
        hasPresetButton: {
            type: Boolean,
            default: false,
        },
        mode: {
            type: String,
            default: "range",
        }
    },
    data: () => ({
        date: [],
        previousDate: [],
        previousPreset: {},
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
            const startDate = this.getFilterValue("start_date");

            if (startDate) {
                this.date.push(new Date(startDate));
            }

            if (this.mode === "range") {
                const endDate = this.getFilterValue("end_date");
                if (endDate) {
                    this.date.push(new Date(endDate));
                }
            }
        },
        handleDateButtonsClicked() {
            this.selectedPreset = { key: "custom", label: "Custom Date" };
        },
        handleConfirm(date) {
            console.log(date)
            const startDate = date[0].toISOString().slice(0,10);
            if (startDate) {
                this.setFilterValue("start_date", startDate);
            }
            if (this.mode === "range") {
                const endDate = date.length > 1 ? date[1].toISOString().slice(0,10) : null;
                if (endDate) {
                    this.setFilterValue("end_date", endDate);
                }
            }
            
        },
        handleClose() {
            // Revert to previous date if closed without clicking Apply
            console.log(this.filters)
            // this.date = this.previousDate;
        },
        changePreset(preset) {
            if (this.mode === "range") {
                this.handleRangeDates(preset);
            } else {
                
            }
        },
        handleRangeDates(preset) {
            let startDate = new Date();
            let endDate = new Date();
            
            switch (preset.key) {
                case "last7days":
                    startDate = new Date(startDate.setDate(startDate.getDate() - 7));
                    endDate = new Date(endDate.setDate(endDate.getDate() - 1));
                    break;
            }

            this.date = [startDate, endDate];
            this.selectedPreset = preset;
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
</style>