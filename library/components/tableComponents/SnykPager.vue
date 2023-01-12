<template>
  <div>
    <div
      v-if="numberOfItems && numberOfItems > itemsPerPage"
      class="pagination-footer flex justify-center relative h-8"
    >
      <!-- Rows Per Page -->
      <t-dropdown
        :disable-active-class="true"
        class="absolute left-2 top-5 text-[15px] text-[#145DEB] font-large"
      >
        <!-- Handle -->
        <div
          slot="handle"
          class="flex items-center gap-1 p-1 text-sm font-large"
        >
          <span>{{ itemsPerPage }} Per Page </span>
          <menu-down-icon size="20" />
        </div>

        <!-- Popup Contents -->
        <div attrs.slot="outside">
          <div class="px-[8px] pt-[4px] pb-[6px] w-full">
            <ul class="max-h-[320px] overflow-auto">
              <li
                v-for="itemsPerPageOption in [10, 50, 100, 500, 1000]"
                :key="itemsPerPageOption"
                class="flex justify-between px-[8px] pb-[1px] text-sm cursor-pointer text-[#555463]"
              >
                <div
                  class="flex items-center justify-between w-full hover:text-[#1C1C21] leading-[16.41px]"
                >
                  {{ itemsPerPageOption.toLocaleString() }}
                  <check-icon
                    v-if="itemsPerPageOption === itemsPerPage"
                    class="text-[#145DEB]"
                  />
                </div>
              </li>
            </ul>
          </div>
        </div>
      </t-dropdown>

      <!-- controls -->
      <ul
        id="pages"
        class="pagination-nav pagination-selector inline-flex pt-[16px]"
      >
        <li class="pagination-nav-item">
          <button
            class="h-8 minWidth text-[#145DEB] text-[15px] mr-[8px] focus:outline-none"
            @click="internalPage === 1 ? 1 : internalPage--"
          >
            <i class="fas fa-arrow-left"></i>
          </button>
        </li>
        <li
          v-for="page in pageNumbersToShow"
          :key="page"
          class="pagination-nav-item"
        >
          <button
            class="h-8 minWidth text-[15px] font-medium leading-5 focus:outline-none"
            :class="[
              page === internalPage
                ? 'active border-[#7FA7F5] bg-[#EAF1FF] rounded text-[#145DEB]'
                : 'text-[#0F47C6]',
            ]"
            @click="internalPage = page !== '...' ? page : internalPage"
          >
            {{ page.toLocaleString() }}
          </button>
        </li>
        <li class="pagination-nav-item">
          <button
            class="h-8 minWidth text-[#145DEB] text-[15px] ml-[8px] font-medium leading-5 focus:outline-none"
            @click="internalPage === lastPage ? lastPage : internalPage++"
          >
            <i class="fas fa-arrow-right"></i>
          </button>
        </li>
      </ul>

      <!-- totals -->
      <div
        class="absolute right-2 top-5 font-normal text-[#727184] text-[13px] leading-[18px]"
      >
        Showing {{ startIndex + 1 }}-
        {{ Math.min(startIndex + itemsPerPage, numberOfItems) }}
        of {{ numberOfItems.toLocaleString() }}
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
      let pageNumbersToShow = [];
      let pageToAdd = this.internalPage;
      let numberOfPagesAdded = 0;

      // if there are only up to 5 pages, only show the valid pages, do
      // not include "..."
      if (this.lastPage <= 5) {
        return [...Array(this.lastPage)].map((item, index) => index + 1);
      }

      if (this.internalPage + 3 < this.lastPage) {
        while (numberOfPagesAdded < 4) {
          pageNumbersToShow.push(pageToAdd);
          pageToAdd++;
          numberOfPagesAdded++;
        }
        pageNumbersToShow.push("...");
        pageNumbersToShow.push(this.lastPage);
      } else {
        pageToAdd = this.lastPage;
        while (numberOfPagesAdded < 4 && pageToAdd >= this.internalPage) {
          pageNumbersToShow.push(pageToAdd);
          pageToAdd--;
          numberOfPagesAdded++;
        }
        pageNumbersToShow.push("...");
        pageToAdd = 5 - numberOfPagesAdded;
        while (numberOfPagesAdded < 5) {
          pageNumbersToShow.push(pageToAdd);
          pageToAdd--;
          numberOfPagesAdded++;
        }
        pageNumbersToShow = pageNumbersToShow.reverse();
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

#pages {
  z-index: 2;
}
</style>
