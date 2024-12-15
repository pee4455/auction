import { createRouter, createWebHistory } from 'vue-router'
import Dashboard from '@/views/Dashboard.vue'
import Auctions from '@/views/Auctions.vue'
import Users from '@/views/Users.vue'
import Register from '@/views/Register.vue'
import RegistrationForm from '@/views/RegistrationForm.vue'
import AdminManagement from '@/views/AdminManagement.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', name: 'Dashboard', component: Dashboard },
    { path: '/auctions', name: 'Auctions', component: Auctions },
    { path: '/users', name: 'Users', component: Users },
    { path: '/register', name: 'Register', component: Register },
    { path: '/registration-form', name: 'RegistrationForm', component: RegistrationForm },
    { 
      path: '/admin-management', 
      name: 'AdminManagement', 
      component: AdminManagement,
      meta: { requiresAuth: true },
      beforeEnter: (to, from, next) => {
        const token = localStorage.getItem('token')
        if (!token) {
          next({ name: 'Login' })
        } else {
          next()
        }
      }
    }
  ]
})

// Navigation guard
router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    const token = localStorage.getItem('token')
    if (!token) {
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router