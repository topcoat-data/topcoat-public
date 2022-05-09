<template>
	<div class="date-filter-container w-max">
		<label class="pb-1 text-sm font-medium" v-if="label || config.title">
			{{ label || config.title }}
		</label>
	  	<div class="inline-flex w-full mt-[5px]">
			<div v-if="!hidePresets && !config.hide_presets" class="relative">
				<base-button
					style="height: 44px; border-top-right-radius: 0px; border-bottom-right-radius: 0px;"
					:style="{ width: pickerMode === 'range' ? '167px' : '155px' }"
					slot="handle"
					@click="openPicker"
					class="!rounded-tl-[2px] !rounded-bl-[2px]"
				>
					<div class="flex items-center justify-center gap-1">
						{{ presetValue }}
						<t-loading-spinner v-if="loading" />
						<span v-else class="mt-2">
							<chevron-up-icon v-if="pickerOpened" />
							<chevron-down-icon v-else />
						</span>
					</div>
				</base-button>
				<div class="absolute top-[45px] w-max z-[99999]" v-if="pickerOpened">
					<base-card
						:condensed="true"
						:style="{
							height: pickerMode === 'range' ? '370px' : '313px',
							width: pickerMode === 'range' ? '167.17px' : '155px'
						}"
						legacy
					>
						<div
							v-for="preset in presets[pickerMode]"
							:key="preset.key"
						>
							<base-dropdown-menu-item
								:value="preset.label"
								:style="{ color: preset.key === datePreset ? '#157575' : 'black' }"
								@click="presetChange(preset, false)"
							/>
						</div>
					</base-card>
				</div>
			</div>
			<div
				class="inline-block h-9"
				:class='{"full-picker": !hidePresets && !config.hide_presets}'
			>
				<!-- Range Picker -->
				<div v-if='pickerMode == "range"' class="flex items-center h-full">
					<div @click="pickerOpened = !pickerOpened" class="h-full">
						<a-range-picker
							class="relative h-full ant-calendar-filter"
							:allowClear="false"
							dropdownClassName="wld-date-picker w-20"
							:open="pickerOpened"
							:separator="separator"
							:format="dateFormat || config.date_format"
							:value="[ startDate, endDate ]"
							@change="onDateChange"
						>
							<template slot="renderExtraFooter">
								<div style="padding: 2.0rem; padding-right: 1.0rem;" class="flex items-center justify-between">
									<div class="flex" v-if="includePrevious || config.include_previous">
										<span class="flex self-center pr-1">
											Compare to previous
										</span>
										<div class="flex items-center">
											<base-button
												:ghost="previousMode !== 'period'"
												:style="{ borderColor: previousMode !== 'period' && 'transparent', margin: '0px' }"
												:disabled="datePreset == 'mtd' || datePreset == 'ytd'"
												@click="previousMode = 'period'"
											>
												Period
											</base-button>
											<base-button
												:ghost="previousMode !== 'year'"
												:style="{ borderColor: previousMode !== 'year' && 'transparent', margin: '0px' }"
												@click="previousMode = 'year'"
											>
												Year
											</base-button>
										</div>
									</div>
									<div
										class="flex content-center justify-end h-full gap-1 ml-1"
										:class='{"w-full": !includePrevious && !config.include_previous}'
									>
										<base-button style="float:right;" ghost class="h-full py-1" @click="close">
											Cancel
										</base-button>
										<base-button style="float:right;" class="h-full py-1" @click="apply">
											Apply
										</base-button>
									</div>
								</div>
							</template>
						</a-range-picker>
					</div>
				</div>

				<!-- Date Picker -->
				<div
					v-else-if="pickerMode == 'single'"
					class="flex items-center h-full"
				>
					<div @click="pickerOpened = !pickerOpened" class="h-full">
					<a-date-picker
						:showToday="false"
						class="h-full ant-calendar-filter date-picker"
						:allowClear="false"
						dropdownClassName="wld-date-picker w-20"
						:format="dateFormat"
						:separator="separator"
						:open="pickerOpened"
						v-model="date"
						@change="onDateChange"
					>
						<template slot="renderExtraFooter">
							<div class="flex content-center justify-end h-full gap-1 pb-2 pr-1 ml-1">
								<base-button style="float:right;" ghost class="h-full py-1" @click="close">
									Cancel
								</base-button>
								<base-button style="float:right;" class="h-full py-1" @click="apply">
									Apply
								</base-button>
							</div>
						</template>
					</a-date-picker>
					</div>
				</div>
			</div>
			<div
				class="flex items-center px-3"
				v-if='(includePrevious || config.include_previous) && pickerMode == "range"'
			>
				<div v-if="refStart && refEnd" class="self-center">
					ref. {{ refStart.format('MM/DD/YYYY ') }} -
					{{ refEnd.format('MM/DD/YYYY ') }}
				</div>
			</div>
	  	</div>
	</div>
  </template>
  
  <script>
  	export default {
	  	props: {
		  	dateFormat: {
			  	type: String,
			  	default: 'MM/DD/YYYY',
		  	},
			defaultPreset: String,
			label: String,
			hidePresets: Boolean,
			includePrevious: Boolean,
            singlePicker: Boolean,
			separator: {
				type: String,
				default: '-',
			}
	  	},
		data() {
			return {
				startDate: null,
				endDate: null,
				date: null,
				pickerOpened: false,
				datePreset: null,
				refStart: null,
				refEnd: null,
				prevDatePreset: null,
				previousMode: null,
				is_filter: true,
				showPreviousMode: false,
				presets: {
					range: [
						{ key: 'yesterday', label: 'Yesterday' },
						{ key: 'last7days', label: 'Last 7 Days' },
						{ key: 'lastmonth', label: 'Last Month' },
						{ key: 'last30days', label: 'Last 30 Days' },
						{ key: 'last90days', label: 'Last 90 Days' },
						{ key: 'mtd', label: 'Month to Date' },
						{ key: 'ytd', label: 'Year to Date' },
						{ key: 'custom', label: 'Custom Range' },
					],
					single: [
						{ key: 'today', label: 'Today' },
						{ key: 'yesterday', label: 'Yesterday' },
						{ key: '7DaysAgo', label: '7 Days Ago' },
						{ key: '30DaysAgo', label: '30 Days Ago' },
						{ key: '90DaysAgo', label: '90 Days Ago' },
						{ key: 'yearAgo', label: 'A Year Ago' },
						{ key: 'custom', label: 'Custom Date' },
					]
				}
			}
		},
		mounted() {
			const ref = this;
			window.addEventListener('resize', function(event) {
				ref.addColSpan();
			}, true);
		},
		computed: {
			presetValue() {
				const { presets, pickerMode, datePreset } = this;
				if (presets[pickerMode] && datePreset) {
					const preset = presets[pickerMode].filter(p => p.key === datePreset)[0];
					if (preset) return preset.label;
				}
				return '';
			},
			pickerMode() {
				if (this.config.picker_mode) {
					return this.config.picker_mode;
				}
				return this.singlePicker ? 'single' : 'range';
			},
			
		},
		methods: {
			addColSpan() {
				this.$nextTick(() => {
					const screenWidth = window.innerWidth;
					let col = !this.previousMode ? 'col-span-2' : 'col-span-3';
					if (screenWidth < 1024) col = 'col-span-1';
		
					const dateFiler = document.querySelector('.date-filter-container');
					const steps = 6; // Steps to reach parent
					let parent = dateFiler ? dateFiler.parentNode : null;
					if (parent) {
						for (let index = 1; index < steps; index ++) {
							parent = parent.parentNode;
						}
						parent.classList.add(col);
						parent.classList.add('w-full');
					}
				});
			},
			close() {
				this.pickerOpened = false;
		
				// Reset values
				this.previousMode = this.getFilterValue("previous_mode");
		
				this.datePreset = this.getFilterValue('date_preset');
				this.startDate = Moment(this.getFilterValue('start_date'));
				this.endDate = Moment(this.getFilterValue('end_date'));
				this.date = Moment(this.getFilterValue('date'));
		
				if (this.previousMode == 'period') {
					var diff = this.endDate.diff(this.startDate, 'days') + 1;
					this.refStart = this.startDate.clone().subtract(diff, 'days');
					this.refEnd = this.endDate.clone().subtract(diff, 'days');
		
				} else {
					this.refStart = this.startDate.clone().subtract(1, 'years');
					this.refEnd = this.endDate.clone().subtract(1, 'years');
				}
			},
			apply() {
				this.pickerOpened = false;
		
				if (this.pickerMode == 'single') {
					this.setFilterValue("date", this.date.format('YYYY-MM-DD'), false);
				} else {
					this.setFilterValue("start_date", this.startDate.format('YYYY-MM-DD'), false);
					this.setFilterValue("end_date", this.endDate.format('YYYY-MM-DD'), false);
		
					var start = this.startDate.clone();
					var end = this.endDate.clone();
		
					if (this.previousMode == 'year') {
						this.refStart = start.subtract(1, 'years');
						this.refEnd = end.subtract(1, 'years');
					} else {
						if (this.datePreset == 'yesterday') {
							this.refStart = start.subtract(1, 'days');
							this.refEnd = end.subtract(1, 'days');
						} else if (this.datePreset == 'last7days') {
							this.refStart = start.subtract(7, 'days');
							this.refEnd = end.subtract(7, 'days');
						} else if (this.datePreset == 'lastmonth') {
							this.refStart = start.subtract(1, 'months').startOf('month');
							this.refEnd = end.subtract(1, 'months').endOf('month');
						} else if (this.datePreset == 'last30days') {
							this.refStart = start.subtract(30, 'days')
							this.refEnd = end.subtract(30, 'days')
						} else if (this.datePreset == 'last90days') {
							this.refStart = start.subtract(90, 'days')
							this.refEnd = end.subtract(90, 'days')
						} else if (this.datePreset == 'custom') {
							var diff = end.diff(start, 'days') + 1;
							this.refStart = start.subtract(diff, 'days');
							this.refEnd = end.subtract(diff, 'days');
						}
					}
					const includePrevious = this.includePrevious || this.config.include_previous;
					const prevMode = includePrevious ? this.previousMode : false;
					const prevStartDate = includePrevious ? this.refStart.format('YYYY-MM-DD') : '';
					const prevEndDate = includePrevious ? this.refEnd.format('YYYY-MM-DD') : '';
					this.setFilterValue("previous_mode", prevMode, false);
					this.setFilterValue("prev_start_date", prevStartDate, false);
					this.setFilterValue("prev_end_date", prevEndDate, true);
				}
				this.setFilterValue("date_preset", this.datePreset, false);
			},
			presetChange(event, first) {
				// Remember previous
				if (this.datePreset) this.prevDatePreset = this.datePreset;
		
				this.datePreset = event.key;
				if (this.pickerMode == 'single') {
					this.handleSingleDates();
				} else {
					this.handleRangeDates(first);
				}
			},
			handleSingleDates() {
				const key = this.datePreset;
				if (key == 'today') {
					this.date = Moment();
				} else if (key == 'yesterday') {
					this.date = Moment().subtract(1, 'days');
				} else if (key == '7DaysAgo') {
					this.date = Moment().subtract(7, 'days');
				} else if (key == '30DaysAgo') {
					this.date = Moment().subtract(30, 'days');
				} else if (key == '90DaysAgo') {
					this.date = Moment().subtract(90, 'days');
				} else if (key == 'yearAgo') {
					this.date = Moment().subtract(1, 'year');
				}
			},
			handleRangeDates(first) {
				const key = this.datePreset;
				if (key == 'yesterday') {
					this.startDate = Moment().subtract(1, 'days');
					this.endDate = Moment().subtract(1, 'days');
					if (!first) this.previousMode = 'period';
				} else if (key == 'last7days') {
					this.startDate = Moment().subtract(7, 'days');
					this.endDate = Moment().subtract(1, 'days');
					if (!first) this.previousMode = 'period';
				} else if (key == 'lastmonth') {
					this.startDate = Moment().subtract(1, 'months').startOf('month');
					this.endDate = Moment().subtract(1, 'months').endOf('month');
					if (!first) this.previousMode = 'period';
				} else if (key == 'last30days') {
					this.startDate = Moment().subtract(30, 'days');
					this.endDate = Moment().subtract(1, 'days');
					if (!first) this.previousMode = 'period';
				} else if (key == 'last90days') {
					this.startDate = Moment().subtract(90, 'days');
					this.endDate = Moment().subtract(1, 'days');
					if (!first) this.previousMode = 'period';
				} else if (key == 'mtd') {
					this.startDate = Moment().startOf('month');
					this.endDate = Moment().subtract(1, 'days');
					if (!first) this.previousMode = 'year';
				} else if (key == 'ytd') {
					this.startDate = Moment().startOf('year');
					this.endDate = Moment().subtract(1, 'days');
					if (!first) this.previousMode = 'year';
				}
			},
			onDateChange(event) {
				if (this.pickerMode == 'single') {
					this.date = event;
				} else {
					this.startDate = event[0];
					this.endDate = event[1];
				}
				this.datePreset = "custom";
			},
			onVisualizationInit() {

				var start_date = this.getFilterValue('start_date');
				var end_date = this.getFilterValue('end_date');
				var date = this.getFilterValue('date');

				const includePrevious = this.includePrevious || this.config.include_previous;
				this.showPreviousMode = includePrevious;

				var defaultPreset = this.defaultPreset || this.config.default_preset;
				if (!defaultPreset) {
					if (this.singlePicker) {
						defaultPreset = this.presets.single[0].key;
					} else {
						defaultPreset = this.presets.range[0].key;
					}
				}
				var date_preset = this.getFilterValue('date_preset');
				if (date_preset) {
					this.datePreset = date_preset;
				} else {
					if (!date_preset && defaultPreset) {
						this.datePreset = defaultPreset;
						this.setFilterValue("date_preset", this.datePreset, false);
					}
				}

				var previous_mode = this.getFilterValue('previous_mode')
				if (previous_mode == null) {
					if (this.datePreset == 'mtd' || this.datePreset == 'ytd') this.previousMode = 'year'
					else this.previousMode = 'period';
					const prevMode = includePrevious ? this.previousMode : '';
					this.setFilterValue("previous_mode", this.previousMode, false);
				} else {
					this.previousMode = previous_mode;
				}

				if (this.datePreset != 'custom') {
					var tmp_event = {
						key: this.datePreset
					}
					this.presetChange(tmp_event, true);
					this.apply();

				} else {
					this.startDate = Moment(start_date);
					this.endDate = Moment(end_date);
					this.date = Moment(date);

					if (this.previousMode == 'period') {
						var diff = this.endDate.diff(this.startDate, 'days') + 1;
						this.refStart = this.startDate.clone().subtract(diff, 'days');
						this.refEnd = this.endDate.clone().subtract(diff, 'days');

					} else {
						this.refStart = this.startDate.clone().subtract(1, 'years');
						this.refEnd = this.endDate.clone().subtract(1, 'years');
					}

					this.setFilterValue("start_date", this.startDate.format('YYYY-MM-DD'), false);
					this.setFilterValue("end_date", this.endDate.format('YYYY-MM-DD'), false);
					this.setFilterValue("date", this.date.format('YYYY-MM-DD'), false);
					const prevStartDate = includePrevious ? this.refStart.format('YYYY-MM-DD') : '';
					const prevEndDate   = includePrevious ? this.refEnd.format('YYYY-MM-DD') : '';
					this.setFilterValue("prev_start_date", prevStartDate, false);
					this.setFilterValue("prev_end_date", prevEndDate, true);
				}
			},
			openPicker() {
				if (this.loading) return;
				this.pickerOpened = !this.pickerOpened
			}
  		}
  	}
</script>
  
<style>
	.wld-date-picker .ant-calendar-range,
	.wld-date-picker .ant-calendar-picker-container-content {
		@apply !absolute !top-[48px];
	}
	
	.date-filter-container input {
		@apply !outline-none;
	}
	
	.full-picker .ant-calendar-filter .ant-calendar-picker-input {
		@apply !rounded-l-none !rounded-r-[2px];
	}

	.ant-calendar-picker-input.ant-input,
	.ant-calendar-picker-input.ant-input {
		@apply h-full border text-sm text-center;
	}

	.ant-calendar-range .ant-calendar-selected-start-date .ant-calendar-date,
	.ant-calendar-range .ant-calendar-selected-end-date .ant-calendar-date,
	.ant-calendar-selected-day .ant-calendar-date,
	.ant-calendar-range .ant-calendar-selected-start-date .ant-calendar-date:hover,
	.ant-calendar-range .ant-calendar-selected-end-date .ant-calendar-date:hover {
		background: #157575;
		border-color: #157575;
		color: white;
	}

	.ant-calendar-today .ant-calendar-date {
		border-color: #157575;
		color: black;
	}

	.ant-calendar-picker-input  {
		background: #fff;
		height: 44px !important;
	}

	.ant-calendar {
		box-shadow: inset 0 0 0 1px #e5e8ed;
	}

    .ant-calendar-range-picker-separator {
		color: black;
	}
</style>
