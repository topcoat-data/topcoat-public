<template>
    <div class="relative">
      <t-modal
        @close-clicked="showPdfModal = false"
        :is-open="showPdfModal"
      >
        <div class="max-w-[552px] text-center">
          <div class="text-2xl font-sans pb-3 text-[#1C1C21]">
            Snyk is generating a PDF
          </div>
          <div class="text-[#555463]">
            Your PDF report generation is under process, will be downloaded shortly, please do not leave or close the page.
          </div>
        </div>
      </t-modal>
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
          showPdfModal: false,
        }),
        methods: {
            async downloadPdf() {
                const url = this.page.url + window.location.search;
                this.$emit("handlePdfDownload", true);
                this.showPdfModal = true;
                await this.downloadPdfFile(url);
                this.$emit("handlePdfDownload", false);
            }
        },
    } 
</script>