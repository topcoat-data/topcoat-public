<template>
    <div class="relative p-2 border-[#E4E3E8] border-t">
        <div class="flex items-center justify-between cursor-pointer" @click="expanded = !expanded">
            <div class="flex items-center">
                <span class="text-[#A2A1AF] mr-1">
                    <chevron-down-icon v-if="expanded" />
                    <chevron-right-icon v-else />
                </span>
                <span class="text-[#555463] text-sm font-normal leading-4 tracking-[0.1px]">
                    <slot name="label"></slot>
                </span>
            </div>
            <div class="pr-1">
                <slot name="icon"></slot>
            </div>
        </div>
        <div class="px-2 pt-1" v-show="expanded">
            <slot :onExpandable="expanded"></slot>
        </div>
    </div>
</template>

<script>
    export default {
        data: () => ({
            expanded: false,
        }),
    }
</script>
