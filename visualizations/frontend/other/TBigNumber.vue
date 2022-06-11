<template>
    <div
        class="w-full lg:p-5 md:p-3 p-1 rounded-[2px]"
        :style="{ background: bgColor, color: textColor }"
    >
        <div class="flex items-center gap-2">
            <div class="hidden opacity-50 md:block">
                <slot name="icon"></slot>
            </div>
            <span class="text-xs font-semibold leading-4">
                {{ label || '--' }}
            </span>
        </div>
        <div class="mt-3">
            <span class="font-normal leading-8 tracking-widest" :class="fontSizes[bigNumberSize]">
                <div class="flex gap-2">
                    <span>{{ value || '--' }}</span>
                    <t-loading-spinner position="relative" v-if="loading" />
                </div>
            </span>
        </div>
    </div>
</template>

<script>
    export default {
        props: {
            bgColor: {
                type: String,
                default: 'transparent'
            },
            bigNumberSize: {
                type: String,
                default: 'medium',
                validator: v => ['small', 'medium', 'big'].includes(v),
            },
            label: {
                type: String,
                default: '',
            },
            textColor: {
                type: String,
                default: '#393842'
            },
        },
        data: () => ({
            is_filter: true,
            fontSizes: {
                small: 'lg:text-3xl md:text-2xl sm:text-lg',
                medium: 'lg:text-4xl md:text-3xl sm:text-2xl',
                big: 'lg:text-5xl md:text-4xl sm:text-3xl',
            }
        }),
        computed: {
            value() {
                // Find by tags
                const column = this.findColumnByTag('value');
                const value = this.getColumn(column)
                return value && value.length ? value[0] : '--';
            },
        },
    }
</script>
