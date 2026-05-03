<script setup lang="ts">
import type { Task } from '~/stores/tasks'

const store = useTaskStore()
const { user, logout } = useAuth()
const router = useRouter()

const showModal = ref(false)
const editingTask = ref<Task | null>(null)
const quickInput = ref('')
const searchInput = ref('')
const isInitializing = ref(true)
const loadError = ref<string | null>(null)

const reloadPage = () => {
  if (typeof window !== 'undefined') {
    window.location.reload()
  }
}

onMounted(async () => {
  try {
    // Check if we need to load data (in case we're reconnecting)
    if (store.columns.length === 0 || store.tasks.length === 0) {
      await Promise.all([
        store.fetchColumns(),
        store.fetchTasks(),
        store.fetchTags(),
        store.fetchProjects()
      ])
    }
  } catch (error: any) {
    loadError.value = error.message || 'Failed to load data'
    console.error('Error loading data:', error)
  } finally {
    isInitializing.value = false
  }
})

const openCreate = () => {
  editingTask.value = null
  showModal.value = true
}

const openEdit = (task: Task) => {
  editingTask.value = task
  showModal.value = true
}

const quickCreate = async () => {
  const title = quickInput.value.trim()
  if (!title) return
  // column_id omitted — service falls back to inbox
  await store.createTask({ title })
  quickInput.value = ''
}

let searchTimer: ReturnType<typeof setTimeout>
const onSearch = () => {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    store.searchQuery = searchInput.value
    store.fetchTasks()
  }, 300)
}

const clearFilters = () => {
  store.clearFilters()
  searchInput.value = ''
  store.fetchTasks()
}

const isKanban = computed(() => !store.hasFilters)

const onDragOver = (e: DragEvent) => {
  e.preventDefault()
  e.dataTransfer!.dropEffect = 'move'
}

const onDrop = async (e: DragEvent, columnId: string) => {
  e.preventDefault()
  const taskId = e.dataTransfer!.getData('task-id')
  if (!taskId) return

  const task = store.tasks.find(t => t.id === taskId)
  if (task && task.column_id !== columnId) {
    await store.updateTask(taskId, { column_id: columnId })
  }
}
</script>

<template>
  <ClientOnly>
    <div class="min-h-screen bg-surface-0 flex flex-col">
      <div class="fixed inset-0 pointer-events-none opacity-50" style="background-image: linear-gradient(rgba(245,245,0,0.02) 1px, transparent 1px), linear-gradient(90deg, rgba(245,245,0,0.02) 1px, transparent 1px); background-size: 40px 40px;" />

    <div class="flex flex-1 relative z-10 overflow-hidden" style="height: 100vh">
      <AppSidebar class="hidden md:flex" />

      <div class="flex-1 flex flex-col overflow-hidden">
        <!-- Top bar -->
        <header class="border-b border-border px-4 py-3 flex items-center gap-3 shrink-0">
          <div class="flex-1 flex items-center gap-2 max-w-lg">
            <span class="font-mono text-accent text-sm shrink-0">›</span>
            <input
                v-model="quickInput"
                class="bg-transparent text-ink text-sm flex-1 focus:outline-none placeholder:text-ink-muted font-sans"
                placeholder="Quick capture — press Enter to add to inbox"
                @keyup.enter="quickCreate"
            />
          </div>

          <div class="flex items-center gap-2 border border-border px-3 py-1.5">
            <span class="text-ink-muted text-xs font-mono">⌕</span>
            <input
                v-model="searchInput"
                @input="onSearch"
                class="bg-transparent text-ink text-xs flex-1 focus:outline-none placeholder:text-ink-muted w-36"
                placeholder="Search tasks..."
            />
          </div>

          <button @click="openCreate" class="btn-primary hidden sm:flex items-center gap-1.5">
            <span>+</span> New task
          </button>

          <div class="flex items-center gap-2 border-l border-border pl-3">
            <span class="font-mono text-xs text-ink-muted hidden sm:block">{{ user?.email }}</span>
            <button @click="logout" class="btn-ghost text-xs py-1 px-2">logout</button>
          </div>
        </header>

        <!-- Filter strip -->
        <div v-if="store.hasFilters" class="border-b border-border px-4 py-2 flex items-center gap-3">
          <span class="font-mono text-xs text-ink-muted">Filtering by:</span>
          <span v-if="store.filterColumnId" class="font-mono text-xs text-accent bg-accent/10 px-2 py-0.5">
            {{ store.columns.find(c => c.id === store.filterColumnId)?.name }}
          </span>
          <span v-if="store.filterTag" class="font-mono text-xs text-accent bg-accent/10 px-2 py-0.5">#{{ store.filterTag }}</span>
          <span v-if="store.filterProject" class="font-mono text-xs text-accent bg-accent/10 px-2 py-0.5">project</span>
          <span v-if="store.searchQuery" class="font-mono text-xs text-accent bg-accent/10 px-2 py-0.5">search: "{{ store.searchQuery }}"</span>
          <button @click="clearFilters" class="font-mono text-xs text-ink-muted hover:text-ink ml-auto">✕ clear</button>
        </div>

        <!-- Content -->
        <div class="flex-1 overflow-y-auto overflow-x-auto">
          <!-- Error state -->
          <div v-if="loadError" class="flex items-center justify-center h-full">
            <div class="text-center p-6">
              <div class="text-red-400 font-mono text-sm mb-4">✗ Error</div>
              <div class="text-ink-muted text-xs font-mono mb-4">{{ loadError }}</div>
              <button @click="reloadPage" class="btn-primary text-xs">Reload</button>
            </div>
          </div>

          <!-- Loading state during initialization -->
          <div v-else-if="isInitializing" class="flex items-center justify-center h-full">
            <div class="text-center">
              <div class="font-mono text-xs text-ink-muted animate-pulse mb-2">connecting...</div>
              <div class="w-8 h-8 border-2 border-accent border-t-transparent rounded-full animate-spin mx-auto" />
            </div>
          </div>

          <!-- Content after initialization -->
          <div v-else-if="store.loading" class="flex items-center justify-center h-32">
            <span class="font-mono text-xs text-ink-muted animate-pulse">loading tasks...</span>
          </div>

          <!-- Kanban view — columns driven by store -->
          <div
              v-else-if="isKanban"
              class="inline-grid gap-0 border-b border-border min-w-full"
              :style="{ gridTemplateColumns: `repeat(${store.columns.length}, minmax(350px, 1fr))` }"
          >
            <div
                v-for="col in store.columns"
                :key="col.id"
                class="border-r border-border last:border-r-0 min-h-[calc(100vh-120px)]"
                @dragover="onDragOver"
                @drop="onDrop($event, col.id)"
            >
              <div class="sticky top-0 z-10 bg-surface-0/90 backdrop-blur-sm border-b border-border px-4 py-2.5 flex items-center justify-between">
                <span class="flex items-center gap-2">
                  <span class="w-1.5 h-1.5 rounded-full" :style="{ backgroundColor: col.color }" />
                  <span class="font-mono text-xs uppercase tracking-widest text-ink-muted">{{ col.name }}</span>
                </span>
                <span class="font-mono text-xs text-ink-muted">{{ store.tasksByColumn[col.id]?.length || 0 }}</span>
              </div>

              <div class="divide-y divide-border/50">
                <TaskCard
                    v-for="task in store.tasksByColumn[col.id]"
                    :key="task.id"
                    :task="task"
                    :columns="store.columns"
                    :projects="store.projects"
                    @edit="openEdit"
                />
                <div v-if="!store.tasksByColumn[col.id]?.length" class="px-4 py-8 text-center">
                  <span class="font-mono text-xs text-ink-muted">empty</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Flat list view (when filtering) -->
          <div v-else class="divide-y divide-border/50 max-w-3xl">
            <TaskCard
                v-for="task in store.sortedTasks"
                :key="task.id"
                :task="task"
                :columns="store.columns"
                :projects="store.projects"
                @edit="openEdit"
            />
            <div v-if="!store.tasks.length" class="p-12 text-center">
              <span class="font-mono text-xs text-ink-muted">no tasks found</span>
            </div>
          </div>
        </div>

        <!-- Mobile FAB -->
        <button
            @click="openCreate"
            class="sm:hidden fixed bottom-6 right-6 w-12 h-12 bg-accent text-surface-0 font-mono text-xl flex items-center justify-center shadow-lg"
        >+</button>
      </div>
    </div>

    <TaskModal
        :open="showModal"
        :task="editingTask"
        @close="showModal = false"
        @saved="store.fetchTasks()"
    />
  </div>
  </ClientOnly>
</template>