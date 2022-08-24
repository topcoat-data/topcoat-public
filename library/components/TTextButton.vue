<template>
  <base-button class="
    rounded
    bg-white" v-on="$listeners" variant="link" style="color: #145deb;">
    <!-- 
      base button's color property for variant="link" has a higher 
      specificity than tailwind classes 
      using 'style' is the only way to override the color of the base button
    -->
    <slot></slot>
  </base-button>
</template>