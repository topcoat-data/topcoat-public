<template>

	<t-dropdown
        :is-expanded="onExpandable"
        :is-active="checked.length ? true : false"
		@open="onDropdownOpen"
    >

		<!-- Handle -->
    	<div slot="handle" class="flex items-center gap-1 p-1 text-sm font-medium" v-if="!isExpanded">
			<div class="pl-1">
				<slot name="icon"></slot>
			</div>
            <span v-if="checked.length">
                {{ checked.length }}
            </span>
			<span>{{ label }}</span>

			<t-loading-spinner v-if="loading" position="relative" />
			<menu-down-icon v-else :size="20" />
    	</div>

		<!-- Popup Contents -->
		<div class="min-w-[294px]" v-bind="popupAttrs">
			<div class="px-[12px] pt-[16px] pb-[8px] flex justify-between items-center w-full">
				<h6 class="text-[10px] text-[#727184] font-semibold uppercase leading-[15px] tracking-widest" v-if="label">
					{{ label }}
				</h6>
				<span
					@click="selectUnselect"
					class="text-[#145DEB] text-[13px] cursor-pointer font-normal leading-[18px]"
					:class="checked.length ? 'text-[#145DEB]' : 'text-[#727184]'"
				>
					<t-loading-spinner v-if="isExpanded && loading" position="relative" />
					<span v-else>
						{{ checked.length < ids.length ? 'Select All' : 'Reset' }}
					</span>
				</span>
			</div>
			<div class="px-2 pt-2 nav-search" v-if="isSearchable">
				<base-search-input
					class="mt-0 mb-3 text-sm search-report !rounded-md"
					:placeholder="searchPlaceholder"
					size="small"
					:clearable="false"
					v-model="search"
				/>
			</div>
			<div class="px-[8px] pt-[4px] pb-[6px] w-full">
				<ul class="max-h-[320px] overflow-auto">
					<li
						class="flex justify-between px-[8px] pb-[1px] text-sm cursor-pointer text-[#555463]"
						v-for="(item, index) in menu"
						:key="index"
					>
						<div class="flex items-center justify-between w-full hover:text-[#1C1C21] leading-[16.41px]">
							<base-checkbox
								class="!min-w-[200px]"
								:label="item.title"
								:value="item.value"
								v-model="checked"
								@change="updateUrlParam"
							/>
						</div>
					</li>
					<small v-if="!menu.length && !loading">
						No items found
					</small>
				</ul>
			</div>
		</div>
	</t-dropdown>
</template>

<script>
	export default {
		props: {
            defaultValue: {
                type: String,
                default: '',
            },
			hasCheckedAll: {
				type: Boolean,
				default: false,
			},
			label: {
				type: String,
				default: ''
			},
			isSearchable: {
				type: Boolean,
				default: false,
			},
			searchPlaceholder: {
				type: String,
				default: 'Search',
			},
            isExpanded: {
                type: Boolean,
                default: false,
            },
			tKeyColumn: {
                type: String,
                default: '',
            },
            tValueColumn: {
                type: String,
                default: '',
            },
            onExpandable: {
                type: Boolean,
                default: false,
            },
		},
		data: () => ({
            checked: [],
			is_filter: true,
			search: '',
		}),
		computed: {
            names() {
				const column_name = this.tValueColumn ? this.tValueColumn : this.findColumnByTag('names');
				return this.getColumn(column_name);
            },
            ids() {
				const column_name = this.tKeyColumn ? this.tKeyColumn : this.findColumnByTag('ids');
				return this.getColumn(column_name, 'value');
            },
			menu() {
                const values = this.ids;
                const titles = this.names;
                const menu = [];

                if (values && titles) {
                    for (let index in values) {
                        const value = values[index] && values[index].toString();
                        const title = titles[index];

						if (this.isSearchable && !title.toLowerCase().includes(this.search.toLowerCase())) {
							continue;
						}

						if (value && title) {
							menu.push({ value, title });
						}
                    }
                }
                return menu;
            },
			popupAttrs() {
				let attrs = {};
				if (this.isExpanded) {
					attrs.slot = "outside";
				}
				return attrs;
			}
        },
		methods: {
            onVisualizationInit() {
				const initial_value = this.getFilterValue("selected_items");

                if (initial_value) {
                    this.checked = initial_value.split('|');
                } else if (this.defaultValue) {
                    this.checked = this.defaultValue.split('|');
                    this.setFilterValue("selected_items", this.defaultValue);
                }
            },
			selectUnselect() {
                if (this.checked.length === this.ids.length) {
                    this.checked = [];
                } else {
                    this.checked = this.ids;
                }
				this.updateUrlParam();
			},
            updateUrlParam() {
                this.setFilterValue("selected_items", this.checked.join('|'));
            },
            onDropdownOpen() {
                this.fetchLayerData();
            }
		}
	}
</script>

<style>
	.nav-search .vue--search-input__field {
		@apply !rounded-3xl !bg-white !opacity-[0.5];
	}
</style>