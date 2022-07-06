<script>
    export default {
        props: {
            tClasses: {
                String,
                default: "flex flex-wrap gap-2"
            },
        },
        data: () => ({
            is_filter: true,
        }),
        render: function (createElement) {
            var list = []
            this.$slots.default.forEach((element,index) => {
                if (element.tag) {

                    // If has no attribute object
                    if (!element.data.attrs) {
                        element.data = { attrs: {}, ...element.data }
                    }

                    // Add parent layer as attribute for topcoat-core
                    element.data.attrs['t-parent-layer'] = this.layer;

                    // Append slot element to list along with loader
                    list.push(
                        createElement('div',
                        {
                            attrs: { class: 'relative' }
                        },
                        [
                            element,
                            this.loading && createElement('t-loading-spinner')
                        ]),
                    )
                }
            });
            return createElement('div', { attrs: { class: `relative ${this.tClasses}` } }, list);
        },
        methods: {
            onVisualizationUpdated() {
                // Update layer data
                this.fetchLayerData();
            }
        }
    }
</script>