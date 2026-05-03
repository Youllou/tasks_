import type { Config } from 'tailwindcss'

export default {
    content: [
        './components/**/*.{js,vue,ts}',
        './layouts/**/*.vue',
        './pages/**/*.vue',
        './plugins/**/*.{js,ts}',
        './app.vue',
    ],
    theme: {
        extend: {
            fontFamily: {
                mono: ['IBM Plex Mono', 'monospace'],
                sans: ['DM Sans', 'sans-serif'],
            },
            colors: {
                surface: {
                    0: '#0a0a0b',
                    1: '#111113',
                    2: '#18181b',
                    3: '#222226',
                    4: '#2c2c32',
                },
                border: {
                    DEFAULT: '#2c2c32',
                    subtle: '#1e1e23',
                    bright: '#3f3f47',
                },
                accent: {
                    DEFAULT: '#f5f500',
                    dim: '#c4c400',
                    muted: 'rgba(245,245,0,0.1)',
                },
                ink: {
                    DEFAULT: '#e8e8e8',
                    dim: '#a0a0a8',
                    muted: '#5a5a64',
                },
                status: {
                    inbox: '#4a9eff',
                    backlog: '#8b8b9a',
                    todo: '#f5a623',
                    done: '#4caf50',
                }
            },
            animation: {
                'slide-up': 'slideUp 0.2s ease-out',
                'fade-in': 'fadeIn 0.15s ease-out',
            },
            keyframes: {
                slideUp: {
                    '0%': { transform: 'translateY(8px)', opacity: '0' },
                    '100%': { transform: 'translateY(0)', opacity: '1' },
                },
                fadeIn: {
                    '0%': { opacity: '0' },
                    '100%': { opacity: '1' },
                }
            }
        },
    },
    plugins: [],
} satisfies Config