import { configDefaults, defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'
import eslint from 'vite-plugin-eslint'
import vuetify from "vite-plugin-vuetify";

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
  server: {
    proxy: {
      'http://localhost:8000/': {
        target: 'http://localhost:8000/',
        changeOrigin: true,
        // rewrite: (path) => path.replace(/^\/service/, ''),
        secure: false,
        // ws: false
      },
    },
    headers: {
      
    },
    cors: {
      origin: 'http://localhost:8000/'
    }
  }
})
