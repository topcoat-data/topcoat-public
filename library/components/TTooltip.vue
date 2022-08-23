<template>
  <div
    class="p-4 bg-[#1C1C21] text-white w-max h-max rounded absolute top-0 z-50"
    :style="{ width, ...tooltipPositions }"
  >
    <slot></slot>
    <div
		class="bg-[#1C1C21] w-4 h-4 absolute rotate-45 m-auto"
		:class="arrowPositions[position]"
	></div>
  </div>
</template>

<script>
  export default {
    props: {
      width: {
        type: String,
        default: "200px",
      },
	  position: {
		type: String,
		default: "top",
	  }
    },
	data: () => ({
		tooltipPositions: {}, // This object should be empty by default to only apply related properties (top, left...)
        arrowPositions: {
            top: "left-0 right-0 -bottom-[7px]",
            bottom: "left-0 right-0 -top-[7px]",
            left: "top-2 -right-[7px]",
            right: "top-2 -left-[7px]",
        }
	}),
	mounted() {
		this.placeTooltip();
	},
	methods: {
		placeTooltip() {

            // Place tooltip near parent according to `position` prop.
			const parent = this.$parent.$el;
            const tooltipPositions = {}
			if (parent) {
				const position = parent.getBoundingClientRect();
				if (this.position === "top") {
					// Push from bottom
					tooltipPositions.top = "-" + (position.bottom + 15) + "px";
				} else if (this.position === "bottom") {
					// Push from top
					tooltipPositions.top = (parent.clientHeight + 15) + "px";
				} else if (this.position === "left") {
                    // Place on left side
                    tooltipPositions.right = (position.width + 15) + "px";
                } else {
                    // Place on right side
                    tooltipPositions.left = (position.width + 15) + "px";
                }
			}
            this.tooltipPositions = tooltipPositions;
		}
	}
  }
</script>
