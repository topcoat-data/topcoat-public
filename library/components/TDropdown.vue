<template>
	<div
		class="relative font-sans cursor-pointer w-max dropdown-filter"
		@mouseover="setActiveState"
		@mouseleave="setActiveState($event, false)"
		ref="dropdownFilter"
	>
        <div
            @click="setPopup(!popup)" :class="active ? 'active' : 'in-active'"
            class="rounded cursor-pointer border-1"
        >
            <slot name="handle"></slot>
        </div>
		<div
			v-show="popup"
			ref="popup"
			class="base-dropdown-menu w-max shadow-md absolute z-[9999] bg-white rounded-lg mt-1"
			:class="alignClass"
		>
            <slot></slot>
		</div>
	</div>
</template>

<script>
	export default {
		data: () => ({
			active: false,
			alignClass: '',
			popup: false,
		}),
		methods: {
			alignPopup() {
				const element = this.$refs.popup;
				if (element) {
					const bounding = element.getBoundingClientRect();
					const availableWidth = window.innerWidth;
					if (bounding.x < 0) {
						return this.alignClass = 'left-0';
					} else if (bounding.x + bounding.width > availableWidth) {
						return this.alignClass = 'right-0';
					}
				}
				return this.alignClass = '';
			},
			handleOutsideClick(event) {
				const container = this.$refs.dropdownFilter;
				if (container && event && !container.contains(event.target)) {
					this.popup = false;
					this.active = false;

					document.body.removeEventListener("click", this.handleOutsideClick);

					this.$nextTick(() => {
						this.alignPopup();
					})
				}
			},
			setActiveState(e, state = true) {
				if (!state && this.popup) return;
				this.active = state;
			},
			setPopup(toggle) {
				this.popup = toggle;
				this.active = toggle;

				if (toggle) {
					document.body.addEventListener("click", this.handleOutsideClick);
				} else {
					document.body.removeEventListener("click", this.handleOutsideClick);
				}

				this.$nextTick(() => {
					this.alignPopup();
				})
			},
		}
	}
</script>

<style>
	.dropdown-filter .active {
		@apply border-[#145DEB] text-[#145DEB] bg-[#EAF1FF];
	}

	.dropdown-filter .in-active {
		@apply border-[#C3C2CB] text-[#555463] bg-white;
	}
</style>