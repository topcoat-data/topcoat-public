<template>
    <div
        class="w-full lg:p-5 md:p-3 p-1 rounded-[2px] break-all"
        :style="{ background: bgColor, color: textColor }"
        :class="hasUnderline && 'border-b-2 border-[#21214c]'"
    >
        <div class="flex items-center gap-2">
            <div class="hidden opacity-50 md:block" v-if="hasIcon">
                <slot name="icon"></slot>
            </div>
            <span class="text-xs font-semibold leading-4 tracking-widest">
                {{ label || '--' }}
            </span>
            <base-tooltip v-if="tooltipText" :description="tooltipText" />
        </div>
        <div :class="hasTallSize ? 'mt-6' : 'mt-3'">
            <span class="font-normal leading-8" :class="fontSizes[bigNumberSize]">
                <div class="flex items-center gap-2">
                    <span>{{ value || '--' }}</span>
                    {{ valueText }}
                    <div v-if="previous">
                        <span class="opacity-80" v-if="num(value) > num(previous)">
                            <arrow-up-icon :size="18" />
                        </span>
                        <span class="opacity-80" v-else-if="num(value) < num(previous)">
                            <arrow-down-icon :size="18" class="opacity-90" />
                        </span>
                        <div class="opacity-30" v-else>-</div>
                    </div>
                    <t-loading-spinner position="relative" v-if="loading && !numberValue" />
                </div>
            </span>
        </div>
        <div v-if="previous" class="flex items-center gap-1 mt-3">
            <div class="font-semibold">
                {{ previous }} {{ previousText }}
            </div>
            <div class="flex gap-2 opacity-80" v-if="percentage">
                {{ percentage }} {{ percentageText }}
            </div>
            <div v-else class="opacity-80">
                {{ noChangeText }}
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        props: {
            bgColor: {
                type: String,
                default: 'transparent'
            },
            bigNumberSize: {
                type: String,
                default: 'medium',
                validator: v => ['small', 'medium', 'big'].includes(v),
            },
            dataLoading: {
                type: Boolean,
                default: false,
            },
            numberValue: {
                type: String,
                default: '',
            },
            numberPrevious: {
                type: String,
                default: '',
            },
            label: {
                type: String,
                default: '',
            },
            textColor: {
                type: String,
                default: '#393842'
            },
            tValueColumn: {
                type: String,
                default: '',
            },
            tPreviousColumn: {
                type: String,
                default: '',
            },
            valueText: {
                type: String,
                default: '',
            },
            previousText: {
                type: String,
                default: '',
            },
            percentageText: {
                type: String,
                default: 'previous period',
            },
            noChangeText: {
                type: String,
                default: 'No change',
            },
            tooltipText: {
                type: String,
                default: '',
            },
            hasUnderline: {
                type: Boolean,
                default: false,
            },
            hasTallSize: {
                type: Boolean,
                default: false,
            }
        },
        data: () => ({
            is_filter: true,
            fontSizes: {
                small: 'lg:text-3xl md:text-2xl sm:text-lg',
                medium: 'lg:text-[2.5rem] md:text-3xl sm:text-2xl',
                big: 'lg:text-5xl md:text-4xl sm:text-3xl',
            },
        }),
        computed: {
            hasIcon() {
                return this.$slots.icon;
            },
            value() {
                if (this.numberValue) return this.numberValue;
                const column = this.tValueColumn ? this.tValueColumn : this.findColumnByTag('value');
                const value = this.getColumn(column)
                return value && value.length ? value[0] : 0;
            },
            previous() {
                if (!this.numberPrevious && !this.layer) return 0;
                if (this.numberPrevious) return this.numberPrevious;
                const column = this.tPreviousColumn ? this.tPreviousColumn : this.findColumnByTag('previous');
                const previous = this.getColumn(column)
                return previous && previous.length ? previous[0] : 0;
            },
            percentage() {
                const value = this.num(this.value);
                const previous = this.num(this.previous);
                if (previous && value !== previous) {
                    const difference = (((value - previous) / previous) * 100).toFixed(2);
                    const appendIncrement = difference > 0 ? '+' : '';
                    return `${appendIncrement}${difference}%`;
                }
                return '';
            }
        },
        methods: {
            num(val) {
                return parseInt(val.replace(/,/g, ''))
            }
        }
    }
</script>
