<script setup lang="ts">
const store = useTaskStore()

const setColumn = (id: string | null) => {
  store.filterColumnId = id
  store.fetchTasks()
}

const setTag = (t: string | null) => {
  store.filterTag = t
  store.fetchTasks()
}

const setProject = (p: string | null) => {
  store.filterProject = p
  store.fetchTasks()
}
</script>

<template>
  <aside class="w-52 shrink-0 border-r border-border h-full flex flex-col">
    <div class="p-4 border-b border-border">
      <h1 class="font-mono text-base font-semibold tracking-tight">
        tasks<span class="text-accent">_</span>
      </h1>
    </div>

    <nav class="flex-1 overflow-y-auto p-3 space-y-5">
      <!-- Column filters -->
      <div>
        <p class="font-mono text-[10px] uppercase tracking-widest text-ink-muted px-2 mb-1">Columns</p>
        <ul class="space-y-0.5">
          <li>
            <button
                @click="setColumn(null)"
                :class="['w-full text-left px-2 py-1.5 font-mono text-xs flex items-center justify-between transition-colors',
                !store.filterColumnId ? 'text-ink bg-surface-3' : 'text-ink-dim hover:text-ink hover:bg-surface-2']"
            >
              <span class="flex items-center gap-2">
                <span class="w-1.5 h-1.5 rounded-full bg-ink-muted" />
                All tasks
              </span>
            </button>
          </li>
          <li v-for="col in store.columns" :key="col.id">
            <button
                @click="setColumn(col.id)"
                :class="['w-full text-left px-2 py-1.5 font-mono text-xs flex items-center justify-between transition-colors',
                store.filterColumnId === col.id ? 'text-ink bg-surface-3' : 'text-ink-dim hover:text-ink hover:bg-surface-2']"
            >
              <span class="flex items-center gap-2">
                <span class="w-1.5 h-1.5 rounded-full" :style="{ backgroundColor: col.color }" />
                {{ col.name }}
              </span>
              <span class="text-ink-muted text-[10px]">
                {{ store.tasksByColumn[col.id]?.length || 0 }}
              </span>
            </button>
          </li>
        </ul>
      </div>

      <!-- Projects -->
      <div v-if="store.projects.length">
        <p class="font-mono text-[10px] uppercase tracking-widest text-ink-muted px-2 mb-1">Projects</p>
        <ul class="space-y-0.5">
          <li>
            <button @click="setProject(null)"
                    :class="['w-full text-left px-2 py-1.5 font-mono text-xs transition-colors',
                !store.filterProject ? 'text-ink bg-surface-3' : 'text-ink-dim hover:text-ink hover:bg-surface-2']"
            >All</button>
          </li>
          <li v-for="p in store.projects" :key="p.id">
            <button @click="setProject(p.id)"
                    :class="['w-full text-left px-2 py-1.5 font-mono text-xs truncate transition-colors',
                store.filterProject === p.id ? 'text-ink bg-surface-3' : 'text-ink-dim hover:text-ink hover:bg-surface-2']"
            >/{{ p.name }}</button>
          </li>
        </ul>
      </div>

      <!-- Tags -->
      <div v-if="store.tags.length">
        <p class="font-mono text-[10px] uppercase tracking-widest text-ink-muted px-2 mb-1">Tags</p>
        <ul class="space-y-0.5">
          <li>
            <button @click="setTag(null)"
                    :class="['w-full text-left px-2 py-1.5 font-mono text-xs transition-colors',
                !store.filterTag ? 'text-ink bg-surface-3' : 'text-ink-dim hover:text-ink hover:bg-surface-2']"
            >All</button>
          </li>
          <li v-for="tag in store.tags" :key="tag.id">
            <button @click="setTag(tag.name)"
                    :class="['w-full text-left px-2 py-1.5 font-mono text-xs truncate transition-colors',
                store.filterTag === tag.name ? 'text-accent bg-accent/5' : 'text-ink-dim hover:text-ink hover:bg-surface-2']"
            >#{{ tag.name }}</button>
          </li>
        </ul>
      </div>
    </nav>
  </aside>
</template>