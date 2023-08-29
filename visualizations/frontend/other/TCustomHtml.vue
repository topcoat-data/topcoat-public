<!-- migrated 2023-08-08 -->
<template>
  <div class="relative">
    <slot :rows="rows"> Empty custom HTML visualization </slot>
  </div>
</template>

<script>
export default {
  data: () => ({
    is_filter: true,
    // Is filter removes height and background css to allow for custom html and css changes.
  }),
};
</script>
