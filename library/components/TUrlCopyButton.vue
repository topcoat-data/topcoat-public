<template>
    <div class="relative">
        
        <t-tooltip position="bottom" width="130px">
            <button
                class="h-[30px] w-[30px] rounded-[4px] flex items-center justify-center border border-[#C3C2CB] p-1 transition-colors"
                @click="copy"
                :class="{ 'bg-[#B4E4D9]': copied }"
                slot="trigger"
            >
                <check-icon :size="18" v-if="copied" />
                <link-icon :size="18" v-else />
                <span class="visually-hidden">{{ copied ? "URL Copied" : "Copy URL" }}</span>
            </button>
            {{ copied ? "URL Copied" : "Copy URL" }}
        </t-tooltip>
    </div>
</template>

<script>
    export default {
        data: () => ({
            copied: false,
        }),
        methods: {
            copy() {
                this.copied = true;
                const tempInput = document.createElement('input'),
                text = window.location.href;
                document.body.appendChild(tempInput);
                tempInput.value = text;
                tempInput.select();
                document.execCommand('copy');
                document.body.removeChild(tempInput);
                setTimeout(() => {
                    this.copied = false;
                }, 1000)
            }
        }
    }
</script>

<style>
/* 
 * Utility class to hide content visually while keeping it screen reader-accessible.
 * Source: https://www.scottohara.me/blog/2017/04/14/inclusively-hidden.html 
 */
    .visually-hidden:not(:focus):not(:active) {
        clip: rect(0 0 0 0); 
        clip-path: inset(100%); 
        height: 1px; 
        overflow: hidden; 
        position: absolute; 
        white-space: nowrap; 
        width: 1px; 
    }
</style>