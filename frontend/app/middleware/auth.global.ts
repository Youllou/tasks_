export default defineNuxtRouteMiddleware(async (to) => {
    const { isAuthenticated, isInitialized, initializeFromStorage } = useAuth()

    // Initialize auth from storage on first load if not already done
    if (!isInitialized.value) {
        initializeFromStorage()
    }

    // Allow access to auth pages without authentication
    if (to.path === '/login' || to.path === '/signup') {
        if (isAuthenticated.value) {
            return navigateTo('/')
        }
        return
    }

    // For protected pages, only redirect if we're sure there's no token
    if (!isAuthenticated.value) {
        return navigateTo('/login')
    }
})
