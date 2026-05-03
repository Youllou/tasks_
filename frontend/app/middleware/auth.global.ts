export default defineNuxtRouteMiddleware((to) => {
    const { isAuthenticated } = useAuth()

    if (!isAuthenticated.value && to.path !== '/login' && to.path !== '/signup') {
        return navigateTo('/login')
    }

    if (isAuthenticated.value && (to.path === '/login' || to.path === '/signup')) {
        return navigateTo('/')
    }
})
