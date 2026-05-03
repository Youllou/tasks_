const TOKEN_KEY = 'taskapp_token'
const USER_KEY = 'taskapp_user'

export const useAuth = () => {
    const token = useState<string | null>('auth_token', () => {
        if (process.client) return localStorage.getItem(TOKEN_KEY)
        return null
    })

    const user = useState<{ id: string; email: string } | null>('auth_user', () => {
        if (process.client) {
            const stored = localStorage.getItem(USER_KEY)
            return stored ? JSON.parse(stored) : null
        }
        return null
    })

    const isAuthenticated = computed(() => !!token.value)

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

    return { token, user, isAuthenticated, setAuth, logout }
}
