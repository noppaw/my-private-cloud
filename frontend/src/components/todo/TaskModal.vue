<script setup>
import { ref, watch } from 'vue'

const props = defineProps(['isOpen', 'editData'])
const emit = defineEmits(['close', 'save', 'delete'])

const COLORS = [
  { name: 'Blue', value: '#3B82F6', class: 'bg-blue-500' },
  { name: 'Red', value: '#EF4444', class: 'bg-red-500' },
  { name: 'Green', value: '#10B981', class: 'bg-green-500' },
  { name: 'Purple', value: '#8B5CF6', class: 'bg-purple-500' },
  { name: 'Orange', value: '#F59E0B', class: 'bg-orange-500' },
  { name: 'Pink', value: '#EC4899', class: 'bg-pink-500' },
]

const form = ref({})
const showDeleteConfirm = ref(false)

// Watch การเปลี่ยนแปลงของ Props เพื่ออัปเดต Form
watch(() => props.editData, (newVal) => {
  if (newVal) {
    form.value = { ...newVal }
  } else {
    // Reset Form for create mode
    form.value = { title: '', color: COLORS[0].value, is_completed: false }
  }
  showDeleteConfirm.value = false // Reset delete modal
}, { immediate: true })

function handleSave() {
  if (!form.value.title) return alert('ใส่หัวข้อหน่อยครับ')
  emit('save', form.value)
}
</script>

<template>
  <div v-if="isOpen">
    <Transition name="modal" appear>
      <div v-if="isOpen" class="fixed inset-0 z-40 flex items-center justify-center">
        <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="$emit('close')"></div>
        <div class="bg-white rounded-2xl shadow-2xl p-6 w-full max-w-md border border-gray-100 relative z-10 modal-content" @click.stop>
          
          <div class="flex justify-between items-start mb-4 border-b pb-2">
            <h3 class="text-xl font-bold text-gray-800 flex items-center gap-2">
              <i class="mdi" :class="form.id ? 'mdi-pencil text-orange-500' : 'mdi-calendar-plus text-blue-600'"></i> 
              {{ form.id ? 'แก้ไขรายละเอียด' : 'เพิ่มงานใหม่' }}
            </h3>
            <button v-if="form.id" @click="showDeleteConfirm = true" class="text-red-400 hover:text-red-600 transition-colors transform hover:scale-110">
              <i class="mdi mdi-trash-can-outline text-2xl"></i>
            </button>
          </div>
          
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-semibold text-gray-600 mb-1">หัวข้องาน</label>
              <input v-model="form.title" type="text" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" placeholder="เช่น ประชุมทีม" autofocus>
            </div>

            <div>
              <label class="block text-sm font-semibold text-gray-600 mb-2">สี / ความสำคัญ</label>
              <div class="flex gap-3">
                <button 
                  v-for="color in COLORS" :key="color.value"
                  @click="form.color = color.value"
                  class="w-8 h-8 rounded-full border-2 transition-all transform hover:scale-110"
                  :class="[color.class, form.color === color.value ? 'border-gray-600 scale-110 ring-2 ring-gray-300' : 'border-transparent opacity-70']"
                ></button>
              </div>
            </div>
            
            <div>
              <label class="block text-sm font-semibold text-gray-600 mb-1">รายละเอียด</label>
              <textarea v-model="form.description" rows="3" class="w-full px-3 py-2 border rounded-lg focus:ring-2 outline-none"></textarea>
            </div>
            
            <div class="grid grid-cols-2 gap-4">
              <div><label class="block text-sm font-semibold mb-1">เริ่ม</label><input v-model="form.start" type="datetime-local" class="w-full px-3 py-2 border rounded-lg text-sm"></div>
              <div><label class="block text-sm font-semibold mb-1">จบ</label><input v-model="form.end" type="datetime-local" class="w-full px-3 py-2 border rounded-lg text-sm"></div>
            </div>

            <div v-if="form.id" class="flex items-center gap-3 pt-2">
               <button @click="form.is_completed = !form.is_completed; handleSave()" class="flex-1 py-2 rounded-lg border font-medium flex items-center justify-center gap-2" :class="form.is_completed ? 'bg-green-100 text-green-700' : 'bg-gray-50 text-gray-500'">
                 <i class="mdi" :class="form.is_completed ? 'mdi-check-circle' : 'mdi-circle-outline'"></i> {{ form.is_completed ? 'เสร็จเรียบร้อย' : 'ทำเสร็จแล้ว?' }}
               </button>
            </div>
          </div>

          <div class="mt-6 flex justify-end gap-3">
            <button @click="$emit('close')" class="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg">ยกเลิก</button>
            <button @click="handleSave" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 shadow-lg">บันทึก</button>
          </div>
        </div>
      </div>
    </Transition>

    <Transition name="modal">
      <div v-if="showDeleteConfirm" class="fixed inset-0 z-50 flex items-center justify-center">
        <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="showDeleteConfirm = false"></div>
        <div class="bg-white rounded-2xl shadow-2xl p-6 w-full max-w-sm border border-red-100 relative z-10 modal-content text-center">
          <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <i class="mdi mdi-alert-circle-outline text-3xl text-red-500"></i>
          </div>
          <h3 class="text-xl font-bold text-gray-800 mb-2">ยืนยันการลบ?</h3>
          <div class="flex justify-center gap-3 mt-6">
            <button @click="showDeleteConfirm = false" class="px-5 py-2.5 bg-gray-100 rounded-xl">เก็บไว้ก่อน</button>
            <button @click="$emit('delete', form.id); showDeleteConfirm = false" class="px-5 py-2.5 bg-red-500 text-white rounded-xl shadow-lg">ลบทิ้งเลย</button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.modal-enter-active, .modal-leave-active { transition: opacity 0.3s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-active .modal-content { transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1); }
.modal-leave-active .modal-content { transition: all 0.2s ease-in; }
.modal-enter-from .modal-content, .modal-leave-to .modal-content { transform: scale(0.90) translateY(10px); opacity: 0; }
</style>