<template>
    <base-select
        :options="options"
        v-bind="props"
        v-model="selected"
        @change="updateUrlParam"
    />
</template>

<script>
    export default {
        props: {
            defaultValue: {
                type: String,
                default: '',
            }
        },
        computed: {
            props() {
                return this.$attrs;
            }
        },
        data: () => ({
            is_filter: true,
            options: [],
            selected: '',
        }),
        methods: {
            getItems() {
                const idColumn = this.findColumnByTag('options');
                const labelColumn = this.findColumnByTag('labels');

                const values = this.getColumn(idColumn);
                const titles = this.getColumn(labelColumn);
                const options = [];

                if (values && titles) {
                    for (let index in values) {
                        const value = values[index];
                        const title = titles[index];
                        options.push({ value, title });
                    }
                }
                this.options = options;
            },
            onVisualizationInit() {
                const initial_value = this.getFilterValue('dropdown');
                this.getItems();
                let option = null;

                if (initial_value) { // Value from url param.
                    option = this.options.filter((item) => item.value == initial_value)[0];
                } else if (this.options.length) {
                    if (this.config.default_value) { // Default value from layer
                        option = this.options.filter((item) => item.value == this.config.default_value)[0];
                    } else if (this.defaultValue) { // Default value from prop
                        option = this.options.filter((item) => item.value == this.defaultValue)[0];
                    } else { // First option available
                        option = this.options[0];
                    }
                } else {
                    return;
                }

                if (option) { // Update url param
                  this.selected = option.value;
                  this.setFilterValue('dropdown', option.value, true);
                }
            },
            updateUrlParam() {
                this.setFilterValue('dropdown', this.selected, true);
            }
        }
    }
</script>