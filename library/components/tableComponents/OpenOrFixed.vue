<template>
  <div class="centerOpenOrFixed center">
    <div
      v-if="isOpen"
      class="text-[10px] text-normal text-[#B9002C] leading-[17px]"
    >
      <span
        class="
          badge-error
          bg-[#FFEEF2]
          rounded
          px-[6px]
          py-1
          border-[#F15366] border
          text-[10px]
          font-medium
          tracking-[0.02em]
          uppercase
          leading-[11px]
        "
      >
        OPEN
      </span>
    </div>
    <div v-else class="text-[10px] text-normal text-[#00BA8F] leading-[17px]">
      <span
        class="
          badge-error
          bg-[#EDFFFB]
          rounded
          px-[6px]
          py-1
          border-[#52F2E0] border
          text-[10px]
          font-medium
          tracking-[0.02em]
          uppercase
          leading-[11px]
        "
      >
        FIXED
      </span>
    </div>
  </div>
</template>

<script>
export default {
  name: "OpenOrFixed",
  props: {
    isOpen: { type: String, required: true },
  },
};
</script>

<style scoped>
.centerOpenOrFixed {
  position: relative;
  top: 4px;
}
</style>