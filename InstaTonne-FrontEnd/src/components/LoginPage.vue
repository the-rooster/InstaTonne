<template>
  <div
    class="viewBox"
  >
    <v-progress-circular
      v-if="loading"
      indeterminate
      width="20"
      size="200"
      style="margin: 10em;"
    />
    <div v-else>
      <div style="display: flex; align-items: center; justify-content: center; padding-top: 10em;">
        <img
          src="../assets/EpicLogo.svg"
          style="width: 9em; padding: 2em;"
        >
        <h1>
          InstaTonne
        </h1>
      </div>
      <div style="width: 40%; transform: translateX(80%); display: flex; flex-direction: column;">
        <v-text-field
          v-model="username"
          label="Username"
        />
        <v-text-field
          v-model="password"
          label="Password"
          :type="showPassword ? 'text' : 'password'"
          :append-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
          hint="At least 8 characters"
          @click:append="showPassword = !showPassword"
        />
        <div v-if="registerMode">
          <v-text-field
            v-model="confirmPassword"
            label="Confirm Password"
            :type="showConfirmPassword ? 'text' : 'password'"
            :append-icon="showConfirmPassword ? 'mdi-eye' : 'mdi-eye-off'"
            @click:append="showConfirmPassword = !showConfirmPassword"
          />
          <div v-if="!passwordsMatch">
            Passwords must match
          </div>
        </div>
        <div>
          <v-btn
            class="button"
            :disabled="!canLogin"
            @click="registerMode ? register() : login()"
          >
            {{ registerMode ? "Sign Up" : "Login" }}
          </v-btn>
        </div>
        <div>
          <v-btn
            class="button"
            @click="registerMode = !registerMode"
          >
            {{ registerMode ? "Return To Login" : "Register" }}
          </v-btn>
        </div>
        <div>Debug Info:</div>
        <div>{{ responseData }}</div>
        <v-btn
          class="button"
          @click="() => $emit('LoggedIn', true)"
        >
          FORCE LOGIN
        </v-btn>
      </div>
    </div>
  </div>
</template>
    
  <script setup lang="ts">
  import { ref, onBeforeMount, computed } from 'vue'
//   import AuthorCard from './AuthorCard.vue'
  import createHTTP from '../axiosCalls'

  defineEmits(["LoggedIn"])

  const username = ref("")

  const registerMode = ref(false)

  const showPassword = ref(false)
  const showConfirmPassword = ref(false)
  const password = ref("")
  const confirmPassword = ref("")

  const passwordsMatch = computed(() => password.value == confirmPassword.value)

  //TEMP
  const responseData = ref({})

  const canLogin = computed(() => 
    (!registerMode.value || passwordsMatch.value) &&
    password.value.length >= 8 && username.value.length > 0)

  async function login() {
    loading.value = true;
    // await createHTTP('login/').post('').then((response: { data: object }) => {
    const credentials = {
        username: 'username1',
        password: 'password1'
    }
    await createHTTP('login/').post(JSON.stringify(credentials)).then((response: { data: object }) => {
        responseData.value = document.cookie;
      loading.value = false;
    });
    return
  }

  async function register() {
    loading.value = true;
    // await createHTTP('login/').post('').then((response: { data: object }) => {
    await createHTTP('authors/1/posts/1/').get().then((response: { data: object }) => {
        responseData.value = response.data;
      loading.value = false;
    });
    return
  }


  
  const loading = ref(true)
  const postData = ref({});
  onBeforeMount(async () => {
    await createHTTP('authors/1/posts/1/').get().then((response: { data: object }) => {
      postData.value = response.data;
      loading.value = false;
    });
  })
  
  </script>
  
  <style scoped>
  .button {
    width: 50%;
  }
  </style>
    