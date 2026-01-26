<script setup>
import { ref, onMounted } from 'vue'
import { Draggable } from '@fullcalendar/interaction'

const props = defineProps(['tasks', 'isNewTemplate'])
const emit = defineEmits(['add', 'update:isNewTemplate', 'click-task'])

const containerRef = ref(null)
const newTitle = ref('')

function handleAdd() {
  if (!newTitle.value.trim()) return
  emit('add', newTitle.value)
  newTitle.value = ''
}

onMounted(() => {
  if (containerRef.value) {
    new Draggable(containerRef.value, {
      itemSelector: '.fc-event',
      eventData: (eventEl) => JSON.parse(eventEl.getAttribute('data-event'))
    })
  }
})
</script>

<template>
  <div ref="containerRef" class="col-span-1 bg-slate-50 p-4 rounded-xl border border-slate-200 flex flex-col h-full shadow-inner">
    <div class="flex justify-between items-center mb-4">
      <h2 class="text-lg font-bold text-slate-700 flex items-center gap-2">
        <i class="mdi mdi-inbox-full text-orange-500"></i> Backlog
      </h2>
      <label class="flex items-center gap-2 cursor-pointer text-sm text-slate-600 select-none hover:text-purple-600">
        <input 
          type="checkbox" 
          :checked="isNewTemplate" 
          @change="$emit('update:isNewTemplate', $event.target.checked)"
          class="accent-purple-500 w-4 h-4"
        >
        <span>Template</span>
      </label>
    </div>

    <div class="mb-4 relative group">
      <input 
        v-model="newTitle"
        @keyup.enter="handleAdd"
        type="text" 
        :placeholder="isNewTemplate ? 'สร้างแม่พิมพ์งานซ้ำ...' : 'เพิ่มงานทั่วไป...'" 
        class="w-full px-4 py-3 pr-10 rounded-lg border focus:outline-none focus:ring-2 shadow-sm transition-all"
        :class="isNewTemplate ? 'border-purple-300 focus:ring-purple-500 bg-purple-50' : 'border-gray-300 focus:ring-blue-500'"
      >
      <button @click="handleAdd" class="absolute right-2 top-2.5 transition-all transform hover:scale-110" :class="isNewTemplate ? 'text-purple-500 hover:text-purple-700' : 'text-gray-400 hover:text-blue-600'">
        <i class="mdi mdi-plus-circle text-2xl"></i>
      </button>
    </div>
    
    <div class="overflow-y-auto flex-1 pr-2 custom-scrollbar">
      <TransitionGroup name="list" tag="div" class="space-y-3 relative">
        <div 
          v-for="task in tasks" 
          :key="task.id" 
          @click="$emit('click-task', task)"
          class="fc-event p-4 rounded-lg shadow-sm border cursor-move transition-all duration-200 group relative overflow-hidden bg-white hover:shadow-md hover:scale-[1.02]"
          :style="{ borderLeftColor: task.color, borderLeftWidth: '4px' }"
          :data-event="JSON.stringify({ 
            id: task.id, 
            title: task.title, 
            description: task.description, 
            is_template: task.is_template,
            color: task.color
          })"
        >
          <div class="flex justify-between items-center pl-2 pointer-events-none">
            <h3 class="font-medium truncate text-slate-700">
              <i v-if="task.is_template" class="mdi mdi-content-copy text-xs mr-1 text-purple-500"></i>
              {{ task.title }}
            </h3>
            <i class="mdi mdi-pencil text-gray-300 group-hover:text-blue-500 opacity-0 group-hover:opacity-100 transition-opacity text-sm"></i>
          </div>
        </div>
      </TransitionGroup>
      <div v-if="tasks.length === 0" class="text-center text-slate-400 py-10 transition-opacity">
        <i class="mdi mdi-leaf text-4xl mb-2 block opacity-50"></i>
        ว่างเปล่า...
      </div>
    </div>
  </div>
</template>

<style scoped>
/* List Animation */
.list-enter-active, .list-leave-active { transition: all 0.4s ease; }
.list-enter-from, .list-leave-to { opacity: 0; transform: translateX(-30px); }
.list-move { transition: transform 0.4s ease; }
.list-leave-active { position: absolute; width: 100%; z-index: 0; }

/* Smooth Drag Styles */
.fc-event { transition: transform 0.2s, box-shadow 0.2s, background-color 0.2s; }
.fc-event:hover { transform: translateY(-2px); }
:deep(.fc-event-mirror) {
  transition: top 0s, left 0s, transform 0.1s !important; 
  pointer-events: none !important;
  opacity: 0.9 !important;
  box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1) !important;
  transform: scale(1.05) rotate(3deg) !important; 
  z-index: 9999 !important;
}
.fc-event.fc-event-dragging { opacity: 0.3; filter: grayscale(100%); transform: scale(0.95); }
</style>