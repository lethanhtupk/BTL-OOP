import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  mode: 'hash',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      component: () => import('@/views/dashboard/Index'),
      children: [
        // Traansactions
        {
          name: 'Giao dịch',
          path: '',
          component: () => import('@/views/dashboard/component/Transactions'),
        },
        {
          name: 'Thống kê',
          path: 'components/report',
          component: () => import('@/views/dashboard/component/Report'),
        },
        {
          name: 'Danh mục',
          path: 'components/categories',
          component: () => import('@/views/dashboard/component/Categories'),
        },
        {
          name: 'Tài khoản',
          path: 'components/account',
          component: () => import('@/views/dashboard/component/Account'),
        },
        {
          name: 'Ví tiền',
          path: 'components/wallet',
          component: () => import('@/views/dashboard/component/Wallet'),
        },
      ],
    },
  ],
})
