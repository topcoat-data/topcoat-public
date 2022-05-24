<template>
	<div class="relative cursor-pointer w-max reports-drodown-filter">
		<label class="pb-1 text-sm font-medium" v-if="label">
			{{ label }}
		</label>
		<div
			@click="popup = !popup"
			class="border-[#C3C2CB] bg-white text-sm text-[#555463] flex gap-1 items-center border-1 rounded py-2 px-3 hover:border-[#727184] hover:text-[#727184]"
			:class="{ 'mt-[5px]': label }"
		>
            <span style="color: #145DEB">
			    <chart-timeline-variant-shimmer-icon />
            </span>
			Selected Report
			<i class="fas fa-caret-down" />
		</div>
		<div v-show="popup" class="base-dropdown-menu w-max shadow-md absolute z-[9999] bg-white rounded-lg mt-1">
			<div class="px-2 pt-4 pb-2 border-b border-[#E4E3E8]">
				<h6 class="text-xs text-[#727184] tracking-[0.1em]">CHOOSE REPORT</h6>
				<ul class="inline-flex gap-2 mt-2 base-tabs">
					<li
						class="p-2 rounded-lg text-xs cursor-pointer text-[#1c1c21]"
						v-for="pane in panes"
						:key="pane.key"
						:class="activeSection === pane.key ? 'bg-[#eaf1ff] text-[#0F47C6]' : 'text-[#1c1c21]'"
						@click="activeSection = pane.key"
					>
                        {{ pane.label }}
					</li>
				</ul>
			</div>

			<div class="px-2 pt-2">
				<base-search-input
					class="mt-0 mb-3 text-sm search-report !rounded-md" 
					placeholder="Search Reports"
					size="small"
					clearable
					v-model="search"
				/>

                <small v-if="activeSection === 'all' && !pages.all.length">No reports found.</small>
                <small v-else-if="activeSection === 'favorites' && !pages.favorites.length">No favorites found.</small>
                <small v-else-if="activeSection === 'recents' && !pages.recents.length">No recents found.</small>

				<ul class="px-2 max-h-[200px] overflow-auto">
					<li
						class="flex justify-between mb-3 text-sm cursor-pointer"
						v-for="(page, index) in pages[activeSection].filter(p => p.url.toLowerCase().includes(search))"
						:key='index'
						:class="navSelected(page.url, 'text-[#1c1c21]', 'text-[#555463]')"
					>
                        <a :href="page.url" class="flex items-center justify-between w-full">
						    {{ page.title }}
							<span
							 	v-if="selected === page.url"
								style="color: #0F47C6"
								class="flex items-center h-full"
							>
								<check-icon />
							</span>
                        </a>
						<div v-if="activeSection !== 'favorites'" class="flex items-center gap-1 selected-report">
							<span
								v-if="pages.favorites.filter(favorite => favorite.url === page.url).length > 0"
								style="color: #FFE792"
							>
								<star-icon @click="pages.favorites = pages.favorites.filter(favorite => favorite.url !== page.url)" />
							</span>
							<span v-else style="color: #C3C2CB">
								<star-outline-icon @click="pages.favorites = [...pages.favorites, page]" />
							</span>
						</div>
					</li>
				</ul>
			</div>
		</div>
	</div>
</template>

<script>
	export default {
		props: {
            activeSectionKey: {
                type: String,
                default: 'active'
            },
			label: String,
            defaultValue: String,
            daysDifference: {
                type: Number,
                default: 7,
            },
		},
        mounted() {
            this.pages.all = this.project.nav;
        },
		data: () => ({
            activeSection: 'all',
            favorites: [],
            pages: {
                all: [],
                favorites: [],
            },
            panes: [
                {
                    label: 'All',
                    key: 'all',
                },
                // {
                //     label: 'Favorites',
                //     key: 'favorites',
                // },
            ],
			popup: false,
			search: '',
		}),
		computed: {
            selected() {
                return window.location.pathname.substring(1);
            }
		},
	}
</script>

<style>
	.reports-drodown-filter .vue--search-input__field {
		@apply !rounded-md !bg-[#e4e3e8] !opacity-[0.5];
	}
</style>