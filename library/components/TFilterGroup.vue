<template>
	<t-dropdown>

		  <!-- Handle -->
    	<div slot="handle" class="flex items-center gap-1 py-1 text-sm">
            <filter-variant-icon size="18" class="pl-1" />
            <span>{{ label }}</span>

            <menu-down-icon size="20" class="pr-1" />
    	</div>

        <!-- Contents -->
        <div class="px-[12px] pt-[16px] pb-[8px] flex justify-between items-center">
            <h6 class="text-[10px] text-[#727184] font-semibold uppercase leading-[15px]">Filters</h6>
            <span class="text-[#145DEB] text-[13px] cursor-pointer font-normal leading-[18px]">
            <!-- Clear All -->
            </span>
        </div>

        <div class="px-3 pt-2 nav-search">
            <base-search-input
                class="mt-0 mb-3 text-sm !rounded-md" 
                placeholder="Search Filters"
                size="small"
                clearable
                v-model="search"
            />
        </div>

        <t-expandable v-show="false" />

        <expansion-wrapper>
            <slot></slot>
        </expansion-wrapper>

	</t-dropdown>
</template>

<script>
    window.Vue.component('expansion-wrapper',{
        render: function(createElement) {
            var list = []
            this.$slots.default.forEach((element,index) => {
                if (element.tag) {
                    const label = element.data && element.data.attrs['item-label'] ? element.data.attrs['item-label'] : '-'
                    list.push(
                        createElement('t-expandable', {}, 
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
                default: 'Select'
            },
        },
        data: () => ({
            popup: false,
            search: '',
            items: []
        }),
    }
</script>

<style>
	.nav-search .vue--search-input__field {
		@apply !rounded-3xl !bg-white !opacity-[0.5];
	}
</style>
