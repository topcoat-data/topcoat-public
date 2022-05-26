<template>
    <base-multiple-value-input
        class="!min-w-[200px]"
        :data="menu"
        :loading="loading"
        v-bind="props"
        v-model="values"
        display-key="name"
        value-key="id"
        @update="update"
        selection-only
    />
</template>

<script>
    export default {
        computed: {
            props() {
                return this.$attrs;
            },
            names() {
                const column_name = this.findColumnByTag('names');
                return this.getColumn(column_name);
            },
            ids() {
                const column_name = this.findColumnByTag('ids');
                return this.getColumn(column_name);
            },
            menu() {
                let menu = [];
                for (let index in this.names) {
                    const id = this.ids[index].replace(/,/g,"");
                    const name = this.names[index];
                    menu.push({ id, name });
                }
                return menu;
            }
        },
        data: () => ({
            is_filter: true,
            values: [],
        }),
        methods: {
            findItems(urlParam) {
                const ids = urlParam.split('|');
                const values = [];
                if (ids.length && this.menu.length) {
                    for (let item of this.menu) {
                        if (ids.indexOf(item.id) > -1) {
                            values.push(item.id);
                        }
                    }
                }
                this.values = values;
            },
            onVisualizationInit() {
                const initial_value = this.getFilterValue('selected_items')
                let urlParams = ''

                if (initial_value) {
                    // Url has selected value (url param is id).
                    this.findItems(initial_value)
                    urlParams = initial_value.split('|').filter(id => this.values.indexOf(id) > -1).join('|');
                } else if (this.config.default_value) {
                    this.findItems(this.config.default_value)
                    urlParams = this.config.default_value.split('|').filter(id => this.values.indexOf(id) > -1).join('|');
                }
                this.setFilterValue('selected_items', urlParams, true)
            },
            update(item) {
                this.setFilterValue('selected_items', item.join('|'), true)
            }
        },
    }
</script>