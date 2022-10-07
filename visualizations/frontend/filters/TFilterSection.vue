<template>
  <div class="w-full h-max border-b border-[#E5E7EB] bg-[#F9F9FA] relative">
    <div class="flex flex-wrap gap-4 p-3" v-if="Object.keys(filters).length">
      <div
        v-for="key in Object.keys(filterObject)"
        class="flex flex-col flex-wrap"
      >
        <div class="font-semibold">
          {{ key.replace(/_/g, " ").toUpperCase() }}
        </div>

        <!-- Filter with multiple items -->
        <!-- Syntax: val1|val2|val3 -->
        <div v-if="Array.isArray(filterObject[key])" class="flex gap-1">
          <div v-for="value in filterObject[key]">
            <div class="tag-chip">
              {{ value }}
              <close-icon
                :size="12"
                @click="removeFromArray(key, value)"
                class="cursor-pointer"
              />
            </div>
          </div>
        </div>

        <!-- Tags object filter -->
        <!-- Syntax: { key: [val1, val2], key_2: [val3, val4] } -->
        <div
          v-else-if="typeof filterObject[key] === 'object'"
          class="flex gap-2"
        >
          <div
            v-for="(tagValues, tagKey) in filterObject[key]"
            :key="tagKey"
            class="tag-chip"
          >
            <span class="font-semibold">{{ tagKey }}:</span>
            <div
              v-for="tagValue in tagValues"
              :key="tagValue"
              class="flex items-center gap-1"
            >
              {{ tagValue }}
              <close-icon
                :size="12"
                @click="removeFromObject(key, tagKey, tagValue)"
                class="cursor-pointer"
              />
            </div>
          </div>
        </div>

        <!-- Plain string -->
        <div v-else>
          <div class="tag-chip">
            {{ filterObject[key] }}
            <close-icon
              :size="12"
              @click="removeString(key, filterObject[key])"
              class="cursor-pointer"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data: () => ({
    is_filter: true,
  }),
  computed: {
    filterObject() {
      // Convert string url values to appopriate data types.
      const filters = {};
      if (this.filters) {
        for (let key of Object.keys(this.filters)) {
          let value = this.filters[key];
          // Is number
          if (typeof value === "number") {
            filters[key] = value;
          } else if (value.includes("|")) {
            // Multiple values
            filters[key] = value.split("|");
          } else if (value[0] === "{" && value[value.length - 1] === "}") {
            // Is object string
            try {
              filters[key] = JSON.parse(value);
            } catch (error) {
              console.error(`Failed to parse ${key} filter`);
            }
          } else {
            // Is string
            filters[key] = value;
          }
        }
      }
      return filters;
    },
  },
  methods: {
    removeFromArray(key, value) {
      const filterState = this.filterObject[key];
      if (filterState) {
        const items = filterState.filter((item) => item !== value).join("|");
        if (items) {
          return this.setFilter({
            name: key,
            value: items,
          });
        }
        return this.deleteFilter({ name: key });
      }
    },
    removeFromObject(key, tagKey, tagValue) {
      const filterState = this.filterObject[key];
      let object = {};
      if (filterState) {
        let tag = filterState[tagKey];
        let newValue = tag.filter((t) => t !== tagValue);
        if (newValue.length) {
          object = { ...filterState, [tagKey]: newValue };
        } else {
          delete filterState[tagKey];
          object = filterState;
        }
      }
      if (Object.keys(object).length) {
        return this.setFilter({
          name: key,
          value: JSON.stringify(object),
        });
      }
      return this.deleteFilter({ name: key });
    },
    removeString(key, value) {
      this.deleteFilter({ name: key });
    },
  },
};
</script>

<style>
.tag-chip {
  @apply flex gap-2 items-center p-1 text-xs bg-[#f4f4f6] border border-[#e8e8e8] rounded w-max;
}
</style>
