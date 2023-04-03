<template>
  <v-dialog
    v-model="show"
    width="auto"
  >
    <v-card>
      <v-card-text>
        {{ props.message }}
      </v-card-text>
      <v-card-actions
        class="justify-center"
      >
        <v-btn
          @click="sendUpdate(false)"
        >
          Cancel
        </v-btn>
        <v-btn
          @click="sendUpdate(true)"
        >
          Confirm
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
  
<script setup lang="ts">
import { ref } from "vue";

const props = defineProps({
    message: {
        type: String,
        required: true
    }
});

const show = ref(false)

defineExpose({ show })

const emit = defineEmits(["selected"])

const sendUpdate = (value: boolean) => {
    emit("selected", value)
}

</script>

<style scoped>
</style>
