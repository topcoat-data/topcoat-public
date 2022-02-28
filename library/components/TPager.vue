<template>
  <div>
    <div v-if="numberOfitems > itemsPerPage" class="center">
      <span
        ref="AngleDoubleLeft"
        class="pagingIcon"
        :class="page === 1 ? 'disabled' : 'enabled'"
        @click="page = 1"
      >
        &#171;
      </span>

      <span
        ref="AngleLeft"
        class="pagingIcon"
        :class="page === 1 ? 'disabled' : 'enabled'"
        @click="page === 1 ? 1 : page--"
      >
        &#8249;
      </span>

      <input id="pageInput" ref="pageInput" v-model="page" class="pageInput" />

      <span
        ref="AngleRight"
        class="pagingIcon"
        :class="page === lastPage ? 'disabled' : 'enabled'"
        @click="page === lastPage ? lastPage : page++"
      >
        &#8250;
      </span>

      <span
        ref="AngleDoubleRight"
        class="pagingIcon"
        :class="page === lastPage ? 'disabled' : 'enabled'"
        @click="page = lastPage"
      >
        &#187;
      </span>
    </div>
  </div>
</template>

<style scoped>
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

<script>
export default {
  name: "TPager",
  // TODO: Prop validation
  props: {
    numberOfitems: { type: Number, required: true },
    itemsPerPage: { type: Number, default: 10 },
  },
  data() {
    return {
      page: 1,
    };
  },
  computed: {
    lastPage() {
      return Math.ceil(this.numberOfitems / this.itemsPerPage);
    },
    startIndex() {
      const startIndex = (this.page - 1) * this.itemsPerPage;
      return startIndex;
    },
    endIndex() {
      let endIndex = this.startIndex + this.itemsPerPage;
      if (endIndex > this.numberOfitems) endIndex = this.numberOfitems;
      return endIndex;
    },
    isValidPage() {
      if (!this.page) return false;
      if (isNaN(this.page)) return false;
      if (this.page <= 0) return false;
      if (this.page > this.lastPage) return false;
      return true;
    },
  },
  watch: {
    numberOfitems() {
      this.page = 1;
    },
    startIndex() {
      if (this.isValidPage) this.$emit("update:startIndex", this.startIndex);
    },
    endIndex() {
      if (this.isValidPage) this.$emit("update:endIndex", this.endIndex);
    },
    page(newval, oldval) {
      if (newval === "") return;
      if (!Number.isInteger(newval)) this.page = Math.floor(newval);

      if (isNaN(this.page)) this.page = oldval;
      else if (this.page < 1) this.page = oldval;
      else if (this.page > this.lastPage) this.page = oldval;
    },
  },
  created() {
    this.$emit("update:startIndex", this.startIndex);
    this.$emit("update:endIndex", this.endIndex);
  },
};
</script>

<style scoped>
.center {
  text-align: center;
}
</style>