<template>
	<div
		@mouseover="handleMouseOver"
		@mouseleave="handleMouseLeave"
		ref="tooltipContainer"
	>
		<div ref="trigger">
			<slot name="trigger">
				<help-circle-outline-icon :size="12" />
			</slot>
		</div>

		<!-- $slots.default is used in cases when the trigger is using v-if on content's div -->
		<transition name="fade">
			<div
				class="p-4 bg-[#1C1C21] text-white w-max h-max rounded fixed z-50"
				:style="{ width, ...positions.tooltip }"
				ref="tooltip"
				v-show="isVisible && $slots.default"
			>
				<slot></slot>
				<div
					class="bg-[#1C1C21] w-4 h-4 fixed rotate-45"
					:style="{ ...positions.arrow }"
				></div>
			</div>
		</transition>
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
		isOpen: { // To control state from a component.
			type: Boolean,
			default: false,
		}
	},
	data: () => ({
		positions: { arrow: {}, tooltip: {} },
		isVisible: this.isOpen,
	}),
	methods: {
		placeTooltip() {
			// Calculate and place both tooltip and arrow.
			const triggerElement = this.$refs.trigger;
			const tooltipElement = this.$refs.tooltip;

			const positions = { ...this.positions };
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
			// Mouseover should also prepare position of tooltip,
			// Without $nextTick, behaviour is glitched.
			this.$nextTick(() => {
				this.placeTooltip();
			})

			if (this.isOpen) {
				return;
			}
			this.show();
		},
		handleMouseLeave() {
			if (this.isOpen) {
				return;
			}
			this.hide();
		},
		show() {
			this.isVisible = true;
		},
		hide() {
			this.isVisible = false;
		}
	},
};
</script>

<style>
	.fade-enter-active,
  	.fade-leave-active {
		transition: opacity 0.5s ease;
  	}
  
  	.fade-enter-from,
  	.fade-leave-to {
		opacity: 0;
  	}
</style>