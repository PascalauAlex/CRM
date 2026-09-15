<template>
  <div class="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8">
    <div class="flex flex-col gap-3">
      <h1 class="font-bold tracking-tight text-gray-900 text-3xl md:text-4xl">Leads</h1>

      <div
        class="inline-flex items-center bg-white border border-gray-200 shadow-sm rounded-lg px-4 py-2 text-sm w-fit"
      >
        <div class="flex items-center gap-2 pr-4 border-r border-gray-200">
          <span class="text-gray-500 font-medium">Total:</span>
          <span class="font-bold text-blue-700 bg-blue-50 px-2.5 py-0.5 rounded-md">
            {{ leadStore.leads.length }}
          </span>
        </div>
        <div class="flex items-center gap-4 pl-4 overflow-x-auto">
          <div
            v-for="(count, status) in leadStatusCounts"
            :key="status"
            class="flex items-center gap-1.5 whitespace-nowrap"
          >
            <span class="text-gray-500 capitalize">{{ status }}:</span>
            <span class="font-bold text-gray-700">{{ count }}</span>
          </div>

          <div class="flex items-center gap-3 ml-2">
            <span class="text-gray-300">|</span>
            <ExportModal :leads="leadStore.leads" @export="exportLeads" />
            <button
              @click="toggleAddLeadModal"
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
              Add new lead
            </button>
            <button
              class="inline-flex items-center gap-1.5 bg-white border border-gray-300 hover:bg-gray-50 text-gray-700 font-medium py-1.5 px-3 rounded-md shadow-sm transition-colors text-sm"
              @click="toggleAIChat"
            >
              AI Assistant
            </button>
            <filter-button @click="toggleFilter">Filter</filter-button>
          </div>
        </div>
      </div>
    </div>

    <div class="flex items-center gap-3">
      <span class="text-sm font-medium text-gray-500">View:</span>

      <div class="flex bg-gray-100 p-1 rounded-lg border border-gray-200/60 shadow-inner">
        <button
          @click="changeLeadShow('kanban')"
          :class="[
            'px-4 py-1.5 text-sm font-medium rounded-md transition-all duration-200 ease-in-out',
            leadsShow === 'kanban'
              ? 'bg-white text-blue-600 shadow-sm ring-1 ring-gray-200/50'
              : 'text-gray-500 hover:text-gray-800 hover:bg-gray-200/50',
          ]"
        >
          Kanban
        </button>

        <button
          @click="changeLeadShow('table')"
          :class="[
            'px-4 py-1.5 text-sm font-medium rounded-md transition-all duration-200 ease-in-out',
            leadsShow === 'table'
              ? 'bg-white text-blue-600 shadow-sm ring-1 ring-gray-200/50'
              : 'text-gray-500 hover:text-gray-800 hover:bg-gray-200/50',
          ]"
        >
          Table
        </button>
      </div>
    </div>
  </div>
  <transition
    enter-active-class="transition duration-300 ease-out"
    enter-from-class="transform -translate-y-4 opacity-0"
    enter-to-class="transform translate-y-0 opacity-100"
    leave-active-class="transition duration-200 ease-in"
    leave-from-class="transform translate-y-0 opacity-100"
    leave-to-class="transform -translate-y-4 opacity-0"
  >
    <div v-if="showFilter" class="mb-4 flex items-center gap-3 bg-white rounded-lg p-4">
      <input
        v-model="searchQuery"
        @keyup.enter="performSearch"
        type="text"
        placeholder="Search by company..."
        class="border border-gray-300 rounded-lg px-4 py-2 w-full max-w-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
      />
      <label class="font-semibold" for="status">Status</label>
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

      <label class="font-semibold" for="status">Priority</label>
      <select
        id="priority"
        class="border border-gray-300 rounded-lg px-2 py-2 w-full max-w-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
        @keyup.enter="performSearch"
        v-model="priorityQuery"
      >
        <option v-for="option in priorityOptions" :key="option.value" :value="option.value">
          {{ option.label }}
        </option>
      </select>
      <label class="font-semibold">Member</label>
      <select
        class="border border-gray-300 rounded-lg px-2 py-2 w-full max-w-sm focus:ring-2 focus:ring-blue-500 focus:outline-none"
        v-model="lead_assigned_member_id"
      >
        <option v-for="member in teamStore.team.members" :key="member.id" :value="member.id">
          {{ member.last_name ?? 'Unassigned' }}
        </option>
      </select>
      <button
        @click="performSearch"
        class="bg-blue-600 inline-block text-white px-5 py-2 rounded-lg hover:bg-blue-700 transition"
      >
        Search
      </button>

      <button @click="clearSearch" class="text-gray-500 hover:text-red-600 px-3 py-2 transition">
        Reset
      </button>
    </div>
  </transition>
  <div v-show="leadsShow === 'kanban'">
    <KanbanLeads></KanbanLeads>
  </div>

  <div v-if="leadsShow === 'table'">
    <h1 class="mb-4 font-bold tracking-tight text-heading md:text-5xl lg:text-4xl text-blue-900">
      Leads
    </h1>

    <div
      class="p-4 mb-4 text-sm text-fg-brand-strong rounded-base bg-brand-softer"
      role="alert"
      v-if="leadStore.succes_message"
    >
      <span class="font-medium">Info alert!</span> {{ leadStore.succes_message }}
    </div>

    <div v-if="leadStore.loading">
      <h3>Loading...</h3>
    </div>
    <div v-else-if="leadStore.leads && leadStore.leads.length > 0">
      <div class="relative overflow-x-auto bg-white shadow-xs rounded-base border border-default">
        <table class="w-full text-sm text-left rtl:text-right text-body">
          <thead
            class="text-sm text-body bg-neutral-secondary-medium border-b border-default-medium"
          >
            <tr>
              <th scope="col" class="px-6 py-3 font-bold text-lg">Company Name</th>
              <th scope="col" class="px-6 py-3 font-bold text-lg">Contact person</th>
              <th scope="col" class="px-6 py-3 font-bold text-lg">Estimated value</th>
              <th scope="col" class="px-6 py-3 font-bold text-lg">Confidence (0-100)</th>
              <th scope="col" class="px-6 py-3 font-bold text-lg">Status</th>
              <th scope="col" class="px-6 py-3 font-bold text-lg">Priority</th>
              <th scope="col" class="px-6 py-3 font-bold text-lg">Assigned to:</th>
            </tr>
          </thead>
          <tbody>
            <tr
              class="bg-neutral-primary-soft border-b border-default hover:bg-gray-100"
              v-for="lead in formattedLeads"
              :key="lead.id"
              id="table-hover"
              @click="$router.push({ name: 'SingleLead', params: { id: lead.id } })"
            >
              <th scope="row" class="px-6 py-4 font-medium text-heading whitespace-nowrap">
                {{ lead.company }}
              </th>
              <td class="px-6 py-4">{{ lead.contact_person }}</td>
              <td class="px-6 py-4">{{ lead.formattedValue }}</td>
              <td class="px-6 py-4">{{ lead.confidence }}</td>
              <td class="px-6 py-4">{{ lead.status }}</td>
              <td class="px-6 py-4">
                <span :class="lead.priorityColor + ' font-bold'">
                  {{ lead.priority }}
                </span>
              </td>
              <td class="px-6 py-4">{{ lead.assignedName }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div v-else>
      <h1 class="font-bold text-2xl text-gray-800">No leads for the moment , add a new one!</h1>
    </div>
  </div>
  <PaginationBar
    :total-count="leadStore.totalCount"
    :current-page="currentPage"
    :page-size="10"
    @page-change="onPageChange"
  />

  <div>
    <ChatAI :display="showAIChat" @close="showAIChat = false" class="h-1/2"/>
  </div>

  <!-- Add Lead -->
  <AddNewLeadModal :modalActive="addLeadModal" @close-modal="toggleAddLeadModal" class="wide-modal">
    <AddLeadComponent></AddLeadComponent>
  </AddNewLeadModal>
</template>

<script setup>
import { useLeadStore } from '@/stores/leadStore.js'
import { computed, onMounted, ref } from 'vue'
import KanbanLeads from '@/components/Leads/KanbanLeads.vue'
import ExportModal from '@/components/Metadata/ExportModal.vue'
import api from '@/utils/api.js'
import { useToast } from 'vue-toast-notification'
import PaginationBar from '@/components/PaginationBar.vue'
import AddLeadComponent from '@/components/Leads/AddLeadComponent.vue'
import AddNewLeadModal from '@/components/Modals/AddNewLeadModal.vue'
import ChatAI from '@/components/AssistantAI/ChatAI.vue'
import FilterButton from '@/components/UI/ Buttons/FilterButton.vue'
import inactiveStatusCount from '@/utils/alerts.js'
import { useTeamStore } from '@/stores/teamStore.js'

const currentPage = ref(1)
const leadStore = useLeadStore()
const searchQuery = ref('')
const showFilter = ref(false)
const statusQuery = ref('')
const priorityQuery = ref('')
const lead_assigned_member_id = ref('')

const toast = useToast()
const teamStore = useTeamStore()

const addLeadModal = ref(false)
const toggleAddLeadModal = () => {
  addLeadModal.value = !addLeadModal.value
}



onMounted(async () => {
  try {
    await leadStore.fetchLeads(currentPage.value)

  } catch (err) {
    console.log(`Error while loading the leads! ERROR: ${err}`)
    toast.error('Error while loading the leads!')
  }
})

const toggleFilter = async () => {
  await teamStore.fetchTeam()
  showFilter.value = !showFilter.value
}

const leadsShow = ref('kanban')
const changeLeadShow = (viewType) => {
  leadsShow.value = viewType
}

const statusOptions = [
  { value: 'new', label: 'New' },
  { value: 'contacted', label: 'Contacted' },
  { value: 'inprogress', label: 'In progress' },
  { value: 'lost', label: 'Lost' },
  { value: 'won', label: 'Won' },
]

const priorityOptions = [
  { value: 'low', label: 'Low' },
  { value: 'medium', label: 'Medium' },
  { value: 'high', label: 'High' },
]

const formattedLeads = computed(() => {
  return leadStore.leads.map((lead) => ({
    ...lead,
    assignedName:
      lead.assigned_to?.last_name + ' ' + lead.assigned_to?.first_name ||
      lead.assigned_to?.username ||
      'N/A',
    formattedValue: `${lead.estimated_value} $`,
    priorityColor: getPriorityColor(lead.priority),
  }))
})

const getPriorityColor = (priority) => {
  const colors = {
    low: 'text-green-600',
    medium: 'text-blue-600',
    high: 'text-red-600',
  }
  return colors[priority] || 'text-gray-600'
}

function onPageChange(page) {
  currentPage.value = page
  leadStore.fetchLeads(page, searchQuery.value)
}

/* Filtering */

const performSearch = () => {
  currentPage.value = 1 //Reset when performing a new search
  leadStore.fetchLeads(
    currentPage.value,
    searchQuery.value,
    statusQuery.value,
    priorityQuery.value,
    lead_assigned_member_id.value,
  )
}

const clearSearch = () => {
  searchQuery.value = ''
  statusQuery.value = ''
  priorityQuery.value = ''
  currentPage.value = 1
  lead_assigned_member_id.value = ''
  leadStore.fetchLeads(currentPage.value)
}

const leadStatusCounts = computed(() => {
  const counts = {}

  if (!leadStore.leads) return counts

  leadStore.leads.forEach((client) => {
    // Presupunem că proprietatea se numește 'status' pe obiectul lead
    const status = client.status || 'unknown'

    if (counts[status]) {
      counts[status]++
    } else {
      counts[status] = 1
    }
  })

  return counts
})

async function exportLeads(format) {
  let res = null
  if (format === 'xlsx') {
    try {
      res = await api.get('/api/v1/leads/exportXLSX', {
        responseType: 'blob',
      })
    } catch (err) {
      console.error(err)
    }
  } else if (format === 'csv') {
    res = await api.get('/api/v1/leads/exportCSV/', {
      responseType: 'blob',
    })
  } else if (format === 'pdf') {
    res = await api.get('/api/v1/leads/exportPDF',{
      responseType: 'blob'
    })
    console.log('PDF format')
  } else {
    toast.error('Incorrect format!')
    return
  }

  const url = URL.createObjectURL(new Blob([res.data]))
  const a = document.createElement('a')
  a.href = url
  a.download = `leads_export.${format}`
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
  URL.revokeObjectURL(url)
  toast.info('Leads exported successfully!')
}

// === AI ASSISTANT ===

const showAIChat = ref(false)

const toggleAIChat = () => {
  showAIChat.value = !showAIChat.value
}
</script>

<style scoped>
.wide-modal :deep(.modal-content) {
  max-width: 90rem !important; /* sau 1440px */
  width: 95vw !important;
}

/* Sau dacă știi clasa specifică din modal */
.wide-modal :deep(.max-w-lg) {
  max-width: 80rem !important;
}
</style>
