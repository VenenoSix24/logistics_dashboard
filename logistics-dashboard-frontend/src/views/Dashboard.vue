<template>
  <div class="dashboard-layout">
    <!-- 顶部 Header -->
    <el-header class="main-header">
      <div class="header-title">物流数据仪表盘</div>
    </el-header>

    <!-- 主内容区 -->
    <el-main class="main-content">
      <!-- 筛选区域 -->
      <el-card shadow="never" class="filter-card">
        <el-form :inline="true" :model="filterParams" class="filter-form">
          <el-form-item label="承运商">
            <el-select v-model="filterParams.carrier" placeholder="选择承运商" clearable>
              <el-option v-for="item in filterOptions.carriers" :key="item" :label="item" :value="item" />
            </el-select>
          </el-form-item>
          <el-form-item label="始发省份">
            <el-select v-model="filterParams.source_province" placeholder="选择始发省份" clearable>
              <el-option v-for="item in filterOptions.source_provinces" :key="item" :label="item" :value="item" />
            </el-select>
          </el-form-item>
          <el-form-item label="目的省份">
            <el-select v-model="filterParams.destination_province" placeholder="选择目的省份" clearable>
              <el-option v-for="item in filterOptions.destination_provinces" :key="item" :label="item" :value="item" />
            </el-select>
          </el-form-item>
          <el-form-item label="货物类别">
            <el-select v-model="filterParams.category_name" placeholder="选择或点击图表" clearable>
              <el-option v-for="item in filterOptions.categories" :key="item" :label="item" :value="item" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">查询</el-button>
            <el-button class="secondary-button" @click="resetFilters">重置</el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <!-- KPI 指标 -->
      <el-row :gutter="20" class="kpi-row">
        <el-col :span="6">
          <el-card shadow="always" class="kpi-card">
            <el-statistic :value="(kpiData.order_fulfillment_rate || 0) * 100" :precision="2">
              <template #title>
                <div class="kpi-title">订单履约率</div>
              </template>
              <template #suffix>%</template>
            </el-statistic>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="always" class="kpi-card">
            <el-statistic :value="(kpiData.average_loading_rate || 0) * 100" :precision="2">
              <template #title>
                <div class="kpi-title">平均车辆装载率</div>
              </template>
              <template #suffix>%</template>
            </el-statistic>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="always" class="kpi-card">
            <el-statistic :value="kpiData.average_cost_per_kg || 0" :precision="2">
              <template #title>
                <div class="kpi-title">单位重量运输成本</div>
              </template>
              <template #suffix>/kg</template>
            </el-statistic>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="always" class="kpi-card">
            <el-statistic :value="kpiData.total_carbon_emission || 0" :precision="2" group-separator=",">
               <template #title>
                <div class="kpi-title">碳排放总量 (kg)</div>
              </template>
            </el-statistic>
          </el-card>
        </el-col>
      </el-row>

      <!-- 新增KPI行 -->
      <el-row :gutter="20" class="kpi-row" style="margin-top: 20px;">
        <el-col :span="6">
          <el-card shadow="always" class="kpi-card">
            <el-statistic :value="kpiData.total_profit || 0" :precision="2" group-separator=",">
              <template #title>
                <div class="kpi-title">总利润</div>
              </template>
              <template #prefix>¥</template>
            </el-statistic>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="always" class="kpi-card">
            <el-statistic :value="kpiData.avg_profit_per_order || 0" :precision="2">
              <template #title>
                <div class="kpi-title">平均每单利润</div>
              </template>
              <template #prefix>¥</template>
            </el-statistic>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="always" class="kpi-card">
            <el-statistic :value="(kpiData.cs_issue_rate || 0) * 100" :precision="2">
              <template #title>
                <div class="kpi-title">客户服务问题率</div>
              </template>
              <template #suffix>%</template>
            </el-statistic>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="always" class="kpi-card">
            <el-statistic :value="kpiData.avg_customer_rating || 0" :precision="2">
              <template #title>
                <div class="kpi-title">平均客户评分</div>
              </template>
            </el-statistic>
          </el-card>
        </el-col>
      </el-row>

      <!-- 图表和预测 -->
      <el-row :gutter="20" style="margin-top: 20px;">
        <el-col :span="12">
          <el-card shadow="hover" body-style="height: 420px">
            <v-chart class="chart" :option="lineChartOption" autoresize />
          </el-card>
        </el-col>
        <el-col :span="7">
          <el-card shadow="hover" body-style="height: 420px">
            <v-chart class="chart" :option="pieChartOption" autoresize @click="handlePieChartClick" />
          </el-card>
        </el-col>
        <el-col :span="5">
          <el-card shadow="hover" body-style="height: 420px; display: flex; flex-direction: column;">
            <div class="prediction-container">
              <h4>运输时效预测</h4>
              <el-form @submit.prevent="handlePrediction" class="prediction-form">
                <el-form-item label="运输距离 (km)">
                  <el-input-number v-model="predictionDistance" :min="1" :controls="false" style="width: 100%;" />
                </el-form-item>
                <el-button type="primary" @click="handlePrediction" :loading="isPredicting" style="width: 100%;">
                  {{ isPredicting ? '计算中...' : '智能预测' }}
                </el-button>
              </el-form>
              <div v-if="predictionResult" class="prediction-result">
                <el-alert
                  :title="`预测结果：约 ${predictionResult.predicted_days} 天`"
                  type="success"
                  :closable="false"
                >
                  <p>对于 <strong>{{ predictionResult.input_distance_km }}</strong> 公里的运输，大约需要 <strong>{{ predictionResult.predicted_hours }}</strong> 小时。</p>
                </el-alert>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 数据表格 -->
      <el-row style="margin-top: 20px;">
        <el-col :span="24">
          <el-card shadow="hover">
            <template #header>
              <div class="card-header">
                <span>订单列表</span>
              </div>
            </template>
            <el-table :data="tableData" stripe v-loading="tableLoading" height="500" style="width: 100%">
              <el-table-column prop="order_id" label="订单ID" width="150" fixed />
              <el-table-column prop="order_date" label="下单日期" width="180" />
              <el-table-column prop="carrier" label="承运商" />
              <el-table-column prop="source_city" label="始发市" width="120" />
              <el-table-column prop="destination_city" label="目的市" width="120" />
              <el-table-column prop="category_name" label="货物类别" />
              <el-table-column prop="total_cost" label="总成本 (元)" />
              <el-table-column prop="is_on_time" label="是否准时" width="100">
                <template #default="scope">
                  <el-tag :type="scope.row.is_on_time ? 'success' : 'danger'">
                    {{ scope.row.is_on_time ? '是' : '否' }}
                  </el-tag>
                </template>
              </el-table-column>
            </el-table>
            <div class="pagination-container">
              <el-pagination
                background
                layout="total, sizes, prev, pager, next, jumper"
                :total="totalOrders"
                v-model:current-page="currentPage"
                v-model:page-size="pageSize"
                :page-sizes="[50, 100, 200, 500]"
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
              />
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-main>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import axios from 'axios';
import { ElMessage } from 'element-plus';
import * as echarts from 'echarts';

// --- 状态定义 ---
const kpiData = ref({});
const chartData = ref({});
const tableData = ref([]); 
const tableLoading = ref(true);
const currentPage = ref(1);
const pageSize = ref(100);
const totalOrders = ref(0);

const filterOptions = ref({
  carriers: [],
  source_provinces: [],
  destination_provinces: [],
  categories: [],
});
const filterParams = reactive({
  carrier: '',
  source_province: '',
  destination_province: '',
  category_name: '',
});

const predictionDistance = ref(null);
const predictionResult = ref(null);
const isPredicting = ref(false);

// --- ECharts Option 定义 ---
const lineChartOption = computed(() => ({
  title: { text: '出库订单量趋势', textStyle: { fontWeight: 'normal', fontSize: 16, color: '#1f2937' } },
  tooltip: { trigger: 'axis' },
  xAxis: { 
    type: 'category', 
    data: chartData.value.daily_orders?.dates || [],
    axisLine: { lineStyle: { color: '#6b7280' } },
    axisLabel: { color: '#6b7280' }
  },
  yAxis: { 
    type: 'value',
    axisLine: { show: true, lineStyle: { color: '#e5e7eb' } },
    axisLabel: { color: '#6b7280' },
    splitLine: { lineStyle: { color: '#e5e7eb', type: 'dashed' } }
  },
  grid: { top: '20%', left: '3%', right: '4%', bottom: '3%', containLabel: true },
  series: [{
    data: chartData.value.daily_orders?.counts || [],
    type: 'line',
    smooth: true,
    symbol: 'none',
    lineStyle: { color: '#00C4B4', width: 3 },
    areaStyle: {
      color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
        { offset: 0, color: 'rgba(0, 196, 180, 0.4)' },
        { offset: 1, color: 'rgba(0, 196, 180, 0)' }
      ])
    }
  }],
}));

const pieChartOption = computed(() => ({
  title: { text: '货物类别占比', subtext: '(可点击筛选)', left: 'center', textStyle: { fontWeight: 'normal', fontSize: 16, color: '#1f2937' } },
  tooltip: { trigger: 'item', formatter: '{a} <br/>{b}: {c} ({d}%)' },
  legend: { orient: 'vertical', left: 'left', top: '15%', textStyle: { color: '#6b7280' } },
  color: ['#00C4B4', '#5470C6', '#91CC75', '#FAC858', '#EE6666', '#73C0DE'],
  series: [{
    name: '货物类别',
    type: 'pie',
    radius: ['45%', '70%'],
    center: ['50%', '60%'],
    avoidLabelOverlap: false,
    itemStyle: {
      borderRadius: 10,
      borderColor: '#fff',
      borderWidth: 2
    },
    label: { show: false, position: 'center' },
    emphasis: { label: { show: true, fontSize: '20', fontWeight: 'bold' } },
    labelLine: { show: false },
    data: chartData.value.category_percentage || [],
  }],
}));

// --- API 请求函数 ---
const fetchData = async () => {
  tableLoading.value = true;
  try {
    const [dashboardRes, ordersRes] = await Promise.all([
      axios.get('http://127.0.0.1:8000/api/v1/dashboard', { params: filterParams }),
      axios.get('http://127.0.0.1:8000/api/v1/orders', {
        params: {
          page: currentPage.value,
          pageSize: pageSize.value,
          ...filterParams,
        },
      })
    ]);
    
    kpiData.value = dashboardRes.data.kpi_data;
    chartData.value = dashboardRes.data.chart_data; // 恢复被误删的图表数据赋值
    tableData.value = ordersRes.data.orders;
    totalOrders.value = ordersRes.data.total;

  } catch (error) {
    console.error("获取数据失败:", error);
    ElMessage.error('数据加载失败，请检查网络或联系管理员。');
    kpiData.value = {};
    tableData.value = [];
    totalOrders.value = 0;
  } finally {
    tableLoading.value = false;
  }
};

const fetchFilterOptions = async () => {
    try {
        const response = await axios.get('http://127.0.0.1:8000/api/v1/filter-options');
        filterOptions.value = response.data;
    } catch (error) { console.error("获取筛选器选项失败:", error); }
}

const handlePrediction = async () => {
  if (!predictionDistance.value) {
    ElMessage({ type: 'warning', message: '请输入运输距离！' });
    return;
  }
  isPredicting.value = true;
  predictionResult.value = null;
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/v1/predict', {
      params: { distance_km: predictionDistance.value },
    });
    predictionResult.value = response.data;
  } catch (error) {
    console.error("预测失败:", error);
    ElMessage.error('预测服务出现异常，请稍后再试。');
  } finally {
    isPredicting.value = false;
  }
};

// --- 事件处理函数 ---
const handleSizeChange = (newSize) => {
  pageSize.value = newSize;
  currentPage.value = 1;
  fetchData();
};

const handleCurrentChange = (newPage) => {
  currentPage.value = newPage;
  fetchData();
};

const handlePieChartClick = (params) => {
  if (params.name) {
    filterParams.category_name = params.name;
    handleSearch();
  }
};

const handleSearch = () => {
  currentPage.value = 1; 
  fetchData();
};

const resetFilters = () => {
  filterParams.carrier = '';
  filterParams.source_province = '';
  filterParams.destination_province = '';
  filterParams.category_name = '';
  handleSearch(); 
};

// --- 生命周期钩子 ---
onMounted(() => {
  fetchFilterOptions();
  fetchData(); 
});
</script>

<style scoped>
:root {
  --primary-color: #00C4B4;
  --primary-color-dark: #00A396;
  --primary-color-light: #E6F9F7;
  --background-color: #f7f8fa;
  --card-background-color: #ffffff;
  --text-color-primary: #1f2937;
  --text-color-secondary: #6b7280;
  --border-color: #e5e7eb;

  /* -- 覆盖 ElementPlus 主题色 -- */
  --el-color-primary: var(--primary-color);
}

.dashboard-layout {
  width: 100%;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

.main-header {
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: var(--card-background-color);
  border-bottom: 1px solid var(--border-color);
  height: 64px;
}

.header-title {
  font-size: 22px;
  font-weight: 600;
  color: var(--text-color-primary);
}

.main-content {
  background-color: var(--background-color);
  padding: 24px;
}

.filter-card {
  margin-bottom: 24px;
  background-color: var(--card-background-color);
  border: 1px solid var(--border-color);
  border-radius: 12px;
}

.filter-form .el-form-item {
  margin-bottom: 0;
}

.filter-form .el-select {
  width: 220px;
}

.secondary-button {
  background-color: var(--card-background-color);
  border-color: var(--border-color);
  color: var(--text-color-primary);
}
.secondary-button:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
  background-color: var(--primary-color-light);
}

.kpi-row {
  --el-border-radius-base: 16px;
}

.kpi-card {
  border: 1px solid transparent;
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.kpi-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05);
}

.kpi-title {
  color: var(--text-color-secondary);
  font-size: 15px;
  font-weight: 500;
}

:deep(.kpi-card .el-statistic__content) {
  font-size: 28px;
  font-weight: 700;
  color: var(--primary-color);
}

.el-card {
  border-radius: 12px;
  border: 1px solid var(--border-color);
}

.chart {
  height: 100%;
  width: 100%;
}

.prediction-container h4 {
  text-align: center;
  margin-top: 10px;
  margin-bottom: 20px;
  color: var(--text-color-primary);
  font-weight: 600;
}

.prediction-result p {
  margin: 5px 0 0;
  font-size: 12px;
}

.pagination-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}
</style>