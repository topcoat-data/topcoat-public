<template>
    <div>
        <label class="pb-1 text-sm font-medium" v-if="label">
          {{ label }}
        </label>
        <base-dropdown-menu class="mt-[5px]">
            <template #handle>
                <base-button
                    class="!bg-[#145DEB] !border-[#145DEB] !text-white"
                    :disabled="is_loading"
                >
                    <t-grids
                    gap="2"
                    column-count="2"
                    >
                    Export
                    <t-loading-spinner
                        v-if="is_loading"
                        position="relative"
                    />
                    <chevron-down-icon
                        v-else
                        class="pt-[2px]"
                    />
                    </t-grids>
                </base-button>
            </template>
            <base-dropdown-menu-item
                value="Export CSV"
                @click="download"
            />
        </base-dropdown-menu>
    </div>
</template>

<script>
  export default {
    props: {
      label: {
        type: String,
        default: '',
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
          return window.open(baseurl + params);
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