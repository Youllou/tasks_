<script setup lang="ts">
import type { Task } from '~/stores/tasks'

const props = defineProps<{
  task?: Task | null
  open: boolean
}>()

const emit = defineEmits<{
  close: []
  saved: []
}>()

const store = useTaskStore()

const form = ref({
  title: '',
  description: '',
  status: 'inbox' as Task['status'],
  due_date: '',
  project_id: '',
  tag_ids: [] as string[],
})

const error = ref('')
const saving = ref(false)

watch(() => props.open, (open) => {
  if (open) {
    if (props.task) {
      form.value = {
        title: props.task.title,
        description: props.task.description || '',
        status: props.task.status,
        due_date: props.task.due_date ? props.task.due_date.slice(0, 10) : '',
        project_id: props.task.project_id || '',
        tag_ids: props.task.tags.map(t => t.id),
      }
    } else {
      form.value = { title: '', description: '', status: 'inbox', due_date: '', project_id: '', tag_ids: [] }
    }
    error.value = ''
  }
}, { immediate: true })

const toggleTag = (id: string) => {
  const idx = form.value.tag_ids.indexOf(id)
  if (idx === -1) form.value.tag_ids.push(id)
  else form.value.tag_ids.splice(idx, 1)
}

const newTagName = ref('')
const addTag = async () => {
  if (!newTagName.value.trim()) return
  const tag = await store.createTag(newTagName.value.trim())
  form.value.tag_ids.push(tag.id)
  newTagName.value = ''
}

const newProjectName = ref('')
const addProject = async () => {
  if (!newProjectName.value.trim()) return
  const p = await store.createProject(newProjectName.value.trim())
  form.value.project_id = p.id
  newProjectName.value = ''
}

const submit = async () => {
  if (!form.value.title.trim()) {
    error.value = 'Title is required'
    return
  }
  saving.value = true
  error.value = ''
  try {
    const payload = {
      title: form.value.title.trim(),
      description: form.value.description || undefined,
      status: form.value.status,
      due_date: form.value.due_date || undefined,
      project_id: form.value.project_id || undefined,
      tag_ids: form.value.tag_ids,
    }
    if (props.task) {
      await store.updateTask(props.task.id, payload)
    } else {
      await store.createTask(payload)
    }
    emit('saved')
    emit('close')
  } catch (e: any) {
    error.value = e.message
  } finally {
    saving.value = false
  }
}

const STATUSES: Task['status'][] = ['inbox', 'backlog', 'todo', 'done']
</script>

<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="open" class="fixed inset-0 z-50 flex items-center justify-center p-4" @click.self="$emit('close')">
        <!-- Backdrop -->
        <div class="absolute inset-0 bg-surface-0/80 backdrop-blur-sm" @click="$emit('close')" />

        <!-- Modal -->
        <div class="relative w-full max-w-lg card animate-slide-up max-h-[90vh] overflow-y-auto">
          <!-- Header -->
          <div class="flex items-center justify-between p-4 border-b border-border">
            <span class="font-mono text-xs uppercase tracking-widest text-ink-muted">
              {{ task ? 'Edit task' : 'New task' }}
            </span>
            <button @click="$emit('close')" class="text-ink-muted hover:text-ink font-mono text-sm">✕</button>
          </div>

          <!-- Body -->
          <div class="p-4 space-y-4">
            <!-- Title -->
            <div>
              <label class="font-mono text-xs text-ink-muted uppercase tracking-wider block mb-1.5">Title *</label>
              <input v-model="form.title" class="input-field" placeholder="What needs to be done?" autofocus />
            </div>

            <!-- Description -->
            <div>
              <label class="font-mono text-xs text-ink-muted uppercase tracking-wider block mb-1.5">Description</label>
              <textarea v-model="form.description" class="input-field resize-none" rows="2" placeholder="Optional details..." />
            </div>

            <!-- Status + Due date row -->
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="font-mono text-xs text-ink-muted uppercase tracking-wider block mb-1.5">Status</label>
                <select v-model="form.status" class="input-field">
                  <option v-for="s in STATUSES" :key="s" :value="s">{{ s }}</option>
                </select>
              </div>
              <div>
                <label class="font-mono text-xs text-ink-muted uppercase tracking-wider block mb-1.5">Due date</label>
                <input v-model="form.due_date" type="date" class="input-field" />
              </div>
            </div>

            <!-- Project -->
            <div>
              <label class="font-mono text-xs text-ink-muted uppercase tracking-wider block mb-1.5">Project</label>
              <div class="flex gap-2">
                <select v-model="form.project_id" class="input-field flex-1">
                  <option value="">No project</option>
                  <option v-for="p in store.projects" :key="p.id" :value="p.id">{{ p.name }}</option>
                </select>
              </div>
              <div class="flex gap-2 mt-1.5">
                <input v-model="newProjectName" class="input-field flex-1 text-xs py-1" placeholder="New project name..." @keyup.enter="addProject" />
                <button @click="addProject" class="btn-ghost text-xs py-1">+ add</button>
              </div>
            </div>

            <!-- Tags -->
            <div>
              <label class="font-mono text-xs text-ink-muted uppercase tracking-wider block mb-1.5">Tags</label>
              <div class="flex flex-wrap gap-1.5 mb-1.5">
                <button
                  v-for="tag in store.tags"
                  :key="tag.id"
                  @click="toggleTag(tag.id)"
                  :class="[
                    'font-mono text-[11px] px-2 py-0.5 border transition-colors',
                    form.tag_ids.includes(tag.id)
                      ? 'border-accent text-accent bg-accent/10'
                      : 'border-border text-ink-muted hover:border-border-bright hover:text-ink-dim'
                  ]"
                >#{{ tag.name }}</button>
              </div>
              <div class="flex gap-2">
                <input v-model="newTagName" class="input-field flex-1 text-xs py-1" placeholder="New tag..." @keyup.enter="addTag" />
                <button @click="addTag" class="btn-ghost text-xs py-1">+ add</button>
              </div>
            </div>

            <div v-if="error" class="font-mono text-xs text-red-400">✗ {{ error }}</div>
          </div>

          <!-- Footer -->
          <div class="flex justify-end gap-2 p-4 border-t border-border">
            <button @click="$emit('close')" class="btn-ghost">Cancel</button>
            <button @click="submit" :disabled="saving" class="btn-primary">
              {{ saving ? 'Saving...' : (task ? 'Update' : 'Create') }}
            </button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.modal-enter-active, .modal-leave-active {
  transition: opacity 0.15s ease;
}
.modal-enter-from, .modal-leave-to {
  opacity: 0;
}
</style>
