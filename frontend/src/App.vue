<script setup>
import { ref, onMounted } from 'vue'

const message = ref('Waiting for Django...')

// เมื่อโหลดหน้าเว็บเสร็จ ให้ยิงไปขอข้อมูล
onMounted(async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/hello/')
    const data = await response.json()
    message.value = data.message
  } catch (error) {
    message.value = 'Error connecting to Backend 😭'
    console.error(error)
  }
})
</script>

<template>
  <div class="container">
    <h1>My Private Cloud ☁️</h1>
    <div class="card">
      <h2>Status from Backend:</h2>
      <p class="response">{{ message }}</p>
    </div>
  </div>
</template>

<style scoped>
.container { text-align: center; margin-top: 50px; font-family: sans-serif; }
.card { border: 1px solid #ddd; padding: 20px; display: inline-block; border-radius: 8px; background: #f9f9f9; }
.response { font-size: 1.5em; color: #42b883; font-weight: bold; }
</style>