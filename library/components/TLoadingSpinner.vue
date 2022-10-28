<template>
  <base-loading-spinner
    :style="{ position: position || 'absolute' }"
    class="top-0 bottom-0 left-0 right-0 z-50 m-auto"
  />
</template>

<script>
export default {
  props: ["position"],
};
</script>
