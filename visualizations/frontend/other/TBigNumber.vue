<template>
    <div
        class="w-full lg:p-5 md:p-3 p-1 rounded-[2px] break-all"
        :style="{ background: bgColor, color: textColor }"
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
        <div class="mt-3">
            <span class="font-normal leading-8" :class="fontSizes[bigNumberSize]">
                <div class="flex items-center gap-2">
                    <span>{{ value || '--' }}</span>
                    {{ valueText }}
                    <div v-if="previous">
                        <span class="opacity-80" v-if="value > previous">
                            <chevron-up-icon />
                        </span>
                        <span class="opacity-80" v-else-if="value < previous">
                            <chevron-down-icon class="opacity-90" />
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
                if (this.numberValue) return parseInt(this.numberValue);
                const column = this.tValueColumn ? this.tValueColumn : this.findColumnByTag('value');
                const value = this.getColumn(column)
                return value && value.length ? parseInt(value[0]) : 0;
            },
            previous() {
                if (this.numberPrevious) return parseInt(this.numberPrevious);
                const column = this.tPreviousColumn ? this.tPreviousColumn : this.findColumnByTag('previous');
                const previous = this.getColumn(column)
                return previous && previous.length ? parseInt(previous[0]) : 0;
            },
            percentage() {
                if (this.previous && this.value !== this.previous) {
                    const difference = Math.floor(((this.value - this.previous) / this.previous) * 100)
                    const appendIncrement = difference > 0 ? '+' : '';
                    return `${appendIncrement}${difference}%`;
                }
                return '';
            }
        },
    }
</script>
