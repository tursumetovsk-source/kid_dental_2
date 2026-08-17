import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  build: {
    outDir: 'dist',
    assetsInlineLimit: 0, // Keep SVGs and images as clean files
  },
  plugins: [
    {
      name: 'copy-static-and-assets-dir',
      closeBundle() {
        const fs = require('fs');
        const path = require('path');

        function copyDir(src, dest) {
          if (!fs.existsSync(src)) return;
          fs.mkdirSync(dest, { recursive: true });
          for (const item of fs.readdirSync(src)) {
            const s = path.join(src, item);
            const d = path.join(dest, item);
            if (fs.statSync(s).isDirectory()) {
              copyDir(s, d);
            } else {
              fs.copyFileSync(s, d);
            }
          }
        }

        // Copy static folder to dist/static
        copyDir(resolve(__dirname, 'static'), resolve(__dirname, 'dist/static'));
        // Copy original assets to dist/assets to ensure all hash variants and static names exist
        copyDir(resolve(__dirname, 'assets'), resolve(__dirname, 'dist/assets'));
      }
    }
  ]
});
