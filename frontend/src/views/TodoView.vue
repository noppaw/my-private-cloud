<script setup>
import { ref, onMounted } from 'vue'
import { useTodo } from '@/composables/useTodo'

// Import Components
import TaskBacklog from '@/components/todo/TaskBacklog.vue'
import TaskCalendar from '@/components/todo/TaskCalendar.vue'
import TaskModal from '@/components/todo/TaskModal.vue'

// Logic from Composable
const { backlogTasks, calendarEvents, fetchTasks, createTask, updateTask, deleteTask } = useTodo()

// Local UI State
const isNewTemplate = ref(false)
const showModal = ref(false)
const modalData = ref(null) // Data to pass to modal (create=null, edit=object)

// --- Handlers ---

// 1. Add Task from Backlog Input
const handleAddBacklog = async (title) => {
  const color = isNewTemplate.value ? '#8B5CF6' : '#3B82F6' // Purple/Blue
  await createTask({ title, is_template: isNewTemplate.value, color })
}

// 2. Open Modal (Create or Edit)
const openModal = (data = null, date = null) => {
  if (data) {
    // Edit Mode
    const isEvent = !!data.extendedProps // Check if it's calendar event
    modalData.value = {
      id: parseInt(data.id),
      title: data.title,
      description: isEvent ? data.extendedProps.description : data.description,
      start: data.start ? toLocalISOString(data.start) : '',
      end: data.end ? toLocalISOString(data.end) : '',
      is_completed: isEvent ? data.extendedProps.is_completed : data.is_completed,
      color: (isEvent ? data.extendedProps.color : data.color) || '#3B82F6'
    }
  } else {
    // Create Mode
    let start = date || new Date()
    if (date && !date.getHours()) start.setHours(9, 0, 0, 0)
    modalData.value = {
      start: toLocalISOString(start),
      end: toLocalISOString(new Date(start.getTime() + 3600000)), // +1hr
      color: '#3B82F6'
    }
  }
  showModal.value = true
}

// 3. Save Task (from Modal)
const handleSave = async (form) => {
  const payload = {
    title: form.title,
    description: form.description,
    start_time: form.start ? new Date(form.start).toISOString() : null,
    end_time: form.end ? new Date(form.end).toISOString() : null,
    is_completed: form.is_completed,
    color: form.color
  }
  
  if (form.id) await updateTask(form.id, payload)
  else await createTask(payload)
  
  showModal.value = false
}

// 4. Delete Task
const handleDelete = async (id) => {
  await deleteTask(id)
  showModal.value = false
}

// 5. Drop Logic
const handleExternalDrop = async (info) => {
  const data = JSON.parse(info.draggedEl.getAttribute('data-event'))
  const date = info.event.start.toISOString()
  
  try {
    if (data.is_template) {
      // Copy Template
      await createTask({ ...data, start_time: date, is_template: false })
    } else {
      // Move Task
      await updateTask(data.id, { start_time: date })
    }
    info.event.remove() // Remove temporary mirror
    await fetchTasks()  // Reload real data
  } catch (e) { info.revert() }
}

const handleEventDrop = async (info) => {
  try {
    await updateTask(info.event.id, {
      start_time: info.event.start.toISOString(),
      end_time: info.event.end ? info.event.end.toISOString() : null
    })
  } catch (e) { info.revert() }
}

// Helper
const toLocalISOString = (d) => {
  const date = new Date(d)
  const pad = (n) => n < 10 ? '0' + n : n
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`
}

onMounted(() => fetchTasks())
</script>

<template>
  <div class="p-4 md:p-8 bg-white min-h-screen font-sans relative">
    
    <div class="flex flex-col md:flex-row items-center justify-between mb-6 gap-4">
      <h1 class="text-3xl font-bold text-gray-800 flex items-center gap-2">
        <i class="mdi mdi-checkbox-marked-circle-outline text-blue-600"></i>
        Smart To-Do List
      </h1>
      <router-link to="/" class="px-4 py-2 text-gray-600 bg-gray-100 hover:bg-gray-200 rounded-lg transition hover:shadow-sm transform hover:scale-105 duration-200">
        <i class="mdi mdi-home"></i> กลับหน้าหลัก
      </router-link>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6 h-[85vh]">
      <TaskBacklog 
        :tasks="backlogTasks" 
        v-model:isNewTemplate="isNewTemplate"
        @add="handleAddBacklog"
        @click-task="openModal"
      />

      <TaskCalendar 
        :events="calendarEvents"
        @event-drop="handleEventDrop"
        @external-drop="handleExternalDrop"
        @date-click="(date) => openModal(null, date)"
        @event-click="openModal"
      />
    </div>

    <TaskModal 
      :isOpen="showModal"
      :editData="modalData"
      @close="showModal = false"
      @save="handleSave"
      @delete="handleDelete"
    />

  </div>
</template>