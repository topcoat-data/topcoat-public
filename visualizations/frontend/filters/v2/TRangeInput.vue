<template>
    <t-loading-spinner position="relative" v-if="loading" />
    <div class="flex flex-col overflow-x-hidden t-range-slider" v-else>
        <label class="pb-[7px] px-3 text-sm font-medium" v-if="label">
            {{ label }}
        </label>
        <base-range-slider
            :min="minValue"
            :max="maxValue"
            :step="step"
            :minValue="barMinValue"
            :maxValue="barMaxValue"
            @input="update"
        />
    </div>
</template>

<script>
    export default {
        data: () => ({
            is_filter: true,
            throttleId: null,
        }),
        props: {
            label: {
                default: '',
            },
            tMaxColumn: {
                default: '',
            },
            tMinColumn: {
                default: '',
            },
            step: {
                default: 1,
            }
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
                    if (item[this.tMinColumn]) {
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
                    this.setFilterValue('min', val, true);
                    return val;
                }
            },
            barMaxValue: {
                get() {
                    const maxInternal = this.getFilterValue("max");
                    return maxInternal ? parseInt(maxInternal) : this.maxValue;
                },
                set(val) {
                    this.setFilterValue('max', val, true);
                    return val;
                }
            }
        },
        methods: {
            update(e) {
                if (this.throttleId) {
                    clearTimeout(this.throttleId);
                }

                this.throttleId = setTimeout(() => {
                    if (e.minValue === e.min && e.maxValue == e.max) {
                        this.unsetFilterValue('min');
                        this.unsetFilterValue('max');
                    } else {
                        this.barMinValue = e.minValue;
                        this.barMaxValue = e.maxValue;
                    }      
                }, 250)
            },
        },
        mounted() {
            this.fetchLayerData();
        },
    }
</script>

<style>
    /* Override default look  */
    .t-range-slider .ruler, .labels { display: none !important; }
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