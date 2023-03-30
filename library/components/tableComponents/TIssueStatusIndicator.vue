<template>
  <div class="centerIssueStatusIndicator center">
    <div class="text-[10px] text-normal leading-[17px]">
      <span
        class="badge-error rounded px-[6px] py-1 border text-[10px] font-medium tracking-[0.02em] uppercase leading-[11px]"
        :class="{
          'bg-[#FFEEF2] border-[#F15366] text-[#B9002C]':
            status.toLowerCase() === 'open',
          'bg-[#EDFFFB] border-[#52F2E0] text-[#00BA8F]':
            status.toLowerCase() === 'resolved',
          'bg-[#f0f0f0] border-[#1f1f1f] text-[#1f1f1f]':
            status.toLowerCase() === 'ignored',
        }"
      >
        {{ status.toUpperCase() }}
      </span>
    </div>
  </div>
</template>

<script>
export default {
  name: "TIssueStatusIndicator",
  props: {
    status: {
      type: String,
      required: true,
      validator(value) {
        return ["open", "ignored", "resolved"].includes(value.toLowerCase());
      },
    },
  },
};
</script>

<style scoped>
.centerIssueStatusIndicator {
  position: relative;
  top: 4px;
}
</style>
