<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/userStore.js'
import { useTeamStore } from '@/stores/teamStore.js'
import { useToast } from 'vue-toast-notification'
import { useRouter,useRoute } from 'vue-router'



const userStore = useUserStore()

const belongToTeam = ref(false)
const teamValidated = ref(false)
const teamCode = ref('')
const phoneNumber = ref('')
const isSubmitting = ref(false)
const createOwnTeam = ref(false)
const teamStore = useTeamStore()
const joinedTeam = ref('')
const router = useRouter()
const route = useRoute()
const teamName = ref('')

const first_name = ref('')
const last_name = ref('')
const email = ref('')
const teamAsigned = ref(false)


const displayName = computed(()=>{
  return `${first_name.value} ${last_name.value}`
})

const displayEmail = computed(()=>{
  return `${email.value}`
})

//The user will be redirected to a separate page for creating his own team
function toggleBelongToTeam() {
  belongToTeam.value = !belongToTeam.value
}

const teamCreated = ref(false)

const toast = useToast()

const toggleCreateOwnTeam = () => {
  createOwnTeam.value = !createOwnTeam.value
}

async function createTeam() {
  const formData = {
    name: teamName.value,
  }
  isSubmitting.value = true
  console.log(formData)

  try {
    const response = await teamStore.addTeam(formData)
    teamCreated.value = !teamCreated.value

    toast.success(`Team ${teamName.value} created successfully!`)
    teamAsigned.value = true
  } catch (err) {
    console.error(err)
    toast.error('Error while creating the team!')
  } finally {
    isSubmitting.value = false
  }
}

async function activateTeamCode() {
  const formData = {
    invite_code: teamCode.value,
  }

  isSubmitting.value = true
  console.log(formData)
  try {
    const response = await teamStore.joinWithTeamCode(formData)
    teamValidated.value = !teamValidated.value
    joinedTeam.value = response.data['team']
    toast.success(`Joined team : ${joinedTeam.value} successfully!`)
    teamAsigned.value = true
  } catch (err) {
    console.error(err)
    toast.error('Error while joining the team!')
  } finally {
    isSubmitting.value = false
  }
}

async function saveProfile() {
  isSubmitting.value = true
  const profileData = {
    phone: phoneNumber.value,
    first_name:first_name.value,
    last_name:last_name.value,
    email:email.value
  }
  try {
    await userStore.editUser(profileData)
    await userStore.profile_completed()
    router.push('/dashboard')
  } catch (err) {
    toast.error('Error while saving the profile')
    console.error('Error while savint the profile!', err)
  } finally {
    isSubmitting.value = false
  }
}

const completionPercent = computed(() => {
  let done = 1 // email e mereu setat
  if (teamValidated.value || belongToTeam.value === false) done++
  if (phoneNumber.value) done++
  return Math.round((done / 3) * 100)
})

const initials = computed(() => {
  const name = userStore.userProfile?.full_name || userStore.user?.email || ''
  return name
    .split(' ')
    .map((w) => w[0])
    .filter(Boolean)
    .slice(0, 2)
    .join('')
    .toUpperCase()
})

onMounted(()=>{
  email.value = route.params.username
  console.log(email.value)
})


</script>

<template>
  <div class="min-h-screen bg-gray-50 py-12 px-4">
    <div class="max-w-2xl mx-auto">
      <!-- Header -->
      <div class="mb-8 text-center">
        <h1 class="text-3xl font-bold text-gray-900">Complete your profile</h1>
        <p class="mt-2 text-gray-600">Just a few more details and you're ready to go.</p>
      </div>

      <!-- Progress bar -->
      <div class="mb-6">
        <div class="flex justify-between text-sm text-gray-600 mb-2">
          <span>Profile completion</span>
          <span class="font-medium">{{ completionPercent }}%</span>
        </div>
        <div class="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
          <div
            class="bg-blue-600 h-full transition-all duration-500 ease-out"
            :style="{ width: `${completionPercent}%` }"
          />
        </div>
      </div>

      <!-- Card 1: Account info -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 mb-4">
        <div class="px-6 py-5 border-b border-gray-100 flex items-center justify-between">
          <div>
            <h2 class="text-lg font-semibold text-gray-900">Account information</h2>
            <p class="text-sm text-gray-500 mt-0.5">Your details from Google</p>
          </div>
          <span
            class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium bg-green-50 text-green-700 border border-green-200"
          >
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="3"
                d="M5 13l4 4L19 7"
              />
            </svg>
            Verified
          </span>
        </div>

        <div class="p-6 flex items-center gap-5">
          <!-- Avatar -->
          <div class="relative shrink-0">
            <img
              v-if="userStore.userProfile?.profile_picture || userStore.userProfile?.picture_url"
              :src="userStore.userProfile.profile_picture || userStore.userProfile.picture_url"
              alt="Profile"
              class="w-20 h-20 rounded-full object-cover border-2 border-white ring-2 ring-gray-200"
            />
            <div
              v-else
              class="w-20 h-20 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white text-xl font-semibold ring-2 ring-gray-200"
            >
              {{ initials }}
            </div>
          </div>

          <!-- Info -->
          <div class="flex-1 min-w-0">
            <p class="text-base font-semibold text-gray-900 truncate">
              {{ userStore.userProfile?.full_name || displayName ||'No name set'  }}
            </p>
            <p class="text-sm text-gray-500 truncate flex items-center gap-1.5 mt-0.5">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                />
              </svg>
              {{ userStore.user?.email || displayEmail}}
            </p>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 mb-4 p-2 flex-wrap"
      v-if="!userStore.user.first_name || !userStore.user.last_name">
        <h3 class="font-bold">Complete profile</h3>
        <div class="block">
            <label class="font-semibold">Last name</label>
            <input type="text" name="last_name" class="block rounded-lg" v-model="last_name">
        </div>
        <div>
          <label class="font-semibold">First name</label>
            <input type="text" name="first_name" class="block rounded-lg" v-model="first_name">
        </div>
      </div>

      <!-- Card 2: Team -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 mb-4">
        <div class="px-6 py-5 border-b border-gray-100">
          <h2 class="text-lg font-semibold text-gray-900">Team</h2>
          <p class="text-sm text-gray-500 mt-0.5">Join an existing team or create your own later</p>
        </div>

        <div class="p-6">
          <!-- Question step -->
          <div v-if="!belongToTeam && !teamValidated">
            <p class="text-sm text-gray-700 mb-4">Do you already belong to a team?</p>
            <div class="flex gap-3">
              <button
                @click="toggleBelongToTeam"
                class="flex-1 px-4 py-2.5 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 hover:border-gray-400 transition"
              >
                Yes, I have a code
              </button>
              <button
                @click="toggleCreateOwnTeam"
                class="flex-1 px-4 py-2.5 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-50 hover:border-gray-400 transition"
              >
                Create your own team
              </button>
            </div>
          </div>

          <!-- Team code input -->
          <div v-else-if="belongToTeam && !teamValidated">
            <form @submit.prevent="activateTeamCode" class="space-y-3">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1.5"> Team code </label>
                <input
                  v-model="teamCode"
                  type="text"
                  placeholder="e.g. TEAM-A4F9-X2K7"
                  class="w-full px-3.5 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent tracking-wider"
                />
              </div>
              <div class="flex gap-2">
                <button
                  type="button"
                  @click="toggleBelongToTeam"
                  class="px-4 py-2.5 text-sm font-medium text-gray-600 hover:text-gray-800"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  :disabled="!teamCode || isSubmitting"
                  class="flex-1 px-4 py-2.5 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition"
                >
                  {{ isSubmitting ? 'Validating...' : 'Activate team' }}
                </button>
              </div>
            </form>
          </div>

          <!-- Validated state -->
          <div
            v-else
            class="flex items-center gap-3 p-3 bg-green-50 border border-green-200 rounded-lg"
          >
            <div
              v-if="!teamValidated"
              class="w-9 h-9 rounded-full bg-green-100 flex items-center justify-center shrink-0"
            >
              <svg
                class="w-5 h-5 text-green-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M5 13l4 4L19 7"
                />
              </svg>
            </div>
            <div
              v-else
              class="w-9 h-9 rounded-full bg-red-100 flex items-center justify-center shrink-0"
            >
              <svg
                class="w-5 h-5 text-red-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </div>
            <div v-if="!teamValidated">
              <p class="text-sm font-medium text-green-900">Team joined successfully</p>
              <p class="text-xs text-green-700">You're now part of the team: {{ joinedTeam }}</p>
            </div>
            <div v-else class="bg-red-50 p-3 rounded-lg">
              <p class="text-sm font-medium text-red-900">The code is not valid or is expired!</p>
              <p class="text-xs text-red-700">
                Type again the code, or ask the administrator of the team to regenerate the invite
                code!
              </p>
              <button class="text-red-900 cursor-pointer" @click="">Back</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Create your own team -->
      <div v-if="createOwnTeam">
        <form @submit.prevent="createTeam" class="space-y-3">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1.5"> Team name </label>
            <input
              v-model="teamName"
              type="text"
              placeholder=" "
              class="w-full px-3.5 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent tracking-wider"
            />
          </div>
          <div class="flex gap-2">
            <button
              type="button"
              @click="toggleCreateOwnTeam"
              class="px-4 py-2.5 text-sm font-medium text-gray-600 hover:text-gray-800"
            >
              Cancel
            </button>
            <button
              type="submit"
              :disabled="!teamName || isSubmitting"
              class="flex-1 px-4 py-2.5 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition"
            >
              {{ isSubmitting ? 'Validating...' : 'Create team' }}
            </button>
          </div>
        </form>
      </div>
      <div v-if="teamCreated" class="mt-2 mb-2 p-2">
        <div>
          <div class="w-9 h-9 rounded-full bg-green-100 flex items-center justify-center shrink-0">
            <svg
              class="w-5 h-5 text-green-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M5 13l4 4L19 7"
              />
            </svg>
          </div>
          <div>
            <p class="text-sm font-medium text-green-900">Team created successfully</p>
            <p class="text-xs text-green-700">You're now part of the team: {{ teamName }}</p>
          </div>
        </div>
      </div>

      <!-- Card 3: Contact -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 mb-6">
        <div class="px-6 py-5 border-b border-gray-100">
          <h2 class="text-lg font-semibold text-gray-900">Contact details</h2>
          <p class="text-sm text-gray-500 mt-0.5">
            Optional — you can fill this in later from your settings
          </p>
        </div>

        <div class="p-6">
          <label class="block text-sm font-medium text-gray-700 mb-1.5"> Phone number </label>
          <div class="relative">
            <span class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
              <svg
                class="w-4 h-4 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"
                />
              </svg>
            </span>
            <input
              v-model="phoneNumber"
              type="tel"
              placeholder="+40 712 345 678"
              class="w-full pl-10 pr-3.5 py-2.5 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
        </div>
      </div>

      <!-- Submit -->
      <div class="flex justify-end gap-3">
        <button
          @click="saveProfile"
          :disabled="isSubmitting && !teamAsigned"
          class="px-5 py-2.5 bg-blue-600 text-white rounded-lg text-sm font-semibold hover:bg-blue-700 disabled:bg-gray-300 transition shadow-sm"
        >
          {{ isSubmitting ? 'Saving...' : 'Complete profile' }}
          <svg
            v-if="isSubmitting"
            class="animate-spin h-5 w-5 text-white ml-2"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              class="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="4"
            ></circle>
            <path
              class="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            ></path>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>
