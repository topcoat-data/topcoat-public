<template>
  <div
    class="relative flex items-center w-full h-max"
    :class="[
      styles.borders[borderStyle],
      styles.textColors[textColor],
      isTrue(isOutlined) && [
        styles.bgColors[innerBgColor],
        styles.borderRadius[isRounded],
      ],
      isTrue(isDisabled) && 'opacity-30 group',
      isTrue(isError) && 'border-error-400 placeholder-error-400',
      !isTrue(isError) &&
        isFocused &&
        styles.borderColors[borderHighlightColor],
      !isTrue(isError) && !isFocused && styles.borderColors[borderColor],
      isTrue(isOutlined)
        ? styles.borderWidthSizes.outline[borderWidth]
        : styles.borderWidthSizes.underline[borderWidth],
    ]"
  >
    <!-- Label -->
    <!-- Note: For Input and Label, cursor classes only work when directly applied to element -->
    <div class="flex flex-col justify-center w-full">
      <div
        class="text-left transition-colors w-max"
        :class="[
          isTrue(isInsideLabel) && 'pt-2',
          isTrue(isError) && 'text-error-400',
        ]"
      >
        <!-- Inside Label -->
        <label
          v-if="isTrue(isInsideLabel)"
          :for="inputUuid"
          class="top-0 px-1 pb-1 ml-4 text-sm opacity-80 group-hover:cursor-not-allowed"
        >
          {{ label }}
        </label>

        <!-- Top Label -->
        <label
          v-else
          class="absolute px-1 ml-4 transition-transform transform group-hover:cursor-not-allowed"
          :for="inputUuid"
          :class="[
            // Translate label according to border-width.
            isTrue(isOutlined) && styles.bgColors[innerBgColor],
            topLabel
              ? styles.borderLabelPosition[borderWidth]
              : 'translate-y-4 h-max',
          ]"
        >
          <div :class="topLabel && 'bottom-1.5'" class="relative">
            {{ label }}
          </div>
        </label>
      </div>

      <!-- Input -->
      <input
        :id="inputUuid"
        :value="value"
        class="pl-5 pr-8 bg-transparent outline-none h-max group-hover:cursor-not-allowed"
        :disabled="isTrue(isDisabled)"
        :placeholder="placeholder"
        :class="[
          styles.borderRadius[isRounded],
          isTrue(isInsideLabel) ? 'pt-1 pb-3' : 'py-4',
        ]"
        aria-label="text field"
        @input="value = $event.target.value"
        @focus="isFocused = true"
        @blur="isFocused = false"
        @keyup.enter="urlParam = value"
      />
    </div>

    <!-- Icon -->
    <div class="absolute top-0 bottom-0 right-0 pt-2 pr-3 my-auto h-max">
      <i
        v-if="(value && isTrue(isClearable)) || isTrue(isLoading)"
        class="w-max"
        :class="[
          isTrue(isLoading)
            ? 'i-mdi:loading animate-spin'
            : 'i-mdi:close cursor-pointer',
          isTrue(isError) ? 'text-error-400' : 'text-neutral-500',
          styles.textColors[textColor],
        ]"
        @click="clearInput"
      ></i>
    </div>
  </div>
</template>

<script>
// import { nanoid } from 'nanoid'
// Todo: enable once spa is live, not supported by topcoat-core currently
export default {
  // eslint-disable-next-line
  name: "t-text-input",
  props: {
    //* Strings
    borderColor: {
      type: String,
      default: "neutral",
    },
    borderHighlightColor: {
      type: String,
      default: "primary",
    },
    borderStyle: {
      type: String,
      default: "solid",
      validator: (v) => ["solid", "dashed", "dotted", "double"].includes(v),
    },
    borderWidth: {
      type: String,
      default: "normal",
      validator: (v) => ["normal", "medium", "bold", "extrabold"].includes(v),
    },
    innerBgColor: {
      type: String,
      default: "light",
      validator: (v) => ["primary", "secondary", "light", "dark"].includes(v),
    },
    label: {
      type: String,
      default: "",
    },
    placeholder: {
      type: String,
      default: "",
    },
    textColor: {
      type: String,
      default: "dark",
    },
    //* String-leans
    isClearable: {
      type: [Boolean, String],
      default: false,
      validator: (v) => ["true", "false"].includes(String(v)),
    },
    isDisabled: {
      type: [Boolean, String],
      default: false,
      validator: (v) => ["true", "false"].includes(String(v)),
    },
    isError: {
      type: [Boolean, String],
      default: false,
      validator: (v) => ["true", "false"].includes(String(v)),
    },
    isInsideLabel: {
      type: [Boolean, String],
      default: false,
      validator: (v) => ["true", "false"].includes(String(v)),
    },
    isLoading: {
      type: [Boolean, String],
      default: false,
      validator: (v) => ["true", "false"].includes(String(v)),
    },
    isOutlined: {
      type: [Boolean, String],
      default: false,
      validator: (v) => ["true", "false"].includes(String(v)),
    },
    isRounded: {
      type: [Boolean, String],
      default: "none",
      validator: (v) =>
        ["true", "none", "sm", "md", "lg", "xl", "2xl", "3xl"].includes(
          String(v)
        ),
    },
  },
  data() {
    return {
      isFocused: false, // true if input has value or typing cursor
      styles: {
        borders: {
          solid: "border-solid",
          dashed: "border-dashed",
          dotted: "border-dotted",
          double: "border-double",
        },
        borderColors: {
          primary: "border-primary-400",
          secondary: "border-secondary-400",
          light: "border-neutral-50",
          dark: "border-neutral-900",
          neutral: "border-neutral-400",
        },
        borderLabelPosition: {
          normal: "-translate-y-0.5 !text-xs",
          medium: "-translate-y-0.5 !text-xs",
          bold: "-translate-y-1 !text-xs",
          extrabold: "-translate-y-2 !text-sm",
        },
        borderRadius: {
          none: "rounded-none",
          true: "rounded",
          sm: "rounded-sm",
          md: "rounded-md",
          lg: "rounded-lg",
          xl: "rounded-xl",
          "2xl": "rounded-2xl",
          "3xl": "rounded-3xl",
        },
        borderWidthSizes: {
          outline: {
            normal: "border",
            medium: "border-2",
            bold: "border-4",
            extrabold: "border-8",
          },
          underline: {
            normal: "border-b",
            medium: "border-b-2",
            bold: "border-b-4",
            extrabold: "border-b-8",
          },
        },
        bgColors: {
          primary: "bg-primary-50",
          secondary: "bg-secondary-50",
          light: "bg-neutral-50",
          dark: "bg-neutral-900",
          neutral: "bg-neutral-400",
        },
        textColors: {
          primary: "text-primary-400",
          secondary: "text-secondary-400",
          light: "text-neutral-50",
          dark: "text-neutral-900",
          neutral: "text-neutral-400",
        },
      },
      value: "",
      text_internal: null,
      is_filter: true, // Todo: remove when spa is live, old backend logic uses to check if component is a viz or filter
    };
  },
  computed: {
    // Unique id for input.
    inputUuid() {
      // Todo: remove when spa is live
      return "xxxx-yy".replace(/[xy]/g, function (c) {
        var r = (Math.random() * 16) | 0,
          v = c == "x" ? r : (r & 0x3) | 0x8;
        return v.toString(16);
      });
      // Todo: enable once spa is live, not supported by topcoat-core currently
      // return nanoid()
    },
    topLabel() {
      // Border label that animates to top if any of these condition are true.
      // Unlike `inside label` top label is only active when input focus or input has value.
      return (
        (this.isFocused || this.placeholder || this.value) &&
        !this.isTrue(this.isInsideLabel)
      );
    },
    urlParam: {
      get() {
        return this.text_internal;
      },
      set(value) {
        this.text_internal = value;
        // Todo: Remove this when spa is live
        this.setFilterValue("query", this.text_internal, true);
        // Todo: Use this when spa is live
        // this.setFilterValue({ filterName: 'query', filterValue: this.text_internal, notify: true })
      },
    },
  },
  methods: {
    clearInput() {
      this.value = "";
      this.isFocused = false;
    },
    isTrue(value) {
      // Handle `string booleans`
      if (typeof value == "string") {
        return value == "true";
      }
      return value;
    },
    onVisualizationInit() {
      const initial_value = this.getFilterValue("query");
      if (initial_value) {
        this.text_internal = initial_value;
      } else if (this.config.default_value) {
        this.text_internal = this.config.default_value;
      } else {
        return;
      }
      this.value = this.text_internal;
      // Todo: Remove this when spa is live
      this.setFilterValue("query", this.text_internal, true);
      // Todo: Use this when spa is live
      // this.setFilterValue({ filterName: 'query', filterValue: this.text_internal, notify: true })
    },
  },
};
</script>
