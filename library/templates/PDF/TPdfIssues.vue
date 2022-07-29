<template>
    <div>
        <!-- Header -->
        <div class="flex items-center justify-between my-5">
            <div class="flex items-center gap-5">
                <snyk-logo />
                <div class="text-[#461D9E] font-semibold text-[22px] tracking-widest ">REPORT</div>
            </div>
            <a href="https://snyk.io/" class="bg-[#461D9E1A] border-[#C3C2CB] items-center rounded py-1 px-2 text-[#461D9E] hover:text-[#461D9E] px-[11px] text-[27px] font-medium leading-[35px]">
                snyk.io
            </a>
        </div>

        <t-grids column-count="2" gap-x="4" gap-y="4" style="grid-template-columns: 40% 60%">
            <slot name="filters"></slot>
        </t-grids>
        
        <div class="page-break">
            <slot></slot>
        </div>
    </div>
</template>

<style>
	body {
		background: #fff;
	}
	@media print {
		.page-break { page-break-before: always; }
	}
    #pagingControls #pages { 
        display: none;
    }
</style>