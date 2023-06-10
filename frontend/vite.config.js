import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import WindiCSS from 'vite-plugin-windicss'
import path from 'path' 
import vueJsx from '@vitejs/plugin-vue-jsx';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(),WindiCSS(),vueJsx()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname,"src") // + 
    }
  },
  server: {
    proxy: {
        '/api': {
          // target: 'http://ceshi13.dishait.cn',
          target: 'http://10.11.19.247:8001',
          // target: 'http://127.0.0.1:8000',
          changeOrigin: true,
          ws: true,
          rewrite: (path) => path.replace(/^\/api/, ''),
        },
    }
  },
})
