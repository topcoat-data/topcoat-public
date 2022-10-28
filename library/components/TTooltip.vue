<template>
  <div
    ref="tooltipContainer"
    class="relative w-max"
    @mouseleave="handleMouseLeave"
    @mouseover="handleMouseOver"
  >
    <div ref="trigger">
      <slot name="trigger">
        <help-circle-outline-icon :size="12" />
      </slot>
    </div>

    <!-- $slots.default is used in cases when the trigger is using v-if on content's div -->
    <transition name="fade">
      <div class="absolute" :style="{ ...styles.tooltip }">
        <div
          v-show="isVisible && $slots.default"
          ref="tooltip"
          class="p-2 bg-[#1C1C21] text-white text-sm w-max h-max rounded relative z-50"
          :style="{ width }"
        >
          <slot></slot>
          <div
            class="bg-[#1C1C21] w-3 h-3 absolute rotate-45"
            :style="{ ...styles.arrow }"
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
    styles: { arrow: {}, tooltip: {} },
    isVisible: false,
  }),
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
  methods: {
    placeTooltip() {
      // Calculate and place both tooltip and arrow.
      const triggerElement = this.$refs.trigger;
      const tooltipElement = this.$refs.tooltip;

      const styles = { ...this.styles };
      if (triggerElement && tooltipElement) {
        if (this.position === "top") {
          styles.tooltip.bottom = triggerElement.clientHeight + "px";
          styles.tooltip.left = "-25px";
          styles.tooltip.paddingBottom = "10px";
          styles.arrow.bottom = "-6px";
          styles.arrow.left = "25px";
        } else if (this.position === "bottom") {
          styles.tooltip.top = triggerElement.clientHeight + "px";
          styles.tooltip.left = "-25px";
          styles.tooltip.paddingTop = "10px";
          styles.arrow.top = "-6px";
          styles.arrow.left = "25px";
        } else if (this.position === "left") {
          styles.tooltip.top = "0px";
          styles.tooltip.left = "-" + (tooltipElement.clientWidth + 10) + "px";
          styles.tooltip.paddingRight = "10px";
          styles.arrow.right = "-6px";
          styles.arrow.top = "10px";
        } else {
          styles.tooltip.top = "0px";
          styles.tooltip.left = triggerElement.clientWidth + "px";
          styles.tooltip.paddingLeft = "10px";
          styles.arrow.left = "-6px";
          styles.arrow.top = "10px";
        }
      }
      this.styles = styles;
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
    show() {
      this.isVisible = true;

      this.$nextTick(() => {
        // Without $nextTick, behaviour is glitched.
        this.placeTooltip();
      });
    },
    hide() {
      this.isVisible = false;
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
