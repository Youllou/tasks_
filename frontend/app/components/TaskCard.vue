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
const isDragging = ref(false)
const showColumnMenu = ref(false)
const isConfirmingDelete = ref(false)

const currentColumn = computed(() => props.columns.find(c => c.id === props.task.column_id))

const handleDeleteClick = async () => {
  if (!isConfirmingDelete.value) {
    isConfirmingDelete.value = true
    // Reset after 3 seconds if not confirmed
    setTimeout(() => {
      isConfirmingDelete.value = false
    }, 3000)
  } else {
    await store.deleteTask(props.task.id)
  }
}

const moveToColumn = async (columnId: string) => {
  if (columnId !== props.task.column_id) {
    await store.updateTask(props.task.id, { column_id: columnId })
  }
  showColumnMenu.value = false
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
  const sorted = [...props.columns].sort((a, b) => a.position - b.position)
  const isLast = col?.id === sorted[sorted.length - 1]?.id
  return !isLast && new Date(props.task.due_date) < new Date()
})

const onDragStart = (e: DragEvent) => {
  isDragging.value = true
  e.dataTransfer!.effectAllowed = 'move'
  e.dataTransfer!.setData('task-id', props.task.id)
}

const onDragEnd = () => {
  isDragging.value = false
}
</script>

<template>
  <div
    draggable="true"
    @dragstart="onDragStart"
    @dragend="onDragEnd"
    :class="['group border border-border hover:border-border-bright bg-surface-1 hover:bg-surface-2 transition-all duration-150 p-4 animate-fade-in cursor-grab active:cursor-grabbing', isDragging && 'opacity-50']"
  >
    <!-- Desktop layout: horizontal -->
    <div class="hidden md:flex items-start gap-3">
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
        <button @click="emit('edit', task)" class="btn-ghost px-2 py-1 text-xs">edit</button>
        <button @click="handleDeleteClick" :class="['btn-ghost px-2 py-1 text-xs', isConfirmingDelete ? 'text-red-400 bg-red-400/10' : 'text-red-400/60 hover:text-red-400']">
          {{ isConfirmingDelete ? 'confirm del' : 'del' }}
        </button>
      </div>
    </div>

    <!-- Mobile layout: vertical -->
    <div class="md:hidden flex flex-col gap-3">
      <!-- Mobile column selector -->
      <div class="relative">
        <button
          @click="showColumnMenu = !showColumnMenu"
          v-if="currentColumn"
          class="font-mono text-[10px] uppercase tracking-widest px-2 py-0.5 border transition-all w-full text-left"
          :style="{
            color: currentColumn.color,
            borderColor: currentColumn.color + '50',
            backgroundColor: currentColumn.color + '18',
          }"
        >
          {{ currentColumn.name }}
        </button>
        <div v-if="showColumnMenu" class="absolute top-full mt-1 left-0 right-0 bg-surface-2 border border-border rounded shadow-lg z-50">
          <button
            v-for="col in columns"
            :key="col.id"
            @click="moveToColumn(col.id)"
            :class="['w-full text-left px-3 py-2 text-xs font-mono transition-colors', col.id === currentColumn?.id ? 'bg-surface-3' : 'hover:bg-surface-3']"
          >
            {{ col.name }}
          </button>
        </div>
      </div>

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

      <!-- Mobile Actions - side by side -->
      <div class="flex items-center gap-2 pt-2 border-t border-border/50">
        <button @click="emit('edit', task)" class="flex-1 btn-ghost px-2 py-1.5 text-xs">edit</button>
        <button @click="handleDeleteClick" :class="['flex-1 btn-ghost px-2 py-1.5 text-xs', isConfirmingDelete ? 'text-red-400 bg-red-400/10' : 'text-red-400/60 hover:text-red-400']">
          {{ isConfirmingDelete ? 'confirm del' : 'del' }}
        </button>
      </div>
    </div>
  </div>
</template>