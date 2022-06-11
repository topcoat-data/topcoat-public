<template>
    <div>
        <report-header v-if="hasHeader" />
        <div class="bg-[#F9F9FA]">
            <div class="flex w-full gap-10 pb-20 content-block">
                <div class="w-full">
                    <div class="flex flex-wrap justify-between items-center w-full py-4 px-6 border-b border-[#E4E3E8] md:flex-row flex-col gap-1">
                        <slot name="filters"></slot>
                    </div>
                    <div class="w-full px-6 py-5">
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

<style>
  body {
    @apply bg-[#F6F7FB];
  }
</style>

<script>
  export default {
    data:()=>({
      is_filter:true,
      popup:false
    }),
    props: {
      // to hide header use this prop
      hasHeader: {
        type: Boolean,
        default: false,
      },
      showSidebar: {
        type: Boolean,
        default: false,
      }
    },
  };
</script>
