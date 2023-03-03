<template>
    
    <div class="viewBox">
        <h1 style="fontSize:large">{{props.postData.title}}</h1>
        <p style="fontSize:large;font-weight:bold">By: {{props.postData.author.displayName}}</p>
        <br>
        <p>{{props.postData.author.url}}</p>
        <p>{{ props.postData.description }}</p>
        <br><br>
        <p>{{ props.postData.content }}</p>
        <br>

        COMMENTS HERE
    </div>
</template>
  
<script setup lang="ts">

import { ref } from 'vue'
const props = defineProps({
postData: {
    type: Object,
    required: true
}
});



// defineProps<{ msg: string }>()

const count = ref(0)


</script>
  
<style scoped>
.read-the-docs {
color: #888;
}
</style>
  