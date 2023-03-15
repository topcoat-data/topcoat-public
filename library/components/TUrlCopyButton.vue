<template>
  <div class="relative">
    <t-tooltip position="bottom" width="130px">
      <button
        slot="trigger"
        class="h-[30px] w-[30px] rounded-[4px] flex items-center justify-center border border-[#C3C2CB] p-1 transition-colors"
        :class="{ 'bg-[#B4E4D9]': copied }"
        @click="copy"
      >
        <t-loading-spinner v-if="!whoami" position="relative" />
        <check-icon v-else-if="copied" :size="18" />
        <link-icon v-else :size="18" />
        <span class="visually-hidden">{{
          copied ? "URL Copied" : "Copy URL"
        }}</span>
      </button>
      {{ copied ? "URL Copied" : "Copy URL" }}
    </t-tooltip>
  </div>
</template>

<script>
export default {
  data: () => ({
    copied: false,
  }),
  computed: {
    url() {
      if (this.parentUrl) {
        this.parentUrl.searchParams.set("context[page]", this.page.url);
        this.filters.map((filter) => {
          this.parentUrl.searchParams.set(
            filter.name,
            encodeURIComponent(filter.value)
          );
        });
        return this.parentUrl.toString();
      }

      return window.location.href;
    },
    parentUrl() {
      try {
        if (this?.whoami?.context?.parent) {
          return new URL(this.whoami.context.parent[0]);
        }
      } catch (e) {
        console.log(e);
      }
      return null;
    },
  },
  methods: {
    copy() {
      if (!this.whoami) return;
      this.copied = true;

      const tempInput = document.createElement("input");
      document.body.appendChild(tempInput);
      tempInput.value = this.url;
      tempInput.select();

      document.execCommand("copy");
      document.body.removeChild(tempInput);

      setTimeout(() => {
        this.copied = false;
        // Timeout to show success message and hide it.
      }, 1000);
    },
  },
};
</script>

<style>
/* 
 * Utility class to hide content visually while keeping it screen reader-accessible.
 * Source: https://www.scottohara.me/blog/2017/04/14/inclusively-hidden.html 
 */
.visually-hidden:not(:focus):not(:active) {
  clip: rect(0 0 0 0);
  clip-path: inset(100%);
  height: 1px;
  overflow: hidden;
  position: absolute;
  white-space: nowrap;
  width: 1px;
}
</style>
