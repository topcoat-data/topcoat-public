<template>
  <div
    class="flex flex-wrap items-center bg-white px-5"
    style="font-family: 'Roboto',"
  >
    <a
      :href="'/' + page.url"
      v-for="page in project.nav"
      :key="page.src"
      class="h-12 px-2 pt-3 text-sm border-b-4"
      :class="
        navSelected(
          'reporting/'+page.url,
          'border-[#145DEB] text-[#1C1C21]',
          'border-transparent text-[#727184]'
        )
      "
    >
      {{ page.title }}
    </a>
  </div>
</template>

<script>
export default {
  name: "TNavigationTabs",
}
</script>
