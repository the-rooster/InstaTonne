<template>
  <div
    class="viewBox"
  >
    {{ props.errorMessage }}
  </div>
</template>

<script setup lang="ts">

const props = defineProps({
errorMessage: {
    type: String,
    default: "404 Page Not Found"
}
})

</script>

<style scoped>
</style>
    