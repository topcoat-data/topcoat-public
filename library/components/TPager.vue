<template>
  <div>
    <div v-if="numberOfItems > itemsPerPage" class="center">
      <span
        ref="AngleDoubleLeft"
        class="pagingIcon"
        :class="page === 1 ? 'disabled' : 'enabled'"
        :disabled="page === 1"
        @click="page = 1"
      >
        &#171;
      </span>

      <span
        ref="AngleLeft"
        class="pagingIcon"
        :class="page === 1 ? 'disabled' : 'enabled'"
        @click="page === 1 ? 1 : page--"
        :disabled="page === 1"
      >
        &#8249;
      </span>

      <input
        id="pageInput"
        ref="pageInput"
        v-model.number="page"
        class="pageInput"
      />

      <span
        ref="AngleRight"
        class="pagingIcon"
        :class="page === lastPage ? 'disabled' : 'enabled'"
        @click="page === lastPage ? lastPage : page++"
        :disabled="page === lastPage"
      >
        &#8250;
      </span>

      <span
        ref="AngleDoubleRight"
        class="pagingIcon"
        :class="page === lastPage ? 'disabled' : 'enabled'"
        @click="page = lastPage"
        :disabled="page === lastPage"
      >
        &#187;
      </span>
    </div>
  </div>
</template>

<script>
export default {
  name: "TPager",
  // TODO: Prop validation
  props: {
    numberOfItems: { type: Number, required: true },
    itemsPerPage: { type: Number, default: 10 },
  },
  emits: ["updateEndIndex", "updateStartIndex"],
  data() {
    return {
      page: 1,
    };
  },
  computed: {
    lastPage() {
      return Math.ceil(this.numberOfItems / this.itemsPerPage);
    },
    startIndex() {
      return (this.page - 1) * this.itemsPerPage;
    },
    endIndex() {
      let endIndex = this.startIndex + this.itemsPerPage;
      if (endIndex > this.numberOfItems) endIndex = this.numberOfItems;
      return endIndex;
    },
    isValidPage() {
      return this.validatePage(this.page);
    },
  },
  watch: {
    numberOfItems() {
      this.page = 1;
    },
    startIndex() {
      if (this.isValidPage) this.$emit("updateStartIndex", this.startIndex);
    },
    endIndex() {
      if (this.isValidPage) this.$emit("updateEndIndex", this.endIndex);
    },
    page(newval, oldval) {
      // allow users to clear out page input
      if (newval === "") return;

      if (this.validatePage(newval)) this.page = newval;
      else this.page = oldval;
    },
  },
  created() {
    this.$emit("updateStartIndex", this.startIndex);
    this.$emit("updateEndIndex", this.endIndex);
  },
  methods: {
    validatePage(page) {
      if (!_.isFinite(page)) return false;
      if (page < 1) return false;
      if (page > this.lastPage) return false;
      return true;
    },
  },
};
</script>

<style scoped>
.center {
  text-align: center;
}
.pagingIcon {
  margin: 0 5px 0 5px;
}

.pageInput {
  width: 40px;
}

.disabled {
  color: darkgray;
}
</style>
