<template>
    <div class="relative">
        <!-- PDF tooltip -->
        <t-tooltip position="left" width="400px" is-clickable>
            <button
                class="bg-[#145DEB] border-[#145DEB] text-white text-sm px-2 py-[5px] rounded-[4px]"
                style="height: fit-content;"
                :disabled="is_loading"
                @click="downloadPdf"
                :class="is_loading && 'opacity-60'"
                slot="trigger"
            >
                <div class="flex items-center gap-1">
                    {{ is_loading ? "Generating PDF" : label }}
                    <t-loading-spinner
                        v-if="is_loading"
                        position="relative"
                    />
                </div>
            </button>
            <div v-if="is_loading">
                Your PDF is downloading. It may take up to 30 seconds to complete. Remain on the this page for the download to complete.
            </div>
        </t-tooltip>
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
        methods: {
            downloadPdf() {
                const url = this.page.url + window.location.search;
                this.downloadPdfFile(url);
                this.trackExport("pdf");
            },
        }
    } 
</script>