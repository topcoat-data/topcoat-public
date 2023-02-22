<template>
  <a
    :href="fullUrl"
    :class="{ tUrl: includeUrlStyle }"
    :target="openInNewTab ? '_blank' : '_top'"
    rel="noopener noreferrer"
  >
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
    openInNewTab: {
      type: Boolean,
      default: true,
    },
    includeUrlStyle: {
      type: Boolean,
      default: true,
    },
    includeContextParam: {
      type: Boolean,
      default: false,
    },
    isDoubleEncoded: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    fullUrl() {
      let allUrlParams = {};
      const allFilters = {};
      this.filters.forEach((f) => (allFilters[f.name] = f.value));
      const {
        "context[org]": org,
        "context[group]": group,
        ...restOfFilters
      } = allFilters;

      if (this.includeContextParam) {
        if (org) {
          allUrlParams["context[org]"] = org;
        } else if (group) {
          allUrlParams["context[group]"] = group;
        }
      }

      if (this.includeFilterParams) {
        // Sometimes the additional URL params will include the same filter as one of the filters already in the URL
        // So the order of the url params below is important, any duplicated keys will end up being the last one added.
        //
        // example: in the executive summary page there is a filter for project name but in a table each row
        // is for a project, so when the user clicks a link in that row to go to the issues-detail page, the
        // url should go to the page with the issues-details filtered on the row's project, not the page where
        // all of the projects selected in the filter are present.
        allUrlParams = {
          ...allUrlParams,
          ...restOfFilters,
          ...this.additionalUrlParams,
        };
      }

      let urlParamString = new URLSearchParams(allUrlParams).toString();

      if (this.isDoubleEncoded) {
        const params = new URLSearchParams();
        for (let key in allUrlParams) {
          params.set(key, encodeURIComponent(allUrlParams[key]));
        }

        urlParamString = params.toString();
      }

      const url = new URL(this.url, window.location.origin).href;

      if (urlParamString.length > 0) {
        return `${url}?${urlParamString}`;
      }

      return url;
    },
  },
};
</script>

<style scoped>
.tUrl {
  color: rgba(20, 93, 235);
}
</style>
