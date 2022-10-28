<template>
  <div class="flex flex-col overflow-x-hidden">
    <label class="pb-[7px] text-sm font-medium" v-if="label">
      {{ label }}
    </label>
    <div
      class="h-[30px] max-w-full min-w-[200px] flex items-center"
      @click="handleClick"
      @mousedown="dragging = true"
      @mouseover="handleDragover"
      @mouseup="handleDragend"
      ref="rangeContainer"
    >
      <div
        class="w-full border-1 border-[#C3C2CB] bg-[#C3C2CB] relative"
        slot="handle"
      >
        <div
          class="border-1 border-[#145DEB]"
          :style="{ width: left + '%' }"
        ></div>
        <div
          class="absolute m-auto bg-white rounded-full top-0 bottom-0 border-1 border-[#C3C2CB] z-10 py-3 px-1 flex items-center justify-center cursor-pointer"
          :style="{ left: left + '%' }"
        >
          {{ value }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data: () => ({
    dragging: false,
    is_filter: true,
    left: 0,
    value: 0,
  }),
  props: {
    label: {
      default: "",
    },
    max: {
      default: 100,
    },
    min: {
      default: 0,
    },
  },
  methods: {
    handleDragover(e) {
      if (this.dragging) {
        this.handlePlacement(e.clientX);
      }
    },
    handleDragend(e) {
      this.dragging = false;
      this.setFilterValue("value", this.value, true);
    },
    handleClick(e) {
      this.dragging = true;
      this.handlePlacement(e.clientX);
      this.dragging = false;
      this.setFilterValue("value", this.value, true);
    },
    handlePlacement(clickPos) {
      const container = this.$refs.rangeContainer;
      if (container) {
        const currentPos = clickPos - container.getBoundingClientRect().left;
        const totalSize = container.clientWidth;
        let currentPercentage = (currentPos * 100) / totalSize;
        if (currentPercentage > 100) {
          currentPercentage = 100;
        } else if (currentPercentage < 0) {
          currentPercentage = 0;
        }
        this.left = currentPercentage;
        this.value = Math.round(
          this.min + (currentPercentage / 100) * (this.max - this.min)
        );
      }
    },
    onVisualizationInit() {
      const internalValue = this.getFilterValue("value");
      this.value =
        !internalValue || internalValue < this.min ? this.min : internalValue;
      const pos = ((this.value - this.min) * 100) / (this.max - this.min);
      this.left = pos;
      this.setFilterValue("value", this.value, true);
    },
  },
};
</script>
