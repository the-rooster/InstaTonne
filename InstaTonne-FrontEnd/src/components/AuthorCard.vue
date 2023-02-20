<template>
  <v-card
    :elevation="10"
    class="authorBox"
  >
    <template #title>
      <a
        :href="props.authorInfo.url"
        style="font-size: 1.25em;"
      >
        {{ props.authorInfo.displayName }}
      </a>
    </template>
    <v-card-item>
      <img
        v-if="props.authorInfo.profileImage"
        :src="props.authorInfo.profileImage"
        class="pfp"
      >
      <img
        v-else
        class="pfp"
        src="../assets/EpicLogo.svg"
      >
    </v-card-item>
    <v-card-item>
      <a
        :href="props.authorInfo.github"
      >
        (github)
      </a>
    </v-card-item>
  </v-card>
</template>
    
<script setup lang="ts">

const props = defineProps({
authorInfo: {
    type: Object,
    required: true
}
})

</script>

<style scoped>
.authorBox {
    width: 10em;
    height: 15em;
    background-color: aquamarine;
}
.pfp {
    width: 7em;
    height: 7em;
}
</style>
    