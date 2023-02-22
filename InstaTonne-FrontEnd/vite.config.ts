import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import eslint from 'vite-plugin-eslint'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), eslint()],
  resolve: {
    alias: {
      vue: "vue/dist/vue.esm-bundler.js"
    }
  },
  server: {
    proxy: {
      '/service': {
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
