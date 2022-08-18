<template>
    <div class="relative">

      <!-- PDF tooltip -->
      <base-tooltip id="tooltip" :open="showPdfTooltip">
          <span><!-- To hide default handle --></span>
          <span slot="description">
            Your PDF report generation is under process, will be downloaded shortly, please do not leave or close the page.
          </span>
    	</base-tooltip>

      <button
          class="bg-[#145DEB] border-[#145DEB] text-white text-sm px-2 py-[5px] rounded-[4px]"
          :class="is_loading && 'opacity-60 cursor-not-allowed'"
          style="height: fit-content;"
          :disabled="is_loading"
          @click="downloadPdf"
      >
          <div class="flex items-center gap-1">
              {{ is_loading ? "Generating PDF" : label }}
              <t-loading-spinner
                  v-if="is_loading"
                  position="relative"
              />
          </div>
      </button>
    </div>
</template>

<script>
    export default {
        props: {
            label: {
                type: String,
                default: "Export to PDF"
            },
        },
        data: () => ({
          showPdfTooltip: false,
        }),
        methods: {
            async downloadPdf() {
                const url = this.page.url + window.location.search;
                this.$emit("handlePdfDownload", true);
                this.showPdfTooltip = true;
                await this.downloadPdfFile(url);
                this.$emit("handlePdfDownload", false);
            }
        },
    } 
</script>