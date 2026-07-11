import { createRouter, createWebHistory } from 'vue-router'
import SignUp from '@/view/Authentificate/SignUp.vue'
import LogIn from '@/view/Authentificate/LogIn.vue'
import MyAccount from '@/view/dashboard/MyAccount.vue'
import { useAuthStore } from '@/stores/auth.js'
import PageNotFound from '@/components/PageNotFound.vue'
import LeadsView from '@/view/Leads/LeadsView.vue'
import HomePage from '@/view/HomePage.vue'
import SingleLead from '@/view/Leads/SingleLead.vue'
import EditLead from '@/view/Leads/EditLead.vue'
import AddTeam from '@/view/Team/AddTeam.vue'
import TeamView from '@/view/Team/TeamView.vue'
import AddMember from '@/view/Team/AddMember.vue'


const params = ''


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage,
      meta: { title: 'Home' },
    },
    {
      path: '/sign-up',
      name: 'SignUp',
      component: SignUp,
      meta: { guestOnly: true, title: 'SignUp' },
    },
    {
      path: '/log-in',
      name: 'LogIn',
      component: LogIn,
      meta: { guestOnly: true, title: 'Log In' }, //only unlogged members can see this page
    },
    {
      path: '/auth/success',
      component: () => import('@/view/Authentificate/AuthSuccess.vue'),
    },
    {
      path: '/set-user-profile/:username',
      name:"SetUserProfile",
      component: () => import('@/view/Authentificate/UserProfile.vue'),
      meta: { title: 'Configure your profile', hideNavbar: true },
    },
    {
      path: '/dashboard',
      name: 'DashboardView',
      //lazy initialization
      component: () => import('@/view/dashboard/DashboardView.vue'),
      meta: { requiresAuth: true, title: 'Dashboard' },
    },
    {
      path: '/dashboard/my-account',
      name: 'MyAccount',
      component: MyAccount,
      meta: { requiresAuth: true, title: 'MyAccount' },
    },
    {
      path: '/dashboard/leads',
      name: 'LeadsView',
      component: LeadsView,
      meta: { requiresAuth: true, title: 'Leads' },
    },
    {
      path: '/dashboard/lead/:id',
      name: 'SingleLead',
      component: SingleLead,
      meta: { requiresAuth: true, title: 'Lead Details' },
    },
    {
      path: '/dashboard/lead/:id/edit',
      name: 'EditLead',
      component: EditLead,
      meta: { requiresAuth: true, title: 'Edit lead' },
    },
    {
      path: '/dashboard/add-team',
      name: 'AddTeam',
      component: AddTeam,
      meta: { requiresAuth: true, title: 'Add Team' },
    },
    {
      path: '/dashboard/team',
      name: 'TeamView',
      component: TeamView,
      meta: { requiresAuth: true, title: 'Teams' },
    },
    {
      path: '/dashboard/team/add-member',
      name: 'AddMember',
      component: AddMember,
      meta: { requiresAuth: true, title: 'Add member' },
    },
    {
      path: '/clients',
      name: 'Clients',
      component: () => import('@/view/Clients/ClientView.vue'),
      meta: { requiresAuth: true, title: 'Clients' },
    },
    {
      path: '/clients/add-client',
      name: 'AddClient',
      component: () => import('@/view/Clients/AddClient.vue'),
      meta: { requiresAuth: true, title: 'Add Client' },
    },
    {
      path: '/clients/:id',
      name: 'SingleClient',
      component: () => import('@/view/Clients/SingleClient.vue'),
      meta: { requiresAuth: true, title: 'Client Details' },
    },
    {
      path: '/clients/:id/edit',
      name: 'EditClient',
      component: () => import('@/view/Clients/EditClient.vue'),
      meta: { requiresAuth: true, title: 'Edit Client' },
    },
    {
      path: '/clients/add-note/:id',
      name: 'AddNote',
      component: () => import('@/view/Clients/AddNote.vue'),
      meta: { requiresAuth: true, title: 'Add Note' },
    },
    {
      path: '/clients/:id/edit-note/:note_id',
      name: 'EditNote',
      component: () => import('@/view/Clients/EditNote.vue'),
      meta: { requiresAuth: true, title: 'Edit note' },
    },
    {
      path: '/dashboard/my-account/edit-profile',
      name: 'EditProfile',
      component: () => import('@/view/dashboard/EditProfile.vue'),
      meta: { requiresAuth: true, title: 'Edit profile' },
    },
    {
      path: '/lead/add-note/:id',
      name: 'AddLeadNote',
      component: () => import('@/view/Leads/AddLeadNote.vue'),
      meta: { requiresAuth: true, title: 'Add Lead Note' },
    },
    {
      path: '/calendar',
      name: 'Calendar',
      component: () => import('@/view/Calendar/CalendarView.vue'),
      meta: { requiresAuth: true, title: 'Calendar' },
    },
    {
      path: '/tasks',
      name: 'Tasks',
      component: () => import('@/view/Tasks/TasksView.vue'),
      meta: { requiresAuth: true, title: 'Tasks' },
    },
    {
      path: '/products',
      name: 'Products',
      component: () => import('@/view/Products/ProductsView.vue'),
      meta: {requiresAuth: true, title: 'Products'}
    },
    {
      path: '/product/:id',
      name: 'SingleProduct',
      component: () => import('@/view/Products/SingleProduct.vue'),
      meta: {requiresAuth: true, title: 'Product Details'}
    },
    {
      path: '/product/:id/edit',
      name: 'EditProduct',
      component: () => import('@/view/Products/EditProduct.vue'),
      meta: {requiresAuth: true, title: 'Edit Product'}
    },
    {
      path: '/team/member/',
      name:"SingleMember",
      component: () => import('@/view/Team/SingleMember.vue'),
      meta: {requiresAuth: true,title: 'Single Member'}
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'PageNotFound',
      component: PageNotFound,
    },
  ],
})

router.beforeEach((to, from, next) => {

  const authStore = useAuthStore()

  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth)
  const isAuthenticated = authStore.token

  document.title = to.meta.title || "CRM"

  if (requiresAuth && !isAuthenticated) {

    next('/log-in')
  } else if (to.path === '/log-in'  && isAuthenticated) {

    next('/dashboard')
  }
  /*Sign-up nu este disponibil pentru userii autentificati
  * pentru a putea acesa aceasta pagina trebuie sa se fac logout */
  else if (to.path === '/sign-up' && isAuthenticated){
    next('/dashboard')
  }
  else {

    next()
  }



})


export default router
