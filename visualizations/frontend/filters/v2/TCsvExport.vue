<template>
	<button
        class="rounded cursor-pointer border-1 border-[#C3C2CB] text-[#555463] bg-white w-max p-1"
        style="height: fit-content;"
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
    props: {
      label: {
        type: String,
        default: 'Download CSV',
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
      download() {
        if (!this.isNonAjax) {
          if (this.is_loading) return;
          this.is_loading = true;
        }
        const baseurl = `/downloadCsv/${this.layer}`
        const urlParams = new URLSearchParams(location.search);
        let params = '?';
        for (let filter of this.config.filters.input) {
          const value = urlParams.get(filter.name);
          if (value) {
            params += `${filter.name}=${value}&`;
          }
        }
        if (this.isNonAjax) {
          return window.open(baseurl + params, "_self");
        }
        window.axios.get(baseurl + params)
          .then(response => {
            this.is_loading = false;
            const aTag = document.createElement('a');
            aTag.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent(response.data);
            aTag.target = '_blank';
            aTag.download = response.headers['content-disposition'].split("=")[1];
            return aTag.click();
          }).catch(error => {
            this.is_loading = false;
            console.error(error);
          })
      },
    },
  }
</script>