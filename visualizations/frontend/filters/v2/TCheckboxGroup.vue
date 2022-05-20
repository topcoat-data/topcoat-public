<template>
   <div class="find-me p-2 rounded-[2px] h-max t-checkbox-group">
        <div class="font-bold" v-if="label">
            {{ label.toUpperCase() }}
        </div>
        <div
            class="relative px-3 py-2 overflow-hidden transition"
            :style="{
                maxHeight: containerHeight,
                transition: '0.3s',
            }"
            :class="{ 'w-max': !isInline }"
        >
            <div ref="checkBoxesContainer">
                <t-loading-spinner position="relative" v-if="componentLoading || loading" />
                <div
                    v-show="!componentLoading && !loading"
                    v-for="key in Object.keys(items)"
                    :key="key"
                >
                    <div class="font-bold">
                        {{ isLabelCapitalized ? key.toUpperCase() : key }}
                    </div>
                    <div class="flex flex-wrap gap-2 px-2 py-3" :class="{ 'flex-col': !isInline }">
                        <div
                            v-for="value in items[key].data"
                            :key="value.value + '_' + key"
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
            </div>
	    </div>
        <div
            class="mt-2 text-center"
            v-if="!isExpanded && !componentLoading && canBeExpanded"
        >
            <base-button
                v-if="containerHeight !== slotHeight + 'px'"
                ghost
                @click="expand"
                :disabled="componentLoading || loading"
            >
                Show More
            </base-button>
            <base-button
                v-else
                ghost
                @click="collapse"
                :disabled="componentLoading || loading"
            >
                Show Less
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
			defaultHeight: {
			   type: String,
			   default: '200px',
			}
		},
		data: () => ({
			canBeExpanded: true,
			checked: [],
			containerHeight: "40px",
			items: {},
			is_filter: true,
			componentLoading: true,
			slotHeight: 0,
		}),
		methods: {
			collapse() {
			   this.containerHeight = this.defaultHeight;
			},
			expand() {
			   this.containerHeight = this.slotHeight + 'px';
			},
			getItems() {
				const items = {};
				const keyColumn = this.findColumnByTag('keys');
				const valueColumn = this.findColumnByTag('values');

				for (let row of this.rows) {
					const key = row[keyColumn];
					if (!key) continue;
					if (items[key.value]) {
						items[key.value].data.push(row[valueColumn]);
					} else {
						items[key.value] = { label: '', data: [] }
						items[key.value].label = key.rendered;
						items[key.value].data = [row[valueColumn]];
					}
				}
				this.items = items;
			},
			handleHeight() {
				// Dom gives wrong max height if not delayed.
				setTimeout(() => {
					this.slotHeight = this.$refs.checkBoxesContainer.clientHeight;
					const containerHeight = parseInt(this.defaultHeight.replace(/\D+/g, ''));
					this.canBeExpanded = containerHeight < this.slotHeight;
					return this.containerHeight = this.isExpanded ? this.slotHeight + 'px' : this.defaultHeight;
				}, 100)
			},
			handleInit() {
				this.componentLoading = true;
				const selected = this.getFilterValue("selected_items");
				this.getItems();
				if (selected) {
					this.checked = selected.split('|');
				} else {
				   this.setFilterValue("selected_items", this.checked.join('|'), true);
				}
				this.componentLoading = false;
				this.handleHeight();
			},
			onVisualizationInit() {
				this.handleInit();
			},
			onVisualizationUpdated() {
				this.handleInit();
			},
			updateUrlParams() {
				this.setFilterValue("selected_items", this.checked.join('|'), true);
			},
		}
	}
</script>

<style scoped>
   .t-checkbox-group {
	  box-shadow: inset 0 0 0 1px hsl(244deg 8% 84%);
   }
</style>