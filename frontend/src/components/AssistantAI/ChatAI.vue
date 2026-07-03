<template>
  <!-- AI Chat Box -->
  <transition
    enter-active-class="transition duration-200 ease-out"
    enter-from-class="opacity-0 translate-y-4"
    enter-to-class="opacity-100 translate-y-0"
    leave-active-class="transition duration-150 ease-in"
    leave-from-class="opacity-100 translate-y-0"
    leave-to-class="opacity-0 translate-y-4"
  >
    <div
      v-if="props.display"
      class="fixed bottom-12 right-12 w-96 h-[600px] max-h-[calc(100vh-6rem)] bg-white rounded-xl shadow-2xl border border-gray-200 flex flex-col overflow-hidden z-50"
    >
      <div
        class="shrink-0 flex items-center justify-between px-4 py-3 border-b border-gray-200 bg-blue-900 rounded-t-xl"
      >
        <div class="flex items-center gap-2">
          <div class="w-2 h-2 bg-green-400 rounded-full"></div>
          <h3 class="font-semibold text-white text-sm">CRM AI Assistant</h3>
        </div>
        <button
          @click="emit('close')"
          class="text-white/80 transition cursor-pointer hover:text-red-500"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="w-5 h-5"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
            stroke-width="2"
          >
            <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Messages -->
      <div class="flex-1 min-h-0 overflow-y-auto p-4 space-y-3 bg-gray-50">
        <div
          v-for="(message, index) in assistantStore.messages.filter((m) => m.content)"
          :key="index"
          class="flex"
          :class="message.role === 'user' ? 'justify-end' : 'justify-start'"
        >
          <div
            class="rounded-lg px-3 py-2 text-sm max-w-[80%] shadow-sm whitespace-pre-wrap break-words"
            :class="
              message.role === 'user'
                ? 'bg-blue-600 text-white'
                : 'bg-white border border-gray-200 text-gray-700'
            "
          >
            {{ message.content }}
          </div>
        </div>
        <div v-if="assistantStore.loading" class="flex justify-start">
          <div class="rounded-lg px-3 py-2 bg-white border border-gray-200 shadow-sm">
            <div class="flex gap-1">
              <span
                class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                style="animation-delay: 0ms"
              ></span>
              <span
                class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                style="animation-delay: 150ms"
              ></span>
              <span
                class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                style="animation-delay: 300ms"
              ></span>
            </div>
          </div>
        </div>
      </div>

      <!-- Input -->
      <div class="shrink-0 p-3 border-t border-gray-200 bg-white rounded-b-xl">
        <div class="flex items-center gap-2">
          <input
            v-model="aiInput"
            @keyup.enter="sendAIMessage"
            type="text"
            :disabled="assistantStore.loading"
            placeholder="Write a message..."
            class="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
          />
          <button
            @click="sendAIMessage"
            class="bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded-lg transition"
            :disabled="assistantStore.loading"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="w-4 h-4"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
              stroke-width="2"
            >
              <path stroke-linecap="round" stroke-linejoin="round" d="M14 5l7 7m0 0l-7 7m7-7H3" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref } from 'vue'
import { useAssistantStore } from '@/stores/assistantStore.js'

const props = defineProps({
  display: Boolean,
})

const emit = defineEmits(['close'])

const aiInput = ref('')

const assistantStore = useAssistantStore()

const sendAIMessage = async () => {
  if (!aiInput.value.trim()) return
  try {
    await assistantStore.sendMessage(aiInput.value)
    aiInput.value = ''
  } catch (error) {
    console.error(error)
  }
  aiInput.value = ''
}
</script>

<style scoped></style>
