import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

// 预测接口
export const predictApi = {
  upload: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/predict', formData)
  },
}

// 历史记录接口
export const historyApi = {
  list: (params?: { skip?: number; limit?: number }) => api.get('/history', { params }),
  detail: (id: number) => api.get(`/history/${id}`),
  delete: (id: number) => api.delete(`/history/${id}`),
  batchDelete: (ids: number[]) => api.delete('/history/batch', { data: { ids } }),
}

// 统计接口
export const statsApi = {
  overview: () => api.get('/stats'),
  trend: (params?: { start_date?: string; end_date?: string; granularity?: string }) =>
    api.get('/stats/trend', { params }),
}

export default api