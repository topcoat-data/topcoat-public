<template>
  <button
    class="
      rounded
      cursor-pointer
      border-1 border-[#C3C2CB]
      text-[#555463]
      bg-white
      w-max
      p-1
    "
    style="height: fit-content"
    :disabled="is_loading"
    @click="download"
  >
    <div class="flex items-center gap-1">
      <t-loading-spinner v-if="is_loading" position="relative" />
      <download-outline-icon v-else :size="18" />
      {{ label }}
    </div>
  </button>
</template>

<script>
export default {
  name: "TCsvExport",
  props: {
    tLayer: {
      type: String,
      required: true,
    },
    label: {
      type: String,
      default: "Download CSV",
    },
  },
  data: () => ({
    is_loading: false,
  }),
  methods: {
    download() {
      this.is_loading = true;
      const queryString = window.location.search;
      const urlParams = new URLSearchParams(queryString);
      let filters = {};
      let filenameFilters = "";
      for (let filterKey of urlParams.keys()) {
        filters[filterKey] = urlParams.get(filterKey);
        filenameFilters += "-" + filterKey + "_" + urlParams.get(filterKey);
      }
      payload = {
        filters,
        layer: this.tLayer,
      };
      this.$store.dispatch("layers/exportCSV", payload).then((response) => {
        this.is_loading = false;
        let aTag = document.createElement("a");
        aTag.setAttribute(
          "href",
          "data:text/plain;charset=utf-8, " +
            encodeURIComponent(response.data.data)
        );
        let filename = this.tLayer + filenameFilters + ".csv";

        aTag.setAttribute("download", filename);
        document.body.appendChild(aTag);
        aTag.click();
        document.body.removeChild(aTag);
      });
    },
  },
};
</script>