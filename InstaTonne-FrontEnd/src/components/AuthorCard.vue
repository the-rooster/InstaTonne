<template>

<v-card
  :elevation="10"
  class="authorBox"
>
    {{ props.authorInfo?.displayName }}

    <v-card-item>
      <img
        v-if="props.authorInfo?.profileImage"
        :src="props.authorInfo?.profileImage"
        class="profile-picture"
      >
      <img
        v-else
        class="profile-picture"
        src="../assets/EpicLogo.svg"
      >
    </v-card-item>

</v-card>
</template>
    
<script setup lang="ts">
import { ref } from 'vue';


const props = defineProps({
authorInfo: {
    type: Object,
    required: true
}
})


</script>

<style scoped>
.authorBox {
    width: 20vw;
    height: 20vh;
    background-color: rgb(214, 227, 222);
    justify-content: center;
}
.profile-picture {
  width: 60%;
  height: 60%;

  border-radius: 100%;
}
</style>
    