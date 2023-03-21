import { configDefaults, defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'
import eslint from 'vite-plugin-eslint'
import vuetify from "vite-plugin-vuetify";

let backend_url ="https://cmput404-group6-instatonne.herokuapp.com"; //http://127.0.0.1:8000";//"https://instatonne-cmput404.herokuapp.com";

let server = {};

server["proxy"] = {};
server["proxy"][backend_url] = {
  target: backend_url,
  changeOrigin: true,
  // rewrite: (path) => path.replace(/^\/service/, ''),
  secure: false,
  // ws: false
};
server["headers"] = {};
server["cors"] = {};
server["cors"]["origin"] = backend_url;

// https://vitejs.dev/config/
export default defineConfig({
  test: {
    exclude: [...configDefaults.exclude, 'packages/template/*'],
    globals: true,
    environment: "jsdom",
    // setupFiles: './vuetify.config.ts',
    deps: {
      inline: ["vuetify"],
    },
  },
  plugins: [vue(), eslint()],
  resolve: {
    alias: {
      vue: "vue/dist/vue.esm-bundler.js"
    }
  },
  server: server
})