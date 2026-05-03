<script setup lang="ts">
const config = useRuntimeConfig()
const { setAuth } = useAuth()
const router = useRouter()

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const mode = ref<'login' | 'signup'>('login')

const submit = async () => {
  if (!email.value || !password.value) return
  loading.value = true
  error.value = ''

  try {
    const endpoint = mode.value === 'login' ? '/auth/login' : '/auth/signup'
    const res = await fetch(`${config.public.apiBase}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: email.value, password: password.value })
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail || 'Auth failed')
    setAuth(data.access_token, data.user)
    router.push('/')
  } catch (e: any) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen bg-surface-0 flex items-center justify-center p-4">
    <!-- Grid background -->
    <div class="fixed inset-0 pointer-events-none" style="background-image: linear-gradient(rgba(245,245,0,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(245,245,0,0.03) 1px, transparent 1px); background-size: 40px 40px;" />

    <div class="w-full max-w-sm relative z-10">
      <!-- Logo -->
      <div class="mb-8">
        <div class="font-mono text-accent text-xs tracking-[0.3em] uppercase mb-1">System</div>
        <h1 class="font-mono text-2xl text-ink font-semibold tracking-tight">tasks<span class="text-accent">_</span></h1>
      </div>

      <!-- Card -->
      <div class="card p-6 animate-slide-up">
        <!-- Mode toggle -->
        <div class="flex border-b border-border mb-6">
          <button
              @click="mode = 'login'"
              class="font-mono text-xs tracking-widest uppercase px-0 py-3 mr-6 border-b-2 transition-colors"
              :class="mode === 'login' ? 'border-accent text-accent' : 'border-transparent text-ink-muted hover:text-ink-dim'"
          >login</button>
          <button
              @click="mode = 'signup'"
              class="font-mono text-xs tracking-widest uppercase px-0 py-3 border-b-2 transition-colors"
              :class="mode === 'signup' ? 'border-accent text-accent' : 'border-transparent text-ink-muted hover:text-ink-dim'"
          >signup</button>
        </div>

        <form @submit.prevent="submit" class="space-y-3">
          <div>
            <label class="font-mono text-xs text-ink-muted uppercase tracking-wider block mb-1.5">Email</label>
            <input
                v-model="email"
                type="email"
                autocomplete="email"
                placeholder="you@example.com"
                class="input-field"
                required
            />
          </div>

          <div>
            <label class="font-mono text-xs text-ink-muted uppercase tracking-wider block mb-1.5">Password</label>
            <input
                v-model="password"
                type="password"
                autocomplete="current-password"
                placeholder="••••••••"
                class="input-field"
                required
            />
          </div>

          <div v-if="error" class="text-red-400 font-mono text-xs py-1">
            ✗ {{ error }}
          </div>

          <button type="submit" :disabled="loading" class="btn-primary w-full mt-2 flex items-center justify-center gap-2">
            <span v-if="loading" class="font-mono text-xs">loading...</span>
            <span v-else>{{ mode === 'login' ? 'Login' : 'Create account' }}</span>
          </button>
        </form>
      </div>

      <p class="font-mono text-xs text-ink-muted text-center mt-6">
        Personal task management system
      </p>
    </div>
  </div>
</template>
