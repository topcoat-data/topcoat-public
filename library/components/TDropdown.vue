<template>
  <div
    ref="dropdownFilter"
    class="relative w-auto font-sans cursor-pointer dropdown-filter"
  >
    <div
      class="rounded cursor-pointer"
      :class="!disableActiveClass && activeClass"
      @click="handlePopup"
    >
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
    disableActiveClass: {
      type: Boolean,
      default: false,
    },
    isOpen: {
      type: Boolean,
      default: false,
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
    isExpanded: function (newVal) {
      if (newVal) {
        this.openPopup();
      }
    },
    isOpen: function (open) {
      if (open) {
        return this.openPopup();
      }
      return this.closePopup();
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
        this.closePopup();
      }
    });
  },
  methods: {
    alignPopup() {
      return (this.alignClass = "top-0");
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
    handlePopup() {
      if (this.isPopupOpen) {
        this.closePopup();
      } else {
        this.openPopup();
      }
    },
    closePopup() {
      this.isPopupOpen = false;
      this.$emit("closed");
    },
    openPopup() {
      this.isPopupOpen = true;
      this.$emit("open");
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
  @apply border-[#C3C2CB] hover:border-[#555463] text-[#555463] bg-white;
}
</style>
