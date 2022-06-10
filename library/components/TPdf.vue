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
            isNonAjax: {
                type: Boolean,
                default: false,
            }
        },
        data: () => ({
            is_filter: true,
            is_loading: false,
        }),
        methods: {
            downloadPdf() {
                if (!this.isNonAjax) {
                    if (this.is_loading) return;
                    this.is_loading = true;
                }
                const baseurl = `/downloadPdf/${this.page.tag}`
                const params = window.location.search;

                if (this.isNonAjax) {
                    return window.open(baseurl + params, "_self");
                }

                window.axios.get(baseurl + params, { responseType: 'blob' })
                .then(response => {
                    this.is_loading = false;

                    // If failed
                    if (response.data.status) {
                        return alert('Failed to download pdf');
                    }

                    // If successfull
                    const aTag = document.createElement('a');
                    var link = document.createElement('a');
                    link.href = window.URL.createObjectURL(response.data);
                    link.download = response.headers['content-disposition'].split("=")[1];
                    link.click();
                    return aTag.click();
                }).catch(error => {
                    this.is_loading = false;
                    console.error(error);
                    return alert('Failed to download pdf');
                })
            }
        }
    } 
</script>