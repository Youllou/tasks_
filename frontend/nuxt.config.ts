// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  site: {
    url: 'https://tasks.youllu.com',
    name: 'Tasks_',
  },
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss', '@pinia/nuxt', '@nuxtjs/robots', '@nuxtjs/sitemap', 'nuxt-og-image'],
  css: ['~/assets/css/main.css'],
  runtimeConfig: {
    public: {
        apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://192.168.1.106:8008'
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
            },
            {
                rel: 'icon',
                href: '/icon-16x16.png',
                sizes:'16x16'
            },
            {
                rel: 'icon',
                href: '/icon-32x32.png',
                sizes:'32x32'
            },
            {
                rel: 'icon',
                href: '/icon-192x192.png',
                sizes:'192x192'
            },
            {
                rel: 'icon',
                href: '/icon-512x512.png',
                sizes:'512x512'
            },
            {
                rel: 'apple-touch-icon',
                href: '/apple-touch-icon.png',
                sizes: '180x180'
            }
        ]
    }
  }
})