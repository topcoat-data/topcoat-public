<template>
    <button
        class="bg-[#145DEB] border-[#145DEB] text-white text-sm px-2 py-[5px] rounded-[4px]"
        style="height: fit-content;"
        :disabled="is_loading"
        @click="downloadPdf"
    >
        <div class="flex items-center gap-1">
            {{ label }}
            <t-loading-spinner
                v-if="is_loading"
                position="relative"
            />
        </div>
    </button>
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
                return this.downloadPdfFile(url);
            }
        }
    } 
</script>