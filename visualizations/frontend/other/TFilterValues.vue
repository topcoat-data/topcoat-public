<template>
    <t-loading-spinner v-if="loading" position="relative" />
    <div v-else-if="items.length">

        <t-grids v-if="isList" column-count="4" gap-x="8">
            <div v-if="label" class="flex-wrap text-base font-semibold whitespace-nowrap h-max">{{ label }}</div>
            <div
                class="relative flex flex-col flex-wrap items-start w-full col-span-3 text-base gap-x-1 whitespace-nowrap"
                :style="{ color: textColor }"
            >
                <div
                    v-for="(item, index) in items"
                    :key="item.key"
                    class="border-b border-[#D3D3D9] w-full text-sm"
                    :class="index == 0 ? 'pb-2' : 'py-2'"
                >
                    {{ item.value }}
                </div>
                <span v-if="truncatedItemsCount" class="text-[#A2A1AF] py-2 text-sm">
                    &nbsp;+ {{ truncatedItemsCount }} more {{ label }}
                </span>
            </div>
        </t-grids>


        <t-grids v-else column-count="2" gap-x="8">
            <div v-if="label" class="flex-wrap text-base font-semibold whitespace-nowrap h-max">{{ label }}</div>
            <div
                class="relative flex flex-wrap items-center text-base gap-x-1 whitespace-nowrap"
                :style="{ color: textColor }"
            >
                <div
                    v-for="(item, index) in items"
                    :key="item.key"
                >
                    {{ item.value }}<span v-if="index < items.length - 1">{{ seperator }}</span>
                </div>
                <span v-if="truncatedItemsCount" class="text-[#A2A1AF] py-2">
                    &nbsp;+ {{ truncatedItemsCount }} more {{ label }}
                </span>
            </div>
        </t-grids>
    </div>
    <div v-else>-</div>
</template>

<script>
    export default {
        props: {
            label: String,
			tKeyColumn: {
                type: String,
                default: '',
            },
            tValueColumn: {
                type: String,
                default: '',
            },
			seperator: {
				type: String,
				default: ','
			},
            visibleItemsCount: {
                type: Number,
                default: -1,
            },
            textColor: {
                type: String,
                default: "#555463",
            },
            isList: {
                type: Boolean,
                default: false,
            },
        },
        data: () => ({
            is_filter: true,
            truncatedItemsCount: 0,
        }),
        computed: {
            keys() {
                if (this.tKeyColumn) {
                    return this.getColumn(this.tKeyColumn)
                }
                return [];
            },
            values() {
                if (this.tValueColumn) {
                    return this.getColumn(this.tValueColumn)
                }
                return [];
            },
            items() {
                const keys = this.keys;
                const values = this.values;
                const items = [];
                let truncatedItems = 0;
                
                const selectedItems = this.urlValue.split("|");
                if (values && keys) {
                    for (let index in keys) {
                        if (this.visibleItemsCount > -1) {
                            if (items.length === this.visibleItemsCount) {
                                truncatedItems = selectedItems.length - items.length;
                                break;
                            }
                        }
                        const key = keys[index];
                        if (selectedItems.indexOf(key) < 0) continue;
                        const value = values[index];
                        items.push({ key, value });
                    }
                }
                this.truncatedItemsCount = truncatedItems;

                return items;
            },
            urlValue() {
                return this.getFilterValue("selected_items");
            },
        },
    }
</script>