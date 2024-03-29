<template>
  <t-dropdown :disable-active-class="$slots.handle ? true : false">
    <slot slot="handle" name="handle">
      <div class="flex items-center gap-1 p-1 text-sm font-medium">
        <span style="color: #145deb" class="pl-1">
          <chart-timeline-variant-shimmer-icon :size="18" />
        </span>
        {{ page.title }}
        <menu-down-icon :size="20" />
      </div>
    </slot>

    <div class="px-2 pt-4 pb-2 border-b border-[#E4E3E8]">
      <h6 class="text-xs text-[#727184] tracking-[0.1em]">CHOOSE REPORT</h6>
      <!-- <ul class="inline-flex gap-2 mt-2 base-tabs">
				<li
					class="p-2 rounded-lg text-xs cursor-pointer text-[#1c1c21]"
					v-for="pane in panes"
					:key="pane.key"
					:class="activeSection === pane.key ? 'bg-[#eaf1ff] text-[#0F47C6]' : 'text-[#1c1c21]'"
					@click="activeSection = pane.key"
				>
					{{ pane.label }}
				</li>
			</ul> -->
    </div>

    <div class="px-2 pt-2 nav-search">
      <base-search-input
        v-model="search"
        class="mt-0 mb-3 text-sm search-report !rounded-md"
        placeholder="Search Reports"
        size="small"
        :clearable="false"
      />

      <small v-if="activeSection === 'all' && !pages.all.length"
        >No reports found.</small
      >
      <small
        v-else-if="activeSection === 'favorites' && !pages.favorites.length"
        >No favorites found.</small
      >
      <small v-else-if="activeSection === 'recents' && !pages.recents.length"
        >No recents found.</small
      >

      <ul class="px-2 max-h-[200px] overflow-auto">
        <li
          v-for="(page, index) in pages[activeSection].filter((p) =>
            p.url.toLowerCase().includes(search)
          )"
          :key="index"
          class="flex justify-between mb-3 text-sm cursor-pointer hover:text-[#1c1c21]"
          :class="navSelected(page.url, 'text-[#1c1c21]', 'text-[#555463]')"
        >
          <a
            :href="page.url"
            class="flex items-center justify-between w-full"
            @click.prevent="redirectToPage($event, page)"
          >
            {{ page.title }}
            <span
              v-if="selected === 'reporting/' + page.main_url"
              style="color: #0f47c6"
              class="flex items-center h-full"
            >
              <check-icon />
            </span>
          </a>
        </li>
      </ul>
    </div>
  </t-dropdown>
</template>

<script>
export default {
  props: {
    label: {
      type: String,
      default: "Select",
    },
  },
  data: () => ({
    active: false,
    activeSection: "all",
    alignClass: "",
    favorites: [],
    panes: [
      {
        label: "All",
        key: "all",
      },
    ],
    popup: false,
    search: "",
  }),
  computed: {
    selected() {
      return window.location.pathname.substring(1);
    },
    pages() {
      const parentContextUrl = this.whoami?.context?.parent;
      const pages = [];
      for (let page of this.project.nav) {
        page.main_url = page.url; // Common parameter for 'active page' check.
        if (parentContextUrl) {
          // If iframe, use parent url.
          page.url = `${parentContextUrl}?context[page]=${page.url}`;
        }
        pages.push(page);
      }

      // Todo: favorites and recent.
      return {
        all: pages,
        favorites: [],
        recents: [],
      };
    },
  },
  methods: {
    redirectToPage(e, page) {
      this.unsetAllFilters();

      if (e.metaKey || e.ctrlKey) {
        window.open(page.url, "_blank");
      } else if (e.shiftKey) {
        window.open(page.url);
      } else {
        window.open(page.main_url, "_self");
      }
    },
  },
};
</script>

<style>
.nav-search .vue--search-input__field {
  @apply !rounded-3xl !bg-white !opacity-[0.5];
}
</style>
