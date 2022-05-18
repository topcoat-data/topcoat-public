<template>
  <div class="cursor-pointer border bg-[#145DEB] border-[#145DEB] !hover:bg-[#0f47c6] hover:border-[#0f47c6] px-2 py-1 rounded text-white gap-2 flex items-center" @click="redirect">
    {{ title }} <chevron-down-icon />
  </div>
</template>

<script>
  export default {
    props: {
      title: {
        type: String,
        default: 'Export CSV',
      }
    },
    data: () => ({
      is_filter: true,
    }),
    layer() {
      const layers = this.config.layers;
      return layers && layers.length ? layers[0] : null;
    },
    methods: {
      redirect() {
        const baseurl = `/downloadCsv/${this.layer}`
        const urlParams = new URLSearchParams(location.search);

        let params = '?';

        for (let filter of this.config.filters.input) {
          const value = urlParams.get(filter.name);
          if (value) {
            params += `${filter.name}=${value}&`;
          }
        }
        window.location.href = baseurl + params;
      },
    }
  }
</script>