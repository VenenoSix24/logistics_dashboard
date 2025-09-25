# 物流数据仪表盘 (Logistics Data Dashboard)

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white) ![FastAPI](https://img.shields.io/badge/FastAPI-0.117%2B-green?logo=fastapi&logoColor=white) ![Vue.js](https://img.shields.io/badge/Vue.js-6.0.1-brightgreen?logo=vue.js&logoColor=white) ![Vite](https://img.shields.io/badge/Vite-7.1.7-purple?logo=vite&logoColor=white) ![pnpm](https://img.shields.io/badge/pnpm-10.17.0-orange.svg?logo=pnpm)

一份现代化、数据驱动的物流监控与分析仪表盘，旨在提供对复杂物流网络的核心指标的实时洞察。

---

### ✨ 项目预览

![ldf001.png](https://s2.loli.net/2025/09/25/RYdZLSH1m7eGvN2.png)

### 🚀 核心功能

- **多维度KPI监控**: 提供8个核心业务指标的实时统计，覆盖运营、财务和客户满意度：
  - 订单履约率
  - 平均车辆装载率
  - 单位重量运输成本
  - 碳排放总量
  - 总利润
  - 平均每单利润
  - 客户服务问题率
  - 平均客户评分
- **数据可视化图表**: 
  - **出库订单量趋势**: 使用平滑的面积折线图展示每日订单量的变化趋势。
  - **货物类别占比**: 使用环形饼图清晰地展示不同货物类别的分布情况，支持点击图例进行数据筛选。
- **智能筛选与查询**: 支持按承运商、始发/目的省份、货物类别进行组合筛选，所有看板数据实时响应。
- **订单列表**: 以分页表格形式展示详细的订单数据。
- **AI时效预测**: 内置一个基于历史数据训练的简易线性回归模型，可根据运输距离预测大致的运输时效。
- **模拟数据生成**: 提供一个高度可定制的Python脚本，用于生成符合业务逻辑的、逼真的大规模模拟数据。

### 🛠️ 技术栈

#### 后端 (Backend)

- **框架**: [FastAPI](https://fastapi.tiangolo.com/) - 高性能的现代Python Web框架。
- **数据处理**: [Pandas](https://pandas.pydata.org/) & [NumPy](https://numpy.org/) - 用于高效的数据读取、清洗和聚合计算。
- **机器学习**: [Scikit-learn](https://scikit-learn.org/) - 用于训练和使用运输时效预测模型。
- **服务器**: [Uvicorn](https://www.uvicorn.org/) - ASGI服务器，为FastAPI提供动力。

#### 前端 (Frontend)

- **框架**: [Vue.js 3](https://vuejs.org/) (使用 `<script setup>` 语法糖)
- **构建工具**: [Vite](https://vitejs.dev/) - 提供极速的开发服务器和打包体验。
- **UI组件库**: [Element Plus](https://element-plus.org/) - 成熟、强大的企业级Vue 3组件库。
- **图表**: [Apache ECharts](https://echarts.apache.org/) - 功能强大的数据可视化库，通过 `vue-echarts` 集成。
- **HTTP客户端**: [Axios](https://axios-http.com/) - 用于与后端API进行通信。
- **包管理器**: [pnpm](https://pnpm.io/) - 快速、节省磁盘空间的包管理器。

### 本地部署与运行指南

请确保您的本地环境已安装 [Python](https://www.python.org/) (3.10+) 和 [Node.js](https://nodejs.org/) (18.x+)。

#### 1. 后端设置

```bash
# 1. 克隆或下载项目到本地

# 2. 进入项目根目录
cd logistics_dashboard

# 3. 创建并激活Python虚拟环境
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
# python3 -m venv .venv
# source .venv/bin/activate

# 4. 安装后端依赖
pip install fastapi uvicorn[standard] pandas scikit-learn numpy Faker
```

#### 2. 生成模拟数据

在项目根目录下，运行数据生成脚本。这将创建一个名为 `logistics_data_v2.csv` 的文件。

```bash
python generate_domestic_data.py
```

#### 3. 前端设置

```bash
# 1. 进入前端项目目录
cd logistics-dashboard-frontend

# 2. 安装Node.js依赖 (推荐使用pnpm)
# 如果没有安装pnpm, 可以先执行: npm install -g pnpm
pnpm install
```

#### 4. 启动应用

您需要**打开两个终端**，分别启动后端和前端服务。

**终端1: 启动后端服务 (在项目根目录)**
```bash
uvicorn main:app --reload
```
服务将运行在 `http://127.0.0.1:8000`。

**终端2: 启动前端服务 (在 `logistics-dashboard-frontend` 目录)**
```bash
pnpm dev
```
服务将运行在 `http://localhost:5173` (或终端提示的其他端口)。

现在，在浏览器中打开前端服务的地址，即可看到运行的仪表盘。

### 📄 API 接口

| 方法 | 路径                       | 描述                                   |
|------|----------------------------|----------------------------------------|
| GET  | `/api/v1/dashboard`        | 获取所有看板的KPI和图表聚合数据        |
| GET  | `/api/v1/orders`           | 获取分页的订单列表数据                 |
| GET  | `/api/v1/filter-options`   | 获取用于筛选器的唯一值选项             |
| GET  | `/api/v1/predict`          | 根据距离预测运输时间                   |

### 📜 开源许可

该项目采用 [MIT License](LICENSE) 开源许可。
