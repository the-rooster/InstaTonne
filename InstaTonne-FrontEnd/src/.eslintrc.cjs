module.exports = {
    extends: [
      // add more generic rulesets here, such as:
      'eslint:recommended',
      'plugin:vue/vue3-recommended',
      'plugin:@typescript-eslint/recommended',
      '@vue/eslint-config-typescript',
    ],
    parser: "vue-eslint-parser",
    rules: {
      // override/add rules settings here, such as:
      // 'vue/no-unused-vars': 'error'
    }
  }