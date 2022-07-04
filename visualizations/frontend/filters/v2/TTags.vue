<template>
   <div class="find-me p-2 rounded-[2px] h-max t-checkbox-group" :class="{ 'is-outlined': isOutlined }">
        <div class="flex justify-between gap-1">
            <div class="font-bold tracking-widest" v-if="label">
                {{ label.toUpperCase() }}
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
        </div>
        <div
            ref="checkBoxesContainer"
            class="relative py-2 overflow-hidden transition"
            :style="{
                maxHeight: containerHeight,
                transition: '0.3s',
            }"
            :class="{ 'w-max': !isInline, 'px-3': label }"
        >
            <div>
                <t-loading-spinner position="relative" v-if="!init || loading" />
                <div
					v-else-if="Object.keys(items).length"
                    v-for="key in Object.keys(items)"
                    :key="key"
                >
                    <div class="font-bold tracking-widest">
                        {{ isLabelCapitalized ? key.toUpperCase() : key }}
                    </div>
                    <div class="flex flex-wrap gap-2 px-2 py-3" :class="{ 'flex-col': !isInline }">
                        <div
                            v-for="value in items[key].data"
                            :key="value.value + '_' + key"
							class="tracking-widest"
                        >
                            <base-checkbox
                                :label="value.rendered"
                                :value="value.value + '_' + key"
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
            v-if="!isExpanded && init && canBeExpanded"
        >
            <base-button
                ghost
                @click="expanded ? collapse() : expand()"
                :disabled="!init || loading"
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
            searchPlaceholder: {
				type: String,
				default: 'Search',
			},
			isExpanded: {
			   type: Boolean,
			   default: false,
			},
			isLabelCapitalized: {
			   type: Boolean,
			   default: false,
			},
			isInline: {
			   type: Boolean,
			   default: false,
			},
            isOutlined: {
                type: Boolean,
                default: false,
            },
            isSearchable: {
				type: Boolean,
				default: false,
			},
			defaultHeight: {
			   type: String,
			   default: '200px',
			}
		},
		data: () => ({
			canBeExpanded: true,
			checked: [],
			containerHeight: "200px",
			is_filter: true,
			init: false,
			slotHeight: 0,
			expanded: false,
            search: '',
		}),
        computed: {
            keyColumn() {
                return this.findColumnByTag('keys');
            },
            valueColumn() {
                return this.findColumnByTag('values');
            },
            items() {
                const items = {};
                this.slotHeight = 0;

				for (let row of this.rows) {
					const key = row[this.keyColumn];
					if (!key) continue;
                    const value = row[this.valueColumn]
                    if (value && value.rendered && this.search) {
                        const text = value.rendered.toLowerCase();
                        if (!text.includes(this.search.toLowerCase())) {
                            continue;
                        }
                    }
					if (items[key.value]) {
						items[key.value].data.push(value);
					} else {
						this.slotHeight += 40;
						items[key.value] = { label: '', data: [] }
						items[key.value].label = key.rendered;
						items[key.value].data = [value];
					}
					this.slotHeight += 40;
				}
                this.handleHeight();
				return items;
            }
        },
		methods: {
			collapse() {
			   this.containerHeight = this.defaultHeight;
			   this.expanded = false;
			},
			expand() {
			   this.containerHeight = this.slotHeight + 'px';
			   this.expanded = true;
			},
			handleHeight() {
				const containerHeight = parseInt(this.defaultHeight.replace(/\D+/g, ''));
				this.canBeExpanded = containerHeight < this.slotHeight;
				return this.containerHeight = this.isExpanded ? this.slotHeight + 'px' : this.defaultHeight;	
			},
			onVisualizationInit() {
                this.init = false;
				const selected = this.getFilterValue("selected_items");
				if (selected) {
					this.checked = selected.split('|');
				} else {
				   this.setFilterValue("selected_items", this.checked.join('|'), true);
				}
				this.init = true;
			},
			updateUrlParams() {
				this.setFilterValue("selected_items", this.checked.join('|'), true);
			},
		}
	}
</script>

<style scoped>
   .t-checkbox-group .is-outlined {
	  box-shadow: inset 0 0 0 1px hsl(244deg 8% 84%);
   }
</style>