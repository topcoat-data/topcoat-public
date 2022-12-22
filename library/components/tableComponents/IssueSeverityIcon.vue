<template>
  <div>
    <div
      v-if="['Critical', 4].includes(severity)"
      class="text-[11px] bg-[#ba1515] w-[20px] h-[20px] text-[#ffffff] inline-flex items-center justify-center rounded-[2px]"
      title="Critical Issues"
    >
      C
    </div>
    <div
      v-else-if="['High', 3].includes(severity)"
      class="text-[11px] bg-[#cc4f19] w-[20px] h-[20px] text-[#ffffff] inline-flex items-center justify-center rounded-[2px]"
      title="High Issues"
    >
      H
    </div>
    <div
      v-else-if="['Medium', 2].includes(severity)"
      class="text-[11px] bg-[#f9a11b] w-[20px] h-[20px] text-[#ffffff] inline-flex items-center justify-center rounded-[2px]"
      title="Medium Issues"
    >
      M
    </div>
    <div
      v-else-if="['Low', 1].includes(severity) "
      class="text-[11px] bg-[#8e8d92] w-[20px] h-[20px] text-[#ffffff] inline-flex items-center justify-center rounded-[2px]"
      title="Low Issues"
    >
      L
    </div>
  </div>
</template>

<script>
export default {
  name: "IssueSeverityIcon",
  props: {
    severity: {
      type: [String, Number],
      required: true,
      validator: function (value) {
        return ["Critical", "High", "Medium", "Low", 1, 2, 3, 4].includes(value);
      },
    },
  },
};
</script>

<style scoped></style>
