<script setup>
import { ref, watch } from 'vue'
import FullCalendar from '@fullcalendar/vue3'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'

const props = defineProps(['events'])
const emit = defineEmits(['event-drop', 'external-drop', 'date-click', 'event-click'])

const calendarRef = ref(null)

// Smart Click Logic (Moved from Parent)
const clickTimer = ref(null)
const clickCount = ref(0)

function handleSmartClick(info) {
  clickCount.value++
  if (clickCount.value === 1) {
    clickTimer.value = setTimeout(() => {
      // Single Click -> Zoom
      const api = calendarRef.value.getApi()
      const view = api.view.type
      if (view === 'dayGridMonth') api.changeView('timeGridWeek', info.dateStr)
      else if (view === 'timeGridWeek') api.changeView('timeGridDay', info.dateStr)
      else api.changeView('dayGridMonth')
      clickCount.value = 0
    }, 300)
  } else if (clickCount.value === 2) {
    // Double Click -> Emit
    clearTimeout(clickTimer.value)
    clickCount.value = 0
    emit('date-click', info.date)
  }
}

function handleRightClick() {
  const api = calendarRef.value.getApi()
  const view = api.view.type
  const date = api.getDate()
  if (view === 'timeGridDay') api.changeView('timeGridWeek', date)
  else if (view === 'timeGridWeek') api.changeView('dayGridMonth', date)
}

const calendarOptions = ref({
  plugins: [ dayGridPlugin, timeGridPlugin, interactionPlugin ],
  initialView: 'dayGridMonth',
  headerToolbar: { left: 'prev,next today', center: 'title', right: 'dayGridMonth,timeGridWeek,timeGridDay' },
  navLinks: true,
  navLinkDayClick: 'timeGridDay',
  navLinkWeekClick: 'timeGridWeek',
  editable: true,
  droppable: true,
  selectable: true,
  selectMirror: true,
  selectMinDistance: 10,
  nowIndicator: true,
  dragRevertDuration: 500,
  dragScroll: true,
  
  // Events Binding
  events: props.events,
  
  // Handlers
  eventDrop: (info) => emit('event-drop', info),
  eventReceive: (info) => emit('external-drop', info),
  dateClick: handleSmartClick,
  select: (info) => {
    if (info.view.type === 'dayGridMonth' && (info.end - info.start <= 86400000)) return
    emit('date-click', info.start)
  },
  eventClick: (info) => emit('event-click', info.event)
})
watch(() => props.events, (newEvents) => {
  calendarOptions.value.events = newEvents
}, { deep: true })
</script>

<template>
  <div class="col-span-3 bg-white border border-gray-200 rounded-xl p-4 shadow-sm h-full overflow-hidden relative z-0">
    <FullCalendar 
      ref="calendarRef" 
      :options="calendarOptions" 
      class="h-full select-none" 
      @contextmenu.prevent="handleRightClick"
    />
  </div>
</template>

<style scoped>
/* View Animation */
:deep(.fc-view) { animation: view-fade-in 0.4s cubic-bezier(0.16, 1, 0.3, 1); }
@keyframes view-fade-in { from { opacity: 0; transform: scale(0.98) translateY(5px); } to { opacity: 1; transform: scale(1) translateY(0); } }

/* FullCalendar Style Overrides */
:deep(.fc) { color: #334155; --fc-border-color: #e2e8f0; --fc-today-bg-color: #eff6ff; }
:deep(.fc-toolbar-title) { font-size: 1.5rem !important; font-weight: 800 !important; color: #1e293b !important; }
:deep(.fc-button) { background-color: white !important; border: 1px solid #e2e8f0 !important; color: #64748b !important; font-weight: 600 !important; box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05) !important; text-transform: capitalize; transition: all 0.2s; }
:deep(.fc-button:hover) { background-color: #f8fafc !important; transform: translateY(-1px); }
:deep(.fc-button:active) { background-color: #eff6ff !important; color: #2563eb !important; border-color: #bfdbfe !important; transform: translateY(0); }
:deep(.fc-day-past) { background-color: #f8fafc !important; background-image: repeating-linear-gradient(45deg, transparent, transparent 10px, #f1f5f9 10px, #f1f5f9 20px) !important; }
:deep(.fc-daygrid-day-top) { cursor: zoom-in; }
.fc-event.fc-h-event { border: none; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); padding: 2px 4px; }
</style>