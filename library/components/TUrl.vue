<template>
  <a :href="fullUrl" class="tUrl">
    <slot ></slot>
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
    additionalFilters: {
      type: String,
      default: "",
    },
  },
  computed: {
    fullUrl() {
      if (!this.includeFilterParams) {
        return this.url;
      }
      const queryString = window.location.search;
      const urlSearchParams = new URLSearchParams(queryString);
      let filters = [];
      for (let filterKey of urlSearchParams.keys()) {
        if (!this.exlude(filterKey)) {
          filters.push(filterKey + "=" + urlSearchParams.get(filterKey));
        }
      }
      let fullUrl = this.url;
      let urlParams= '?'
      if (filters.length > 0) {
        const pageFilters = filters.join("&");
        urlParams += pageFilters;
      }
      if(this.additionalFilters){
        if(this.additionalFilters[0] !== "&" && filters.length > 0 ){
          urlParams+='&'
        }
        urlParams +=this.additionalFilters
      }

      if(urlParams.length > 0){
        return fullUrl+urlParams;
      }else{
        return fullUrl;
      }
    },
  },
  methods: {
    exlude(filterToCheck) {
      // Note: forEach doesn't allow early termination
      for(const [index, filter] of this.excludeFilters.entries()){
        if (filterToCheck.toLowerCase().startsWith(filter.toLowerCase())){
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
