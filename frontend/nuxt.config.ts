// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss', '@pinia/nuxt'],
  css: ['~/assets/css/main.css'],
  runtimeConfig: {
    public: {
        apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://192.168.1.143:8008'
    }
  },
  routeRules: {
    // Only SSR login/signup pages, disable for protected routes
    '/login': { ssr: true },
    '/signup': { ssr: true },
    '/**': { ssr: false } // Disable SSR for all other routes (they need auth)
  },
  app: {
    head: {
        title: 'Tasks_',
        link: [
            { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
            { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
            {
                rel: 'stylesheet',
                href: 'https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=DM+Sans:wght@300;400;500;600&display=swap'
            }
        ]
    }
  }
})