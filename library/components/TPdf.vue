<template>
    <div class="relative" @mouseover="handleTooltip" @mouseleave="showPdfTooltip = false">
        <!-- PDF tooltip -->
        <t-tooltip v-if="showPdfTooltip" position="left" width="400px">
            Your PDF is downloading. It may take up to 30 seconds to complete. Remain on the this page for the download to complete.
        </t-tooltip>

        <button
            class="bg-[#145DEB] border-[#145DEB] text-white text-sm px-2 py-[5px] rounded-[4px]"
            style="height: fit-content;"
            :disabled="is_loading"
            @click="downloadPdf"
            :class="is_loading && 'opacity-60'"
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
        data: () => ({
            showPdfTooltip: false,
        }),
        props: {
            label: {
                type: String,
                default: "Export to PDF"
            },
        },
        methods: {
            downloadPdf() {
                const url = this.page.url + window.location.search;
                this.showPdfTooltip = true;
                this.downloadPdfFile(url);
            },
            handleTooltip() {
                if (this.is_loading) {
                    this.showPdfTooltip = true;
                }
            }
        }
    } 
</script>