<template>
  <div
    class="grid"
    :class="[
      gapX && styles.gapsX[gapX],
      gapY && styles.gapsY[gapY],
      isPadded && 'p-4',
      styles.bgColors[bgColor],
      styles.columns[columnCount],
      styles.gaps[gap],
      styles.rows[rowCount],
      styles.shadows[isElevated],
    ]"
  >
    <slot></slot>
  </div>
</template>

<script>
export default {
  // eslint-disable-next-line
  name: 't-grids',
  props: {
    //* Strings
    bgColor: {
      type: String,
      default: 'transparent',
      validator: (v) => ['transparent', 'primary', 'secondary', 'light', 'dark', 'neutral'].includes(v),
    },
    columnCount: {
      type: String,
      default: 'none',
      validator: (v) => ['none', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'].includes(v),
    },
    gap: {
      type: String,
      default: '0',
      validator: (v) => ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'].includes(v),
    },
    gapX: {
      type: String,
      default: '0',
      validator: (v) => ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'].includes(v),
    },
    gapY: {
      type: String,
      default: '0',
      validator: (v) => ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'].includes(v),
    },
    rowCount: {
      type: String,
      default: 'none',
      validator: (v) => ['none', '1', '2', '3', '4', '5', '6'].includes(v),
    },
    //* String-leans
    isElevated: {
      type: [Boolean, String],
      default: 'none',
      validator: (v) => [true, false, 'normal', 'sm', 'md', 'lg', 'xl', '2xl', 'inner', 'none'].includes(v),
    },
    isPadded: {
      type: [Boolean, String],
      default: false,
      validator: (v) => ['true', 'false'].includes(String(v)),
    },
  },
  data() {
    return {
      styles: {
        bgColors: {
          primary: 'bg-primary-400',
          secondary: 'bg-secondary-400',
          light: 'bg-neutral-50',
          dark: 'bg-neutral-900',
          neutral: 'bg-neutral-200',
          transparent: 'bg-transparent',
        },
        columns: {
          1: 'grid-cols-1',
          2: 'grid-cols-2',
          3: 'grid-cols-3',
          4: 'grid-cols-4',
          5: 'grid-cols-5',
          6: 'grid-cols-6',
          7: 'grid-cols-7',
          8: 'grid-cols-8',
          9: 'grid-cols-9',
          10: 'grid-cols-10',
          11: 'grid-cols-11',
          12: 'grid-cols-12',
          none: 'grids-cols-none',
        },
        gaps: {
          0: 'gap-0',
          1: 'gap-1',
          2: 'gap-2',
          3: 'gap-3',
          4: 'gap-4',
          5: 'gap-5',
          6: 'gap-6',
          7: 'gap-7',
          8: 'gap-8',
          9: 'gap-9',
          10: 'gap-10',
        },
        gapsX: {
          0: 'gap-x-0',
          1: 'gap-x-1',
          2: 'gap-x-2',
          3: 'gap-x-3',
          4: 'gap-x-4',
          5: 'gap-x-5',
          6: 'gap-x-6',
          7: 'gap-x-7',
          8: 'gap-x-8',
          9: 'gap-x-9',
          10: 'gap-x-10',
        },
        gapsY: {
          0: 'gap-y-0',
          1: 'gap-y-1',
          2: 'gap-y-2',
          3: 'gap-y-3',
          4: 'gap-y-4',
          5: 'gap-y-5',
          6: 'gap-y-6',
          7: 'gap-y-7',
          8: 'gap-y-8',
          9: 'gap-y-9',
          10: 'gap-y-10',
        },
        rows: {
          1: 'grid-rows-1',
          2: 'grid-rows-2',
          3: 'grid-rows-3',
          4: 'grid-rows-4',
          5: 'grid-rows-5',
          6: 'grid-rows-6',
          none: 'grids-rows-none',
        },
        shadows: {
          true: 'shadow',
          normal: 'shadow',
          sm: 'shadow-sm',
          md: 'shadow-md',
          lg: 'shadow-lg',
          xl: 'shadow-xl',
          '2xl': 'shadow-2xl',
          inner: 'shadow-inner',
          none: 'shadow-none',
        },
      },
    }
  },
}
</script>