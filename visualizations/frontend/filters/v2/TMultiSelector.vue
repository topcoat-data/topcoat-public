<template>
	<t-dropdown>

		<!-- Handle -->
    	<div slot="handle" class="flex items-center gap-1 py-1 text-sm">
			<div class="pl-1">
				<slot name="icon"></slot>
			</div>
			<span>{{ label }}</span>

			<t-loading-spinner v-if="loading" position="relative" />
			<menu-down-icon v-else size="20" class="pr-1" />
    	</div>

		<!-- Popup Contents -->
		<div class="min-w-[294px]">
			<div class="px-[12px] pt-[16px] pb-[8px] flex justify-between items-center w-full" v-if="menuLabel">
				<h6 class="text-[10px] text-[#727184] font-semibold uppercase leading-[15px]">
					{{ menuLabel }}
				</h6>
				<span
					@click="reset"
					class="text-[#145DEB] text-[13px] cursor-pointer font-normal leading-[18px]"
					:class="checked.length ? 'text-[#145DEB]' : 'text-[#727184]'"
				>
					Reset
				</span>
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
			hasCheckedAll: {
				type: Boolean,
				default: false,
			},
			label: {
				type: String,
				default: 'Select'
			},
            menuLabel: {
                type: String,
				default: ''
            },
			selectedAsLabel: {
				type: Boolean,
				default: false,
			}
		},
		data: () => ({
			is_filter: true,
            checked: [],
		}),
		computed: {
            names() {
                try {
                    const column_name = this.findColumnByTag('names');
                    return this.getColumn(column_name);
                } catch (err) {
                    return []
                }
            },
            ids() {
                try {
                    const column_name = this.findColumnByTag('ids');
                    return this.getColumn(column_name);
                } catch (err) {
                    return []
                }
            },
			menu() {
                const values = this.ids;
                const titles = this.names;
                const menu = [];

                if (values && titles) {
                    for (let index in values) {
                        const value = values[index];
                        const title = titles[index];
                        menu.push({ value, title });
                    }
                }
                return menu;
            }
		},
		methods: {
            onVisualizationInit() {
                // See if the page was loaded with a url param value
                const initial_value = this.getFilterValue("selected_items");
                if (initial_value) {
                    this.checked = initial_value.split('|').filter(id => this.ids.indexOf(id) > -1);
                }

				if (!initial_value && typeof initial_value !== 'string' && this.hasCheckedAll) {
					this.checked = this.ids;
				}
                this.setFilterValue("selected_items", this.checked.join('|'), true);
            },
			reset() {
				this.checked = [];
				this.updateUrlParam();
			},
            updateUrlParam() {
                this.setFilterValue("selected_items", this.checked.join('|'), true);
            },
		}
	}
</script>
