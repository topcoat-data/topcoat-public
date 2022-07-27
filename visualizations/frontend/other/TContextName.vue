<template>
    <div v-if="text">
        {{ text }}
    </div>
</template>

<script>
    export default {
        props: {
            itemId: String,
            tKeyColumn: String,
            tValueColumn: String,
        },
        data: () => ({
            is_filter: true,
            text: '',
        }),
        computed: {
            keys() {
                if (this.tKeyColumn) {
                    return this.getColumn(this.tKeyColumn)
                }
                return [];
            },
            values() {
                if (this.tValueColumn) {
                    return this.getColumn(this.tValueColumn)
                }
                return [];
            },
            items() {
                const keys = this.keys;
                const values = this.values;
                const items = [];

                if (values && keys) {
                    for (let index in keys) {
                        const key = keys[index];
                        const value = values[index];
                        items.push({ key, value });
                    }
                }
                return items;
            },
        },
        methods: {
            onVisualizationInit() {
                if (this.itemId && this.items && this.items.length) {
                    for (let item of this.items) {
                        if (item.key === this.itemId) {
                            this.text = item.value;
                        }
                    }
                }
            }
        }
    }
</script>