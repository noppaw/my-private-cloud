<script setup>
import { ref, onMounted } from 'vue'

// 1. สร้างตัวแปรเก็บข้อมูล apps
const apps = ref([])
const loading = ref(true)
const error = ref(null)

// 2. ฟังก์ชันดึงข้อมูลจาก API
const fetchApps = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/apps/')
    if (!response.ok) throw new Error('Failed to fetch')
    apps.value = await response.json()
  } catch (err) {
    error.value = 'ไม่สามารถเชื่อมต่อกับ Server ได้ 😭'
    console.error(err)
  } finally {
    loading.value = false
  }
}

// 3. ทำงานทันทีเมื่อเข้าหน้าเว็บ
onMounted(() => {
  fetchApps()
})
</script>

<template>
  <div class="min-h-screen bg-gray-200 p-8 font-sans">
    
    <div class="max-w-5xl mx-auto mb-10 text-center">
      <h1 class="text-4xl font-bold text-gray-800 mb-2">My Private Cloud ☁️</h1>
      <p class="text-gray-500">ศูนย์รวมแอปพลิเคชันส่วนตัวของคุณ</p>
    </div>

    <div v-if="loading" class="text-center text-gray-400 animate-pulse">
      กำลังโหลดข้อมูล...
    </div>

    <div v-else-if="error" class="text-center text-red-500 bg-red-50 p-4 rounded-lg max-w-lg mx-auto border border-red-200">
      {{ error }}
    </div>

    <div v-else class="max-w-5xl mx-auto grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      
      <a 
        v-for="app in apps" 
        :key="app.id" 
        :href="app.url" 
        target="_blank"
        class="block bg-white p-6 rounded-xl shadow-sm hover:shadow-md transition-shadow border border-gray-100 group"
      >
        <div class="w-12 h-12 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center mb-4 group-hover:bg-blue-600 group-hover:text-white transition-colors">
          <span class="text-xl font-bold"><i :class="['mdi', app.icon_name, 'text-3xl']"></i></span>
        </div>

        <h2 class="text-xl font-semibold text-gray-800 mb-1 group-hover:text-blue-600">
          {{ app.title }}
        </h2>

        <p class="text-gray-500 text-sm">
          {{ app.description }}
        </p>
      </a>

    </div>
  </div>
</template>