<template>
  <div>
    <div id="searchContainer" class="searchContainer">
      <div id="searchIcon" ref="searchIcon" class="searchIcon">&#128269;</div>
      <input
        id="easySearch"
        ref="easySearch"
        v-model="tableSearch"
        placeholder="Search"
        class="easySearch"
      />
    </div>
  </div>
</template>

<script>
export default {
  name: "TSearch",
  props: {
    highlightQuerySelector: {
      type: String,
      required: true,
    },
    highlightOptions: {
      type: Object,
      default() {
        return {};
      },
    },
  },
  emits: ["updateSearchTerm"],
  data() {
    return {
      searchTerm: "",
      ignoreDomUpdates: false,
    };
  },
  computed: {
    tableSearch: {
      get() {
        return this.searchTerm;
      },
      set(newSearchTerm) {
        this.searchTerm = newSearchTerm;
        this.$emit("updateSearchTerm", newSearchTerm);
        this.updateHighlighting();
      },
    },
    markJSInstance() {
      if (this.highlightQuerySelector) {
        const element = document.querySelector(this.highlightQuerySelector);
        if (element) {
          // Vue's props down/events up doesn't work real well when the parent
          // component changes the DOM that needs to be marked, either the parent
          // needs to use the $refs "hack" to manually update the highlighting which
          // is fragile or it needs to use props, which are data, to pass what is
          // fundamentally an event to the search, which is both confusing and fragile.
          // Instead use pure javascript to watch the DOM element that is being
          // highlighted and call it a day.
          const config = { attributes: true, childList: true, subtree: true };
          const observer = new MutationObserver(this.updateHighlighting);
          observer.observe(element, config);

          return new Mark(element);
        } else {
          console.warn(
            "highlightQuerySelector: ",
            this.highlightQuerySelector,
            " did not match any elements"
          );
          return null;
        }
      }
      return null;
    },
  },
  methods: {
    updateHighlighting() {
      if (this.markJSInstance && !this.ignoreDomUpdates) {
        this.ignoreDomUpdates = true;
        this.markJSInstance.unmark();
        this.$nextTick(() => {
          this.markJSInstance.mark(this.searchTerm, this.highlightOptions);
          this.$nextTick(() => {
            this.ignoreDomUpdates = false;
          });
        });
      }
    },
  },
};
</script>

<style scoped>
.searchContainer {
  display: flex;
  border: 1px solid grey;
  border-radius: 3px;
  padding: 4px;
  width: 188px;
  background-color: transparent;
  margin: 10px 0;
}

.searchIcon {
  padding-left: 4px;
  padding-right: 4px;
}

.easySearch {
  display: block;
  border: none;
  background-color: transparent;
}

.easySearch:focus {
  outline: none;
  background-color: transparent;
}
</style>
