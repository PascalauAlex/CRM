import { defineStore } from 'pinia'
import {ref} from 'vue'
import api from '@/utils/api.js'


export const useUserStore = defineStore('user',()=>{
  const user = ref({})
  const users = ref([])
  const error = ref('')
  const loading = ref(false)
  const userProfile = ref({})

  async function getUser(){
    try{
      const token = localStorage.getItem('token')

      if (!token){
        throw new Error('No token found. Cannot get the user.')
      }

      const response = await api.get('/api/v1/users/me/', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      user.value = response.data
      


    }catch (err){
      console.error('Error while getting the user',err)
    }
  }


  async function fetchUsers(){
    loading.value = true
    error.value = null

    try{
      const response = await api.get('/api/v1/teams/member/')
      users.value = response.data
    }catch (err){
      error.value = 'Error while getting the users'
      console.error(err,error.value)
    }finally {
      loading.value = false
    }

  }

  async function editUser(userData){
    try{
      const token = localStorage.getItem('token')

      const response = await api.patch(`/api/v1/users/me/`,userData,{
        headers: {
          Authorization : `Bearer ${token}`,
        }
      })
      user.value = response.data

    }catch (err){
      error.value = 'Error while editing the user'
      console.error(err)
      throw err
    }
    finally {
      loading.value = false
    }
  }

  async function getUserProfile(id){
    loading.value = true
    error.value = null

    try{
      const response = await api.get(`/api/v1/user-profile/${id}`)
      userProfile.value = response.data
    }catch (err){
      console.error(err)
    }finally {
      loading.value = false
    }
  }

  async function profile_completed(){
    loading.value = true
    error.value = null

    try{
      const response = await api.get('/api/v1/profile-completed')
    }catch(err){
      console.error(err)
    }finally{
      loading.value = false
    }
  }



  return {
    user,
    getUser,
    users,
    fetchUsers,
    editUser,
    getUserProfile,
    userProfile,
    profile_completed
  }

})
