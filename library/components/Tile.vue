<!----------------------- begin global tiles ----------------------->
<template>
  <base-card legacy>
    <div v-if="loading && !nospinner">
      <div :style="{ height: height - 2 + 'px' }">
        <t-loading-spinner />
      </div>
    </div>
    <div v-else>
      <div :style="{ height: height - 2 + 'px' }">
        <slot></slot>
      </div>
    </div>
  </base-card>
</template>

<script>
export default {
  props: ["hideBackground"],
};
</script>
