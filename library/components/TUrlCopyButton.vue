<template>
    <div class="relative" @mouseover="showTooltip = true" @mouseleave="showTooltip = false">
        
        <t-tooltip v-if="showTooltip" position="left" width="max-content">
            {{ copied ? "URL Copied" : "Copy URL" }}
        </t-tooltip>

        <button
            class="h-[30px] w-[30px] rounded-[4px] flex items-center justify-center border border-[#C3C2CB] p-1 transition-colors"
            @click="copy"
            :class="{ 'bg-[#B4E4D9]': copied }"
        >
            <check-icon :size="18" v-if="copied" />
            <link-icon :size="18" v-else />
        </button>
    </div>
</template>

<script>
    export default {
        data: () => ({
            copied: false,
            showTooltip: false,
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