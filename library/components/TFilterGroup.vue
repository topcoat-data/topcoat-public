<template>
	<t-dropdown
        :is-active="activeFilters > 0"
        @closed="handleClosed"
        z-index="800"
        :outsideElementClasses="outsideElementClasses"
    >
		  <!-- Handle -->
    	<div slot="handle" class="flex items-center gap-1 p-1 text-sm font-medium">
            <filter-variant-icon :size="18" />
            <span>{{ activeFilters ? '+' + activeFilters + ' Filters' : label }}</span>

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

        <t-expandable v-show="false" /> <!-- Bug: Render functions cannot use t-expandable without this line -->

        <div class="overflow-auto" :style="{ maxWidth, maxHeight }">
            <expansion-wrapper ref="expansionWrapper">
                <slot></slot>
            </expansion-wrapper>
        </div>

	</t-dropdown>
</template>

<script>
window.Vue.component('expansion-wrapper', {
    render: function (createElement) {
        var list = []

        //TODO: Refactor this function. Element componentInstance is not declare de first time we called this function so we are relying on re-renders
        //to make this code to work.
        //We are mutating _props.onExpandable here as well. We should not be doing that but it's the way we found to pass a prop from the slot to
        //the children.
        this.$slots.default.forEach((element, index) => {
            if (element.tag) {
                const label = element.data && element.data.attrs && element.data.attrs['item-label'] ? element.data.attrs['item-label'] : '-'
                const id = `${label.replace(" ", "_")}-${index}`;
                const tag_id = element && element.componentInstance ? element.componentInstance.tag_unique : '';

                list.push(
                    createElement('t-expandable', {
                        attrs: { id },
                        scopedSlots: {
                            default: (props) => {
                                if (element.componentInstance) {
                                    element.componentInstance._props.onExpandable = props.onExpandable;
                                }

                                return element;
                            },
                            label: (props) => {
                                return createElement('span', { attrs: { id: `elem-label-${tag_id}`, ref: 'label' } }, label);
                            },
                            icon: (props) => {
                                return createElement('div', { attrs: { class: 'active-round-element', id: `elem-icon-${tag_id}`, ref: 'icon' } });
                            }
                        }
                    })
                );
            }
        });

        return createElement('div', {}, list)
    }
});

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
        isPersisted: {
            type: Boolean,
            default: false,
        },
        outsideElementClasses: {
            type: Array,
            default: [],
        }
    },
    data: function () {
        return {
            popup: false,
            search: '',
            items: [],
            visibleFilters: [],
            activeFilters: 0,
            observer: null,
        };
    },
    mounted() {
        this.handleActiveFilters();
    },
    updated() {
        this.handleActiveFilters();
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
        },
        handleActiveFilters() {
            let setFilters = {}

            for (let component of this.$slots.default) {
                let componentInstance = component ? component.componentInstance : null;

                if (componentInstance) {
                    const metadata = componentInstance.metadata;
                    const filters = metadata && metadata.filters ? metadata.filters.output : [];

                    for (let filter of filters) {
                        const value = this.getFiltersState[filter.urlparam];

                        if (value) {
                            const obj = setFilters[componentInstance.tag_unique];
                            if (obj) {
                                setFilters[componentInstance.tag_unique].push(value);
                            } else {
                                setFilters[componentInstance.tag_unique] = [value];
                            }
                        } else {
                            this.showInactive(componentInstance.tag_unique);
                        }
                    }
                }
            }

            this.activeFilters = Object.keys(setFilters).length;
            this.showActive(setFilters);
        },
        showActive(setFilters) {
            for (let key of Object.keys(setFilters)) {
                const icon = document.getElementById(`elem-icon-${key}`);
                const label = document.getElementById(`elem-label-${key}`);

                if (icon) {
                    icon.style.display = "block"
                }

                if (label) {
                    label.classList.add('text-[#1C1C21]', 'font-medium');
                    label.classList.remove('text-[#555463]', 'font-normal');
                }
            }
        },
        showInactive(id) {
            const icon = document.getElementById(`elem-icon-${id}`);
            if (icon) {
                icon.style.display = "none";
            }

            const label = document.getElementById(`elem-label-${id}`);
            if (label) {
                label.classList.add('text-[#555463]', 'font-normal');
                label.classList.remove('text-[#1C1C21]', 'font-medium');
            }
        },
        handleClosed() {
            if (this.isPersisted) return;
            for (slotItem of this.$slots.default) {
                if (slotItem && slotItem.componentInstance && slotItem.componentInstance.$parent) {
                    slotItem.componentInstance.$parent.expanded = false;
                }
            }
        },
        onFiltersUpdated() {
            this.handleActiveFilters();
        }
    },
};
</script>

<style>
	.nav-search .vue--search-input__field {
		@apply !rounded-3xl !bg-white !opacity-[0.5];
	}
    .active-round-element {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #145DEB;
        display: none;
    }
</style>
