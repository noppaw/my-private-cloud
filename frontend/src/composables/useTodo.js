import { ref, computed } from 'vue'
import axios from 'axios'

// Global State (เก็บไว้นอก function เพื่อให้แชร์ได้ถ้าจำเป็น)
const tasks = ref([])

export function useTodo() {
  
  // Computed: แยกประเภทงานอัตโนมัติ
  const backlogTasks = computed(() => tasks.value.filter(t => !t.start_time))
  
  const calendarEvents = computed(() => tasks.value
    .filter(t => t.start_time)
    .map(t => ({
      id: t.id,
      title: t.title,
      start: t.start_time,
      end: t.end_time,
      extendedProps: { 
        description: t.description,
        is_completed: t.is_completed,
        is_template: t.is_template,
        color: t.color
      },
      backgroundColor: t.is_completed ? '#94a3b8' : t.color,
      borderColor: 'transparent',
      className: t.is_completed ? 'opacity-50 line-through' : ''
    }))
  )

  // --- API Actions ---
  const fetchTasks = async () => {
    try {
      const res = await axios.get('http://localhost:8000/api/todo/tasks/')
      tasks.value = res.data
    } catch (e) { console.error(e) }
  }

  const createTask = async (payload) => {
    await axios.post('http://localhost:8000/api/todo/tasks/', payload)
    await fetchTasks()
  }

  const updateTask = async (id, payload) => {
    await axios.patch(`http://localhost:8000/api/todo/tasks/${id}/`, payload)
    await fetchTasks()
  }

  const deleteTask = async (id) => {
    await axios.delete(`http://localhost:8000/api/todo/tasks/${id}/`)
    await fetchTasks()
  }

  return {
    tasks,
    backlogTasks,
    calendarEvents,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask
  }
}