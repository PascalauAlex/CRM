<template>
  <div>
    <h1 class="font-extrabold text-4xl text-shadow-blue-900 text-shadow-2xs mb-2">Tasks</h1>
    <div class="pb-2">
      <ActionsBar>
        <template #statistics>Actions</template>
        <template #addNew>
          <button
            @click="toggleAddTaskModal"
            class="inline-flex items-center gap-1.5 bg-white border border-gray-300 hover:bg-gray-50 text-gray-700 font-medium py-1.5 px-3 rounded-md shadow-sm transition-colors text-sm"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              stroke-width="2"
              stroke="currentColor"
              class="w-4 h-4"
            >
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
            </svg>
            Add Task
          </button>
        </template>

        <template #filter>
          <button
            @click="toggleFilter"
            class="inline-flex items-center gap-1.5 bg-white border border-gray-300 hover:bg-gray-50 text-gray-700 font-medium py-1.5 px-3 rounded-md shadow-sm transition-colors text-sm"
          >
            <svg
              class="w-4 h-4"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <path
                stroke="currentColor"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M18.796 4H5.204a1 1 0 0 0-.753 1.659l5.302 6.058a1 1 0 0 1 .247.659v4.874a.5.5 0 0 0 .2.4l3 2.25a.5.5 0 0 0 .8-.4v-7.124a1 1 0 0 1 .247-.659l5.302-6.059c.566-.646.106-1.658-.753-1.658Z"
              />
            </svg>
            Filter
          </button>
        </template>
      </ActionsBar>
    </div>
    <DefaultModal @close-modal="toggleAddTaskModal" :modalActive="addTaskModal">
      <AddTaskComponent></AddTaskComponent>
    </DefaultModal>

    <div>
      <transition
        enter-active-class="transition duration-300 ease-out"
        enter-from-class="transform -translate-y-4 opacity-0"
        enter-to-class="transform translate-y-0 opacity-100"
        leave-active-class="transition duration-200 ease-in"
        leave-from-class="transform translate-y-0 opacity-100"
        leave-to-class="transform -translate-y-4 opacity-0"
      >
        <div v-if="showFilter" class="mb-4 flex items-center gap-3">
          <label for="status">Status</label>
          <select
            id="status"
            class="border border-gray-300 rounded-lg px-2 py-2 w-full max-w-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
            v-model="statusQuery"
            @keyup.enter="performSearch"
          >
            <option v-for="option in statusOptions" :key="option.value" :value="option.value">
              {{ option.label }}
            </option>
          </select>

          <label for="assigned_to">Assigned to</label>
          <select
            v-model="assigned_to_filter"
            class="border border-gray-300 rounded-lg px-2 py-2 w-full max-w-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
          >
            <option value="">All</option>
            <option v-for="user in uniqueAssignedUsers" :key="user.id" :value="user.id">
              {{ user.last_name }} {{ user.first_name }}
            </option>
          </select>

          <button
            @click="performSearch"
            class="bg-blue-600 inline-block text-white px-5 py-2 rounded-lg hover:bg-blue-700 transition"
          >
            Search
          </button>

          <button
            @click="clearSearch"
            class="text-gray-500 hover:text-red-600 px-3 py-2 transition"
          >
            Reset
          </button>
        </div>
      </transition>
    </div>


    <div class="flex gap-4">
      <!-- Panoul stâng - Task-uri -->
      <div class="bg-white shadow-sm w-1/2 p-4 rounded-lg">
        <div class="h-[calc(100vh-10rem)] overflow-y-auto pr-2 space-y-4">
          <div
            class="rounded-lg p-6 shadow-sm"
            v-for="task in taskStore.tasks"
            :key="task.title"
            :class="
              daysLeft(task.due_date) < 1 && task.status !== 'closed'
                ? 'bg-red-50 border-l-4 border-red-500 shadow-lg shadow-red-200'
                : 'bg-white border border-gray-200 shadow-lg shadow-gray-300'
            "
          >
            <div>
              <div
                v-if="daysLeft(task.due_date) < 1 && task.status !== 'closed'"
                class="inline-flex items-center gap-1 bg-red-500 text-white text-xs font-bold px-3 py-1 rounded-full mb-2"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-3 w-3"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fill-rule="evenodd"
                    d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
                    clip-rule="evenodd"
                  />
                </svg>
                URGENT
              </div>
            </div>

            <div>
              <h1
                class="font-bold text-lg text-white border-2 border-blue-800 rounded-lg p-2 shadow-sm"
                :class="
                  daysLeft(task.due_date) < 1 && task.status !== 'closed'
                    ? 'bg-red-600 border-red-500'
                    : 'bg-blue-900 border-blue-800'
                "
              >
                {{ task.title }}
              </h1>
              <RouterLink
                v-if="task.lead"
                class="inline-block text-sm font-bold bg-blue-500 mt-2 mb-2 p-2 border-2 border-blue-500 rounded-lg text-white"
                :to="{ name: 'SingleLead', params: { id: task.lead.id } }"
                :class="
                  daysLeft(task.due_date) < 1 && task.status !== 'closed'
                    ? 'bg-red-600 border-red-500 hover:bg-red-400'
                    : 'bg-blue-900 border-blue-800 hover:bg-blue-700 hover:border-blue-600'
                "
              >
                {{ task.lead.company }}
              </RouterLink>
              <div
                class="p-2 space-y-2"
                :class="
                  daysLeft(task.due_date) < 1 && task.status !== 'closed'
                    ? 'text-red-600'
                    : 'text-black'
                "
              >
                <p class="shadow-sm rounded-lg p-2 font-semibold">{{ task.description }}</p>

                <div class="flex justify-between">
                  <strong>Status</strong>
                  <span>{{ task.status }}</span>
                </div>

                <div class="flex justify-between">
                  <strong>Due date</strong>
                  <span>{{ formatDate(task.due_date) }}</span>
                </div>
                <div class="flex justify-between" v-if="task.status !== 'closed'">
                  <strong>Days left</strong>
                  <span>{{ daysLeft(task.due_date) }} days</span>
                </div>

                <div class="flex justify-between">
                  <strong>Member assigned</strong>
                  <span
                    >{{ task.assigned_to?.last_name ?? 'Unassigned' }}
                    {{ task.assigned_to?.first_name }}</span
                  >
                </div>
              </div>

              <div class="flex justify-end items-center gap-1">
                <!-- Show more -->
                <button
                  @click="toggleLeadDetail(task)"
                  class="group hover:cursor-pointer w-8 h-8 flex items-center justify-center"
                >
                  <img
                    src="/icons/show-more-horizontal-svgrepo-com.svg"
                    alt="showMore"
                    class="w-5 h-5 transition-all group-hover:brightness-0 group-hover:[filter:invert(27%)sepia(100%)saturate(500%)hue-rotate(190deg)]"
                  />
                </button>

                <!-- Play -->
                <button
                  v-if="task.status === 'open'"
                  @click="startTask(task.id)"
                  class="group cursor-pointer w-8 h-8 flex items-center justify-center"
                  :style="task.status === 'inprogress' ? 'cursor: not-allowed' : ''"
                >
                  <img
                    src="/icons/play-svgrepo-com.svg"
                    class="w-4 h-4 transition-all group-hover:brightness-0 group-hover:[filter:invert(50%)sepia(100%)saturate(400%)hue-rotate(90deg)]"
                    alt="start"
                  />
                </button>

                <!-- Check -->
                <button
                  v-if="task.status !== 'closed'"
                  @click="taskDone(task.id)"
                  class="group hover:cursor-pointer w-8 h-8 flex items-center justify-center"
                >
                  <img
                    src="/icons/check-read-svgrepo-com.svg"
                    alt="checked"
                    class="w-5 h-5 transition-all group-hover:brightness-0 group-hover:[filter:invert(50%)sepia(100%)saturate(400%)hue-rotate(90deg)]"
                  />
                </button>

                <button
                  @click="handleDelete(task.id)"
                  class="group hover:cursor-pointer w-8 h-8 flex items-center justify-center"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="h-4 w-4 text-gray-500 transition-colors group-hover:text-red-500"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                    />
                  </svg>
                </button>
              </div>

              <div class="shadow-sm rounded-lg p-1" v-if="activeTask === task">
                <h4>Lead details</h4>
                <p><strong>Status: </strong>{{ task.lead.status }}</p>
                <p><strong>Priority: </strong>{{ task.lead.priority }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- -->
      <div class="bg-white shadow-sm w-1/2 p-4 rounded-lg">
        <h2 class="font-bold text-2xl mb-4 text-blue-900">Details</h2>
        <div>
          <div class="bg-white shadow-sm p-2 font-semibold">
            <p class="text-medium">
              Total Tasks
              <span class="text-black bg-gray-200 px-3 py-1 rounded-2xl font-bold text-center">{{
                taskStore.tasks.length
              }}</span>
            </p>
          </div>

          <div class="bg-white shadow-sm p-2 font-semibold">
            <div class="bg-white shadow-sm p-6 rounded-lg">
              <h3 class="font-bold text-2xl mb-6 text-center text-blue-900">Tasks per status</h3>
              <div class="space-y-4">
                <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <span class="font-semibold text-gray-700">Open</span>
                  <span
                    class="text-white bg-green-600 px-4 py-2 rounded-full font-bold text-center"
                  >
                    {{ openTasks }}
                  </span>
                </div>
                <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <span class="font-semibold text-gray-700">In Progress</span>
                  <span
                    class="text-white bg-yellow-500 px-4 py-2 rounded-full font-bold ] text-center"
                  >
                    {{ inProggress }}
                  </span>
                </div>
                <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <span class="font-semibold text-gray-700">Urgent</span>
                  <span
                    class="text-white bg-red-600 px-4 py-2 rounded-full font-bold text-center"
                    >{{ urgent }}</span
                  >
                </div>
                <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <span class="font-semibold text-gray-700">Attention</span>
                  <span
                    class="text-white bg-orange-400 px-4 py-2 rounded-full font-bold text-center"
                  >
                    {{ attentionNeeded }}
                  </span>
                </div>
                <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <span class="font-semibold text-gray-700">Closed</span>
                  <span class="text-white bg-gray-600 px-4 py-2 rounded-full font-bold text-center">
                    {{ closed }}
                  </span>
                </div>
              </div>
            </div>
            <div>
              <h3 class="font-bold text-xl mb-3">
                Assigned Members <span class="text-sm">(unique)</span>
              </h3>
              <div
                v-for="user in uniqueAssignedUsers"
                :key="user.id"
                class="p-2 bg-gray-50 rounded mb-2"
              >
                {{ user.last_name }} {{ user.first_name }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useTaskStore } from '@/stores/taskStore.js'
import { computed, onMounted, ref } from 'vue'
import formatDate from '/services/formatDate.js'
import { useToast } from 'vue-toast-notification'
import ActionsBar from '@/components/ActionsBar.vue'
import DefaultModal from '@/components/Modals/DefaultModal.vue'
import AddTaskComponent from '@/components/Tasks/AddTaskComponent.vue'

const taskStore = useTaskStore()
const activeTask = ref(null) // reține care task e deschis
const toast = useToast()

const toggleLeadDetail = (task) => {
  activeTask.value = activeTask.value === task ? null : task
}

const uniqueAssignedUsers = computed(() => {
  const usersMap = new Map()

  taskStore.tasks.forEach((task) => {
    if (task.assigned_to && task.assigned_to.id) {
      usersMap.set(task.assigned_to.id, task.assigned_to)
    }
  })

  return Array.from(usersMap.values())
})

const openTasks = computed(() => {
  return taskStore.tasks.filter((task) => task.status === 'open').length
})

const inProggress = computed(() => {
  return taskStore.tasks.filter((task) => task.status === 'inprogress').length
})

const closed = computed(() => {
  return taskStore.tasks.filter((task) => task.status === 'closed').length
})

const urgent = computed(() => {
  const today = Date.now()

  return taskStore.tasks.filter((task) => {
    if (!task.due_date) return false
    return new Date(task.due_date).getTime() < today
  }).length
})

const attentionNeeded = computed(() => {
  const twoDays = Date.now() + 24 * 60 * 60 * 1000

  return taskStore.tasks.filter((task) => {
    if (!task.due_date) return false
    return new Date(task.due_date).getTime() < twoDays
  }).length
})

const daysLeft = (date) => {
  const due_date = new Date(date)
  const today = Date.now()
  const days = (due_date - today) / (1000 * 60 * 60 * 24)
  return Math.ceil(days) // rounds
}

const handleDelete = async (taskID) => {
  confirm('Are you sure that you want to delete the task? ')
  await taskStore.deleteTask(taskID)
  toast.success('Task deleted successfully!')
}

const startTask = async (taskId) => {
  const newStatus = {
    status: 'inprogress',
  }

  const success = await taskStore.changeStatus(taskId, newStatus)
  if (success) {
    toast.success(`Task started successfully!`)
  } else {
    toast.error('Error while starting the task, please try again.')
  }
}

const taskDone = async (taskId) => {
  const newStatus = {
    status: 'closed',
  }
  const success = await taskStore.finishTask(taskId, newStatus)
  if (success) {
    toast.success('Task finished successfully!')
  } else {
    toast.error('Error while finishing the task, please try again.')
  }
}
const addTaskModal = ref(false)
const toggleAddTaskModal = () => {
  addTaskModal.value = !addTaskModal.value
}

onMounted(async () => {
  await taskStore.getTasks()
})

const showFilter = ref(false)

const toggleFilter = () => {
  showFilter.value = !showFilter.value
}
const statusQuery = ref('')
const assigned_to_filter = ref('')

const statusOptions = [
  { value: 'open', label: 'Open' },
  { value: 'inprogress', label: 'In progress' },
  { value: 'closed', label: 'Closed' },
]

const performSearch = async () => {
  try {
    await taskStore.getTasks(statusQuery.value, assigned_to_filter.value)
  } catch (err) {
    console.error('Error while filtering', err)
  }
}

const clearSearch = async () => {
  statusQuery.value = ''
  await taskStore.getTasks()
}
</script>

<style scoped>
.task-inprogress {
  cursor: not-allowed;
}
</style>
