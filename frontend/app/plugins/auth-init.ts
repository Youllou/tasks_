export default defineNuxtPlugin(async (nuxtApp) => {
  const { token, isInitialized, initializeFromStorage, clearAuth } = useAuth()

  // Initialize from localStorage
  initializeFromStorage()

  // If we have a token on initial load, verify it (optional)
  if (token.value && isInitialized.value) {
    try {
      const api = useApi()

      // Try to verify token (optional - only if endpoint exists)
      try {
        await api.get('/auth/verify')
        // Token is valid, we're good
      } catch (verifyError: any) {
        // If it's 401 Unauthorized, clear the token
        if (verifyError.message?.includes('401')) {
          console.warn('Token is unauthorized, clearing auth')
          clearAuth()
        }
        // For other errors (404, network), continue anyway - let the page handle it
      }
    } catch (e: any) {
      console.error('Unexpected error during auth init:', e.message)
    }
  }
})



