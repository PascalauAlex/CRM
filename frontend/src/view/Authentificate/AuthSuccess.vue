<template>
  <div class="flex flex-col items-center justify-center h-screen gap-4">
    <div
      class="animate-spin h-10 w-10 border-4 border-blue-600 border-t-transparent rounded-full"
    ></div>
    <p class="text-gray-600">Loging in...</p>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth.js'
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

onMounted(() => {
  const access = route.query.access
  const refresh = route.query.refresh
  const set_profile = route.query.set_profile
  console.log(`Access ${access}, Refresh: ${refresh}, set_profile:${set_profile}`)
  authStore.setToken(access,refresh)
  

  if(set_profile === 'True'){
    router.replace('/set-user-profile')
  }else{
    router.replace('/')
  }
  
})
</script>

<style scoped></style>
