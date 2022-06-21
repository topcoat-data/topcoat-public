<template>
    <span>
        {{ label }}
    </span>
</template>

<script>
    export default {
        props: {
            filters: {
                type: [Array, String],
                default: [],
            }
        },
        data: () => ({
            is_filter: true,
        }),
        computed: {
            label() {
                let label = '';
                let globalFilters = this.global_filters;
                let filters = typeof this.filters === 'string' ? [this.filters] : this.filters;
                for (let filter of filters) {
                    let current = globalFilters[filter];
                    if (typeof current === 'object' && current.hasOwnProperty('title')) {
                        label = `Issues in ${current.title}`;
                        break;
                    }
                }
                return label;
            }
        },
    }
</script>