<template>
    <base-input v-bind="props" v-model="value"  @keyup.enter="updateUrlParam" />
</template>

<script>
export default {
    data: () => ({
        value: '',
        is_filter: true,
    }),
    computed: {
        props() {
            return this.$attrs;
        }
    },
    methods: {
        onVisualizationInit() {
            const initial_value = this.getFilterValue('query')
            if (initial_value) {
                this.value = initial_value
            } else if (this.config.default_value) {
                this.value = this.config.default_value
            } else {
                return
            }
            this.setFilterValue('query', this.value, true)
        },
        updateUrlParam() {
            this.setFilterValue('query', this.value, true)
        }
    }
}
</script>