<template>
   <div class="find-me rounded-[2px] h-max t-checkbox-group" :class="{ 'is-outlined': isOutlined }">
        <div class="pb-3 font-bold tracking-widest" v-if="label">
            {{ label }}
        </div>
        <div
            ref="checkBoxesContainer"
            class="relative overflow-hidden transition"
            :class="{ 'w-max': !isInline }"
        >
            <div>
                <t-loading-spinner position="relative" v-if="loading" />
				<div v-else-if="menu.length">
					<span
						@click="reset"
						class="text-[#145DEB] text-[13px] cursor-pointer font-normal leading-[18px]"
						:class="checked.length ? 'text-[#7FA7F5]' : 'text-[#727184]'"
					>
						Clear
					</span>
					<div class="flex flex-wrap gap-2 pt-3" :class="{ 'flex-col': !isInline }">
						<div
							v-for="item in menu"
							:key="item"
							class="tracking-widest"
						>
							<base-checkbox
								:label="item.name"
								:value="item.id"
								v-model="checked"
								@change="updateUrlParams"
							/>
						</div>
					</div>
				</div>
				<small v-else>
					No data found
				</small>
            </div>
	    </div>
        <div
            class="mt-2 text-center"
            v-if="!isExpanded && canBeExpanded"
        >
            <base-button
                ghost
                @click="expanded ? collapse() : expand()"
                :disabled="loading"
            >
				<span v-if="expanded">Show Less</span>
				<span v-else>Show More</span>
            </base-button>
        </div>
    </div>
</template>

<script>
	export default {
		props: {
			label: {
				type: String,
				default: '',
			},
			isInline: {
			   type: Boolean,
			   default: false,
			},
            isOutlined: {
                type: Boolean,
                default: false,
            },
		},
		data: () => ({
			checked: [],
			is_filter: true,
		}),
		computed: {
			ids() {
				const column = this.findColumnByTag('ids');
				return this.getColumn(column);
			},
			names() {
				const column = this.findColumnByTag('names');
				return this.getColumn(column);
			},
			menu() {
				const ids = this.ids;
                const names = this.names;
                const menu = [];

                if (ids && names) {
                    for (let index in ids) {
                        const id = ids[index];
                        const name = names[index];
                        menu.push({ id, name });
                    }
                }
                return menu;
			}
		},
		methods: {
			onVisualizationInit() {
				const selected = this.getFilterValue("selected_items");
				if (selected) {
					this.checked = selected.split('|');
				} else {
				   this.setFilterValue("selected_items", this.checked.join('|'), true);
				}
			},
			updateUrlParams() {
				this.setFilterValue("selected_items", this.checked.join('|'), true);
			},
			reset() {
				this.checked = [];
				this.updateUrlParams();
			},
		}
	}
</script>

<style scoped>
   .t-checkbox-group .is-outlined {
	  box-shadow: inset 0 0 0 1px hsl(244deg 8% 84%);
   }
</style>