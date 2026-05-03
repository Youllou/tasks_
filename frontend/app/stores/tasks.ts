import { defineStore } from 'pinia'

export interface Tag {
    id: string
    name: string
}

export interface Column {
    id: string
    name: string
    color: string
    position: number
    is_inbox: boolean
}

export interface Task {
    id: string
    user_id: string
    column_id: string
    project_id?: string
    title: string
    description?: string
    due_date?: string
    tags: Tag[]
    created_at: string
    updated_at: string
}

export interface Project {
    id: string
    name: string
}

export const useTaskStore = defineStore('tasks', () => {
    const tasks = ref<Task[]>([])
    const columns = ref<Column[]>([])
    const tags = ref<Tag[]>([])
    const projects = ref<Project[]>([])
    const loading = ref(false)
    const error = ref<string | null>(null)

    // Filters
    const filterColumnId = ref<string | null>(null)
    const filterTag = ref<string | null>(null)
    const filterProject = ref<string | null>(null)
    const searchQuery = ref('')

    const api = useApi()

    const fetchTasks = async () => {
        loading.value = true
        error.value = null
        try {
            const params = new URLSearchParams()
            if (filterColumnId.value) params.set('column_id', filterColumnId.value)
            if (filterTag.value) params.set('tag', filterTag.value)
            if (filterProject.value) params.set('project_id', filterProject.value)
            if (searchQuery.value) params.set('search', searchQuery.value)
            const qs = params.toString()
            tasks.value = await api.get<Task[]>(`/tasks${qs ? '?' + qs : ''}`)
        } catch (e: any) {
            error.value = e.message
        } finally {
            loading.value = false
        }
    }

    const fetchColumns = async () => {
        columns.value = await api.get<Column[]>('/columns')
    }

    const fetchTags = async () => {
        tags.value = await api.get<Tag[]>('/tags')
    }

    const fetchProjects = async () => {
        projects.value = await api.get<Project[]>('/projects')
    }

    const createTask = async (data: Partial<Task> & { tag_ids?: string[] }) => {
        const task = await api.post<Task>('/tasks', data)
        tasks.value.unshift(task)
        return task
    }

    const updateTask = async (id: string, data: Partial<Task> & { tag_ids?: string[] }) => {
        const updated = await api.patch<Task>(`/tasks/${id}`, data)
        const idx = tasks.value.findIndex(t => t.id === id)
        if (idx !== -1) tasks.value[idx] = updated
        return updated
    }

    const deleteTask = async (id: string) => {
        await api.delete(`/tasks/${id}`)
        tasks.value = tasks.value.filter(t => t.id !== id)
    }

    const createTag = async (name: string) => {
        const tag = await api.post<Tag>('/tags', { name })
        tags.value.push(tag)
        return tag
    }

    const createProject = async (name: string) => {
        const project = await api.post<Project>('/projects', { name })
        projects.value.push(project)
        return project
    }

    // Tasks grouped by column_id, ordered by column position, sorted by due date
    const tasksByColumn = computed(() => {
        const groups: Record<string, Task[]> = {}
        for (const col of columns.value) {
            groups[col.id] = []
        }
        for (const task of tasks.value) {
            if (groups[task.column_id]) {
                groups[task.column_id].push(task)
            }
        }

        // Sort each column's tasks by due date (earliest first, tasks without due date last)
        for (const colId in groups) {
            groups[colId].sort((a, b) => {
                // Tasks with no due date go to the bottom
                if (!a.due_date && !b.due_date) return 0
                if (!a.due_date) return 1
                if (!b.due_date) return -1

                // Sort by due date ascending (earliest first)
                return new Date(a.due_date).getTime() - new Date(b.due_date).getTime()
            })
        }

        return groups
    })

    const inboxColumn = computed(() => columns.value.find(c => c.is_inbox) ?? null)

    // Sorted tasks for flat list view (when filtering)
    const sortedTasks = computed(() => {
        return [...tasks.value].sort((a, b) => {
            // Tasks with no due date go to the bottom
            if (!a.due_date && !b.due_date) return 0
            if (!a.due_date) return 1
            if (!b.due_date) return -1

            // Sort by due date ascending (earliest first)
            return new Date(a.due_date).getTime() - new Date(b.due_date).getTime()
        })
    })

    const hasFilters = computed(() =>
        !!filterColumnId.value || !!filterTag.value || !!filterProject.value || !!searchQuery.value
    )

    const clearFilters = () => {
        filterColumnId.value = null
        filterTag.value = null
        filterProject.value = null
        searchQuery.value = ''
    }

    return {
        tasks, columns, tags, projects, loading, error,
        filterColumnId, filterTag, filterProject, searchQuery,
        tasksByColumn, sortedTasks, inboxColumn, hasFilters,
        fetchTasks, fetchColumns, fetchTags, fetchProjects,
        createTask, updateTask, deleteTask,
        createTag, createProject,
        clearFilters,
    }
})