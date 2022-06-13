<template>
	<t-dropdown>

		<!-- Handle -->
    	<div slot="handle" class="flex items-center gap-1 py-1 text-sm">
			<div class="pl-1">
				<slot name="icon"></slot>
			</div>
			<span>{{ selectedItemLabel || label }}</span>

			<t-loading-spinner v-if="loading" position="relative" />
			<menu-down-icon v-else size="20" class="pr-1" />
    	</div>

		<!-- Popup Contents -->
		<template v-slot:default="{ popup }">
			<div class="min-w-[254px]">
				<div class="px-[12px] pt-[16px] pb-[8px] flex justify-between items-center w-full" v-if="menuLabel">
					<h6 class="text-[10px] text-[#727184] font-semibold uppercase leading-[15px] tracking-widest">
						{{ menuLabel }}
					</h6>
				</div>
				<div class="px-[8px] pt-[4px] pb-[6px] w-full">
					<ul class="max-h-[200px] overflow-auto">
						<li
							class="flex justify-between px-[8px] py-[6px] text-sm cursor-pointer text-[#555463]"
							v-for="(item, index) in menu"
							:key="index"
							@click="selectItem(item, popup)"
						>
							<div class="flex items-center justify-between w-full hover:text-[#1C1C21] leading-[16.41px]">
								{{ item.title }}
								<div
									style="color: #0F47C6"
									class="relative flex items-center h-1 h-full"
									v-show="selected_internal === item.value"
								>
									<check-icon />
								</div>
							</div>
						</li>
						<small v-if="!options.length && !loading">
							No items found
						</small>
					</ul>
				</div>
			</div>
		</template>
	</t-dropdown>
</template>

<script>
	export default {
		props: {
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
            selected_internal: '',
		}),
		computed: {
            labels() {
                try {
                    const column_name = this.findColumnByTag('labels');
                    return this.getColumn(column_name);
                } catch (err) {
                    return []
                }
            },
            options() {
                try {
                    const column_name = this.findColumnByTag('options');
                    return this.getColumn(column_name);
                } catch (err) {
                    return []
                }
            },
			menu() {
                const values = this.options;
                const titles = this.labels;
                const menu = [];

                if (values && titles) {
                    for (let index in values) {
                        const value = values[index];
                        const title = titles[index];
                        menu.push({ value, title });
                    }
                }
                return menu;
            },
			selectedItemLabel() {
				const selected = this.menu.filter(item => item.value === this.selected_internal)[0]
				return selected ? selected.title : null;
			},
		},
		methods: {
            onVisualizationInit() {
                // See if the page was loaded with a url param value
                const initial_value = this.getFilterValue("dropdown");
                const column_name = this.findColumnByTag('labels');

                if (initial_value) {
                    this.selected_internal = initial_value;
                } else if (this.config.default_value) {
                    this.selected_internal = this.config.default_value;
                }
                this.setFilterValue("dropdown", this.selected_internal, true);
            },
            selectItem(item, popup) {
                this.selected_internal = item.value;
                this.setFilterValue("dropdown", this.selected_internal, true);
				popup(false);
            },
		}
	}
</script>
