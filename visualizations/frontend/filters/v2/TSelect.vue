<template>
    <div class="relative">
        <div class="absolute top-0 left-0 z-40 w-full h-full m-auto cursor-not-allowed" v-if="loading" />
        <base-select
            :class="loading && 'opacity-90'"
            :options="menu"
            v-bind="props"
            v-model="selected"
            @change="updateUrlParam"
        />
    </div>
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
            },
            options() {
                const column_name = this.findColumnByTag('options');
                return this.getColumn(column_name);
            },
            labels() {
                const column_name = this.findColumnByTag('labels');
                return this.getColumn(column_name);
            },
            menu() {
                const values = this.options;
                const titles = this.labels;
                const menu = [];

                if (values && titles) {
                    for (let index in values) {
                        const value = values[index];
                        const title = titles[index];
                        menu.push({ value, title });
                    }
                }
                return menu;
            }
        },
        data: () => ({
            is_filter: true,
            selected: '',
        }),
        methods: {
            onVisualizationInit() {
                const initial_value = this.getFilterValue('dropdown');
                let option = null;

                if (initial_value) { // Value from url param.
                    option = this.menu.filter((item) => item.value == initial_value)[0];
                } else if (this.menu.length) {
                    if (this.config.default_value) { // Default value from layer
                        option = this.menu.filter((item) => item.value == this.config.default_value)[0];
                    } else if (this.defaultValue) { // Default value from prop
                        option = this.menu.filter((item) => item.value == this.defaultValue)[0];
                    }
                }

                if (!option && this.menu.length) {
                    option = this.menu[0];
                }
                console.log(option)
                this.selected = option ? option.value : '';
                this.setFilterValue('dropdown', option ? option.value : '', true);
            },
            updateUrlParam() {
                this.setFilterValue('dropdown', this.selected, true);
            }
        }
    }
</script>