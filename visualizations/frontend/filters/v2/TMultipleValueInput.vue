<template>
    <base-multiple-value-input
        class="!min-w-[200px]"
        :data="data"
        selection-only
        v-bind="props"
        v-model="values"
    />
</template>

<script>
    export default {
        computed: {
            props() {
                return this.$attrs;
            },
        },
        data: () => ({
            data: [],
            is_filter: true,
            values: [],
        }),
        methods: {
            onVisualizationInit() {
                const initial_value = this.getFilterValue('selected_items')
                let urlParams = ''
                this.getItems()

                if (initial_value) {
                    // Url has selected value (url param is id).
                    this.findItems(initial_value)
                    urlParams = initial_value
                } else if (this.config.default_value) {
                    this.findItems(this.config.default_value)
                    urlParams = this.config.default_value
                } else {
                    // Found nothing, keep url empty.
                    return this.unsetFilterValue('selected_items', true)
                }
                this.setFilterValue('selected_items', urlParams, true)
            },
            getItems() {
                const idColumn = this.findColumnByTag('ids');
                const nameColumn = this.findColumnByTag('names');

                const ids = this.getColumn(idColumn);
                const names = this.getColumn(nameColumn);

                const data = [];
                if (ids && names) {
                    for (let index in ids) {
                        const id = ids[index];
                        const name = names[index];
                        data.push({ id, name });
                    }
                }
                this.data = data;
            },
        },
    }
</script>