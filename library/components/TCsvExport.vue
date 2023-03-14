<template>
  <button
    class="rounded cursor-pointer border-1 border-[#C3C2CB] text-[#555463] bg-white w-max p-1"
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
    additionalFilters: {
      type: Object,
      default: () => {},
    },
  },
  data: () => ({
    is_loading: false,
  }),
  methods: {
    download() {
      this.is_loading = true;
      const payload = {
        layer: this.tLayer,
      };
      let filters = this.getFiltersState() ? this.getFiltersState() : [];

      const formattedFilters = filters.reduce((acc, filter) => {
        return { ...acc, [filter.name]: filter.value };
      }, {});

      if (this.additionalFilters) {
        filters = { ...formattedFilters, ...this.additionalFilters };
      }

      this.trackExport("csv");
      payload.filters = filters;
      this.$store.dispatch("layers/exportCSV", payload).then((response) => {
        this.is_loading = false;
        let aTag = document.createElement("a");
        if (response.data.data.url) {
          aTag.setAttribute("href", response.data.data.url);
        } else {
          aTag.setAttribute(
            "href",
            "data:text/plain;charset=utf-8, " +
              encodeURIComponent(response.data.data)
          );
        }
        const filename = `${this.tLayer}.csv`;
        aTag.setAttribute("download", filename);
        document.body.appendChild(aTag);
        aTag.click();
        document.body.removeChild(aTag);
      });
    },
  },
};
</script>
