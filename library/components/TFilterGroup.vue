<template>
	<t-dropdown
        :is-active="activeFilters > 0"
        @closed="handleClosed"
        z-index="800"
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
    window.Vue.component('expansion-wrapper',{
        render: function(createElement) {
            var list = []
            this.$slots.default.forEach((element,index) => {
                if (element.tag) {
                    const label = element.data && element.data.attrs && element.data.attrs['item-label'] ? element.data.attrs['item-label'] : '-'
                    const id = `${label.replace(" ", "_")}-${index}`;
                    const tag_id = element && element.componentInstance ? element.componentInstance.tag_unique : '';
                    list.push(
                        createElement('t-expandable', {attrs: { id }}, 
                            [
                                createElement('span', {slot: 'label', attrs: { id: `elem-label-${tag_id}` }}, label),
                                createElement('div', {slot: 'icon', attrs: { class: 'active-round-element', id: `elem-icon-${tag_id}` }}),
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
            isPersisted: {
                type: Boolean,
                default: false,
            }
        },
        data: () => ({
            popup: false,
            search: '',
            items: [],
            visibleFilters: [],
			activeFilters: 0,
            filters: {},
            observer: null,
        }),
        mounted() {
            this.observeUrlChanges();
        },
        destroyed() {
            if (this.observer) {
                this.observer.disconnect();
            }
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
                this.filters = [];
                for (let component of this.$slots.default) {
                    let componentInstance = component ? component.componentInstance : null;
                    if (componentInstance) {
                        const metadata = componentInstance.metadata;
                        const filters = metadata && metadata.filters ? metadata.filters.output : [];
                        for (let filter of filters) {
                            const value = this.getValueByUrl(filter.urlparam);
                            if (value) {
                                const obj = this.filters[componentInstance.tag_unique];
                                if (obj) {
                                    this.filters[componentInstance.tag_unique].push(value);
                                } else {
                                    this.filters[componentInstance.tag_unique] = [value];
                                }
                            } else {
                                this.showInactive(componentInstance.tag_unique);
                            }
                        }
                    }
                }
                this.activeFilters = Object.keys(this.filters).length;
                this.showActive();
            },
            getValueByUrl(urlParam) {
                const params = new URLSearchParams(location.search)
                return params.get(urlParam);
            },
            showActive() {
                for (let key of Object.keys(this.filters)) {
                    const icon = document.getElementById(`elem-icon-${key}`);
                    if (icon) {
                        icon.style.display = "block"
                    }
                    const label = document.getElementById(`elem-label-${key}`);
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
            observeUrlChanges() {
                let previousUrl = '';
                const ref = this;
                this.observer = new MutationObserver(function(mutations) {
                    if (location.href !== previousUrl) {
                        ref.handleActiveFilters();
                    }
                });
                const config = {subtree: true, childList: true};
                this.observer.observe(document, config);
            }
        },
    }
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
