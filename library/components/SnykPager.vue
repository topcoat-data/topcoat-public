<template>
  <div>
    <div
      class="pagination-footer flex justify-center relative"
      v-if="numberOfItems"
    >
      <ul class="pagination-nav pagination-selector inline-flex pt-[16px]">
        <li class="pagination-nav-item">
          <button
            class="
              h-8
              minWidth
              text-[#145DEB] text-[15px]
              mr-[8px]
              focus:outline-none
            "
            @click="internalPage === 1 ? 1 : internalPage--"
          >
            <i class="fas fa-arrow-left"></i>
          </button>
        </li>
        <li v-for="page in pageNumbersToShow" class="pagination-nav-item">
          <button
            class="
              h-8
              minWidth
              text-[15px]
              font-medium
              leading-5
              focus:outline-none
            "
            @click="internalPage = page !== '...' ? page : internalPage"
            :class="[
              page === internalPage
                ? 'active border-[#7FA7F5] bg-[#EAF1FF] rounded text-[#145DEB]'
                : 'text-[#0F47C6]',
            ]"
          >
            {{ page }}
          </button>
        </li>
        <li class="pagination-nav-item">
          <button
            class="
              h-8
              minWidth
              text-[#145DEB] text-[15px]
              ml-[8px]
              font-medium
              leading-5
              focus:outline-none
            "
            @click="internalPage === lastPage ? lastPage : internalPage++"
          >
            <i class="fas fa-arrow-right"></i>
          </button>
        </li>
      </ul>
      <div
        class="
          absolute
          right-2
          top-5
          font-normal
          text-[#727184] text-[13px]
          leading-[18px]
        "
      >
        Showing {{ startIndex + 1 }}-{{
          Math.min(startIndex + itemsPerPage, numberOfItems)
        }}
        of {{ numberOfItems }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SnykPager",
  props: {
    numberOfItems: { type: Number, required: true },
    itemsPerPage: { type: Number, default: 10 },
  },
  emits: ["updateStartIndex", "updateEndIndex", "setResetFunction"],
  data() {
    return {
      internalPage: 1,
    };
  },
  computed: {
    pageNumbersToShow() {
      pageNumbersToShow = [];
      let pageToAdd = this.internalPage;
      let numberOfPagesAdded = 0;
      while (pageToAdd <= this.lastPage && numberOfPagesAdded < 4) {
        pageNumbersToShow.push(pageToAdd);
        pageToAdd++;
        numberOfPagesAdded++;
      }
      if (numberOfPagesAdded === 4) {
        pageNumbersToShow.push("...");
        pageNumbersToShow.push(this.lastPage);
      } else {
        pageToAdd = 1;
        prePages = [];
        while (this.internalPage <= this.lastPage && numberOfPagesAdded <= 4) {
          prePages.push(pageToAdd);
          pageToAdd++;
          if (numberOfPagesAdded === 4) {
            prePages.push("...");
          }
          numberOfPagesAdded++;
        }
        pageNumbersToShow = prePages.concat(pageNumbersToShow);
      }
      return pageNumbersToShow;
    },
    lastPage() {
      return Math.ceil(this.numberOfItems / this.itemsPerPage);
    },
    startIndex() {
      return (this.internalPage - 1) * this.itemsPerPage;
    },
    endIndex() {
      let endIndex = this.startIndex + this.itemsPerPage;
      if (endIndex > this.numberOfItems) endIndex = this.numberOfItems;
      return endIndex;
    },
    isValidPage() {
      return this.validatePage(this.internalPage);
    },
  },
  watch: {
    numberOfItems() {
      this.internalPage = 1;
    },
    startIndex() {
      if (this.isValidPage) this.$emit("updateStartIndex", this.startIndex);
    },
    endIndex() {
      if (this.isValidPage) this.$emit("updateEndIndex", this.endIndex);
    },
    internalPage(newval, oldval) {
      // allow users to clear out internalPage input
      if (newval === "") return;

      if (this.validatePage(newval)) this.internalPage = newval;
      else this.internalPage = oldval;
    },
  },
  created() {
    this.$emit("updateStartIndex", this.startIndex);
    this.$emit("updateEndIndex", this.endIndex);
    this.$emit("setResetFunction", this.reset);
  },
  methods: {
    reset() {
      this.internalPage = 1;
    },
    validatePage(internalPage) {
      if (!_.isFinite(internalPage)) return false;
      if (internalPage < 1) return false;
      if (internalPage > this.lastPage) return false;
      return true;
    },
  },
};
</script>

<style scoped>
.minWidth {
  min-width: 2em;
  margin-right: 0.25em;
}
</style>
