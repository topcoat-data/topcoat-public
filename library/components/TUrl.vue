<template>
  <a :href="fullUrl" class="tUrl" :target="openInNewTab ? '_blank' : '_top'" rel="noopener noreferrer">
    <slot></slot>
  </a>
</template>

<script>
export default {
  name: "TUrl",
  props: {
    url: {
      type: String,
      required: true,
    },
    includeFilterParams: {
      type: Boolean,
      default: true,
    },
    additionalUrlParams: {
      type: Object,
      default() {
        return {};
      },
    },
    openInNewTab:{
      type: Boolean,
      default: true,
    }
  },
  computed: {
    fullUrl() {
      let allUrlParams = this.additionalUrlParams;

      if (this.includeFilterParams ) {
        const { 'context[org]': org, 'context[group]': group, ...restOfFilters } = this.getFiltersState;

        allUrlParams = {
          ...allUrlParams,
          ...restOfFilters
        };
      }

      const urlParamString = new URLSearchParams(allUrlParams).toString();

      if (urlParamString.length > 0) {
        return `${this.url}?${urlParamString}`;
      }

      return this.url;
    },
  }
};
</script>

<style scoped>
.tUrl {
  color: rgba(20, 93, 235);
  text-decoration: underline;
}
</style>
