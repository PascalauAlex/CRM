<template>
  <div class="max-w-4xl mx-auto max-h-[80vh] overflow-y-auto pr-2">
    <!-- Header -->
    <div class="bg-white shadow-sm rounded-lg mb-6 px-6 py-4 border border-gray-200">
      <div class="flex items-center justify-between">
        <div class="justify-items-center align-center">
          <h1 class="text-2xl font-bold text-gray-900">Add New Lead</h1>
        </div>
      </div>
    </div>

    <!-- Form -->
    <form @submit.prevent="onSubmit" class="space-y-6">
      <!-- Company Information -->
      <div class="bg-white shadow-sm rounded-lg border border-gray-200 overflow-hidden">
        <div class="bg-blue-50 from-blue-50 to-indigo-50 px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-semibold text-gray-900 flex items-center">
            <svg
              class="w-5 h-5 mr-2 text-blue-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
              />
            </svg>
            Company Information
          </h2>
          <p class="text-sm text-gray-600 mt-1">Details about the company or organization</p>
        </div>

        <div class="px-6 py-3 space-y-5">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Company Name -->
            <div>
              <label for="company" class="block text-sm font-medium text-gray-700 mb-2">
                Company Name <span class="text-red-500">*</span>
              </label>
              <input
                type="text"
                v-model="company"
                id="company"
                placeholder="Acme Corporation"
                required
                class="w-full px-4 py-2.5 text-gray-900 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 placeholder:text-gray-400"
              />
            </div>

            <!-- Website -->
            <div>
              <label for="website" class="block text-sm font-medium text-gray-700 mb-2">
                Website
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg
                    class="h-5 w-5 text-gray-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9"
                    />
                  </svg>
                </div>
                <input
                  type="url"
                  v-model="website"
                  id="website"
                  placeholder="https://example.com"
                  class="w-full pl-10 pr-4 py-2.5 text-gray-900 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 placeholder:text-gray-400"
                />
              </div>
            </div>
          </div>

          <!-- Estimated Value -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label for="estimated_value" class="block text-sm font-medium text-gray-700 mb-2">
                Source
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <img src="/icons/circle-bottom-up-svgrepo-com.svg" alt="icon" class="w-5 h-5" />
                </div>
                <input
                  type="text"
                  v-model="source"
                  id="source"
                  placeholder="Website, Call, Email"
                  step="0.01"
                  required
                  class="w-full pl-14 pr-4 py-2.5 text-gray-900 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 placeholder:text-gray-400"
                />
              </div>
              <p class="mt-1.5 text-xs text-gray-500">Source of lead</p>
            </div>

            <!-- CUI / Fiscal Identification -->
            <div>
              <label for="cui" class="block text-sm font-medium text-gray-700 mb-2">
                CUI / CIF <span class="text-red-500">*</span>
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg
                    class="h-5 w-5 text-gray-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                    />
                  </svg>
                </div>
                <input
                  type="text"
                  v-model="cui"
                  id="cui"
                  placeholder="RO12345678"
                  class="w-full pl-10 pr-4 py-2.5 text-gray-900 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 placeholder:text-gray-400"
                />
              </div>
              <p class="mt-1.5 text-xs text-gray-500">Fiscal identification</p>
            </div>
          </div>
        </div>
      </div>

      <div>
        <div class="bg-white shadow-sm rounded-lg border border-gray-200 overflow-hidden">
          <div class="bg-yellow-50 from-yellow-50 to-orange-50 px-6 py-4 border-b border-gray-200">
            <h2 class="text-lg font-semibold text-gray-900 flex items-center">
              <svg
                class="w-5 h-5 mr-2 text-yellow-500"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M21 7.5l-9-5.25L3 7.5m18 0l-9 5.25m9-5.25v9l-9 5.25M3 7.5l9 5.25M3 7.5v9l9 5.25m0-9v9"
                />
              </svg>
              Products or Services
            </h2>
            <p class="text-sm text-gray-600 mt-1">Lead products interest</p>
          </div>

          <div class="px-6 py-3 space-y-5">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label for="category" class="block text-sm font-medium text-gray-700 mb-2">
                  Category <span class="text-red-500">*</span>
                </label>
                <select class="border-gray-300 rounded-lg w-full" v-model="category">
                  <option disabled selected>Select category</option>
                  <option value="product">Product</option>
                  <option value="service">Service</option>
                </select>
              </div>
              <div>
                <label for="product" class="block text-sm font-medium text-gray-700 mb-2">
                  Product <span class="text-red-500">*</span>
                </label>
                <select
                  class="border-gray-300 rounded-lg w-full"
                  v-model="selectedProduct"
                  @change="addProductToLead"
                >
                  <option :value="null" disabled>Select a product</option>
                  <option v-for="item in productsByCategory(category)" :key="item.id" :value="item">
                    [{{ item.sku }}] {{ item.name }} -- ({{ item.base_price }} {{ item.currency }})
                  </option>
                </select>
              </div>

              <div class="w-full">
                <ul class="mt-3 space-y-1">
                  <li
                    v-for="item in leadInterest"
                    :key="item.product.id"
                    class="flex items-center justify-between"
                  >
                    <span class="w-full"
                      ><span class="bg-yellow-100 rounded-lg p-2">{{ item.product.name }}</span> ×
                      {{ item.quantity }}</span
                    >
                    <button
                      type="button"
                      @click="removeFromCart(item.product.id)"
                      class="text-red-500 cursor-pointer"
                    >
                      x
                    </button>
                    <label class="ml-3 mr-3">Discount</label>
                    <input
                      v-model="item.discount"
                      @input="limiteazaDiscount(item)"
                      class="border-gray0399 rounded-lg w-1/2"
                      type="number"
                      placeholder="%"
                      max="100"
                      min="0"
                    />
                    <span class="ml-20">Value {{ lineTotal(item) }}</span>
                  </li>
                  <li>Cart total: {{ cartTotal }}</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Contact Details -->
      <div class="bg-white shadow-sm rounded-lg border border-gray-200 overflow-hidden">
        <div class="bg-green-50 from-green-50 to-emerald-50 px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-semibold text-gray-900 flex items-center">
            <svg
              class="w-5 h-5 mr-2 text-green-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
              />
            </svg>
            Contact Details
          </h2>
          <p class="text-sm text-gray-600 mt-1">Primary contact person information</p>
        </div>

        <div class="px-6 py-3 space-y-5">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Contact Person -->
            <div>
              <label for="contact_person" class="block text-sm font-medium text-gray-700 mb-2">
                Contact Person <span class="text-red-500">*</span>
              </label>
              <input
                type="text"
                v-model="contact_person"
                id="contact_person"
                placeholder="John Doe"
                required
                class="w-full px-4 py-2.5 text-gray-900 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200 placeholder:text-gray-400"
              />
            </div>

            <!-- Phone -->
            <div>
              <label for="phone" class="block text-sm font-medium text-gray-700 mb-2">
                Phone Number <span class="text-red-500">*</span>
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg
                    class="h-5 w-5 text-gray-400"
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
                </div>
                <input
                  type="tel"
                  v-model="phone"
                  id="phone"
                  placeholder="+40 721 234 567"
                  required
                  class="w-full pl-10 pr-4 py-2.5 text-gray-900 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200 placeholder:text-gray-400"
                />
              </div>
            </div>
          </div>

          <!-- Email -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
              Email Address <span class="text-red-500">*</span>
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg
                  class="h-5 w-5 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                  />
                </svg>
              </div>
              <input
                type="email"
                v-model="email"
                id="email"
                required
                placeholder="john.doe@example.com"
                class="w-full pl-10 pr-4 py-2.5 text-gray-900 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200 placeholder:text-gray-400"
              />
            </div>
            <p class="mt-1.5 text-xs text-gray-500">
              This email will be used for all communications
            </p>
          </div>
        </div>
      </div>

      <!-- Assignment -->
      <div class="bg-white shadow-sm rounded-lg border border-gray-200 overflow-hidden">
        <div class="bg-linear-to-r from-purple-50 to-pink-50 px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-semibold text-gray-900 flex items-center">
            <svg
              class="w-5 h-5 mr-2 text-purple-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
              />
            </svg>
            Assignment
          </h2>
          <p class="text-sm text-gray-600 mt-1">Assign this lead to a team member</p>
        </div>

        <div class="px-6 py-5">
          <div class="max-w-md">
            <label for="assigned_to" class="block text-sm font-medium text-gray-700 mb-2">
              Assign to Team Member <span class="text-red-500">*</span>
            </label>
            <div class="relative">
              <select
                id="assigned_to"
                v-model="assigned_to"
                required
                class="block w-full px-4 py-2.5 text-gray-900 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200 appearance-none cursor-pointer"
              >
                <option value="" disabled selected>Choose a team member</option>
                <option
                  v-for="member in teamStore.team.members"
                  :key="member.id"
                  :value="member.id"
                >
                  {{ member.first_name }} {{ member.last_name }}
                </option>
              </select>
              <div class="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
                <svg
                  class="h-5 w-5 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M19 9l-7 7-7-7"
                  />
                </svg>
              </div>
            </div>
            <p class="mt-1.5 text-xs text-gray-500">
              The assigned member will receive notifications
            </p>
          </div>
        </div>
      </div>

      <div class="bg-white shadow-sm rounded-lg border border-gray-200 overflow-hidden">
        <div class="bg-orange-50 px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-semibold text-gray-900 flex items-center">
            <svg
              class="w-5 h-5 mr-2 text-orange-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
              />
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
              />
            </svg>
            Address Information
          </h2>
          <p class="text-sm text-gray-600 mt-1">Company or contact address details</p>
        </div>

        <div class="px-6 py-3 space-y-5">
          <!-- Country & County -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label for="country" class="block text-sm font-medium text-gray-700 mb-2">
                Country</label
              >
              <select
                id="country"
                v-model="address.country"
                required
                class="block w-full px-4 py-2.5 text-gray-900 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200 appearance-none cursor-pointer"
              >
                <option value="" disabled>Select country</option>
                <option v-for="country in countries" :key="country.code" :value="country.code">
                  {{ country.name }}
                </option>
              </select>
            </div>

            <div>
              <label for="county" class="block text-sm font-medium text-gray-700 mb-2">
                County
              </label>
              <input
                type="text"
                v-model="address.county"
                id="county"
                placeholder="Cluj"
                class="w-full px-4 py-2.5 text-gray-900 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200 placeholder:text-gray-400"
              />
            </div>
          </div>

          <!-- City & Zipcode -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label for="city" class="block text-sm font-medium text-gray-700 mb-2"> City </label>
              <input
                type="text"
                v-model="address.city"
                id="city"
                placeholder="Cluj-Napoca"
                class="w-full px-4 py-2.5 text-gray-900 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200 placeholder:text-gray-400"
              />
            </div>

            <div>
              <label for="zipcode" class="block text-sm font-medium text-gray-700 mb-2">
                Zipcode / Cod Poștal
              </label>
              <input
                type="text"
                v-model="address.zipcode"
                id="zipcode"
                placeholder="400000"
                class="w-full px-4 py-2.5 text-gray-900 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200 placeholder:text-gray-400"
              />
            </div>
          </div>

          <!-- Street & Street Number -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div class="md:col-span-2">
              <label for="street" class="block text-sm font-medium text-gray-700 mb-2">
                Street / Strada
              </label>
              <input
                type="text"
                v-model="address.street"
                id="street"
                placeholder="Calea Turzii"
                class="w-full px-4 py-2.5 text-gray-900 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200 placeholder:text-gray-400"
              />
            </div>

            <div>
              <label for="street_number" class="block text-sm font-medium text-gray-700 mb-2">
                Number / Nr.
              </label>
              <input
                type="text"
                v-model="address.street_number"
                id="street_number"
                placeholder="123"
                class="w-full px-4 py-2.5 text-gray-900 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200 placeholder:text-gray-400"
              />
            </div>
          </div>

          <!-- Building, Floor, Apartment -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label for="building" class="block text-sm font-medium text-gray-700 mb-2">
                Building / Bloc <span class="text-xs text-gray-500">(optional)</span>
              </label>
              <input
                type="text"
                v-model="address.building"
                id="building"
                placeholder="A1"
                class="w-full px-4 py-2.5 text-gray-900 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200 placeholder:text-gray-400"
              />
            </div>

            <div>
              <label for="floor" class="block text-sm font-medium text-gray-700 mb-2">
                Floor / Etaj <span class="text-xs text-gray-500">(optional)</span>
              </label>
              <input
                type="text"
                v-model="address.floor"
                id="floor"
                placeholder="3"
                class="w-full px-4 py-2.5 text-gray-900 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200 placeholder:text-gray-400"
              />
            </div>

            <div>
              <label for="apartament_number" class="block text-sm font-medium text-gray-700 mb-2">
                Apartment / Ap. <span class="text-xs text-gray-500">(optional)</span>
              </label>
              <input
                type="text"
                v-model="address.apartment_number"
                id="apartament_number"
                placeholder="12"
                class="w-full px-4 py-2.5 text-gray-900 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all duration-200 placeholder:text-gray-400"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="bg-white shadow-sm rounded-lg border border-gray-200 px-6 py-4">
        <div class="flex items-center justify-between">
          <p class="text-sm text-gray-500"><span class="text-red-500">*</span> Required fields</p>
          <p v-for="err in leadStore.error" :key="err">{{}}</p>
          <div class="flex items-center space-x-3">
            <button
              type="submit"
              class="inline-flex items-center px-6 py-2.5 text-sm font-medium text-white bg-linear-to-r from-blue-600 to-blue-700 rounded-lg hover:from-blue-700 hover:to-blue-800 focus:ring-4 focus:ring-blue-300 shadow-md hover:shadow-lg transition-all duration-200"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M5 13l4 4L19 7"
                />
              </svg>
              Save Lead
            </button>
          </div>
        </div>
      </div>
    </form>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useTeamStore } from '@/stores/teamStore.js'
import { useLeadStore } from '@/stores/leadStore.js'
import { useToast } from 'vue-toast-notification'
import { useRouter } from 'vue-router'
import CountryISOCodes from '@/utils/CountryISOCodes.js'
import { useProductStore } from '@/stores/productStore.js'

// Lead details
const company = ref('')
const contact_person = ref('')
const email = ref('')
const phone = ref('')
const website = ref('')
const estimated_value = ref('')
const cui = ref('')
const assigned_to = ref('')
const countries = CountryISOCodes
const source = ref('')

//Address details
const address = ref({
  country: '',
  county: '',
  city: '',
  street: '',
  street_number: '',
  building: '',
  floor: '',
  apartment_number: '',
  zipcode: '',
})

const category = ref('')

const teamStore = useTeamStore()
const leadStore = useLeadStore()
const toast = useToast()
const router = useRouter()
const productStore = useProductStore()

onMounted(async () => {
  await teamStore.fetchTeam()
  await productStore.getProducts()
  console.log(productStore.products)
})

const onSubmit = async () => {
  const formData = {
    company: company.value,
    contact_person: contact_person.value,
    email: email.value,
    phone: phone.value,
    website: website.value,
    estimated_value: estimated_value.value,
    assigned_to_id: assigned_to.value,
    address: address.value,
    source: source.value,
    product_interests: leadInterest.value.map((i) => ({
      product: i.product.id,
      quantity: i.quantity,
      estimated_value: i.estimated_value,
      notes: i.notes,
      discount: i.discount,
    })),
  }

  try {
    const newLead = await leadStore.addLead(formData)

    if (!newLead) {
      return
    }
    toast.success('New lead added succesfully!')
    await router.push({ name: 'SingleLead', params: { id: newLead.id } })
  } catch (err) {
    console.error('Save failed', err.response?.data)
    toast.error('Failed to add the lead.Please try again.')
  }
}

function productsByCategory(category) {
  if (!category) {
    return []
  }
  if (category === 'product') {
    return productStore.products.filter((p) => p.type === category)
  } else return productStore.products.filter((p) => p.type === category)
}

const selectedProduct = ref(null)
const leadInterest = ref([])

function addProductToLead() {
  if (!selectedProduct.value) {
    return
  }
  const product = selectedProduct.value
  const existing = leadInterest.value.find((i) => i.product.id === product.id)

  if (existing) {
    existing.quantity++
  } else {
    leadInterest.value.push({
      product,
      quantity: 1,
      estimated_value: null,
      notes: '',
      discount: 0,
    })
  }
  selectedProduct.value = null
}

function removeFromCart(productId) {
  leadInterest.value = leadInterest.value.filter((i) => i.product.id !== productId)
}

function lineTotal(item) {
  const price = Number(item.product.base_price)
  const discount = Number(item.discount) || 0
  return price * item.quantity * (1 - discount / 100)
}

const cartTotal = computed(() => leadInterest.value.reduce((sum, item) => sum + lineTotal(item), 0))

const limiteazaDiscount = (item) => {
  if (item.discount > 100) {
    item.discount = 100
  } else if (item.discount < 0) {
    item.discount = 0
  }
}
</script>

<style scoped></style>
