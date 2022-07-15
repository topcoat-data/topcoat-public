<template>
  <a :href="fullUrl" class="tUrl">
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
    excludeFilters: {
      type: Array,
      default() {
        return ["context"];
      },
    },
    additionalUrlParams: {
      type: Object,
      default:{},
    },
  },
  computed: {
    fullUrl() {
      let allUrlParams = this.additionalUrlParams;

      if (this.includeFilterParams ) {
        const queryString = window.location.search;
        const urlSearchParams = new URLSearchParams(queryString);
        urlSearchParams.forEach((value, key)=>{
          if (!this.exlude(key)) {
            allUrlParams[key] = value; 
          }
        })
      }

      const urlParamString = new URLSearchParams(allUrlParams).toString();
      if (urlParamString.length > 0) {
        return this.url + "?" + urlParamString;
      }
      return this.url;
    },
  },
  methods: {
    exlude(filterToCheck) {
      // Note: forEach doesn't allow early termination
      for (const [index, filter] of this.excludeFilters.entries()) {
        if (filterToCheck.toLowerCase().startsWith(filter.toLowerCase())) {
          return true;
        }
      }
      return false;
    },
  },
};
</script>

<style scoped>
.tUrl {
  color: rgba(20, 93, 235);
  text-decoration: underline;
}
</style>
