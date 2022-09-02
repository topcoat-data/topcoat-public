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
        <div ref="plot"></div>
      </div>
    </visualization-wrapper>
  </template>
  
  <script>
  export default {
    data: () => ({
        is_init: false,
        resizeObserver: null,
    }),
    computed: {
      plotlyHeight() {
        // Start with outermost height
        let height = this.$refs.top.clientHeight - 20;
  
        // If there is a title and/or subtitle
        if (this.$refs.title) {
          height -= this.$refs.title.offsetHeight;
        }

        if (this.$refs.subtitle) {
          height -= this.$refs.subtitle.offsetHeight;
        }

        return height;
      },
    },
    mounted() {
      this.resizeObserver = new ResizeObserver((entries) => {
        for (const entry of entries) {
          const update = {
            width: entry.contentRect.width
          };

          if (this.$refs.plot) {
            window.Plotly.relayout(this.$refs.plot, update);
          }
        }
      });

      this.resizeObserver.observe(this.$refs.plot);
    },
    beforeDestroy() {
      this.resizeObserver && this.resizeObserver.unobserve(this.$refs.plot);
    },
    methods: {
      plotlyRender() {
        const config = {
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
            this.$refs.plot,
            this.figure.data,
            Object.assign({}, this.figure.layout),
            config
          );
        } else {
          window.Plotly.purge(this.$refs.plot);
        }
      },
      onVisualizationInit() {
        // Temporary fix, plotly needs proper revamp.
        if (this.is_init) {
            return;
        }

        this.$nextTick(() => {
          this.handlePlotly();
          this.is_init = true;
        });
      },
      onVisualizationUpdated() {
        this.handlePlotly();
      },
      handlePlotly() {
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
    },
  };
  </script>