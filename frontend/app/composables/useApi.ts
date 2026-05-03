export const useApi = () => {
    const config = useRuntimeConfig()
    const { token } = useAuth()

    const request = async <T>(
        path: string,
        options: RequestInit = {}
    ): Promise<T> => {
        const headers: Record<string, string> = {
            'Content-Type': 'application/json',
            ...(options.headers as Record<string, string> || {})
        }

        if (token.value) {
            headers['Authorization'] = `Bearer ${token.value}`
        }

        const res = await fetch(`${config.public.apiBase}${path}`, {
            ...options,
            headers,
        })

        if (!res.ok) {
            const err = await res.json().catch(() => ({ detail: 'Request failed' }))
            throw new Error(err.detail || 'Request failed')
        }

        if (res.status === 204) return undefined as T
        return res.json()
    }

    return {
        get: <T>(path: string) => request<T>(path),
        post: <T>(path: string, body: unknown) =>
            request<T>(path, { method: 'POST', body: JSON.stringify(body) }),
        patch: <T>(path: string, body: unknown) =>
            request<T>(path, { method: 'PATCH', body: JSON.stringify(body) }),
        delete: (path: string) => request<void>(path, { method: 'DELETE' }),
    }
}
