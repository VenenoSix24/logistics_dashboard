import pandas as pd
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, Optional, List
import numpy as np

# --- 机器学习相关导入 ---
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# --- 1. 数据预加载 ---
DATA_FILE = 'logistics_data_v2.csv'
logistics_df = pd.read_csv(DATA_FILE)
print(f"数据已成功预加载并处理完毕！共 {len(logistics_df)} 条记录。")


# --- 1.5. 训练并加载预测模型 ---
prediction_model = None

def train_prediction_model(df: pd.DataFrame) -> LinearRegression:
    """
    使用历史数据训练一个简单的线性回归模型，用于预测运输时间。
    """
    print("开始训练运输时效预测模型...")
    
    model_df = df.dropna(subset=['shipping_date', 'delivery_date', 'distance_km']).copy()
    model_df['shipping_date'] = pd.to_datetime(model_df['shipping_date'])
    model_df['delivery_date'] = pd.to_datetime(model_df['delivery_date'])
    
    model_df['actual_transport_hours'] = (model_df['delivery_date'] - model_df['shipping_date']).dt.total_seconds() / 3600
    
    model_df = model_df[(model_df['actual_transport_hours'] > 0) & (model_df['actual_transport_hours'] < 1000)]
    
    X = model_df[['distance_km']]
    y = model_df['actual_transport_hours']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"模型训练完成。均方误差 (MSE): {mse:.2f}")
    
    return model

prediction_model = train_prediction_model(logistics_df)


# --- 2. 创建 FastAPI 应用 ---
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 3. API 接口 ---

def apply_filters(
    df: pd.DataFrame, 
    carrier: Optional[str], 
    source_province: Optional[str], 
    destination_province: Optional[str],
    category_name: Optional[str]
) -> pd.DataFrame:
    """辅助函数，应用所有筛选条件"""
    filtered_df = df.copy()
    if carrier:
        filtered_df = filtered_df[filtered_df['carrier'] == carrier]
    if source_province:
        filtered_df = filtered_df[filtered_df['source_province'] == source_province]
    if destination_province:
        filtered_df = filtered_df[filtered_df['destination_province'] == destination_province]
    if category_name:
        filtered_df = filtered_df[filtered_df['category_name'] == category_name]
    return filtered_df

@app.get("/api/v1/filter-options")
def get_filter_options() -> Dict[str, List[str]]:
    """为前端提供筛选器的选项列表"""
    return {
        "carriers": sorted(logistics_df['carrier'].unique().tolist()),
        "source_provinces": sorted(logistics_df['source_province'].unique().tolist()),
        "destination_provinces": sorted(logistics_df['destination_province'].unique().tolist()),
        "categories": sorted(logistics_df['category_name'].unique().tolist()),
    }

@app.get("/api/v1/dashboard")
def get_dashboard_data(
    carrier: Optional[str] = Query(None),
    source_province: Optional[str] = Query(None),
    destination_province: Optional[str] = Query(None),
    category_name: Optional[str] = Query(None)
) -> Dict[str, Any]:
    """看板聚合数据接口"""
    filtered_df = apply_filters(logistics_df, carrier, source_province, destination_province, category_name)
    
    if filtered_df.empty:
        return { "kpi_data": {}, "chart_data": { 'daily_orders': {'dates': [], 'counts': []}, 'category_percentage': [] } }
        
    temp_df = filtered_df.copy()
    completed_df = temp_df.dropna(subset=['delivery_date']).copy()
    
    # --- 核心运营指标 ---
    on_time_deliveries = (completed_df['delivery_date'] <= completed_df['plan_delivery_date']).sum()
    order_fulfillment_rate = on_time_deliveries / len(completed_df) if len(completed_df) > 0 else 0
    average_loading_rate = temp_df['loading_rate_by_weight'].mean()
    average_cost_per_kg = temp_df['cost_per_kg'].mean()
    total_carbon_emission = temp_df['carbon_emission_kg'].sum()

    # --- 财务与客户服务指标 ---
    total_profit = temp_df['order_profit_per_order'].sum()
    avg_profit_per_order = temp_df['order_profit_per_order'].mean()
    cs_issue_rate = temp_df['has_cs_issue'].sum() / len(temp_df) if len(temp_df) > 0 else 0
    avg_customer_rating = temp_df.dropna(subset=['customer_rating'])['customer_rating'].mean()

    kpi_data = {
        "order_fulfillment_rate": order_fulfillment_rate,
        "average_loading_rate": average_loading_rate,
        "average_cost_per_kg": average_cost_per_kg,
        "total_carbon_emission": total_carbon_emission,
        "total_profit": total_profit,
        "avg_profit_per_order": avg_profit_per_order,
        "cs_issue_rate": cs_issue_rate,
        "avg_customer_rating": avg_customer_rating,
    }

    temp_df['shipping_date_only'] = pd.to_datetime(temp_df['shipping_date']).dt.date.astype(str)
    daily_orders = temp_df.groupby('shipping_date_only').size().reset_index(name='count')
    category_counts = temp_df['category_name'].value_counts().reset_index()
    category_counts.columns = ['name', 'value']
    
    chart_data = {
        'daily_orders': {'dates': daily_orders['shipping_date_only'].tolist(), 'counts': daily_orders['count'].tolist()},
        'category_percentage': category_counts.to_dict('records')
    }
    
    return {"kpi_data": kpi_data, "chart_data": chart_data}

@app.get("/api/v1/orders")
def get_orders_data(
    page: int = 1, pageSize: int = 100,
    carrier: Optional[str] = Query(None),
    source_province: Optional[str] = Query(None),
    destination_province: Optional[str] = Query(None),
    category_name: Optional[str] = Query(None)
) -> Dict[str, Any]:
    """分页订单列表接口"""
    filtered_df = apply_filters(logistics_df, carrier, source_province, destination_province, category_name)
    
    start_index = (page - 1) * pageSize
    end_index = start_index + pageSize
    paginated_data = filtered_df.iloc[start_index:end_index]
    
    return {
        "total": len(filtered_df),
        "page": page,
        "pageSize": pageSize,
        "orders": paginated_data.to_dict(orient='records')
    }

# --- 4. 预测API接口 ---
@app.get("/api/v1/predict")
def predict_transport_time(distance_km: float = Query(..., gt=0)):
    """
    接收运输距离，使用已训练的模型预测运输时间。
    """
    if not prediction_model:
        return {"error": "Model is not trained yet."}
    
    distance_array = np.array([[distance_km]])
    
    predicted_hours = prediction_model.predict(distance_array)[0]
    
    return {
        "input_distance_km": distance_km,
        "predicted_hours": round(predicted_hours, 2),
        "predicted_days": round(predicted_hours / 24, 1)
    }