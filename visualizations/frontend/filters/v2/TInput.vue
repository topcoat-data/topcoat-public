<template>
    <base-input
        v-bind="props"
        v-model="value" 
        @change="() => { props.type && props.type === 'date' && updateUrlParam() }"
        @keyup.enter="updateUrlParam"
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
        value: '',
    }),
    methods: {
        onVisualizationInit() {
            const initial_value = this.getFilterValue('query');
            if (initial_value) { // Value from url param.
                this.value = initial_value;
            } else if (this.config.default_value) { // Default value from layer
                this.value = this.config.default_value;
            } else if (this.defaultValue) { // Default value from prop
                this.value = this.defaultValue;
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