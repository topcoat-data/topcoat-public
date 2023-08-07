<template>
  <div class="flex gap-1 items-center justify-start">
    Updated {{ relativeDateTime }}
    <t-loading-spinner v-if="loading" position="relative" />
  </div>
</template>

<script>
var units = {
  year: 24 * 60 * 60 * 1000 * 365,
  month: 24 * 60 * 60 * 1000 * 365 / 12,
  day: 24 * 60 * 60 * 1000,
  hour: 60 * 60 * 1000,
  minute: 60 * 1000,
  second: 1000
};

var rtf = new Intl.RelativeTimeFormat('en', { numeric: 'auto', style: 'short' });

var getRelativeTime = (d1, d2 = new Date()) => {
  var elapsed = d1 - d2;
  for (var u in units)
    if (Math.abs(elapsed) > units[u] || u == 'second')
      return rtf.format(Math.round(elapsed / units[u]), u);
};

export default {
  props: {
    baseDateTime: {
      type: String,
      required: true
    }
  },
  computed: {
    relativeDateTime() {
      if (!this.baseDateTime) {
        return '';
      }

      const dateTime = new Date(this.baseDateTime);
      return getRelativeTime(dateTime);
    }
  }
};
</script>

<!-- <template>
    <div class="flex gap-1 items-center justify-start">
        Updated {{ relativeDateTime }}
        <t-loading-spinner v-if="loading" position="relative" />
    </div>
</template>

<script>
export default {
  props: {
    updateDateTime: {
      type: String,
      required: true,
    }
  }, 
  data: () => ({
    is_filter: true,
    // Is filter removes height and background css to allow for custom html and css changes.
  }),
  computed: {
    relativeDateTime() {
        if(!this.baseDateTime) {
            return ""
        }
      // console.log(typeof this.baseDateTime);
      const dateTime = new Date(this.baseDateTime);
      const now = new Date();
      const differenceInSeconds = Math.floor((dateTime - now) / 1000);
      const rtf1 = new Intl.RelativeTimeFormat('en', { style: 'short' });
       if (Math.abs(differenceInSeconds) >= 60 * 60 * 24 * 365) {
        return rtf1.format(Math.floor(differenceInSeconds / (60 * 60 * 24 * 365)), 'year');
      }
      if (Math.abs(differenceInSeconds) >= 60 * 60 * 24 * 30) {
        return rtf1.format(Math.floor(differenceInSeconds / (60 * 60 * 24 * 30)), "month");
      }
      if (Math.abs(differenceInSeconds) >= 60 * 60 * 24) {
        return rtf1.format(Math.floor(differenceInSeconds / (60 * 60 * 24)), "day");
      }
      if (Math.abs(differenceInSeconds) >= 60 * 60) {
        return rtf1.format(Math.floor(differenceInSeconds / (60 * 60)), "hour");
      }
      if (Math.abs(differenceInSeconds) >= 60) {
        return rtf1.format(Math.floor(differenceInSeconds / (60)), "minute");
      }
      return rtf1.format(Math.floor(differenceInSeconds), "second");
    },
  },
};
</script> -->

