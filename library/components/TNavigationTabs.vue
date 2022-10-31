<template>
  <div
    class="flex flex-wrap items-center bg-white px-5"
    style="font-family: 'Roboto'"
  >
    <a
      v-for="page in project.nav"
      :key="page.src"
      :href="'/' + page.url"
      class="h-12 px-2 pt-3 text-sm border-b-4"
      :class="
        navSelected(
          page.url,
          'border-[#145DEB] text-[#1C1C21]',
          'border-transparent text-[#727184]'
        )
      "
    >
      {{ page.title }}
    </a>
  </div>
</template>
