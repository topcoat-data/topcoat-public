<template>
  <div
    ref="dropdownFilter"
    class="relative w-auto font-sans cursor-pointer dropdown-filter"
  >
    <div :class="activeClass" class="rounded cursor-pointer" @click="openPopup">
      <slot name="handle"></slot>
    </div>
    <slot name="outside"></slot>
    <div
      ref="popup"
      class="absolute mt-1 bg-white rounded-lg shadow-md base-dropdown-menu w-max"
      :class="[
        alignClass,
        isPopupOpen ? 'h-max' : 'h-[0px] opacity-0 overflow-y-hidden',
      ]"
      :style="{ zIndex }"
      @click.stop
    >
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    isActive: {
      type: Boolean,
      default: false,
    },
    zIndex: {
      type: String,
      default: "999",
    },
    isExpanded: {
      type: Boolean,
      default: false,
    },
    outsideElementClasses: {
      type: Array,
      // Todo: Remove & Replace with a better fix.
      default: () => ["mx-datepicker-popup"],
    },
  },
  data: () => ({
    alignClass: "",
    isPopupOpen: false,
  }),
  computed: {
    activeClass() {
      if (!this.isExpanded) {
        return this.isPopupOpen || this.isActive
          ? "border-1 active"
          : "border-1 in-active";
      }
      return "";
    },
  },
  watch: {
    isExpanded: function (newVal, oldVal) {
      if (newVal) {
        this.isPopupOpen = true;
        this.$emit("open");
      }
    },
  },
  mounted() {
    onClickOutside(this.$refs.dropdownFilter, (event) => {
      // Temporary solution
      // If a component is appending it's inner dropdown directly to body.
      for (let cl of this.outsideElementClasses) {
        // If an outside element is still open, keep the dropdown from closing.
        if (document.querySelector(`.${cl}`)) return;
      }
      if (this.isPopupOpen) {
        this.isPopupOpen = false;
        this.$emit("closed");
      }
    });
  },
  methods: {
    alignPopup() {
      const element = this.$refs.popup;

      if (element) {
        const bounding = element.getBoundingClientRect();
        const availableWidth = window.innerWidth;

        if (bounding.x < 0) {
          return (this.alignClass = "left-0");
        }

        if (bounding.x + bounding.width > availableWidth) {
          return (this.alignClass = "right-0");
        }
      }

      return (this.alignClass = "");
    },
    openPopup() {
      if (this.isPopupOpen) {
        this.isPopupOpen = false;
        this.$emit("closed");
      } else {
        this.isPopupOpen = true;
        this.$emit("open");
      }

      this.$nextTick(() => {
        this.alignPopup();
      });
    },
  },
};
</script>

<style>
.dropdown-filter .active {
  @apply border-[#145DEB] text-[#145DEB] bg-[#EAF1FF];
}

.dropdown-filter .in-active {
  @apply border-[#C3C2CB] text-[#555463] bg-white;
}
</style>
