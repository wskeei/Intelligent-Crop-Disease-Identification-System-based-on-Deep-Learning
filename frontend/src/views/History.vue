<template>
  <div class="history-page">
    <h2>历史记录</h2>
    
    <el-card>
      <template #header>
        <div class="header-actions">
          <span>共 {{ total }} 条记录</span>
          <el-button type="danger" :disabled="!selectedIds.length" @click="handleBatchDelete">
            批量删除 ({{ selectedIds.length }})
          </el-button>
        </div>
      </template>
      
      <el-table :data="records" @selection-change="handleSelectionChange" v-loading="loading">
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
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { historyApi } from '@/api'
import type { PredictionRecord } from '@/types'

const records = ref<PredictionRecord[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)
const loading = ref(false)
const selectedIds = ref<number[]>([])

const fetchData = async () => {
  loading.value = true
  try {
    const { data } = await historyApi.list({
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value,
    })
    records.value = data
    total.value = data.length < pageSize.value ? 
      (currentPage.value - 1) * pageSize.value + data.length : 
      currentPage.value * pageSize.value + 1
  } finally {
    loading.value = false
  }
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
.history-page h2 {
  margin-bottom: 24px;
}
.header-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>