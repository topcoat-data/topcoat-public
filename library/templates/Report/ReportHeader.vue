<template>
  <div
    class="flex justify-between px-4 py-2 items-center border-b border-[#E5E7EB] bg-white sticky top-0 m-auto z-50"
  >
    <div class="flex items-center gap-4">
      <snyk-logo />
      <!-- <div class="text-[#461D9E] font-semibold text-base tracking-widest">INSIGHTS</div> -->
    </div>
    <div class="flex items-center justify-between gap-4">
      <div class="flex items-center gap-2">
        <span class="text-sm font-medium text-[#21214C] md:block hidden">
          {{ project.user.firstname }} {{ " " }} {{ project.user.lastname }}
        </span>
        <div
          class="flex items-center justify-center w-8 h-8 rounded-full name-intials"
        >
          <span class="text-sm text-white">
            {{ project.user.firstname[0]
            }}{{ project.user.lastname ? project.user.lastname[0] : "" }}
          </span>
        </div>
        <t-dropdown disable-handle-class>
          <menu-down-icon slot="handle" />
          <div class="flex flex-col gap-2 px-2 py-2 md:px-5">
            <a href="/logout">Logout</a>
            <a href="https://snyk.io/" class="md:hidden">Go to snyk.io</a>
          </div>
        </t-dropdown>
      </div>
      <a
        href="https://snyk.io/"
        class="md:flex md:gap-1 md:border-1 border-[#C3C2CB] items-center hidden rounded py-1 px-2"
      >
        Go to snyk.io
        <open-in-new-icon :size="18" />
      </a>
    </div>
  </div>
</template>

<style>
.name-intials {
  background: linear-gradient(104.04deg, #9043c6 0%, #441c99 100%);
  border-radius: 100px;
}
</style>
