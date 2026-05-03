const TOKEN_KEY = 'taskapp_token'
const USER_KEY = 'taskapp_user'

export const useAuth = () => {
    const token = useState<string | null>('auth_token', () => null)
    const user = useState<{ id: string; email: string } | null>('auth_user', () => null)
    const isInitialized = useState<boolean>('auth_initialized', () => false)

    const isAuthenticated = computed(() => !!token.value)

    // Initialize from localStorage on client side
    const initializeFromStorage = () => {
        if (process.client && !isInitialized.value) {
            const storedToken = localStorage.getItem(TOKEN_KEY)
            const storedUser = localStorage.getItem(USER_KEY)

            if (storedToken) {
                token.value = storedToken
            }
            if (storedUser) {
                try {
                    user.value = JSON.parse(storedUser)
                } catch (e) {
                    console.error('Failed to parse stored user:', e)
                    localStorage.removeItem(USER_KEY)
                }
            }

            isInitialized.value = true
        }
    }

    const setAuth = (accessToken: string, userData: { id: string; email: string }) => {
        token.value = accessToken
        user.value = userData
        if (process.client) {
            localStorage.setItem(TOKEN_KEY, accessToken)
            localStorage.setItem(USER_KEY, JSON.stringify(userData))
        }
    }

    const logout = () => {
        token.value = null
        user.value = null
        if (process.client) {
            localStorage.removeItem(TOKEN_KEY)
            localStorage.removeItem(USER_KEY)
        }
        navigateTo('/login')
    }

    const clearAuth = () => {
        token.value = null
        user.value = null
        if (process.client) {
            localStorage.removeItem(TOKEN_KEY)
            localStorage.removeItem(USER_KEY)
        }
    }

    return { token, user, isAuthenticated, isInitialized, setAuth, logout, clearAuth, initializeFromStorage }
}
