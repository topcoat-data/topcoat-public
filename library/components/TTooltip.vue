<template>
  <div ref="tooltipContainer">
    <div
      ref="trigger"
      @mouseleave="handleMouseLeave"
      @mouseover="handleMouseOver"
    >
      <slot name="trigger">
        <help-circle-outline-icon :size="12" />
      </slot>
    </div>

    <!-- $slots.default is used in cases when the trigger is using v-if on content's div -->
    <transition name="fade">
      <div class="relative w-0 h-0" :style="{ ...positions.tooltip }">
        <div
          class="p-2 bg-[#1C1C21] text-white text-sm w-max h-max rounded absolute z-50"
          :style="{ width }"
          ref="tooltip"
          v-show="isVisible && $slots.default"
          @mouseover="handleTooltipFocus(true)"
          @mouseleave="handleTooltipFocus(false)"
        >
          <slot></slot>
          <div
            class="bg-[#1C1C21] w-3 h-3 absolute rotate-45 bg-red"
            :style="{ ...positions.arrow }"
          ></div>
        </div>
      </div>
    </transition>
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
    },
    isOpen: {
      // To control state from a component.
      type: Boolean,
      default: false,
    },
  },
  data: () => ({
    positions: { arrow: {}, tooltip: {} },
    isVisible: false,
    isTooltipFocused: false, // If cursor is on tooltip.
  }),
  methods: {
    placeTooltip() {
      // Calculate and place both tooltip and arrow.
      const triggerElement = this.$refs.trigger;
      const tooltipElement = this.$refs.tooltip;

      const positions = { ...this.positions };
      if (triggerElement && tooltipElement) {
        if (this.position === "top") {
          positions.tooltip.bottom =
            triggerElement.clientHeight +
            tooltipElement.clientHeight +
            10 +
            "px";
          positions.tooltip.right = "25px";
          positions.arrow.bottom = "-6px";
          positions.arrow.left = "25px";
        } else if (this.position === "bottom") {
          positions.tooltip.top = "12px";
          positions.tooltip.right = "25px";
          positions.arrow.top = "-6px";
          positions.arrow.left = "25px";
        } else if (this.position === "left") {
          positions.tooltip.top = "-" + triggerElement.clientHeight + "px";
          positions.tooltip.right = tooltipElement.clientWidth + 10 + "px";
          positions.arrow.right = "-6px";
          positions.arrow.top = "10px";
        } else {
          positions.tooltip.top = "-" + triggerElement.clientHeight + "px";
          positions.tooltip.left = triggerElement.clientWidth + 10 + "px";
          positions.arrow.left = "-6px";
          positions.arrow.top = "10px";
        }
      }
      this.positions = positions;
    },
    handleMouseOver() {
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
    handleTooltipFocus(isFocused) {
      this.isTooltipFocused = isFocused;
      if (!isFocused) {
        this.hide();
      }
    },
    show() {
      this.isVisible = true;

      this.$nextTick(() => {
        // Without $nextTick, behaviour is glitched.
        this.placeTooltip();
      });
    },
    hide: window._.debounce(function () {
      // Debounce will give user chance to hover to tooltip and keep it open, as long as cursor stays on it.
      // This is useful when tooltip contains clickable links.
      if (this.isTooltipFocused) {
        // If user is interacting with tooltip
        return;
      }
      this.isVisible = false;
    }, 100),
  },
  watch: {
    // Watcher triggers placement logic as well.
    isOpen(n) {
      if (n) {
        this.show();
      } else {
        this.hide();
      }
    },
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
