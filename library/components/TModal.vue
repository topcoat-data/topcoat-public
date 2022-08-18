<template>
  <transition>
    <div
      class="fixed top-0 left-0 m-auto w-full h-full z-[9999] flex justify-center"
      v-if="isOpen"
      style="background: rgba(33, 33, 74, 0.6);"
    >
      <div
        class="bg-white mt-28 w-max box-borderborder border-[#E4E3E8] rounded-md"
        style="box-shadow: 0px 8px 12px 1px rgba(0, 0, 0, 0.15); height: max-content;"
      >
        <div class="flex justify-between pt-6 px-6 pb-2">
          <div class="text-2xl font-semibold text-black">{{ label }}</div>
          <div class="cursor-pointer">
            <close-icon :size="20" @click="$emit('close-clicked')" />
          </div>
        </div>
        <div class="flex justify-center px-12 pb-12 pt-2">
          <slot></slot>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
  export default {
    props: {
      label: String,
      isOpen: Boolean,
    }
  }
</script>

<style>

  /* Modal transition */
  .v-enter-active,
  .v-leave-active {
    transition: opacity 0.3s ease;
  }

  .v-enter,
  .v-leave-to {
    transition: opacity 0.3s ease;
    opacity: 0;
  }
</style>