<template>
  <div
    class="relative"
    @mouseover="showTooltip = true"
    @mouseleave="showTooltip = false"
  >
    <!-- PDF tooltip -->
    <t-tooltip
      position="left"
      width="400px"
      :is-open="is_loading && showTooltip"
    >
      <button
        slot="trigger"
        class="bg-[#145DEB] border-[#145DEB] text-white text-sm px-2 py-[5px] rounded-[4px]"
        style="height: fit-content"
        :disabled="is_loading"
        :class="is_loading && 'opacity-60'"
        @click="downloadPdf"
      >
        <div slot="handle" class="flex items-center gap-1 text-sm font-normal">
          <slot name="icon"></slot>
          <div class="flex items-center gap-1">
            {{ is_loading ? "Generating PDF" : label }}
            <t-loading-spinner v-if="is_loading" position="relative" />
          </div>
        </div>
      </button>
      <div v-if="is_loading && showTooltip">
        Your PDF is downloading. It may take up to 30 seconds to complete.
        Remain on this page for the download to complete.
      </div>
    </t-tooltip>
  </div>
</template>

<script>
export default {
  props: {
    label: {
      type: String,
      default: "Export to PDF",
    },
    options: {
      type: Object,
      default: {},
    },
    absoluteDateFilter: {
      type: Object,
      default: {},
      // { name: "end_date", format: "YYYY-MM-DD" }
    },
    timeout: {
      type: Number,
      default: 300,
    },
    errorMessage: {
      type: String,
      default: "Failed to download PDF",
    },
  },
  data: () => ({
    showTooltip: false,
  }),
  computed: {
    endDateFilter() {
      let filter = this.absoluteDateFilter;
      let filterName = filter.name;
      if (filterName && !this.getFilterState(filter.name)) {
        let todayDate = window
          .Moment()
          .format(filter.format ? filter.format : "YYYY-MM-DD");
        return `&${filterName}=${todayDate}`;
      }
      return "";
    },
  },
  methods: {
    downloadPdf() {
      const url = this.page.url + window.location.search + this.endDateFilter;
      this.downloadPdfFile(url, {
        pdf: this.options,
        timeout: this.timeout,
        errorMessage: this.errorMessage,
      });
      this.trackExport("pdf");
    },
  },
};
</script>
