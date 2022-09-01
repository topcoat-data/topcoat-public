<template>
  <visualization-wrapper ref="wrapper" v-slot="{ height }">
    <div style="width: inherit; height: inherit; padding: 10px" ref="top">
      <div
        v-if="metadata && metadata.title"
        ref="title"
        style="padding: 10px; font-weight: 700; font-size: 16px"
      >
        {{ metadata.title }}
      </div>
      <div
        v-if="metadata && metadata.subtitle"
        ref="subtitle"
        style="font-weight: 400; font-size: 12px"
      >
        {{ metadata.subtitle }}
      </div>
      <div :id="tag_unique + _uid + '_plot'" ref="plot"></div>
    </div>
  </visualization-wrapper>
</template>

<script>
export default {
  data: () => ({
      is_init: false,
  }),
  computed: {
    plotlyHeight: function () {
      // Start with outermost height
      var height = this.$refs.top.clientHeight - 20;

      // If there is a title and/or subtitle
      if (this.$refs.title) height -= this.$refs.title.offsetHeight;
      if (this.$refs.subtitle) height -= this.$refs.subtitle.offsetHeight;
      return height;
    },
  },
  methods: {
    plotlyRender: function () {
      var config = {
        displaylogo: false,
        scrollZoom: false,
        displayModeBar: false,
        modeBarButtonsToRemove: [
          "sendDataToCloud",
          "toImage",
          "lasso2d",
          "select2d",
          "pan2d",
          "zoomIn2d",
          "zoomOut2d",
          "autoScale2d",
          "hoverCompareCartesian",
          "hoverClosestCartesian",
          "toggleSpikelines",
          "toggleHover",
          "hoverClosestPie",
          "hoverClosestGeo",
          "zoom3d",
          "pan3d",
          "orbitRotation",
          "tableRotation",
          "handleDrag3d",
          "resetCameraDefault3d",
          "resetCameraLastSave3d",
          "hoverClosest3d",
        ],
      };
      if (this.figure && this.figure.data) {
        this.figure.layout.height = this.plotlyHeight;
        this.figure.layout.width = this.$refs.top.offsetWidth - 20;
        window.Plotly.react(
          this.tag_unique + this._uid + "_plot",
          this.figure.data,
          Object.assign({}, this.figure.layout),
          config
        );
      } else {
        console.log("reaching - 2")
        window.Plotly.purge(this.tag_unique + this._uid + "_plot");
      }
    },
    onVisualizationInit: function () {
      // Temporary fix, plotly needs proper revamp.
      if (this.is_init) return;
      this.$nextTick(() => {
        this.handlePlotly();
        this.is_init = true;
      });
    },
    onVisualizationUpdated: function () {
      console.log("update called")
      this.handlePlotly();
    },
    handlePlotly: function() {
      this.plotlyRender();
      if (this.$refs.plot.on) {
        this.$refs.plot.on("plotly_click", function (data) {
          if (typeof data.points[0].customdata != "undefined") {
            if (data.points[0].customdata.type == "drilldown") {
              const url = data.points[0].customdata.format
                .split("#drilldown_url=")[1]
                .replace("{}", data.points[0].customdata.value);
              window.location.assign(url);
            }
          }
        });
      }
    },
    wldFigureResize: function () {
      var update = {
        width: this.$refs.top.offsetWidth,
        height: this.plotlyHeight,
      };
      window.Plotly.relayout(this.tag_unique + this._uid + "_plot", update);
    },
  },
  watch: {
    filters: {
      handler(n, o) {
        this.$nextTick(() => {
            console.log({n, o})
          this.handlePlotly();
        })
      },
      deep: true,
    }
  }
};
</script>
