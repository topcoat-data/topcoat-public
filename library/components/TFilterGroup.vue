<template>
	<t-dropdown>

		  <!-- Handle -->
    	<div slot="handle" class="flex items-center gap-1 p-1 text-sm">
            <filter-variant-icon :size="18" />
            <span>{{ totalItems ? totalItems + ' Filters' : label }}</span>

            <menu-down-icon :size="20" />
    	</div>

        <!-- Contents -->
        <div class="px-[12px] pt-[16px] pb-[8px] flex justify-between items-center">
            <h6 class="text-[10px] text-[#727184] font-semibold uppercase leading-[15px] tracking-widest">Filters</h6>
            <span class="text-[#145DEB] text-[13px] cursor-pointer font-normal leading-[18px]">
            <!-- Clear All -->
            </span>
        </div>

        <div class="px-3 pt-2 nav-search">
            <base-search-input
                class="mt-0 mb-3 text-sm !rounded-md" 
                placeholder="Search Filters"
                size="small"
                v-model="search"
                :clearable="false"
                @change="searchFilter"
            />
        </div>

        <t-expandable v-show="false" />
        <!-- Bug: Render functions cannot use t-expandable without this line -->
        <div class="overflow-auto" :style="{ maxWidth, maxHeight }">
            <expansion-wrapper ref="expansionWrapper">
                <slot></slot>
            </expansion-wrapper>
        </div>

	</t-dropdown>
</template>

<script>
    window.Vue.component('expansion-wrapper',{
        render: function(createElement) {
            var list = []
            this.$slots.default.forEach((element,index) => {
                if (element.tag) {
                    const label = element.data && element.data.attrs && element.data.attrs['item-label'] ? element.data.attrs['item-label'] : '-'
                    const id = `${label.replace(" ", "_")}-${index}`;
                    list.push(
                        createElement('t-expandable', {attrs: { id }}, 
                            [
                                createElement('span', {slot: 'label'}, label),
                                element
                            ]
                        )
                    )
                }
            });
            return createElement('div',{},list)
        }
    })
    export default {
        props: {
            label: {
                type: String,
                default: 'Add filters'
            },
            maxHeight: {
                type: String,
                default: '300px'
            },
            maxWidth: {
                type: String,
                default: '400px'
            },
        },
        data: () => ({
            popup: false,
            search: '',
            items: [],
            visibleFilters: [],
			totalItems: 0,
        }),
		mounted() {
			const element = this.$refs.expansionWrapper;
			const children = element ? element.$children : [];
			this.totalItems = children.length;
		},
        methods: {
            searchFilter() {
                const children = this.$refs.expansionWrapper.$children || [];
                for (let child of children) {

                    const id = child.$attrs.id;
                    const element = document.getElementById(id);

                    if (element) {
                        if (id.toLowerCase().includes(this.search.toLowerCase())) {
                            element.style.display = "block";
                        } else {
                            element.style.display = "none";
                        }
                    }
                }
            }
        }
    }
</script>

<style>
	.nav-search .vue--search-input__field {
		@apply !rounded-3xl !bg-white !opacity-[0.5];
	}
</style>
