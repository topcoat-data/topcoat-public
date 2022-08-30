<template>
	<div
        @mouseover="handleMouseOver"
        @mouseleave="handleMouseLeave"
        @click="handleClick"
        ref="tooltipContainer"
    >
		<div ref="trigger">
			<slot name="trigger">
				<help-circle-outline-icon :size="12" />
			</slot>
		</div>

        <!-- $slots.default is used in cases when the trigger is using v-if on content's div -->
		<div
			class="p-4 bg-[#1C1C21] text-white w-max h-max rounded fixed z-50"
			:style="{ width, ...positions.tooltip }"
			ref="tooltip"
			v-show="showTooltip && $slots.default"
		>
			<slot></slot>
			<div
				class="bg-[#1C1C21] w-4 h-4 fixed rotate-45"
				:style="{ ...positions.arrow }"
			></div>
		</div>
	</div>
</template>

<script>
export default {
	props: {
		width: {
			type: String,
			default: "200px"
		},
		position: {
			type: String,
			default: "top"
		},
	},
	data: () => ({
		positions: {},
		showTooltip: false,
        isFocused: false,
	}),
	mounted() {
		onClickOutside(this.$refs.tooltipContainer, () => {
			this.hide();
		});
	},
	methods: {
		placeTooltip() {
			// Calculate and place both tooltip and arrow.
			const triggerElement = this.$refs.trigger;
			const tooltipElement = this.$refs.tooltip;
			const tooltipPositions = {};
			const positions = { arrow: {}, tooltip: {} };
			if (triggerElement && tooltipElement) {
				const position = triggerElement.getBoundingClientRect();
				if (this.position === "top") {
					positions.tooltip.top = position.top - (tooltipElement.clientHeight + 10) + "px";
					positions.tooltip.left = position.left - tooltipElement.clientWidth / 2 + "px";
					positions.arrow.top = position.top - 20 + "px";
					positions.arrow.left = position.left + "px";
				} else if (this.position === "bottom") {
					positions.tooltip.top = position.top + triggerElement.clientHeight + 15 + "px";
					positions.tooltip.left = position.left - tooltipElement.clientWidth / 2 + "px";
					positions.arrow.top = position.top + triggerElement.clientHeight + 10 + "px";
					positions.arrow.left = position.left + "px";
				} else if (this.position === "left") {
					positions.tooltip.top = position.top - tooltipElement.clientHeight / 2 + "px";
					positions.tooltip.left = position.left - tooltipElement.clientWidth - 15 + "px";
					positions.arrow.top = position.top + "px";
					positions.arrow.left = position.left - 25 + "px";
				} else {
					positions.tooltip.top = position.top - tooltipElement.clientHeight / 2 + "px";
					positions.tooltip.left = position.left + triggerElement.clientWidth + 15 + "px";
					positions.arrow.top = position.top + "px";
					positions.arrow.left = position.left + triggerElement.clientWidth + 10 + "px";
				}
			}
			this.positions = positions;
		},
		handleMouseOver() {
			if (this.isFocused) return;
			this.show();
		},
		handleMouseLeave() {
			if (this.isFocused) return;
			this.hide();
		},
		handleClick() {
            this.isFocused = true;
            this.show();
		},
		show() {
			this.showTooltip = true;
			// Glitchy behaviour without nextTick()
			this.$nextTick(() => {
				this.placeTooltip();
			});
		},
		hide() {
			this.showTooltip = false;
            this.isFocused = false;
		}
	}
};
</script>