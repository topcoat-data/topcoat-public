<template>
  <div class="flex gap-1 items-center justify-start">
    Updated {{ relativeDateTime }}
  </div>
</template>

<script>
const SECOND_IN_MS = 1000;
const MINUTE_IN_MS = 60 * SECOND_IN_MS;     // 60000 ms
const HOUR_IN_MS = 60 * MINUTE_IN_MS;       // 3600000 ms
const DAY_IN_MS = 24 * HOUR_IN_MS;          // 86400000 ms
const MONTH_IN_MS = (365 * DAY_IN_MS) / 12; // 2628000000 ms
const YEAR_IN_MS = 365 * DAY_IN_MS;         // 31536000000 ms

const UNITS = [
    { unit: "year", ms: YEAR_IN_MS },
    { unit: "month", ms: MONTH_IN_MS },
    { unit: "day", ms: DAY_IN_MS },
    { unit: "hour", ms: HOUR_IN_MS },
    { unit: "minute", ms: MINUTE_IN_MS },
    { unit: "second", ms: SECOND_IN_MS },
];

const rtf = new Intl.RelativeTimeFormat("en", { numeric: "auto" });

/**
 * Get language-sensitive relative time message from Dates.
 * @param relative  - the relative dateTime, generally is in the past or future
 * @param pivot     - the dateTime of reference, generally is the current time
 * @return {string} - the language-sensitive relative time message
 */
function relativeTimeFromDates(relative, pivot = new Date()) {
    if (!relative) return "";
    const elapsed = relative.getTime() - pivot.getTime();
    return relativeTimeFromElapsed(elapsed);
};

/**
 * Get language-sensitive relative time message from elapsed time.
 * @param elapsed   - the elapsed time in milliseconds
 * @return {string} - the language-sensitive relative time message
 */
function relativeTimeFromElapsed(elapsed) {
    for (const { unit, ms } of UNITS) {
        if (Math.abs(elapsed) >= ms || unit === "second") {
            return rtf.format(Math.round(elapsed / ms), unit);
        }
    }
    return "";
};

/**
 * Examples, relative to 1691424920213 (Mon Aug 07 2023 18:15:20 GMT+0200):
 * 
 * "467074800000 ms" 20/10/1984 00:00:00 (Relative to now) → 39 years ago
 * "1445292000000 ms" 20/10/2015 00:00:00 (Relative to now) → 8 years ago
 * "1659888920213 ms" 07/08/2022 18:15:20 (Relative to now) → last year
 * "1688796920213 ms" 08/07/2023 08:15:20 (Relative to now) → last month
 * "1691338520213 ms" 06/08/2023 18:15:20 (Relative to now) → yesterday
 * "1691421320213 ms" 07/08/2023 17:15:20 (Relative to now) → 1 hour ago
 * "1691424860213 ms" 07/08/2023 18:14:20 (Relative to now) → 1 minute ago
 * "1691425040213 ms" 07/08/2023 18:17:20 (Relative to now) → in 2 minutes
 * "1692029720213 ms" 14/08/2023 18:15:20 (Relative to now) → in 7 days
 */

export default {
  name: "TRelativeDate",
  props: {
    baseDateTime: {
      type: String,
      required: true,
    },
  },
  computed: {
    relativeDateTime() {
      if (!this.baseDateTime) {
        return "";
      }

      return relativeTimeFromDates(new Date(this.baseDateTime));
    },
  },
};
</script>
