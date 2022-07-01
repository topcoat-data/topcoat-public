<template>
  <div class="rootTableContainer">
    <slot name="columnConfig" :setColumnConfig="setColumnConfig"></slot>

    <TSearch
      v-if="canSearch"
      ref="easySearch"
      :highlight-query-selector="
        enableSearchHighlight ? '#tableContainer' : null
      "
      :highlight-options="highlightOptions"
      @updateSearchTerm="updateSearchTerm"
    />

    <div
      v-if="isDataAvailable"
      id="tableContainer"
      ref="tableContainer"
      :style="columnWidthsStyle"
    >
      <!-- Title -->
      <div v-if="title" id="title" class="spanAllColumns">
        {{ title }}
      </div>

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
        <slot :name="generateSlotName('header', column.header)" v-bind="column">
          {{ column.header }}
        </slot>

        <span
          v-if="column.sort || column.initialSort"
          @click="reverseSort(column.property)"
        >
          <slot
            v-if="arrowDirection[column.property] === 'asc'"
            name="sortAscendingIcon"
            v-bind="column"
          >
            <div class="icon move_up">&#8964;</div>
          </slot>
          <slot v-else name="sortDescendingIcon" v-bind="column">
            <div class="icon move_down">&#8963;</div>
          </slot>
        </span>
      </div>

      <!-- Loading data, showSpinner -->
      <div v-if="showSpinner" class="spinnerOverlay">
        <base-loading-spinner class="spinner" />
      </div>

      <!-- No table data -->
      <div
        v-if="
          !internalRows ||
          internalRows.length === 0 ||
          !displayRows ||
          displayRows.length === 0
        "
        class="spanAllColumns center_cell"
      >
        <div><i class="i-fa-solid i-fa-inbox"></i></div>
        <div>{{ noDataMessage }}</div>
      </div>

      <!-- Data Rows -->
      <div v-else class="makeGridIgnoreDiv">
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
            <div v-if="canCollapseDetailRows">
              <div v-if="row.detailRowOpen" @click="collapseRow(row)">
                <slot name="expandedDetailRowIcon">
                  <div class="icon move_up">-</div>
                </slot>
              </div>
              <div v-else @click="expandRow(row)">
                <slot name="collapsedDetailRowIcon">
                  <div class="icon move_up">+</div>
                </slot>
              </div>
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
              :class="generateCellClasses({ column, cindex, rindex })"
            >
              <slot
                :name="column.property"
                :row="row.originalRow"
                :value="getRawCellValue(row, column)"
                :rendered_value="getCellValue(row, column)"
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
              <slot name="detail_row_slot" v-bind="row.originalRow"></slot>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div style="margin: 0px auto">
      <SnykPager
        v-if="canPage || canPageServer"
        id="pagingControls"
        :start-index="startIndex"
        :end-index="endIndex"
        class="pagingControls"
        :number-of-items="totalRows"
        :items-per-page="rowsPerPage"
        @updateStartIndex="updateStartIndex"
        @updateEndIndex="updateEndIndex"
        @setResetFunction="setPagerResetFunction"
      />
    </div>
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
    groupByColumn: {
      type: String,
      default: null,
    },
    canSearch: {
      type: Boolean,
      default: true,
    },
    canSort: {
      type: Boolean,
      default: true,
    },
    sortDirection: {
      type: String,
      default: "asc",
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
        "py-2 border-b border-[#D3D3D9] text-[10px] text-[#555463] font-semibold leading-[15px] tracking-[0.12em] uppercase",
    },
    cellClasses: {
      type: String,
      default:
        "border-b border-[#D3D3D9] align-top pt-[12px] pb-[17px] snykCell",
    },
    exludeFromColumns: {
      type: Array,
      default: () => [],
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
      columnSortDirection: [],
      arrowDirection: {},
      internalSelectedItem: null,
      internalSelectedItems: [],
      internalGroups: [],
      internalRows: [],
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
    };
  },
  computed: {
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
    // internal columns takes any column configurations from the TColumnConfig
    // component and creates default column configurations based on the fields
    // of the first row of data. That way users don't have to manually specify
    // all of the columns- it is assmumed that if the layer is providing a column
    // then the data should be shown. So if the first row object is {foo: 2, bar: 2222}
    // and there is a column config for a calculated column {header: 'baz', property:'baz'}
    // the final columns will end up being:
    // [
    //   {header: 'foo', property:'foo'},
    //   {header: 'bar', property:'bar'},
    //   {header: 'baz', property:'baz'}
    // ]
    //  plus configurations for sorting etc.
    internalColumns() {
      let cols = this.columns;
      if (typeof this.columns === "function") cols = [];

      if (cols.length === 0 && this.rows && this.rows.length > 0) {
        cols = Object.keys(this.rows[0]);
      }
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
        (col) => !this.exludeFromColumns.includes(col.property)
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
      if (this.canSort) {
        // Note: the "+" in "+col.sort.priority" converts strings to numbers
        const sortPriorities = cols
          .map((col) => (col.sort ? +col.sort.priority : null))
          .filter((priority) => priority !== null)
          .sort();

        let maxSortPriority =
          sortPriorities.length > 0 ? sortPriorities.pop() : 0;

        cols.forEach((col) => {
          if (!col.sort) {
            maxSortPriority += 1;
            col.sort = {
              direction: this.sortDirection,
              priority: maxSortPriority,
            };
          }
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

      return cols;
    },
    layerRows() {
      if (typeof this.rows === "function")
        return this.rows(this.$attrs?.["t-layer"]);
      if (this.rows) return this.rows;
      return [];
    },
  },
  watch: {
    loading() {
      if (!this.loading) {
        this.updateEndIndex(this.rowsPerPage);
        this.updateStartIndex(0);
        this.pagerResetFunction();
        this.fetchTotalRows();
      }
      this.showSpinner = this.loading;
    },
    internalSelectedItem() {
      this.$emit("update:selectedItem", this.internalSelectedItem);
      this.$emit("selectedItemChanged", this.internalSelectedItem);
    },
    internalSelectedItems() {
      this.$emit("update:selectedItems", this.internalSelectedItems);
      this.$emit("selectedItemsChanged", this.internalSelectedItems);
    },
  },
  mounted() {
    this.fetchTotalRows();
  },
  methods: {
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
    init() {
      // Error checking
      let validProps = this.errorPropValidations();
      if (!validProps) return;
      if (!this.rows) return;

      // Handle sorting setup
      let sortableColumns = this.internalColumns.filter((c) => {
        return (
          c.sort && typeof c.sort.priority === "number" && c.sort.direction
        );
      });

      if (sortableColumns.length > 0) {
        sortableColumns = _.sortBy(sortableColumns, ["sort.priority"]);
        sortableColumns = _.reverse(sortableColumns);
        sortableColumns.forEach((sortableColumn) => {
          this.columnSortDirection.push({
            property: sortableColumn.property,
            direction: sortableColumn.sort.direction,
            format: sortableColumn.format,
            sortBy: sortableColumn.sortBy,
          });
          this.arrowDirection[sortableColumn.property] =
            sortableColumn.sort.direction;
        });
      }

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
    sortRows(rows) {
      if (this.columnSortDirection.length > 0) {
        let sortedRows = [];
        this.internalGroups.forEach((group) => {
          let rowsInGroup = rows.slice(
            group.filteredStartIndex,
            group.filteredEndIndex
          );
          this.columnSortDirection.forEach((sortableColumn) => {
            rowsInGroup = _.sortBy(rowsInGroup, [
              (row) => {
                if (sortableColumn.sortBy) {
                  return sortableColumn.sortBy(
                    row.originalRow[sortableColumn.property],
                    row.originalRow
                  );
                }
                return this.getCellValue(row, sortableColumn);
              },
            ]);
            if (sortableColumn.direction === "desc")
              rowsInGroup = _.reverse(rowsInGroup);
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
    reverseSort(columnProperty) {
      const sortObject = this.getSortByProperty(columnProperty);
      _.pull(this.columnSortDirection, [sortObject]);

      if (sortObject.direction === "asc") {
        this.arrowDirection[columnProperty] = "desc";
        sortObject.direction = "desc";
      } else {
        this.arrowDirection[columnProperty] = "asc";
        sortObject.direction = "asc";
      }

      this.columnSortDirection.push(sortObject);
      this.setupInternalRows();
    },
    getSortByProperty(columnProperty) {
      return this.columnSortDirection.find(
        (csd) => csd.property === columnProperty
      );
    },
    showGroupHeader(group) {
      const anyRowsInRange =
        this.indexInPagedRows(group.filteredStartIndex) ||
        this.indexInPagedRows(group.filteredEndIndex - 1);
      const hasRows = group.filteredStartIndex < group.filteredEndIndex;
      return group.displayHeader && anyRowsInRange && hasRows;
    },
    indexInPagedRows(index) {
      if (!this.rowsPerPage) return true;
      return index >= this.startIndex && index < this.endIndex;
    },
    getRawCellValue(row, column) {
      let cellValue = _.get(
        row.originalRow,
        column.property,
        column.default_value
      );
      if (cellValue && typeof cellValue === "object") {
        if (cellValue.rendered) cellValue = cellValue.rendered;
        else cellValue = "";
      }
      return cellValue;
    },
    getCellValue(row, column) {
      const cellValue = this.getRawCellValue(row, column);
      return column.format
        ? column.format(cellValue, row.originalRow)
        : cellValue;
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

      // sorting
      let sortableColumns = this.internalColumns.filter((c) => {
        return c.sort;
      });
      if (sortableColumns.length > 0) {
        sortableColumns = _.sortBy(sortableColumns, ["sort.priority"]);
        let lastSortableColumn = null;
        sortableColumns.forEach((column) => {
          const sortOptions = column.sort;

          if (typeof sortOptions.priority !== "number") {
            console.warn(
              "The sort priority option must be a number. For column " +
                column.property +
                " it is a " +
                typeof sortOptions.priority
            );
          }
          if (!["asc", "desc"].includes(sortOptions.direction)) {
            console.warn(
              "The sort direction option must be either 'asc' or 'desc'. For column " +
                column.property +
                " it is " +
                sortOptions.direction
            );
          }
          if (
            lastSortableColumn !== null &&
            lastSortableColumn.sort.priority === column.sort.priority
          ) {
            console.warn(
              "The sort priority option for column " +
                column.property +
                " is the same as the sort priority option for " +
                lastSortableColumn.property
            );
          }
          lastSortableColumn = column;
        });
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
    generateCellClasses({ column, cindex, rindex }) {
      let classes = "row ";
      classes += " cellPadding ";
      classes += _.camelCase(column.property);
      classes += cindex % 2 === 0 ? " evenColumn" : " oddColumn";
      classes += rindex % 2 === 0 ? " evenRow" : " oddRow";
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
        const thisTable = this.$store.state.layers.components[this.tag_unique];
        if (!thisTable.filters) {
          thisTable.filters = {};
        }
        thisTable.filters.limit = "" + this.rowsPerPage;
        thisTable.filters.offset = "" + this.startIndex;
        this.fetchPagedLayer();
        return;
      } else {
        this.setupInternalRows();
      }
    },
    updateEndIndex(newEndIndex) {
      this.endIndex = newEndIndex;
      if (!this.canPageServer) this.setupInternalRows();
    },
    fetchTotalRows() {
      const payload = this.createRequestPayload();
      this.$store
        .dispatch("layers/fetchLayerCount", payload)
        .then((totalRows) => {
          this.totalRows = totalRows;
        });
    },
    fetchPagedLayer(limit, offset) {
      const payload = this.createRequestPayload();
      this.showSpinner = true;
      this.$store.dispatch("layers/fetchPagedLayer", payload).then(() => {
        if (!this.isDataAvailable) this.init();
        this.setupInternalRows();
      });
    },
    createRequestPayload() {
      let properties = ((obj) => {
        let {
          columns,
          dimensions,
          filters,
          is_iframe,
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
  },
};
</script>

<style scoped>
.rootTableContainer {
  display: inline-block;
  width: 100%;
  height: 100%;
  max-width: inherit;
  max-height: inherit;
  position: relative;
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
.icon {
  float: left;
  font-size: large;
  padding-right: 5px;
}

.move_up {
  position: relative;
  top: -6px;
}

.move_down {
  position: relative;
  top: 5px;
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

#title {
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
}

.snykCell {
  word-break: break-word;
}
</style>
