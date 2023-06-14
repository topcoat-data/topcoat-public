<template>
  <div class="relative overflow-auto">
    <t-loading-spinner v-if="loading" position="relative" />
    <slot name="header" :loading="loading"></slot>
    <div :class="containerClass">
      <table class="w-full table-fixed">
        <thead>
          <th v-for="column in columns" :key="column" :class="columnsClass">
            <slot :name="'col-' + column" :column="column">
              {{ column }}
            </slot>
          </th>
        </thead>
        <tbody>
          <tr v-for="(row, index) in rows" :key="'row-' + index">
            <td
              v-for="column in columns"
              :key="column"
              class="break-all"
              :class="rowsClass"
            >
              <slot :name="'row-' + column" :row="row">
                {{ row[column] ? row[column].rendered : "" }}
              </slot>
            </td>
          </tr>
        </tbody>
        <div v-if="!loading && !rows.length" class="text-center">No Data</div>
      </table>
    </div>
    <slot
      name="footer"
      :rows-limit="rowsLimit"
      :rows-total="rowsTotal"
      :loading="loading"
    >
      <div class="pt-4 text-right">
        Showing {{ rowsLimit }} of {{ rowsTotal }}
      </div>
    </slot>
  </div>
</template>

<script>
export default {
  props: {
    hiddenColumns: {
      type: Array,
      default: () => [],
    },
    dynamicColumns: {
      type: Array,
      default: () => [],
    },
    customColumns: {
      type: Array,
      default: () => [],
    },
    rowsLimit: {
      type: Number,
      default: 5,
    },
    containerClass: {
      type: String,
      default: "",
    },
    columnsClass: {
      type: String,
      default: "",
    },
    rowsClass: {
      type: String,
      default: "",
    },
  },
  data: () => ({
    is_filter: true,
    rowsTotal: 0,
  }),
  computed: {
    columns() {
      const columns = this.rows.length ? Object.keys(this.rows[0]) : [];
      const filteredInternalColumns = columns.filter(
        (col) => !this.hiddenColumns.includes(col)
      );
      return [...filteredInternalColumns, ...this.customColumns];
    },
    visibleLayerColumns() {
      let columns = [];
      for (let column of this.dynamicColumns) {
        if (this.filteredColumns.includes(column.url_value)) {
          columns.push(column.sql_value);
        }
      }
      return columns;
    },
    filteredColumns() {
      const layerColumnsFilterName = `${this.layer}_cols`;
      const urlParam =
        this.filters.filter((f) =>
          f.name.includes(layerColumnsFilterName)
        )[0] || {};
      return urlParam.value ? urlParam.value.split("|") : [];
    },
    requestPayload() {
      return {
        render: {
          visualization: this.tag,
        },
        target: this.tag_unique,
        layer: this.layer,
      };
    },
  },
  created() {
    this.fetchOnMounted = false;
  },
  mounted() {
    this.prepareFilters();
    this.fetchLayerData();
    this.fetchRowsCount();
  },
  methods: {
    prepareFilters() {
      this.setLayerFilter("limit", this.rowsLimit);
      this.setLayerFilter("offset", 0); // Always showing first page on PDF, pagination not required there.
      this.setLayerFilter("orderBy", this.getFilterState(`${this.layer}_sort`));
      this.setLayerFilter(
        "column_list",
        JSON.stringify(this.visibleLayerColumns)
      );
    },
    fetchRowsCount() {
      this.$store
        .dispatch("layers/fetchLayerCount", this.requestPayload)
        .then((rowsTotal) => {
          this.rowsTotal = rowsTotal;
        });
    },
    setLayerFilter(filterName, filterValue) {
      this.tableFilters = { ...this.tableFilters, [filterName]: filterValue };
      this.storeAttribute({
        target: this.tag_unique,
        attribute: "filters",
        value: this.tableFilters,
      });
    },
  },
};
</script>
