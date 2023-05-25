<template>
    <div class="sparkline">
    </div>
</template>

<script>
export default {
    props: {
        height: {
            type: Number,
            default: 200,
        },
        width: {
            type: Number,
            default: 400,
        },
        stroke: {
            type: String,
            default: "hsl(258.1, 100%, 66.9%)",
        },
        datum: {
            type: [String, Array],
            default: null,
        },
    },
    data() {
        return {
            _svg: null,
            _line: null,
            _markerLine: null,
            _markerDot: null,
            _width: null,
            _height: null,
            _text: null,
            _rect: null,
            fixedData: null,
        };
    },
    created() {
        if (this.datum && this.datum.length) {
            this.fixedData = Array.isArray(this.datum) ? this.datum : JSON.parse(this.datum);
        }
    },
    mounted() {
        const { width, height } = this.$refs.wrapper.$el.getBoundingClientRect();
        this._width = width;
        this._height = height;
        const el = this.$refs.wrapper.$el.querySelector('.sparkline');
        const wrapper = d3Select(el);
        this._svg = wrapper
            .append('svg')
            .attr('height', `${height}px`)
            .attr('width', `${width}px`);

        this._line = this._svg
            .append('path')
            .attr('stroke', this.stroke)
            .attr('stroke-width', 1)
            .attr('stroke-linejoin', 'round')
            .attr('fill', 'none');

        this._markerLine = this._svg
            .append('line')
            .attr('x1', 0)
            .attr('x2', 0)
            .attr('y1', 0)
            .attr('y2', this._height - 0.5)
            .attr('stroke-width', 1)
            .attr('stroke', '#727184')
            .attr('opacity', 0);

        this._markerDot = this._svg
            .append('circle')
            .attr('cx', 0)
            .attr('cy', 0)
            .attr('r', 2)
            .attr('fill', this.stroke)
            .attr('opacity', 0);

        this._tooltip = this._svg
            .append('g')
            .append('g')
            .attr('class', 'tooltip')
            .attr('opacity', 0);

        this._rect = this._tooltip
            .append('rect')
            .attr('width', '16px')
            .attr('height', '16px')
            .attr('x', '0')
            .attr('y', '0');

        this._text = this._tooltip
            .append('text')
            .attr('text-anchor', 'middle')
            .attr('x', '8px')
            .attr('y', '0')
            .append('tspan')
            .attr('dy', '13px');

        if (this.fixedData && this.fixedData.length) {
            this.createSparkline();
        }
    },
    computed: {
        tooltipPositioning() {
            const quadrantPosition = new Map();
            quadrantPosition.set(0, function (textLength, fontSize) {
                return function (x, y) {
                    return {
                        x: x - (textLength + 2),
                        y: y,
                    };
                };
            });
            quadrantPosition.set(1, function (textLength, fontSize) {
                return function (x, y) {
                    return {
                        x: x + 2,
                        y: y ,
                    };
                };
            });
            quadrantPosition.set(2, function (textLength, fontSize) {
                return function (x, y) {
                    return {
                        x: x + 2,
                        y: y - (fontSize * 1.5),
                    };
                };
            });
            quadrantPosition.set(3, function (textLength, fontSize) {
                return function (x, y) {
                    return {
                        x: x - (textLength + 2),
                        y: y - (fontSize * 1.5),
                    };
                };
            });

            return quadrantPosition;
        },
    },
    methods: {
        onVisualizationUpdated() {
            this.$nextTick(() => {
                this.createSparkline();
            });
        },
        xAccessor(d) {
            return d.x;
        },
        yAccessor(d) {
            return d.y;
        },
        getQuadrant(x, y) {
            const center_x = this._width / 2;
            const center_y = this._height / 2;

            if (x > center_x && y < center_y) {
                return 0;
            }
            
            if (x < center_x && y < center_y) {
                return 1;
            }
            
            if (x <= center_x && y >= center_y) {
                return 2;
            }
            
            if (x >= center_x && y >= center_y) {
                return 3;
            }

            return 0;
        },
        createSparkline() {
            // TODO: This is a hack to get the width and height of the sparkline
            // to render properly on TTable. It seems that cells get rendered after
            // the DOM element is created and width and height are not available.
            if (this._width === 0 || this._height === 0) {
                const { width, height } = this.$refs.wrapper.$el.getBoundingClientRect();

                this._width = width;
                this._height = height;
            }

            const data = [];
            const xColumn = this.dimensions[0];
            const yColumn = this.measures[0];
            const hasFetchedData = this.fixedData && this.fixedData.length ? false : true;
            
            if (hasFetchedData) {
                for (let i = 0; i < this.rows.length; i++) {
                    data.push({
                        x: new Date(this.rows[i][xColumn].rendered),
                        y: this.rows[i][yColumn].value,
                    });
                }
            } else {
                for (let i = 0; i < this.fixedData.length; i++) {
                    data.push({
                        x: i,
                        y: this.fixedData[i],
                    });
                }
            }

            const xDomain = d3Extent(data, this.xAccessor);
            const maxY = d3Max(data, this.yAccessor);
            const minY = d3Min(data, this.yAccessor);
            const yDomain = [minY,  maxY === 0 ? 1 : maxY];

            const xScale = hasFetchedData ? d3ScaleTime() : d3ScaleLinear();
            
            xScale
                .domain(xDomain)
                .range([0, this._width]);

            const yScale = d3ScaleLinear()
                .domain(yDomain)
                .range([this._height - 0.5, 0.5]);

            const lineGenerator = d3Line()
                .x((d) => xScale(this.xAccessor(d)))
                .y((d) => yScale(this.yAccessor(d)));

            this._line
                .datum(data)
                .attr('d', lineGenerator);

            const bisect = d3Bisector(this.xAccessor);

            this._svg.on('mousemove', (e) => {
                const [xCoord] = d3Pointer(e);
                const xCoordDomain = xScale.invert(xCoord);
                const index = bisect.center(data, xCoordDomain);
                const point = data[index];
                const xDomain = this.xAccessor(point);
                const yDomain = this.yAccessor(point);
                const x = xScale(xDomain);
                const y = yScale(yDomain);

                this._markerLine
                    .attr('x1', x)
                    .attr('x2', x)
                    .attr('opacity', 1);

                this._markerDot
                    .attr('cx', x)
                    .attr('cy', y)
                    .attr('opacity', 1);


                const valueLength = yDomain.toString().length;
                const chartWidth = 8;
                const textLength = valueLength * chartWidth;
                const fontSize = 12;

                const quadrant = this.getQuadrant(x, y);
                const tooltipPosition = this.tooltipPositioning.get(quadrant)(textLength, fontSize)(x, y);
                this._tooltip
                    .attr("opacity", 1)
                    .attr("transform", "translate(" 
                    + tooltipPosition.x + "," 
                    + tooltipPosition.y + ")");

                this._rect
                    .attr('width', `${textLength}px`);

                this._text
                    .attr('x', `${textLength / 2}px`);

                this._text.text(yDomain);
            });

            this._svg.on('mouseleave', () => {
                this._markerLine.attr('opacity', 0);
                this._markerDot.attr('opacity', 0);
                this._tooltip.attr("opacity", 0)
            });
        }
    },
};
</script>

<style scoped>
    .sparkline svg:hover {
        cursor: crosshair;
    }

    .sparkline .tooltip {
        pointer-events:none; /*let mouse events pass through*/
        transition: opacity 0.2s;
        font-size: 12px;
    }

    .sparkline .tooltip rect {
        fill: #ffffff;
        fill-opacity: 0.7;
    }
</style>
