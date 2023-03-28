<style>
.viewBox {
  width: 80%;
  margin: 0 auto;
  margin-top: 20;
  text-align: center;
  background-color: #f9f9f9;
  padding: 2rem;
  border-radius: 10pt;
  font-family: Arial, sans-serif;
  color: #333;
}

.viewBox h1 {
  font-size: 2.5rem;
  color: #4a90e2;
  margin-bottom: 1rem;
}

.viewBox p {
  font-size: 1.1rem;
  line-height: 1.5;
  max-width: 90%;
  margin: 0 auto;
  margin-bottom: 1.5rem;
}

.viewBox a {
  color: #4a90e2;
  text-decoration: none;
}

.viewBox a:hover {
  text-decoration: underline;
}

.viewBox strong {
  font-size: 1.2rem;
  font-weight: bold;
}

.viewBox p:last-child {
  margin-bottom: 0;
}
</style>
<template>
  <div class="viewBox">
    <h1>Welcome to InstaTonne!</h1>
    <p>
      InstaTonne is a revolutionary social networking app that embraces the
      interconnectedness and the web's peer-to-peer nature. Our aim is to
      provide users with more autonomy and choice while connecting them to
      various independent social networks without being limited to a single
      platform like Facebook, Instagram or Twitter.
    </p>
    <p>
      Inspired by
      <a href="https://diasporafoundation.org/" target="_blank">Diaspora</a>,
      InstaTonne offers a far simpler solution for users to share and discover
      content. Our platform allows the importing of posts from various sources
      like GitHub and other social networks. It also enables the distribution
      and sharing of posts and content across different servers.
    </p>
    <p>
      With InstaTonne, authors can aggregate their friends' posts from other
      servers, creating a seamless and interconnected experience. We utilize an
      inbox model for sharing, where you can send your posts directly to your
      friends, similar to the
      <a href="https://www.w3.org/TR/activitypub/" target="_blank"
        >ActivityPub</a
      >
      protocol. However, we've made it simpler and more accessible for everyday
      users.
    </p>
    <p>
      Our name, InstaTonne, is a playful nod to the popular platform Instagram,
      with the idea that we're a "tonne" better in terms of user control and
      freedom. Join us in redefining the social networking experience by taking
      control of your own content and connections.
    </p>
    <p>
      To learn more, check out our GitHub repository:
      <a href="https://github.com/the-rooster/InstaTonne" target="_blank"
        >InstaTonne</a
      >
    </p>
    <p>
      <strong>InstaTonne - Brought to you by CMPUT 404 W2023 Group 6</strong>
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

// defineProps<{ msg: string }>()

const count = ref(0);
</script>

<style scoped>
.read-the-docs {
  color: #888;
}
</style>
