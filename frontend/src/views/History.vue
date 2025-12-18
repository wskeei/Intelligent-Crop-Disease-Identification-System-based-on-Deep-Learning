<template>
  <div class="history-page">
    <h2>历史记录</h2>
    
    <!-- 筛选条件区 -->
    <el-card class="filter-card">
      <el-form :inline="true" :model="filters">
        <el-form-item label="病害状态">
          <el-select v-model="filters.status" placeholder="全部" clearable @change="fetchData">
            <el-option label="全部" value="" />
            <el-option label="健康" value="healthy" />
            <el-option label="病害" value="diseased" />
          </el-select>
        </el-form-item>
        <el-form-item label="时间范围">
          <el-date-picker v-model="filters.dateRange" type="daterange" start-placeholder="开始日期" end-placeholder="结束日期" @change="fetchData" />
        </el-form-item>
        <el-form-item label="关键词">
          <el-input v-model="filters.keyword" placeholder="搜索病害名称" clearable @clear="fetchData" @keyup.enter="fetchData" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">搜索</el-button>
          <el-button @click="resetFilters">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card>
      <template #header>
        <div class="header-actions">
          <span>共 {{ total }} 条记录</span>
          <div>
            <el-radio-group v-model="viewMode" size="small" style="margin-right: 16px">
              <el-radio-button value="table">列表</el-radio-button>
              <el-radio-button value="card">卡片</el-radio-button>
            </el-radio-group>
            <el-button type="danger" :disabled="!selectedIds.length" @click="handleBatchDelete">
              批量删除 ({{ selectedIds.length }})
            </el-button>
          </div>
        </div>
      </template>
      
      <!-- 列表视图 -->
      <el-table v-if="viewMode === 'table'" :data="records" @selection-change="handleSelectionChange" v-loading="loading">
        <el-table-column type="selection" width="50" />
        <el-table-column label="图片" width="100">
          <template #default="{ row }">
            <el-image :src="`/uploads/${row.image_path}`" style="width: 60px; height: 60px" fit="cover" />
          </template>
        </el-table-column>
        <el-table-column label="病害名称" prop="predicted_class">
          <template #default="{ row }">
            {{ formatClassName(row.predicted_class) }}
          </template>
        </el-table-column>
        <el-table-column label="置信度" width="180">
          <template #default="{ row }">
            <el-progress :percentage="Math.round(row.confidence * 100)" :stroke-width="10" />
          </template>
        </el-table-column>
        <el-table-column label="识别时间" prop="created_at" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button type="danger" link @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 卡片视图 -->
      <div v-else class="card-view" v-loading="loading">
        <el-checkbox-group v-model="selectedIds">
          <div class="card-grid">
            <div v-for="row in records" :key="row.id" class="record-card">
              <el-checkbox :value="row.id" class="card-checkbox" />
              <el-image :src="`/uploads/${row.image_path}`" fit="cover" class="card-image" />
              <div class="card-info">
                <div class="card-title">{{ formatClassName(row.predicted_class) }}</div>
                <el-progress :percentage="Math.round(row.confidence * 100)" :stroke-width="8" />
                <div class="card-time">{{ formatDate(row.created_at) }}</div>
              </div>
              <el-button type="danger" link size="small" @click="handleDelete(row.id)">删除</el-button>
            </div>
          </div>
        </el-checkbox-group>
      </div>

      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next"
        style="margin-top: 16px"
        @change="fetchData"
      />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { historyApi } from '@/api'
import type { PredictionRecord } from '@/types'

const records = ref<PredictionRecord[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const loading = ref(false)
const selectedIds = ref<number[]>([])
const viewMode = ref<'table' | 'card'>('table')
const filters = reactive({ status: '', dateRange: null as [Date, Date] | null, keyword: '' })

const fetchData = async () => {
  loading.value = true
  try {
    const params: Record<string, unknown> = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value,
    }
    if (filters.status) params.status = filters.status
    if (filters.keyword) params.keyword = filters.keyword
    if (filters.dateRange) {
      params.start_date = filters.dateRange[0].toISOString().split('T')[0]
      params.end_date = filters.dateRange[1].toISOString().split('T')[0]
    }
    const { data } = await historyApi.list(params)
    records.value = data
    total.value = data.length < pageSize.value ?
      (currentPage.value - 1) * pageSize.value + data.length :
      currentPage.value * pageSize.value + 1
  } finally {
    loading.value = false
  }
}

const resetFilters = () => {
  filters.status = ''
  filters.dateRange = null
  filters.keyword = ''
  fetchData()
}

const handleSelectionChange = (rows: PredictionRecord[]) => {
  selectedIds.value = rows.map(r => r.id)
}

const handleDelete = async (id: number) => {
  await ElMessageBox.confirm('确定删除此记录？', '提示')
  await historyApi.delete(id)
  ElMessage.success('删除成功')
  fetchData()
}

const handleBatchDelete = async () => {
  await ElMessageBox.confirm(`确定删除选中的 ${selectedIds.value.length} 条记录？`, '提示')
  await historyApi.batchDelete(selectedIds.value)
  ElMessage.success('删除成功')
  selectedIds.value = []
  fetchData()
}

const formatClassName = (name: string) => name.replace(/___/g, ' - ').replace(/_/g, ' ')
const formatDate = (date: string) => new Date(date).toLocaleString('zh-CN')

onMounted(fetchData)
</script>

<style scoped lang="scss">
.history-page h2 { margin-bottom: 24px; }
.filter-card { margin-bottom: 16px; }
.header-actions { display: flex; justify-content: space-between; align-items: center; }
.card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 16px; }
.record-card { border: 1px solid #eee; border-radius: 8px; padding: 12px; position: relative; }
.card-checkbox { position: absolute; top: 8px; left: 8px; z-index: 1; }
.card-image { width: 100%; height: 120px; border-radius: 4px; }
.card-info { margin-top: 8px; }
.card-title { font-weight: bold; margin-bottom: 8px; font-size: 13px; }
.card-time { font-size: 12px; color: #909399; margin-top: 8px; }
</style>