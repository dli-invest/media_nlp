import { defineConfig } from 'astro/config';
  import react from '@astrojs/react';
  import vue from '@astrojs/vue';
// https://astro.build/config
export default defineConfig({
  // site
  integrations: [
    react(),
    vue(),
  ],
  build: {
    site: "https://dli-invest.github.io/media_nlp"
  }
});