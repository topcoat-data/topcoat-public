<template>
  <div>
    <div v-if="numberOfItems > itemsPerPage" class="center">
      <span
        ref="angleDoubleLeft"
        class="pagingIcon"
        :class="internalPage === 1 ? 'disabled' : 'enabled'"
        :disabled="internalPage === 1"
        @click="internalPage = 1"
      >
        &#171;
      </span>

      <span
        ref="angleLeft"
        class="pagingIcon"
        :class="internalPage === 1 ? 'disabled' : 'enabled'"
        :disabled="internalPage === 1"
        @click="internalPage === 1 ? 1 : internalPage--"
      >
        &#8249;
      </span>

      <input id="pageInput" ref="pageInput" v-model.number="internalPage" class="pageInput" />

      <span
        ref="angleRight"
        class="pagingIcon"
        :class="internalPage === lastPage ? 'disabled' : 'enabled'"
        :disabled="internalPage === lastPage"
        @click="internalPage === lastPage ? lastPage : internalPage++"
      >
        &#8250;
      </span>

      <span
        ref="angleDoubleRight"
        class="pagingIcon"
        :class="internalPage === lastPage ? 'disabled' : 'enabled'"
        :disabled="internalPage === lastPage"
        @click="internalPage = lastPage"
      >
        &#187;
      </span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TPager',
  // TODO: Prop validation
  props: {
    numberOfItems: { type: Number, required: true },
    itemsPerPage: { type: Number, default: 10 },
    reset: {type: Boolean, default: false}
  },
  emits: ['updateStartIndex', 'updateEndIndex', 'setResetFunction'],
  data() {
    return {
      internalPage: 1,
    }
  },
  computed: {
    lastPage() {
      return Math.ceil(this.numberOfItems / this.itemsPerPage)
    },
    startIndex() {
      return (this.internalPage - 1) * this.itemsPerPage
    },
    endIndex() {
      let endIndex = this.startIndex + this.itemsPerPage
      if (endIndex > this.numberOfItems) endIndex = this.numberOfItems
      return endIndex
    },
    isValidPage() {
      return this.validatePage(this.internalPage)
    },
  },
  watch: {
    numberOfItems() {
      this.internalPage = 1
    },
    startIndex() {
      if (this.isValidPage) this.$emit('updateStartIndex', this.startIndex)
    },
    endIndex() {
      if (this.isValidPage) this.$emit('updateEndIndex', this.endIndex)
    },
    internalPage(newval, oldval) {
      // allow users to clear out internalPage input
      if (newval === '') return

      if (this.validatePage(newval)) this.internalPage = newval
      else this.internalPage = oldval
    },
  },
  created() {
    this.$emit('updateStartIndex', this.startIndex)
    this.$emit('updateEndIndex', this.endIndex)
    this.$emit('setResetFunction', this.reset)
  },
  methods: {
    reset(){
      if(this.reset) this.internalPage = 1
    },
    validatePage(internalPage) {
      if (!_.isFinite(internalPage)) return false
      if (internalPage < 1) return false
      if (internalPage > this.lastPage) return false
      return true
    },
  },
}
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
