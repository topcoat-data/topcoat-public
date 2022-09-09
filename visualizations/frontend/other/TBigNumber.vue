<template>
	<div
		class="w-full lg:p-5 md:p-3 p-1 rounded-[2px] break-all relative"
		:style="{ background: bgColor, color: textColor }"
		:class="[hasUnderline && 'border-b-2 border-[#21214c]', customClass]"
		@mouseleave="showTooltip = false"
	>
		<div class="relative flex items-center gap-2">
			<div class="hidden opacity-50 md:block" v-if="$slots.icon">
				<slot name="icon"></slot>
			</div>
			<span class="text-xs font-semibold leading-4 tracking-widest">
				{{ label || "--" }}
			</span>

			<div v-show="$slots.tooltip">
				<t-tooltip :width="tooltipWidth" :position="tooltipPosition" :open="showTooltip" @show="showTooltip = true">
					<slot name="tooltip"></slot>
				</t-tooltip>
			</div>
		</div>

		<div class="mt-3">
			<span class="font-normal leading-8" :class="fontSizes[bigNumberSize]">
				<div class="flex items-center gap-2">
					<t-tooltip position="right">
						<span slot="trigger" :style="{ color: numberTextColor }">
							{{ formatNumber(value) }} {{ valueText }}
						</span>
						<div
							v-if="value.value > numberFormatLimit"
							class="text-sm"
						>
							{{ value.rendered }}
						</div>
					</t-tooltip>
					<div v-if="previous.value" class="opacity-80">
						<arrow-up-icon :size="18" v-if="value.value > previous.value" />
						<arrow-down-icon :size="18" v-else-if="value.value < previous.value" />
						<div class="opacity-30" v-else>-</div>
					</div>
					<t-loading-spinner position="relative" v-if="loading" />
				</div>
			</span>
		</div>
		<div v-if="previous.value" class="flex items-center gap-1 mt-3">
			<t-tooltip position="right" v-if="value.value != previous.value">
				<div class="font-semibold" slot="trigger">
					{{ formatNumber(previous) }}
					<span class="font-normal opacity-80">{{ previousText }}</span>
				</div>
				<div v-if="previous.value > numberFormatLimit" class="text-sm">
					{{ previous.rendered }}
				</div>
			</t-tooltip>
			<div v-else class="opacity-80">
				No change
			</div>
		</div>
	</div>
</template>

<script>
export default {
	props: {
		bgColor: {
			type: String,
			default: "transparent"
		},
		bigNumberSize: {
			type: String,
			default: "medium",
			validator: v => ["small", "medium", "big"].includes(v)
		},
		numberValue: {
			type: Number,
			default: ""
		},
		numberPrevious: {
			type: Number,
			default: ""
		},
		label: {
			type: String,
			default: ""
		},
		textColor: {
			type: String,
			default: "#393842"
		},
		tValueColumn: {
			type: String,
			default: ""
		},
		tPreviousColumn: {
			type: String,
			default: ""
		},
		valueText: {
			type: String,
			default: ""
		},
		previousText: {
			type: String,
			default: "previous period"
		},
		tooltipText: {
			type: String,
			default: ""
		},
		hasUnderline: {
			type: Boolean,
			default: false
		},
		tooltipWidth: {
			type: String,
			default: "200px"
		},
		tooltipPosition: {
			type: String,
			default: "top"
		},
		numberFormatLimit: {
			type: Number,
			default: 999999,
		},
		numberTextColor: {
			type: String,
			default: '#393842'
		},
		customClass: {
			type: String,
			default: "",
		}
	},
	data: () => ({
		is_filter: true,
		fontSizes: {
			small: "lg:text-3xl md:text-2xl sm:text-lg",
			medium: "lg:text-[2.5rem] md:text-3xl sm:text-2xl",
			big: "lg:text-5xl md:text-4xl sm:text-3xl"
		},
		showTooltip: false,
	}),
	computed: {
		row() {
			return this.rows.length ? this.rows[0] : null;
		},
		value() {
			if (this.numberValue) {
				return { value: this.numberValue, rendered: this.numberValue.toLocaleString("en") };
			}

			const column = this.tValueColumn
				? this.tValueColumn
				: this.findColumnByTag("value");

			return this.getColumnValue(column);
		},
		previous() {
			if (this.numberPrevious)
				return { value: this.numberPrevious, rendered: this.numberPrevious.toLocaleString("en") };

			const column = this.tPreviousColumn
				? this.tPreviousColumn
				: this.findColumnByTag("previous");

			return this.getColumnValue(column);
		},
	},
	methods: {
		getColumnValue(column) {
			// Expected column.value values: number, null, string
			if (this.row && this.row[column]) {
				const columbObject = this.row[column];

				if (typeof columbObject.value === "string") {
					// if '3.9'
					columbObject.value = parseInt(columbObject.value);
				}

				if (!columbObject.value) {
					// In some cases, value is returned null inside row object
					columbObject.value = 0;
				}

				if (!columbObject.rendered) {
					// In some cases, rendered is returned null inside row object
					columbObject.rendered = "--";
				}

				return columbObject;
			}

			return {
				value: 0,
				rendered: "--"
			};
		},
		formatNumber({ value, rendered }) {
			// If number is greater than 6 digits, format it.
			if (value > this.numberFormatLimit) {
				let formatter = Intl.NumberFormat('en', { notation: 'compact' });
				return formatter.format(value);
			}

			// Else return default rendered value from sql.
			return rendered;
		}
	}
};
</script>
