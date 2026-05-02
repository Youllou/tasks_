import { defineStore } from 'pinia'

export interface Tag {
    id: string
    name: string
}

export interface Task {
    id: string
    user_id: string
    title: string
        description?: string
    status: 'inbox' | 'backlog' | 'todo' | 'done'
    due_date?: string
    project_id?: string
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
    const tags = ref<Tag[]>([])
    const projects = ref<Project[]>([])
    const loading = ref(false)
    const error = ref<string | null>(null)

    // Filters
    const filterStatus = ref<string | null>(null)
    const filterTag = ref<string | null>(null)
    const filterProject = ref<string | null>(null)
    const searchQuery = ref('')

    const api = useApi()

    const fetchTasks = async () => {
        loading.value = true
        error.value = null
        try {
            const params = new URLSearchParams()
            if (filterStatus.value) params.set('status', filterStatus.value)
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

    const tasksByStatus = computed(() => {
        const groups: Record<string, Task[]> = {
            inbox: [],
            backlog: [],
            todo: [],
            done: [],
        }
        for (const task of tasks.value) {
            groups[task.status]?.push(task)
        }
        return groups
    })

    return {
        tasks, tags, projects, loading, error,
        filterStatus, filterTag, filterProject, searchQuery,
        tasksByStatus,
        fetchTasks, fetchTags, fetchProjects,
        createTask, updateTask, deleteTask,
        createTag, createProject,
    }
})
