import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: () => import('@/layouts/AppLayout.vue'),
      children: [
        { path: '', name: 'Dashboard', component: () => import('@/views/Dashboard.vue') },
        { path: 'predict', name: 'Predict', component: () => import('@/views/Predict.vue') },
        { path: 'history', name: 'History', component: () => import('@/views/History.vue') },
        { path: 'analytics', name: 'Analytics', component: () => import('@/views/Analytics.vue') },
        { path: 'diseases', name: 'Diseases', component: () => import('@/views/Diseases.vue') },
        { path: 'diseases/:id', name: 'DiseaseDetail', component: () => import('@/views/DiseaseDetail.vue') },
        { path: 'settings', name: 'Settings', component: () => import('@/views/Settings.vue') },
      ],
    },
    { path: '/:pathMatch(.*)*', name: 'NotFound', component: () => import('@/views/NotFound.vue') },
  ],
})

export default router