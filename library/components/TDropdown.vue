<template>
	<div
		class="relative font-sans cursor-pointer w-max dropdown-filter"
		@mouseover="hasMouseOver = true"
		@mouseleave="hasMouseOver = false"
		ref="dropdownFilter"
	>
        <div
            @click="openPopup" :class="activeClass"
            class="rounded cursor-pointer"
        >
            <slot name="handle"></slot>
        </div>
		<slot name="outside"></slot>
		<div
			v-show="isPopupOpen"
			ref="popup"
			class="absolute mt-1 bg-white rounded-lg shadow-md base-dropdown-menu w-max min-w-"
			:class="alignClass"
			:style="{ zIndex }"
            :key="componentKey"
		>
            <slot></slot>
		</div>
	</div>
</template>

<script>
	export default {
        props: {
            isActive: {
                type: Boolean,
                default: false,
            },
            zIndex: {
                type: String,
                default: '999',
            },
			isExpanded: {
				type: Boolean,
				default: false,
			}
        },
		data: () => ({
			alignClass: '',
			isPopupOpen: false,
            componentKey: '',
			hasMouseOver: false,  // Useful in some cases when a child is also a dropdown, clicking on it can cause main dropdown to close
		}),
        computed: {
            activeClass() {
                if (!this.isExpanded) {
                    return this.isPopupOpen || this.isActive ? 'border-1 active' : 'border-1 in-active'
                }
                return '';
            },
        },
		created: function() {
			document.body.addEventListener("click", this.handleOutsideClick);
		},
		beforeDestroy: function() {
			document.body.removeEventListener("click", this.handleOutsideClick);
		},
		methods: {
			alignPopup() {
				const element = this.$refs.popup;

				if (element) {
					const bounding = element.getBoundingClientRect();
					const availableWidth = window.innerWidth;

					if (bounding.x < 0) {
						return this.alignClass = 'left-0';
					}

					if (bounding.x + bounding.width > availableWidth) {
						return this.alignClass = 'right-0';
					}
				}

				return this.alignClass = '';
			},
			handleOutsideClick(event) {
				if (this.$refs.dropdownFilter.contains(event.target) || this.hasMouseOver) {
					return;
				}

				this.isPopupOpen = false;
				this.$emit('closed');
				this.$nextTick(() => {
					this.alignPopup();
				})
			},
			openPopup() {
				if (this.isPopupOpen) {
					this.isPopupOpen = false;
					this.$emit('closed');
				} else {
					this.isPopupOpen = true;
					this.$emit('open');
				}

				this.$nextTick(() => {
					this.alignPopup();
				});
			},
		},
		watch: {
			isExpanded: function(newVal, oldVal) {
				if (newVal) {
					this.isPopupOpen = true;
					this.$emit('open');
				}
			}
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