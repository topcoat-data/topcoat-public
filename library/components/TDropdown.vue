<template>
	<div
		class="relative font-sans cursor-pointer w-max dropdown-filter"
		@mouseover="setActiveState"
		@mouseleave="setActiveState($event, false)"
		ref="dropdownFilter"
	>
        <div
            @click="setPopup(!popup)" :class="activeClass"
            class="rounded cursor-pointer"
        >
            <slot name="handle"></slot>
        </div>
		<slot name="outside"></slot>
		<div
			v-show="popup"
			ref="popup"
			class="absolute mt-1 bg-white rounded-lg shadow-md base-dropdown-menu w-max min-w-"
			:class="alignClass"
			:style="{ zIndex }"
            :key="componentKey"
		>
            <slot :popup="setPopup"></slot>
		</div>
	</div>
</template>

<script>
	export default {
        props: {
            disableHandleClass: {
                type: Boolean,
                default: false,
            },
            isActive: {
                type: Boolean,
                default: false,
            },
			isPersisted: {
                type: Boolean,
                default: false,
            },
            zIndex: {
                type: String,
                default: '999',
            }
        },
		data: () => ({
			internal_active: false,
			alignClass: '',
			popup: false,
            componentKey: '',
		}),
        computed: {
            activeClass() {
                if (!this.disableHandleClass) {
                    return this.internal_active || this.isActive ? 'border-1 active' : 'border-1 in-active'
                }
                return '';
            },
        },
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
					this.internal_active = false;
					this.$emit('closed');

					document.body.removeEventListener("click", this.handleOutsideClick);

					this.$nextTick(() => {
						this.alignPopup();
					})
				}
			},
			setActiveState(e, state = true) {
				if (!state && this.popup) return;
				this.internal_active = state;
				if (!state) {
                    this.$emit('closed')
                }
			},
			setPopup(toggle) {
				this.popup = toggle;
				this.internal_active = toggle;

				if (toggle) {
					document.body.addEventListener("click", this.handleOutsideClick);
				} else {
					document.body.removeEventListener("click", this.handleOutsideClick);
					this.$emit('closed');
				}

				this.$nextTick(() => {
					this.alignPopup();
				})
			},
		},
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