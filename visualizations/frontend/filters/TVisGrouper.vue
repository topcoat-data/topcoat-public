<script>
export default {
  props: {
    tClass: {
      String,
      default: "flex flex-wrap gap-2",
    },
  },
  data: () => ({
    init: false,
    is_filter: true,
  }),
  render: function (createElement) {
    var list = [];
    this.$slots.default.forEach((element, index) => {
      if (element.tag) {
        // If has no attribute object
        if (!element.data.attrs) {
          element.data = { attrs: {}, ...element.data };
        }

        // Add parent layer as attribute for topcoat-core
        element.data.attrs["t-parent-layer"] = this.layer;
        element.data.attrs["t-parent-tag"] = this.tag_unique;

        // Append slot element to list along with loader
        list.push(
          createElement(
            "div",
            {
              attrs: { class: "relative" },
            },
            [element]
          )
        );
      }
    });
    return createElement(
      "div",
      { attrs: { class: `relative ${this.tClass}` } },
      list
    );
  },
};
</script>
