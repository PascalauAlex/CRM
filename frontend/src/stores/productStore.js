import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/utils/api.js'



export const useProductStore = defineStore('products',()=>{
  const products = ref([])
  const categories = ref([])
  const loading = ref(false)
  const error = ref('')
  const product = ref({})
  const leadProduct = ref({})



  async function getProducts(){
    loading.value = true
    error.value = null

    try{
      const response = await api.get('/api/v1/products/')
      products.value = response.data
    }catch (err){
      console.error(err)
    }finally {
      loading.value = false
    }
  }



  async function createProduct(productsData){
    loading.value = true
    error.value = null

    try{
      const reponse = await api.post('/api/v1/products/',productsData)
    }catch (err){
      console.error(err)
    }finally {
      loading.value = false
    }
  }

  async function createCategory(categoryName){
    loading.value = true
    error.value = null

    try{
      const response = await api.post('/api/v1/product-category/',categoryName)

    }catch (err){
      console.error(err)
    }finally {
      loading.value = false
    }
  }

  async function getCategories(){
    loading.value = true
    error.value = null

    try{
      const response = await api.get('/api/v1/product-category/')
      categories.value = response.data
    }catch (err){
      console.error(err)
    }finally {
      loading.value =false
    }
  }

  async function editProduct(product_data,productID){
    loading.value = true
    error.value = null
    try{
      const response = await api.patch(`/api/v1/products/${productID}/`,product_data)

    }catch (err){
      console.error(err)
    }finally {
      loading.value = false
    }
  }

  async function getProductById(productID){
      loading.value = true
      error.value = null
      try {
        const response = await api.get(`/api/v1/products/${productID}/`)
        product.value = response.data
      } catch (err) {
        console.error(err)
      } finally {
        loading.value = false
      }
    }

  async function getLeadProduct(lead){
    loading.value = true
    error.value = null
    try{
      const response = await api.get(`/api/v1/lead-products/`,{params: {lead}})
      leadProduct.value = response.data
    }catch (err){
      console.error(err)
    }finally {
      loading.value = false
    }
  }


  async function addLeadProducts(productData){
    loading.value = true
    error.value = null

    try {
      const response = await api.post('/api/v1/lead-products/',productData)
      leadProduct.value.push(response.data)
    }catch (err){
      console.error('Error while adding a new product to the lead!',err)
    }finally {
      loading.value = false
    }
  }

  async function deleteLeadProductInterest(lead_product_interest_id){
    loading.value = true
    error.value = null

    try{
      const response = await api.delete(`/api/v1/lead-products/${lead_product_interest_id}/`)
    }catch (err){
      console.error(err)
    }
  }



  return {
    products,
    product,
    loading,
    error,
    getProducts,
    createProduct,
    createCategory,
    getCategories,
    categories,
    editProduct,
    getProductById,
    getLeadProduct,
    addLeadProducts,
    leadProduct,
    deleteLeadProductInterest,
  }
})
