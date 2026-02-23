import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
    plugins: [vue()],
    server: {
        port: 8080,
        proxy: {
            '^/(api|assets|files|private)': {
                target: 'http://127.0.0.1:8000',
                changeOrigin: true,
                ws: true,
            }
        }
    },
    build: {
        outDir: '../order_picking/public/frontend',
        emptyOutDir: true,
        target: 'es2015',
    }
});
