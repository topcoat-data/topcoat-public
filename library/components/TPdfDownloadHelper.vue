<template>
  <div v-if="isVisible" id="seleniumComponent" class="fixed top-0 bottom-0" />
</template>

<script>
export default {
  data: () => ({
    responses: 0,
    isVisible: false,
  }),
  watch: {
    responses: _.debounce(function (newVal) {
      this.showSeleniumComponent();
    }, 1000),
  },
  created() {
    this.countAjaxResponses();
  },
  methods: {
    countAjaxResponses() {
      var $this = this;
      axios.interceptors.response.use(
        function (response) {
          $this.responses += 1;
          return response;
        },
        function (error) {
          $this.responses += 1;
          return Promise.reject(error);
        }
      );
    },
    showSeleniumComponent() {
      this.isVisible = true;
    },
  },
};
</script>
