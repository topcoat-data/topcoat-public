<template>
  <div>
    <div class="bg-[#F9F9FA]">
      <div class="flex w-full gap-10 content-block">
        <div class="w-full">
          <slot name="head"></slot>
          <div
            v-if="$slots['filters']"
            class="flex flex-wrap justify-between items-center w-full py-4 px-6 border-b border-[#E4E3E8] md:flex-row flex-col gap-1"
          >
            <slot name="filters"></slot>
          </div>
          <div v-if="$slots['mid']" class="w-full px-6 py-5">
            <slot name="mid"></slot>
          </div>
          <div class="py-5 px-6 bg-[#ffffff] border-t border-[#E4E3E8]">
            <slot></slot>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    // to hide the header use this prop
    // the header is shown only if the report is not shown in an iframe
    hasHeader: {
      type: Boolean,
      default: () => window.location === window.parent.location,
    },
    showSidebar: {
      type: Boolean,
      default: false,
    },
  },
  data: () => ({
    is_filter: true,
    popup: false,
  }),
};
</script>

<style>
body {
  @apply bg-[#F6F7FB];
}
</style>
