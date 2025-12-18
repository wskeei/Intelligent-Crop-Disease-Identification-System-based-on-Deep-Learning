// 预测结果
export interface TopPrediction {
  class: string
  confidence: number
}

export interface PredictionResult {
  predicted_class: string
  confidence: number
  image_url: string
  top_predictions: TopPrediction[]
}

// 历史记录
export interface PredictionRecord {
  id: number
  image_path: string
  predicted_class: string
  confidence: number
  created_at: string
}

// 统计数据
export interface StatsOverview {
  total: number
  today_count: number
  healthy_count: number
  diseased_count: number
  healthy_rate: number
  by_class: { class: string; count: number }[]
  by_crop: { crop: string; count: number; healthy: number; diseased: number }[]
}

export interface TrendData {
  date: string
  total: number
  healthy: number
  diseased: number
}