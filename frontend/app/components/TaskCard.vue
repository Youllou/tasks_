<script setup lang="ts">
import type { Task, Column } from '~/stores/tasks'

const props = defineProps<{
  task: Task
  columns: Column[]
  projects: { id: string; name: string }[]
}>()

const emit = defineEmits<{
  edit: [task: Task]
}>()

const store = useTaskStore()

const currentColumn = computed(() => props.columns.find(c => c.id === props.task.column_id))

const cycleColumn = async () => {
  const sorted = [...props.columns].sort((a, b) => a.position - b.position)
  const idx = sorted.findIndex(c => c.id === props.task.column_id)
  const next = sorted[(idx + 1) % sorted.length]
  await store.updateTask(props.task.id, { column_id: next.id })
}

const confirmDelete = async () => {
  if (confirm('Delete this task?')) {
    await store.deleteTask(props.task.id)
  }
}

const projectName = computed(() => {
  if (!props.task.project_id) return null
  return props.projects.find(p => p.id === props.task.project_id)?.name
})

const formatDate = (d?: string) => {
  if (!d) return null
  return new Date(d).toLocaleDateString('en-CA', { month: 'short', day: 'numeric' })
}

const isOverdue = computed(() => {
  if (!props.task.due_date) return false
  const col = currentColumn.value
  // consider "done-like" columns: last by position
  const sorted = [...props.columns].sort((a, b) => a.position - b.position)
  const isLast = col?.id === sorted[sorted.length - 1]?.id
  return !isLast && new Date(props.task.due_date) < new Date()
})
</script>

<template>
  <div class="group border border-border hover:border-border-bright bg-surface-1 hover:bg-surface-2 transition-all duration-150 p-4 animate-fade-in">
    <div class="flex items-start gap-3">
      <!-- Column badge — click to cycle -->
      <button
          v-if="currentColumn"
          @click="cycleColumn"
          class="font-mono text-[10px] uppercase tracking-widest px-2 py-0.5 border shrink-0 mt-0.5 transition-all"
          :style="{
          color: currentColumn.color,
          borderColor: currentColumn.color + '50',
          backgroundColor: currentColumn.color + '18',
        }"
          :title="`Column: ${currentColumn.name} — click to cycle`"
      >
        {{ currentColumn.name }}
      </button>

      <!-- Content -->
      <div class="flex-1 min-w-0">
        <p class="text-sm font-medium leading-snug text-ink">{{ task.title }}</p>

        <p v-if="task.description" class="text-xs text-ink-muted mt-1 leading-relaxed line-clamp-2">
          {{ task.description }}
        </p>

        <!-- Meta row -->
        <div v-if="task.tags.length || projectName || task.due_date" class="flex flex-wrap items-center gap-2 mt-2">
          <span v-if="projectName" class="font-mono text-[10px] text-ink-muted bg-surface-3 px-1.5 py-0.5">
            /{{ projectName }}
          </span>
          <span
              v-if="task.due_date"
              :class="['font-mono text-[10px] px-1.5 py-0.5', isOverdue ? 'text-red-400 bg-red-400/10' : 'text-ink-muted bg-surface-3']"
          >
            {{ isOverdue ? '! ' : '' }}{{ formatDate(task.due_date) }}
          </span>
          <span
              v-for="tag in task.tags"
              :key="tag.id"
              class="font-mono text-[10px] text-accent/70 bg-accent/5 px-1.5 py-0.5"
          >#{{ tag.name }}</span>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity shrink-0">
        <button @click="$emit('edit', task)" class="btn-ghost px-2 py-1 text-xs">edit</button>
        <button @click="confirmDelete" class="btn-ghost px-2 py-1 text-xs text-red-400/60 hover:text-red-400">del</button>
      </div>
    </div>
  </div>
</template>