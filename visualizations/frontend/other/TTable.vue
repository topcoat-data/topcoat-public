<template>
  <div class="rootTableContainer" :class="{ makeTooltipVisible: tooltip }">
    <slot name="columnConfig" :set-column-config="setColumnConfig"></slot>

    <!-- Title -->
    <div v-if="showTableHeader" class="tableHeaderContainer">
      <div class="title">
        <div class="title__prefix"><slot name="titlePrefix"></slot></div>
        <div v-if="title">{{ title }}</div>
        <t-tooltip v-if="tooltip" position="top" class="tooltip" width="260px">
          <help-circle-outline-icon slot="trigger" :size="16" />
          <div class="text-sm leading-[18px] font-normal">
            {{ tooltip }}
          </div>
        </t-tooltip>
      </div>

      <div v-show="!isPdf" class="tableControls">
        <!-- <div>Future Group By</div> -->
        <!-- So this is a bit funky. Multiple front end columns can use the same layer column.
            Multiple layer columns can be used in a front end column. When the user is selecting
            a front end column to show or hide, they don't care about the layer columns, and the
            selected front end columns are what needs to be saved as part of the url because there
            is no way to know for sure which front end column was selected to be shown based on
            layer columns. However when filtering in the layer, the layer columns are what matter.
            This leads to some fun below, in particular the addition of additionalFilters in the
            csv export that is the layer columns necessary to show the visible front end columns,
            and that the url filter != the filter sent to the back end when fetching a layer with
            modifiable columns. -->
        <t-select-columns
          v-if="modifiableColumns"
          :modifiable-columns="modifiableColumns"
          :url-filter="modifiableColumnsFilter"
          :t-layer="layer"
          @updateFilteredColumns="updateFilteredColumns"
        />
        <TCsvExport
          v-if="enableCsvDownload"
          :t-layer="layer"
          :additional-filters="additionalFilters"
          class="csvExportButton"
        />
        <TSearch
          v-if="canSearch"
          ref="easySearch"
          :highlight-query-selector="
            enableSearchHighlight ? '#tableContainer' : null
          "
          :highlight-options="highlightOptions"
          @updateSearchTerm="updateSearchTerm"
        />
      </div>
    </div>

    <!-- Loading data, showSpinner -->
    <div v-if="showSpinner">
      <div class="spinnerOverlay">
        <base-loading-spinner class="spinner" />
      </div>
    </div>

    <slot
      name="head"
      :total-count="totalRows"
      :visible-count="internalRowsPerPage"
      :start-index="startIndex"
      :end-index="endIndex"
    ></slot>

    <div
      v-if="isDataAvailable"
      id="tableContainer"
      ref="tableContainer"
      :style="columnWidthsStyle"
      :class="extraClass"
    >
      <!-- Empty div to keep the headers lined up with their columns when there are exapnd/collapse buttons  -->
      <div v-if="canCollapseDetailRows"></div>
      <!-- Empty div to keep the headers lined up with their columns when there are radio buttons  -->
      <div v-if="showRadioButtons"></div>
      <!-- Toggle all of the check boxes  -->
      <input
        v-if="showCheckboxes"
        ref="checkAll"
        v-model="allChecked"
        type="checkbox"
        :indeterminate.prop="someChecked"
      />
      <!-- Headings -->
      <div
        v-for="(column, index) in internalColumns"
        :key="column.header"
        :ref="'headerCell_' + index"
        class="headerCell"
        :class="generateHeaderClasses(column.property, index)"
      >
        <div style="display: flex; align-items: center">
          <slot
            :name="generateSlotName('header', column.header)"
            v-bind="column"
          >
            {{ column.header }}
          </slot>

          <div v-if="column.sort" class="sortIcon" @click="updateSort(column)">
            <slot
              v-if="column.sort.direction === 'ASC'"
              name="sortAscendingIcon"
              v-bind="column"
            >
              <menu-up-icon :size="20" />
            </slot>
            <slot
              v-else-if="column.sort.direction === 'DESC'"
              name="sortDescendingIcon"
              v-bind="column"
            >
              <menu-down-icon :size="20" />
            </slot>
            <slot v-else name="sortUnsortedIcon" v-bind="column">
              <menu-swap-icon :size="20" class="unsortedIcon" />
            </slot>
          </div>
        </div>
      </div>

      <!-- No table data -->
      <div
        v-if="
          !showSpinner &&
          (!internalRows ||
            internalRows.length === 0 ||
            !displayRows ||
            displayRows.length === 0)
        "
        class="spanAllColumns center_cell"
      >
        <slot name="no_data">
          <div><i class="i-fa-solid i-fa-inbox"></i></div>
          <div>{{ noDataMessage }}</div>
        </slot>
      </div>

      <!-- Data Rows -->
      <div v-else class="makeGridIgnoreDiv tableDataContainer">
        <div
          v-for="(group, gindex) in internalGroups"
          :key="gindex"
          class="makeGridIgnoreDiv"
        >
          <!-- Group Header -->
          <div
            v-if="showGroupHeader(group)"
            class="spanAllColumns groupHeader row"
          >
            <slot name="group_header" v-bind="group.originalGroup">
              {{ group.header }}
            </slot>
          </div>

          <div
            v-for="(row, rindex) in filterDisplayRowsInGroup(group)"
            :key="rindex + row.toString()"
            class="makeGridIgnoreDiv row"
          >
            <!-- Expand/Collapse controls for the details row -->
            <div
              v-if="canCollapseDetailRows"
              class="bg-[#F9F8FA] border-b border-[#d3d3d9] pt-[12px]"
            >
              <button
                class="focus:outline-none focus-visible:ring"
                @click="toggleRow(row)"
              >
                <span aria-hidden="true">
                  <chevron-down-icon v-if="row.detailRowOpen" />
                  <chevron-right-icon v-else />
                </span>
                <span class="sr-only">
                  {{ row.detailRowOpen ? "collapse row" : "open row" }}
                </span>
              </button>
            </div>

            <!-- Radio buttons -->
            <input
              v-if="showRadioButtons"
              :id="rindex"
              :ref="'radio_' + rindex"
              v-model="internalSelectedItem"
              type="radio"
              :value="row.originalRow"
            />

            <!-- Check boxes -->
            <input
              v-if="showCheckboxes"
              :id="rindex"
              :ref="'check_' + rindex"
              v-model="internalSelectedItems"
              type="checkbox"
              :value="row.originalRow"
            />

            <!-- Columns for the row -->
            <div
              v-for="(column, cindex) in internalColumns"
              :key="column.property"
              :ref="'rowCell_' + gindex + '_' + rindex + '_' + cindex"
              class="border-b border-[#D3D3D9] align-top py-[12px]"
              :class="generateCellClasses({ column, cindex, row, rindex })"
              @click="
                ($event) =>
                  handleCellClick(getCellValue(row, column), row, column)
              "
            >
              <slot
                :name="column.property"
                :row="row.originalRow"
                :value="getRawCellValue(row, column)"
                :rendered_value="getCellValue(row, column)"
                :rendered="getRenderedCellValue(row, column)"
              >
                {{ getCellValue(row, column) }}
              </slot>
            </div>

            <!-- Detail row -->
            <div
              v-if="!canCollapseDetailRows || row.detailRowOpen"
              :key="'detailRow' + rindex"
              class="spanAllColumns"
            >
              <div class="px-4">
                <slot name="detail_row_slot" v-bind="row.originalRow"></slot>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="!isPdf" style="margin: 0px auto">
      <SnykPager
        v-if="canPage || canPageServer"
        id="pagingControls"
        :start-index="startIndex"
        :end-index="endIndex"
        class="pagingControls"
        :number-of-items="totalRows"
        :items-per-page="internalRowsPerPage"
        :items-per-page-options="rowsPerPageOptions"
        @updateItemsPerPage="updateItemsPerPage"
        @updateStartIndex="updateStartIndex"
        @updateEndIndex="updateEndIndex"
        @setResetFunction="setPagerResetFunction"
      />
    </div>
    <slot
      name="footer"
      :total-count="totalRows"
      :visible-count="internalRowsPerPage"
      :start-index="startIndex"
      :end-index="endIndex"
    ></slot>
  </div>
</template>

<script>
export default {
  name: "TTable",
  props: {
    title: {
      type: String,
      default: "",
    },
    tooltip: {
      type: String,
      default: "",
    },
    isHeaderFixed: {
      type: Boolean,
      default: false,
    },
    noDataMessage: {
      type: String,
      default: "No Data",
    },
    noDataIcon: {
      type: String,
      default: "No Data",
    },
    showRadioButtons: {
      type: Boolean,
      defaut: false,
    },
    selectedItem: {
      type: Object,
      default: null,
    },
    showCheckboxes: {
      type: Boolean,
      defaut: false,
    },
    selectedItems: {
      type: Array,
      default: () => [],
    },
    canCollapseDetailRows: {
      type: Boolean,
      default: false,
    },
    onlyShowOneDetailRow: {
      type: Boolean,
      default: false,
    },
    canPage: {
      type: Boolean,
      default: true,
    },
    canPageServer: {
      type: Boolean,
      default: false,
    },
    rowsPerPage: {
      type: Number,
      default: 10,
    },
    rowsPerPageOptions: {
      type: Array,
      default: () => [10],
    },
    groupByColumn: {
      type: String,
      default: null,
    },
    canSearch: {
      type: Boolean,
      default: true,
    },
    enableSearchFilter: {
      type: Boolean,
      default: true,
    },
    enableSearchHighlight: {
      type: Boolean,
      default: true,
    },
    highlightOptions: {
      type: Object,
      default() {
        return {};
      },
    },
    headerClasses: {
      type: String,
      default:
        "py-2 border-b border-[#D3D3D9] text-[12px] text-[#555463] font-semibold leading-[15px] tracking-[0.12em] uppercase",
    },
    cellClasses: {
      type: String,
      default: "break-all",
    },
    layerColumnsToHide: {
      type: Array,
      default: () => [],
    },
    extraClass: {
      type: String,
      default: "",
    },
    enableCsvDownload: {
      type: Boolean,
      default: true,
    },
    modifiableColumns: {
      type: Array,
    },
    sort: {
      type: String,
      default: "none",
      validator(value) {
        return ["none", "sql", "front"].includes(value);
      },
    },
    sortDirection: {
      type: String,
      default: null,
      validator(value) {
        return [null, "ASC", "DESC"].includes(value);
      },
    },
    excludeFromSort: {
      type: Array,
      default: () => [],
    },
    defaultSort: {
      type: Array,
      default: null,
      validator(sorts) {
        const directionList = ["ASC", "DESC"];
        if (sorts) {
          return sorts.every(
            (sort) =>
              directionList.includes(sort?.direction) &&
              typeof sort?.column === "string"
          );
        }
        return true;
      },
    },
    cellCssFunction: {
      type: Function,
      default: null,
    },
    onCellClick: {
      type: Function,
      default: null,
    },
  },
  emits: {
    "update:selectedItem": null,
    selectedItemChanged: null,
    "update:selectedItems": null,
    selectedItemsChanged: null,
  },
  data() {
    return {
      internalSelectedItem: null,
      internalSelectedItems: [],
      internalGroups: [],
      internalRows: [],
      internalRowsPerPage: 10,
      searchTerm: "",
      totalRows: 0,
      startIndex: 0,
      endIndex: 0,
      isDataAvailable: false,
      columnConfigs: [],
      groups: null,
      is_filter: true,
      showSpinner: true,
      displayRows: [],
      pagerResetFunction: null,
      filterableColumnsToShow: [],
      additionalFilters: {},
      internalColumns: [],
      modifiableColumnsFilter: null,
    };
  },
  computed: {
    isPdf() {
      return window.location.href.includes("/pdf?");
    },
    allInitializationComplete() {
      const isPagingInitialized = !this.canPageServer || this.endIndex;
      const isModifiableColumnsInitialized =
        !this.modifiableColumns ||
        this.$store.state.layers.components[this.tag_unique]?.filters
          ?.column_list !== undefined;
      return isPagingInitialized && isModifiableColumnsInitialized;
    },
    showTableHeader() {
      return (
        this.title ||
        this.tooltip ||
        this.enableCsvDownload ||
        this.canSearch ||
        this.modifiableColumns?.length > 0
      );
    },
    columnWidthsStyle() {
      if (Array.isArray(this.internalColumns)) {
        let columnsWidths = "grid-template-columns:";
        if (this.showRadioButtons) {
          columnsWidths += " 2em";
        }
        if (this.showCheckboxes) {
          columnsWidths += " 2em";
        }
        if (this.canCollapseDetailRows) {
          columnsWidths += " 2em";
        }

        this.internalColumns.forEach((column) => {
          if (column.width) columnsWidths += ` ${column.width}`;
          else columnsWidths += " auto";
        });
        return columnsWidths;
      } else {
        return "";
      }
    },
    allChecked: {
      get() {
        return (
          this.internalSelectedItems.length === this.uniqueOriginalRows.length
        );
      },
      set(checked) {
        // it is a bit confusing to "check all" and only have some items be checked,
        // while the check all box remains indeterminate, but checking filtered out
        // rows is even more confusing, as is showing that "all rows are checked"
        // even if only some rows are checked. Life is messy, when rows are filtered
        // by a search term just add the rows that pass the filter to the selected rows.
        const filteredRows = this.filterRowsBySearchValue(
          this.internalRows,
          this.searchTerm,
          this.enableSearchFilter
        ).map((row) => row.originalRow);

        if (checked) {
          this.internalSelectedItems =
            this.internalSelectedItems.concat(filteredRows);
          this.internalSelectedItems = _.uniq(this.internalSelectedItems);
        } else {
          if (this.searchTerm) {
            this.internalSelectedItems = _.difference(
              this.internalSelectedItems,
              filteredRows
            );
          } else {
            this.internalSelectedItems = [];
          }
        }
      },
    },
    someChecked() {
      return (
        this.internalSelectedItems?.length < this.uniqueOriginalRows.length &&
        this.internalSelectedItems?.length > 0
      );
    },
    uniqueOriginalRows() {
      return _.uniq(this.internalRows.map((r) => r.originalRow));
    },
    layerRows() {
      if (typeof this.rows === "function")
        return this.rows(this.$attrs?.["t-layer"]);
      if (this.rows) return this.rows;
      return [];
    },
    sortFilterName() {
      return `${this.layer}_sort`;
    },
    modifiableColumnsFilterName() {
      return `${this.layer}_cols`;
    },
  },
  watch: {
    internalSelectedItem() {
      this.$emit("update:selectedItem", this.internalSelectedItem);
      this.$emit("selectedItemChanged", this.internalSelectedItem);
    },
    internalSelectedItems() {
      this.$emit("update:selectedItems", this.internalSelectedItems);
      this.$emit("selectedItemsChanged", this.internalSelectedItems);
    },
    loading() {
      this.showSpinner = this.loading;
    },
  },
  mounted() {
    this.fetchTotalRows();

    if (this.isPdf) {
      this.internalRowsPerPage = 50;
    } else {
      this.internalRowsPerPage =
        this.getFilterState("tableRowsPerPage") || this.rowsPerPage;
      this.internalRowsPerPage = parseInt(this.internalRowsPerPage, 10);
      // Only allow valid rows per pages regardless of the url value or prop
      if (!this.rowsPerPageOptions.includes(this.internalRowsPerPage)) {
        this.internalRowsPerPage = this.rowsPerPageOptions[0];
        this.setUrlFilter("tableRowsPerPage", this.internalRowsPerPage);
      }
    }

    const modifiableColumnsFilter = this.getFilterState(
      this.modifiableColumnsFilterName
    );
    if (this.modifiableColumns && this.modifiableColumns.length > 0) {
      // Note: this is the front-end columns, the layer filter will be set in initialization
      this.modifiableColumnsFilter = modifiableColumnsFilter;
    }
    const orderByUrlFilter = this.getFilterState(this.sortFilterName);
    if (orderByUrlFilter && this.sort) {
      this.setLayerFilter("orderBy", orderByUrlFilter);
    }
    if (this.canPageServer) {
      this.setLayerFilter("limit", "" + this.internalRowsPerPage);
      this.setLayerFilter("offset", "" + this.startIndex);
    }
  },
  methods: {
    // internal columns takes any column configurations from the TColumnConfig
    // component and creates default column configurations based on the fields
    // of the first row of data. That way users don't have to manually specify
    // all of the columns- it is assumed that if the layer is providing a column
    // then the data should be shown. So if the first row object is {foo: 2, bar: 2222}
    // and there is a column config for a calculated column {header: 'baz', property:'baz'}
    // the final columns will end up being:
    // [
    //   {header: 'foo', property:'foo'},
    //   {header: 'bar', property:'bar'},
    //   {header: 'baz', property:'baz'}
    // ]
    //  plus configurations for sorting etc.
    setInternalColumns(setColumnSort = true) {
      if (!this.rows || this.rows.length === 0) return [];
      let cols = Object.keys(this.rows[0]);

      cols = cols.map((columnString) => {
        return {
          header: _.toString(columnString),
          property: columnString,
        };
      });

      // exclude the grouping column
      if (this.groupByColumn) {
        cols = cols.filter((col) => col.property !== this.groupByColumn);
      }

      // remove the excluded columns
      cols = cols.filter(
        (col) => !this.layerColumnsToHide.includes(col.property)
      );

      if (this.columnConfigs) {
        this.columnConfigs.forEach((columnConfig) => {
          const defaultConfigIndex = cols.findIndex((dc) => {
            return dc.property === columnConfig.property;
          });

          if (defaultConfigIndex !== -1) {
            const defaultConfig = cols[defaultConfigIndex];
            if (!columnConfig.header) {
              columnConfig.header = defaultConfig.header;
            }
            if (columnConfig?.sort?.priority) {
              columnConfig.sort.priority = Number(columnConfig.sort.priority);
            }
            cols.splice(defaultConfigIndex, 1, columnConfig);
          } else {
            cols.push(columnConfig);
          }
        });
      }

      // All computed columns cannot currently be sorted and will be removed from the sorting configuration
      //
      // If the url includes sortable column configuration, use that to determine direction and ignore
      // the default sort direction
      if (setColumnSort && this.sort !== "none") {
        let sortableColumns = cols.map((col) => {
          const sortCol = {
            column: col.property,
            direction: this.sortDirection,
          };
          return sortCol;
        });

        const urlSortConfig = this.getUrlSortConfiguration();
        // sort sortableColumns by order of URL column configs if urlSortConfig is set
        if (urlSortConfig) {
          let sortConfig = [];
          urlSortConfig.forEach((usc) => {
            if (sortableColumns.find((sc) => sc.column === usc.column)) {
              sortConfig.push(usc);
              sortableColumns = sortableColumns.filter(
                (sc) => sc.column !== usc.column
              );
            }
          });
          // append remaining sortable but not sorted columns to the configuration
          sortConfig = sortConfig.concat(sortableColumns);
          sortableColumns = sortConfig;
        } else if (this.defaultSort) {
          let sortConfig = [];
          this.defaultSort.forEach((ds) => {
            if (sortableColumns.find((sc) => sc.column === ds.column)) {
              sortConfig.push(ds);
              sortableColumns = sortableColumns.filter(
                (sc) => sc.column !== ds.column
              );
            }
          });
          // append remaining sortable but not sorted columns to the configuration
          sortConfig = sortConfig.concat(sortableColumns);
          sortableColumns = sortConfig;
        }

        this.excludeFromSort.forEach((efs) => {
          let cleanSortableColumns = _.remove(sortableColumns, (sc) => {
            return !efs.includes(sc.column);
          });
          sortableColumns = cleanSortableColumns;
        });
        // Note: the _.reverse here is because when sorting on the front end, lodash uses
        // a stable sort. The increasing order of priority preserves user's previouse sorts.
        // Here the code needs to emulate that first priority sort being the "latest" column
        // that is sorted by, same with second etc. So to make the priorities match, the
        // sortable columns need to be reversed so the first column ends up with the largest
        // sort priority.
        _.reverse(sortableColumns).forEach((sortableColumn, index) => {
          const column = cols.find((c) => sortableColumn.column === c.property);
          if (column) {
            column.sort = {
              priority: index,
              direction: sortableColumn.direction,
            };
          } else {
            console.warn("Invalid sortable column:", sortableColumn.column);
          }
        });
      }

      // remove hidden columns
      if (this.modifiableColumns) {
        const labelsOfColumnToShow = this.filterableColumnsToShow.map(
          (fcts) => fcts.label
        );
        const columnsToHide = this.modifiableColumns.filter((fc) => {
          const filterableColumnLabel = fc.displayColumn;
          return !labelsOfColumnToShow.includes(filterableColumnLabel);
        });
        const headerNamesOfColumnsToHide = columnsToHide.map((c) =>
          c.displayColumn.toLowerCase()
        );
        cols = cols.filter((col) => {
          return !headerNamesOfColumnsToHide.includes(col.header.toLowerCase());
        });
      }

      // remove sorting on calculated columns for now.
      // TODO: figure out if there is a way to get the computed value in each cell slot so that dynamic columns can be sorted
      const baseColumns = Object.keys(this.rows[0]);
      cols.forEach((col) => {
        if (!baseColumns.includes(col.property)) {
          col.sort = null;
        }
      });

      this.internalColumns = cols;
      this.setOrderByFilters();
    },
    setDisplayRows() {
      let rows = this.filterRowsBySearchValue(
        this.internalRows,
        this.searchTerm,
        this.enableSearchFilter
      );
      rows = this.sortRows(rows);
      rows = this.pageRows(rows);
      this.displayRows.splice(0, this.displayRows.length, ...rows);
    },
    updateSearchTerm(newSearchTerm) {
      this.searchTerm = newSearchTerm;
      this.setupInternalRows();
    },
    setColumnConfig(columnConfig) {
      this.columnConfigs = this.columnConfigs.concat(columnConfig);
    },
    onVisualizationInit() {
      if (!this.canPageServer) {
        this.init();
      }
    },
    onVisualizationUpdated() {
      this.updateEndIndex(this.internalRowsPerPage);
      this.updateStartIndex(0);
      if (this.pagerResetFunction) this.pagerResetFunction();
      this.fetchTotalRows();
    },
    handleCellClick(cellValue, row, column) {
      if (this.onCellClick !== null && this.onCellClick instanceof Function) {
        this.onCellClick({
          cellValue,
          row,
          column,
          table: this,
        });
      }
    },
    init() {
      // Error checking
      let validProps = this.errorPropValidations();
      if (!validProps) return;
      if (!this.rows) return;

      this.setupInternalRows();

      // Handle radio buttons setup
      if (this.selectedItem) {
        if (this.internalRows.find((r) => r.originalRow === this.selectedItem))
          this.internalSelectedItem = this.selectedItem;
        else {
          console.warn(
            "The 'selectedItem' prop is not one of the objects in the rows: ",
            this.selectedItem
          );
        }
      }

      // Handle checkboxes setup
      if (this.selectedItems) {
        this.internalSelectedItems = _.intersection(
          this.selectedItems,
          this.uniqueOriginalRows
        );
      }

      this.warningPropValidations();
      this.isDataAvailable = true;
    },
    setupInternalRows() {
      // Handle internal rows setup
      let groupedRows;
      if (this.groupByColumn) {
        const groupNames = _.uniq(
          this.rows.map((r) => r[this.groupByColumn].rendered)
        );
        if (groupNames) {
          this.groups = groupNames.map((gn) => {
            return {
              header: gn,
              filter: (row) => {
                return row[this.groupByColumn].rendered === gn;
              },
            };
          });
        }
      }
      groupedRows = this.groupRows(this.rows);

      // The detail rows with accordian controls get really hinky
      // given that 1) the *original* object needs to be preserved
      // so users can "===" on them and it works as expected for the
      // selectedItem and selectedItems. 2) The table supports having
      // multiple copies of the same object in different groups. 3)
      // filtering changes the index of objects in the visible rows.
      // Because of 1 and 2 the object can't be used to determine if
      // a detail row is open while 2 and 3 make using indexs challening.
      // So instead, each row will be its own object, with the state of
      // the detail row and a reference to the original object. Makes
      // the rest of the code a bit more convoluted, but that is the
      // least bad option.
      this.internalRows = groupedRows.map((row) => {
        return {
          originalRow: row,
          detailRowOpen: !this.canCollapseDetailRows,
        };
      });

      this.setInternalColumns();
      this.setDisplayRows();
      this.showSpinner = false;
    },
    groupRows(rows) {
      this.internalGroups = [];
      let groupedRows = [];
      if (this.groups) {
        let startIndex = 0;
        this.groups.forEach((group) => {
          if (group.filter) {
            const rowsInGroup = rows.filter((row) => {
              return group.filter(row);
            });
            groupedRows = groupedRows.concat(rowsInGroup);
          } else {
            groupedRows = groupedRows.concat(group.rows);
          }

          const newGroup = {
            header: group.header,
            displayHeader: true,
            startIndex: startIndex,
            filteredStartIndex: startIndex,
            endIndex: groupedRows.length,
            filteredEndIndex: groupedRows.length,
            originalGroup: group,
          };
          this.internalGroups.push(newGroup);
          startIndex = groupedRows.length;
        });
      } else {
        this.internalGroups.push({
          displayHeader: false,
          startIndex: 0,
          filteredStartIndex: 0,
          endIndex: rows.length,
          filteredEndIndex: rows.length,
        });
        // todo
        groupedRows = _.clone(rows);
      }
      if (!this.canPageServer) this.totalRows = groupedRows.length;
      return groupedRows;
    },
    filterRowsBySearchValue(rows, searchTerm, enableSearchFilter) {
      if (searchTerm && enableSearchFilter) {
        let filteredRows = [];
        let filteredStartIndex = 0;
        this.internalGroups.forEach((group) => {
          const rowsInGroup = this.internalRows.slice(
            group.startIndex,
            group.endIndex
          );
          const filteredRowsInGroup = rowsInGroup.filter((row) => {
            // Note: stringifyRow only includes visible fields
            // That way searching for say "12" doesn't incorrectly
            // also include rows that have a non-visible ID field
            // that happens to include "12"
            return this.stringifyRow(row)
              .toLowerCase()
              .includes(searchTerm.toLowerCase());
          });
          group.filteredStartIndex = filteredStartIndex;
          group.filteredEndIndex =
            filteredStartIndex + filteredRowsInGroup.length;
          filteredStartIndex = filteredStartIndex + filteredRowsInGroup.length;
          filteredRows = filteredRows.concat(filteredRowsInGroup);
        });
        if (!this.canPageServer) this.totalRows = filteredRows.length;
        return filteredRows;
      }

      this.internalGroups.forEach((group) => {
        group.filteredStartIndex = group.startIndex;
        group.filteredEndIndex = group.endIndex;
      });
      if (!this.canPageServer) this.totalRows = rows.length;
      return rows;
    },
    getSortedColumns() {
      let sortedColumns = this.internalColumns.filter(
        (c) => c.sort && c.sort.direction
      );
      return _.sortBy(sortedColumns, [
        function (c) {
          return c.sort.priority;
        },
      ]);
    },
    sortRows(rows) {
      sortedColumns = this.getSortedColumns();
      if (this.sort !== "sql" && sortedColumns.length > 0) {
        let sortedRows = [];
        this.internalGroups.forEach((group) => {
          let rowsInGroup = rows.slice(
            group.filteredStartIndex,
            group.filteredEndIndex
          );
          sortedColumns.forEach((sortableColumn) => {
            rowsInGroup = _.sortBy(rowsInGroup, [
              (row) => {
                if (sortableColumn.sort.sortBy) {
                  return sortableColumn.sort.sortBy(
                    row.originalRow[sortableColumn.property],
                    row.originalRow
                  );
                }
                return this.getCellValue(row, sortableColumn);
              },
            ]);
            if (sortableColumn.sort.direction === "DESC") {
              rowsInGroup = _.reverse(rowsInGroup);
            }
          });
          sortedRows = sortedRows.concat(rowsInGroup);
        });
        return sortedRows;
      }
      return rows;
    },
    pageRows(rows) {
      if (this.canPage && !this.canPageServer) {
        return rows.slice(this.startIndex, this.endIndex);
      }
      return rows;
    },
    stringifyRow(row) {
      return this.internalColumns
        .map((column) => this.getCellValue(row, column))
        .filter((cell) => !_.isNil(cell))
        .join(" ");
    },
    updateSort(column) {
      const sortPriorities = this.internalColumns
        .filter((c) => c.sort)
        .map((c) => c.sort.priority);
      const maxSortPriority = sortPriorities.reduce(
        (previousValue, currentValue) => {
          return previousValue > currentValue ? previousValue : currentValue;
        }
      );
      column.sort.priority = maxSortPriority + 1;

      if (column.sort.direction === "ASC") {
        column.sort.direction = "DESC";
      } else if (column.sort.direction === "DESC") {
        column.sort.direction = null;
      } else {
        column.sort.direction = "ASC";
      }

      if (this.sort === "sql") {
        this.fetchLayerOnSort();
      } else {
        this.setupInternalRows();
      }
    },
    fetchLayerOnSort: _.debounce(function () {
      this.setOrderByFilters();
      this.fetchPagedLayer(false);
    }, 500),
    setOrderByFilters() {
      let sortedColumns = _.reverse(this.getSortedColumns());
      let orderByFilter = sortedColumns
        .map((sc) => {
          return ` ${sc.property} ${sc.sort.direction}, `;
        })
        .reduce((previous, current) => {
          return previous + current;
        }, "");
      // remove trailing comma
      if (orderByFilter.length > 1) {
        orderByFilter = orderByFilter.slice(0, -2);
      }
      this.setUrlFilter(this.sortFilterName, orderByFilter);
      this.setLayerFilter("orderBy", orderByFilter);
      Vue.set(this.additionalFilters, "orderBy", orderByFilter);
    },
    showGroupHeader(group) {
      const anyRowsInRange =
        this.indexInPagedRows(group.filteredStartIndex) ||
        this.indexInPagedRows(group.filteredEndIndex - 1);
      const hasRows = group.filteredStartIndex < group.filteredEndIndex;
      return group.displayHeader && anyRowsInRange && hasRows;
    },
    indexInPagedRows(index) {
      if (!this.internalRowsPerPage) return true;
      return index >= this.startIndex && index < this.endIndex;
    },
    getRawCellValue(row, column) {
      const cellValue = _.get(
        row.originalRow,
        column.property,
        column.default_value
      );
      return cellValue && typeof cellValue === "object" ? cellValue.value : "";
    },
    getCellValue(row, column) {
      return column.format
        ? column.format(this.getRenderedCellValue(row, column), row.originalRow)
        : this.getRenderedCellValue(row, column);
    },
    getRenderedCellValue(row, column) {
      const cellValue = _.get(
        row.originalRow,
        column.property,
        column.default_value
      );
      return cellValue && typeof cellValue === "object"
        ? cellValue.rendered
        : "";
    },
    generateHeaderClasses(header, index) {
      let classes = _.camelCase(header);
      classes += " cellPadding ";
      classes += " " + _.camelCase("header " + header);
      classes += index % 2 === 0 ? " evenColumn" : " oddColumn";
      classes += " " + this.headerClasses;
      if (this.isHeaderFixed) classes += " isHeaderFixed";
      return classes;
    },
    generateSlotName(prefix, value) {
      return _.snakeCase(prefix + " " + value);
    },
    errorPropValidations() {
      // validate columns
      if (!this.columns) {
        console.error("columns is required");
        return false;
      }
      if (!Array.isArray(this.columns) && typeof this.columns !== "function") {
        console.error(
          "'columns' must be an array or function, not",
          typeof this.columns
        );
        return false;
      }

      // rows and groups
      if (!this.rows) {
        if (!this.groups) {
          console.error(
            "The rows prop or groups with rows properties are required"
          );
          return false;
        }
        const rowsInGroups = this.groups.map((group) => group.rows);
        if (!rowsInGroups) {
          console.error(
            "The rows prop or groups with rows properties are required"
          );
          return false;
        }

        const groupFilters = this.groups.map((group) => group.filter);
        if (groupFilters.length > 0) {
          console.error("Groups with filter properties require the row prop.");
          return false;
        }
      }
      if (this.groups) {
        // Filter property on groups needs to be an function
        const groupsWithBadFilters = this.groups
          .filter((group) => group.filter && typeof group.filter !== "function")
          .map((g) => g.header);
        if (groupsWithBadFilters.length > 0) {
          console.error(
            "The filter property in group objects must be a function, these groups have non-function filters: " +
              groupsWithBadFilters
          );
          return false;
        }

        // Rows property on groups needs to be an Array
        const groupsWithBadRows = this.groups
          .filter((group) => group.rows && !Array.isArray(group.rows))
          .map((g) => g.header);
        if (groupsWithBadRows.length > 0) {
          console.error(
            "The rows property in group objects must be an Array, these groups have non-array rows: " +
              groupsWithBadRows
          );
          return false;
        }

        // Groups require either rows or filter property
        const groupsWithNoRowsOrFilters = this.groups
          .filter((group) => !group.rows && !group.filter)
          .map((g) => g.header);
        if (groupsWithNoRowsOrFilters.length > 0) {
          console.error(
            "Every group must have either a 'rows' property or a 'filter' property, these groups have nither: " +
              groupsWithNoRowsOrFilters
          );
          return false;
        }
      }

      // Rows Per Page
      if (this.rowsPerPage < 1) {
        console.error("The 'rowsPerPage' prop must be greater than 0");
        return false;
      }
      return true;
    },
    warningPropValidations() {
      // radio buttons
      if (this.selectedItem && !this.showRadioButtons) {
        console.warn(
          "The 'selectedItem' prop is only valid when the 'showRadioButtons' prop is true"
        );
      }

      if (
        this.selectedItems &&
        this.selectedItems.length > 0 &&
        !this.showCheckboxes
      ) {
        console.warn(
          "The 'selectedItems' prop is only valid when the 'showCheckboxes' prop is true"
        );
      }

      // canCollapseDetailRows
      if (this.onlyShowOneDetailRow && !this.canCollapseDetailRows) {
        console.warn(
          "The 'onlyShowOneDetailRow' prop is only valid when the 'canCollapseDetailRows' is true"
        );
      }

      // selected items
      if (this.selectedItems) {
        const selectedItemsNotInRows = _.difference(
          this.selectedItems,
          this.uniqueOriginalRows
        );
        if (selectedItemsNotInRows.length > 0) {
          console.warn(
            "These selected items are not in the rows: ",
            selectedItemsNotInRows
          );
        }
      }

      // searching
      if (
        this.canSearch &&
        !this.enableSearchFilter &&
        !this.enableSearchHighlight
      ) {
        console.warn(
          "The search input is visible but both the enableSearchFilter and the enableSearchHighlight props are disabled so searching will have no effect"
        );
      }
    },
    expandRow(row) {
      if (this.onlyShowOneDetailRow) {
        this.internalRows.forEach((row) => (row.detailRowOpen = false));
      }
      row.detailRowOpen = true;
      const index = this.internalRows.indexOf(row);
      this.$set(this.internalRows, index, row);
    },
    collapseRow(row) {
      row.detailRowOpen = false;
      const index = this.internalRows.indexOf(row);
      this.$set(this.internalRows, index, row);
    },
    toggleRow(row) {
      row.detailRowOpen ? this.collapseRow(row) : this.expandRow(row);
    },
    generateCellClasses({ column, cindex, row, rindex }) {
      let classes = "row ";
      classes += " cellPadding ";
      classes += _.camelCase(column.property);
      classes += cindex % 2 === 0 ? " evenColumn" : " oddColumn";
      classes += rindex % 2 === 0 ? " evenRow" : " oddRow";
      classes += this.canCollapseDetailRows ? " bg-[#F9F8FA]" : "";
      if (
        this.cellCssFunction !== null &&
        this.cellCssFunction instanceof Function
      ) {
        classes +=
          " " + this.cellCssFunction(column, cindex, row, rindex) + " ";
      }
      classes += " " + this.cellClasses;
      return classes;
    },
    // These should be changed to use the 'v-model:start-index="startIndex' syntax
    // when we switch to vue 3, since the .sync and v-model and incompatible and
    // I am trying to keep this working in both expandable-modules and in topcoat
    // this will have to do for now.
    updateStartIndex(newStartIndex) {
      this.startIndex = newStartIndex;
      if (this.canPageServer) {
        this.fetchPagedLayer();
      } else {
        this.setupInternalRows();
      }
    },
    updateItemsPerPage(newItemsPerPage) {
      this.internalRowsPerPage = newItemsPerPage;
      this.setUrlFilter("tableRowsPerPage", newItemsPerPage);
      // avoid confusion and issues when the currently selected page is larger than
      // the total number of pages when internalRowsPerPage is increased
      this.startIndex = 0;
      if (this.canPageServer) {
        this.fetchPagedLayer();
      } else {
        this.setupInternalRows();
      }
    },
    updateEndIndex(newEndIndex) {
      this.endIndex = newEndIndex;
      if (!this.canPageServer) {
        this.setupInternalRows();
      }
    },
    fetchTotalRows() {
      const payload = this.createRequestPayload();
      this.$store
        .dispatch("layers/fetchLayerCount", payload)
        .then((totalRows) => {
          this.totalRows = totalRows;
        });
    },
    fetchPagedLayer(setColumnSort = true) {
      this.setLayerFilter("limit", "" + this.internalRowsPerPage);
      this.setLayerFilter("offset", "" + this.startIndex);
      const payload = this.createRequestPayload();
      this.showSpinner = true;
      this.$store.dispatch("layers/fetchPagedLayer", payload).then(() => {
        if (!this.isDataAvailable) {
          this.init();
        } else {
          this.setInternalColumns(setColumnSort);
          this.setupInternalRows();
        }
      });
    },
    createRequestPayload() {
      let properties = ((obj) => {
        let {
          columns,
          dimensions,
          filters,
          layers,
          load_phase,
          measures,
          tag,
          type,
          output_filters,
          persist_filters,
          default_value,
          ...properties
        } = obj;
        return properties;
      })(this.metadata);
      return (payload = {
        render: {
          visualization: this.tag,
          properties: properties,
        },
        target: this.tag_unique,
        layer: this.layer,
      });
    },
    filterDisplayRowsInGroup(group) {
      const startIndex = this.canPageServer ? 0 : this.startIndex;
      return this.displayRows.slice(
        Math.max(group.filteredStartIndex - startIndex, 0),
        Math.max(group.filteredEndIndex - startIndex, 0)
      );
    },
    setPagerResetFunction(resetFunction) {
      this.pagerResetFunction = resetFunction;
    },
    updateFilteredColumns(filterableColumnsToShow) {
      this.filterableColumnsToShow = filterableColumnsToShow;

      let allValidColumns = [];
      filterableColumnsToShow.forEach((fcts) => {
        allValidColumns = allValidColumns.concat(fcts.sqlColumns);
      });
      // remove duplicate entries
      allValidColumns = [...new Set(allValidColumns)];
      if (allValidColumns.includes(undefined)) {
        console.error(
          'Modify Column Configuration includes "undefined" value, please check that all layer column names are quoted!'
        );
      }

      const columnList = JSON.stringify(allValidColumns);
      const urlLabels = filterableColumnsToShow
        .map((fcts) => fcts.label)
        .join("|");
      // If the urlLabels is empty, the back end will remove the filter, which will make the
      // TSelectColumns component show the default columns instead of just the columns that
      // can't be hidden. So the '~`<>' is a hack to keep the back end from removing the filter
      // while also being extremely unlikely to ever be a valid column label.
      this.setUrlFilter(
        this.modifiableColumnsFilterName,
        urlLabels ? urlLabels : "~`<>"
      );
      this.setLayerFilter("column_list", columnList);
      Vue.set(
        this.additionalFilters,
        "column_list",
        allValidColumns.length > 0 ? columnList : []
      );

      if (this.canPageServer) {
        this.fetchPagedLayer();
      } else {
        this.setInternalColumns();
      }
    },
    getUrlSortConfiguration() {
      const urlFilter = this.getFilterState(this.sortFilterName);
      const useUrlParams = typeof urlFilter === "string";
      if (useUrlParams) {
        const urlSortableColumns = [];
        const urlFilterArray = urlFilter.split(" ").filter((s) => s !== "");
        for (let i = 0; i < urlFilterArray.length; i += 2) {
          urlSortableColumns.push({
            column: urlFilterArray[i],
            direction: urlFilterArray[i + 1].replaceAll(",", ""),
          });
        }
        return urlSortableColumns;
      }
      return null;
    },
    setLayerFilter(filterName, filterValue) {
      const thisTable = this.$store.state.layers.components[this.tag_unique];
      if (!thisTable.filters) {
        thisTable.filters = {};
      }
      Vue.set(thisTable.filters, filterName, filterValue);
    },
    setUrlFilter(filterName, filterValue) {
      if (!this.metadata.filters.output.find((f) => f.name === filterName)) {
        this.metadata.filters.output.push({
          name: filterName,
          urlparam: filterName,
        });
      }
      this.setFilterValue(filterName, filterValue, undefined, true);
    },
  },
};
</script>

<style scoped>
.sortIcon {
  color: #323232;
}
.unsortedIcon {
  opacity: 0.5;
}
.tableDataContainer {
  max-width: 100%;
  overflow-x: scroll;
}
.table-data {
  padding-top: 12px;
  padding-bottom: 17px;
  border-bottom: 1px solid #d3d3d9;
}

.rootTableContainer {
  display: inline-block;
  width: 100%;
  height: 100%;
  max-width: 100%;
  max-height: 100%;
  position: relative;
  min-height: 120px;
  overflow-x: hidden;
}

.spinnerOverlay {
  z-index: 2;
  background: rgba(0, 0, 0, 0.05);
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
}
.spinner {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: scale(3);
}

/* Here be magic. This tells browsers to treat this:
    <div> <--- row div
      <div>cell</div>
      <div>cell</div>
      <div>cell</div>
    </div> <--- end row div
    like it is this:
    <div>cell</div>
    <div>cell</div>
    <div>cell</div>
*/
.makeGridIgnoreDiv {
  display: contents;
}

#tableContainer {
  display: grid;
  margin: 5px;
  position: relative;
  width: 100%;
  overflow-x: scroll;
}

.spanAllColumns {
  grid-column: 1/-1;
}

.isHeaderFixed {
  position: sticky;
  top: 0;
  /* TODO */
  background-color: var(--page-background-color);
}

.headerCell {
  font-weight: 700;
  font-size: 1.2em;
}

.row.groupHeader {
  text-align: left;
  font-size: 1.1em;
  background-color: rgb(250, 250, 250);
  padding-left: 6px;
}

.easySearch {
  display: block;
}

/* Note: gap leaves spaces when
highlighting a row on hover etc. */
.cellPadding {
  padding-left: 5px;
  padding-right: 5px;
}

.headerCell,
.row {
  margin: 0px 0;
}

.center_cell {
  place-self: center;
  text-align: center;
}

.title {
  font-family: "Nunito", sans-serif;
  font-style: normal;
  font-weight: 400;
  font-size: 20px;
  line-height: 23px;
  display: flex;
  align-items: center;
  font-feature-settings: "tnum" on, "lnum" on;
  padding-top: 15px;
  padding-bottom: 15px;
  gap: 10px;
}

.tooltip {
  margin-left: 5px;
}

.tableHeaderContainer {
  display: flex;
  justify-content: space-between;
  width: 100%;
  overflow: visible;
}
.tableControls {
  display: flex;
  gap: 10px;
  align-items: center;
}

.csvExportButton {
  min-width: 130px;
}

.makeTooltipVisible {
  overflow: visible;
}

.pagingControls {
  height: 54px;
}
</style>
