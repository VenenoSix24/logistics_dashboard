import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import uuid
import numpy as np

def generate_logistics_data(num_records=10000):
    """
    生成更逼真的、模拟国内真实业务场景的物流数据。(版本 2.0)
    """
    fake = Faker('zh_CN')

    # --- 1. 基础数据 ---

    # 1.1) 地域分布权重
    provinces_cities = {
        '广东': (['深圳', '广州', '东莞', '佛山', '珠海', '中山', '惠州'], 0.18),
        '江苏': (['苏州', '南京', '无锡', '常州', '南通', '徐州', '扬州'], 0.14),
        '浙江': (['杭州', '宁波', '温州', '金华', '台州', '嘉兴', '绍兴'], 0.14),
        '上海': (['上海市'], 0.10),
        '北京': (['北京市'], 0.08),
        '四川': (['成都', '绵阳', '德阳', '南充', '乐山', '眉山'], 0.07),
        '湖北': (['武汉', '宜昌', '襄阳', '黄冈', '荆州', '孝感'], 0.06),
        '山东': (['青岛', '济南', '烟台', '临沂', '潍坊', '淄博'], 0.05),
        '河南': (['郑州', '洛阳', '南阳', '新乡', '开封', '商丘'], 0.04),
        '河北': (['石家庄', '唐山', '保定', '廊坊', '沧州'], 0.03),
        '福建': (['福州', '厦门', '泉州', '莆田', '漳州'], 0.03),
        '湖南': (['长沙', '岳阳', '常德', '株洲', '衡阳'], 0.02),
        '安徽': (['合肥', '芜湖', '蚌埠', '阜阳', '滁州'], 0.02),
        '辽宁': (['沈阳', '大连', '鞍山', '锦州'], 0.01),
        '重庆': (['重庆市'], 0.01),
        '黑龙江': (['哈尔滨', '齐齐哈尔', '大庆'], 0.01),
        '江西': (['南昌', '九江', '赣州'], 0.01)
    }
    provinces = list(provinces_cities.keys())
    province_weights = [v[1] for v in provinces_cities.values()]

    # 1.2) 商品品类
    categories = {
        '服装鞋帽': {'distribution_weight': 0.20, 'products': ["安踏运动鞋", "李宁卫衣", "波司登羽绒服", "优衣库T恤", "Nike Air Force 1", "Adidas Samba", "斯凯奇休闲鞋", "斐乐运动裤"], 'weight_range': (0.5, 3), 'price_range': (100, 2000), 'volume_range': (0.005, 0.02)},
        '电子产品': {'distribution_weight': 0.18, 'products': ["华为Mate 60 Pro", "小米14 Ultra", "大疆无人机Air 3", "联想小新Pro 16", "Apple iPhone 15 Pro", "小米手环8", "索尼PS5游戏机", "微软Xbox Series X", "佳能EOS R6相机"], 'weight_range': (0.2, 5), 'price_range': (500, 8000), 'volume_range': (0.001, 0.05)},
        '家居用品': {'distribution_weight': 0.15, 'products': ["网易严选四件套", "全棉时代浴巾", "德力西插座", "喜临门乳胶床垫", "宜家收纳盒", "小米台灯", "双立人刀具", "得力文具套装"], 'weight_range': (1, 20), 'price_range': (50, 1500), 'volume_range': (0.01, 0.1)},
        '美妆护肤': {'distribution_weight': 0.12, 'products': ["雅诗兰黛小棕瓶", "兰蔻粉水", "SK-II神仙水", "薇诺娜舒敏保湿霜", "完美日记眼影盘", "花西子口红", "欧莱雅洗发水", "高夫男士护肤套装"], 'weight_range': (0.1, 1.5), 'price_range': (200, 3000), 'volume_range': (0.0005, 0.005)},
        '生鲜食品': {'distribution_weight': 0.10, 'products': ["山东烟台苹果", "智利车厘子", "筋头巴脑牛腩块", "每日鲜牛奶", "厄瓜多尔白虾", "阳澄湖大闸蟹", "内蒙古羔羊肉", "三文鱼刺身"], 'weight_range': (2, 10), 'price_range': (80, 600), 'volume_range': (0.005, 0.05)},
        '家用电器': {'distribution_weight': 0.08, 'products': ["美的智能电饭煲", "海尔洗衣机", "格力空调", "九阳豆浆机", "苏泊尔电压力锅", "戴森V15吸尘器", "飞利浦电动牙刷", "科沃斯扫地机器人"], 'weight_range': (1, 30), 'price_range': (300, 10000), 'volume_range': (0.02, 0.5)},
        '母婴用品': {'distribution_weight': 0.07, 'products': ["帮宝适纸尿裤", "好奇金装纸尿裤", "飞鹤奶粉", "爱他美奶粉", "贝亲奶瓶", "好孩子婴儿推车", "宝宝巴士故事机"], 'weight_range': (1, 8), 'price_range': (100, 1200), 'volume_range': (0.01, 0.08)},
        '运动户外': {'distribution_weight': 0.04, 'products': ["迪卡侬帐篷", "骆驼冲锋衣", "凯乐石登山鞋", "斯伯丁篮球", "李宁羽毛球拍", "美利达山地自行车"], 'weight_range': (0.5, 15), 'price_range': (200, 5000), 'volume_range': (0.01, 0.3)},
        '图书文娱': {'distribution_weight': 0.04, 'products': ["三体全集", "活着", "明朝那些事儿", "王者荣耀皮肤卡", "乐高积木", "PSN点卡"], 'weight_range': (0.1, 2), 'price_range': (30, 500), 'volume_range': (0.001, 0.01)},
        '酒水饮料': {'distribution_weight': 0.02, 'products': ["茅台飞天", "五粮液", "拉菲红酒", "科罗娜啤酒", "农夫山泉矿泉水", "可口可乐整箱"], 'weight_range': (2, 25), 'price_range': (50, 2000), 'volume_range': (0.005, 0.08)}
    }

    # 1.3) 定义承运商及其绩效，用于模拟更真实的履约率
    carriers_performance = {
        '京东物流': {'on_time_rate': 0.96, 'avg_delay_days': 0.5},
        '顺丰速运': {'on_time_rate': 0.95, 'avg_delay_days': 0.7},
        '圆通快递': {'on_time_rate': 0.82, 'avg_delay_days': 1.4},
        '中通快递': {'on_time_rate': 0.83, 'avg_delay_days': 1.3},
        '韵达快递': {'on_time_rate': 0.78, 'avg_delay_days': 1.6},
        '申通快递': {'on_time_rate': 0.75, 'avg_delay_days': 1.9},
        '百世快递': {'on_time_rate': 0.72, 'avg_delay_days': 2.1}
    }
    
    shipping_modes = {
        '当日达': {'ratio': 0.1, 'carriers': ['京东物流', '顺丰速运'], 'cost_multiplier': 1.8},
        '次日达': {'ratio': 0.2, 'carriers': ['京东物流', '顺丰速运', '圆通快递'], 'cost_multiplier': 1.3},
        '标准快递': {'ratio': 0.5, 'carriers': ['顺丰速运', '圆通快递', '中通快递', '韵达快递'], 'cost_multiplier': 1.0},
        '经济快递': {'ratio': 0.2, 'carriers': ['中通快递', '韵达快递', '申通快递', '百世快递'], 'cost_multiplier': 0.8}
    }
    
    # 1.4) 车辆类型
    vehicles = {
        '面包车': {'capacity_kg': 500, 'volume_cbm': 3, 'fuel_consumption_L_per_100km': 8},
        '厢式货车': {'capacity_kg': 2000, 'volume_cbm': 10, 'fuel_consumption_L_per_100km': 15},
        '轻卡': {'capacity_kg': 5000, 'volume_cbm': 20, 'fuel_consumption_L_per_100km': 20},
        '重卡': {'capacity_kg': 15000, 'volume_cbm': 60, 'fuel_consumption_L_per_100km': 30}
    }
    carbon_emission_factors = {'gasoline': 2.3} 

    # 1.5) 时间分布
    month_weights = [1.0, 1.0, 1.5, 1.2, 1.5, 2.5, 1.2, 1.2, 1.5, 2.0, 4.0, 2.0]

    data = []
    print(f"开始生成 {num_records} 条更真实的模拟数据 (v2.0)...")

    # --- 2. 循环生成每条记录 ---
    for _ in range(num_records):
        # 2.1) 基础信息生成
        current_year = datetime.now().year
        month = random.choices(range(1, 13), weights=month_weights, k=1)[0]
        day = random.randint(1, 28)
        # year = random.choice(range(current_year - 2, current_year + 1))
        year = current_year - 1 # 将所有数据生成到去年，确保所有订单都有确定的交付日期
        order_date = datetime(year, month, day, random.randint(0, 23), random.randint(0, 59))

        mode_name = random.choices(list(shipping_modes.keys()), [v['ratio'] for v in shipping_modes.values()], k=1)[0]
        mode_info = shipping_modes[mode_name]
        
        carrier = random.choice(mode_info['carriers'])
        carrier_info = carriers_performance[carrier]

        shipping_date = order_date + timedelta(hours=random.randint(2, 24))

        source_province = random.choices(provinces, weights=province_weights, k=1)[0]
        source_city = random.choice(provinces_cities[source_province][0])
        destination_province = random.choices(provinces, weights=province_weights, k=1)[0]
        destination_city = random.choice(provinces_cities[destination_province][0])
        
        if source_province != destination_province:
            distance_km = random.randint(500, 2500)
        else:
            distance_km = random.randint(50, 500)
        
        # 2.2) 模拟真实履约率
        # 计划送达时间：基于距离和运输模式给出一个较稳定的承诺
        base_days = 2 + (distance_km / 500) # 基础天数，大致认为500公里/天
        plan_transport_days = base_days * (2.0 - mode_info['cost_multiplier']) # 越贵的模式承诺越快
        plan_delivery_date = shipping_date + timedelta(days=plan_transport_days)

        # 实际送达时间：基于承运商的可靠性模拟
        is_on_time = random.random() < carrier_info['on_time_rate']
        if is_on_time:
            # 准时：在计划时间附近小范围浮动
            actual_transport_days = plan_transport_days - random.uniform(0, carrier_info['avg_delay_days'])
        else:
            # 延误：延误应该是在基础天数上增加，而不是在可能很小的计划天数上增加
            delay = np.random.exponential(scale=carrier_info['avg_delay_days'])
            actual_transport_days = base_days + delay

        # 确保实际运输天数不会是负数或零，同时移除不合理的0.5天最低限制
        actual_transport_days = max(0.1, actual_transport_days)
        delivery_date = shipping_date + timedelta(days=actual_transport_days)

        # 2.3) 商品信息
        category_names = list(categories.keys())
        category_weights = [categories[name]['distribution_weight'] for name in category_names]
        category_name = random.choices(category_names, weights=category_weights, k=1)[0]
        category_info = categories[category_name]
        product_name = random.choice(category_info['products'])

        actual_weight = round(random.uniform(*category_info['weight_range']), 2)
        actual_volume = round(random.uniform(*category_info['volume_range']), 4)
        sales = round(random.uniform(*category_info['price_range']), 2)
        if month in [6, 11] and random.random() < 0.8:
            sales = round(sales * random.uniform(0.6, 0.95), 2)
        
        # 2.4) 模拟车辆装载与成本，解决装载率和单位成本问题
        vehicle_type = random.choices(list(vehicles.keys()), [0.4, 0.4, 0.15, 0.05], k=1)[0]
        vehicle_info = vehicles[vehicle_type]
        vehicle_capacity_kg = vehicle_info['capacity_kg']
        
        # 模拟该包裹所在的车辆的“整车”装载率，这是一个符合现实的随机数
        simulated_vehicle_loading_rate = random.uniform(0.65, 0.98)
        
        # 模拟“整车”运输的总成本，主要与里程和车辆类型有关
        simulated_vehicle_journey_cost = (distance_km * random.uniform(0.8, 1.5)) + (vehicle_capacity_kg * 0.05)
        
        # 模拟“整车”实际装载的总重量
        total_simulated_weight_on_vehicle = vehicle_capacity_kg * simulated_vehicle_loading_rate
        
        # 计算出这趟运输的合理“平均单位重量成本”
        realistic_base_cost_per_kg = simulated_vehicle_journey_cost / total_simulated_weight_on_vehicle
        
        # 根据运输模式的溢价，计算出该包裹的最终单位成本
        final_cost_per_kg = realistic_base_cost_per_kg * mode_info['cost_multiplier']
        
        # 根据包裹的实际重量，计算出其应付的运费
        freight_cost = round(final_cost_per_kg * actual_weight, 2)
        
        # 其他成本计算
        other_cost = round(sales * random.uniform(0.01, 0.05), 2)
        total_cost = freight_cost + other_cost
        order_profit_per_order = round(sales - total_cost, 2)

        # 2.5) 其他信息
        if delivery_date > datetime.now():
            order_status = '运输中'
            logistics_track = "包裹已揽收"
        else:
            is_returned = random.random() < 0.02
            if is_returned: order_status = '已退货'; logistics_track = "客户已拒收，包裹正在退回"
            else: order_status = '已签收'; logistics_track = "客户已签收"

        customer_id = str(uuid.uuid4().hex)[:8]
        customer_name = fake.name()
        customer_address = fake.address()
        if order_status == '已签收':
            # 使用加权随机数生成更真实的评分，让高分更常见
            ratings = [1, 2, 3, 4, 5]
            weights = [0.05, 0.05, 0.15, 0.35, 0.4] # 权重向4星和5星倾斜
            customer_rating = random.choices(ratings, weights=weights, k=1)[0]
        else:
            customer_rating = None
        
        fuel_consumption = vehicle_info['fuel_consumption_L_per_100km']
        carbon_emission = round((distance_km / 100) * fuel_consumption * carbon_emission_factors['gasoline'], 2)

        has_cs_issue = random.random() < 0.1
        cs_issue_type = random.choice(['物流异常', '商品破损', '退货咨询', '地址错误']) if has_cs_issue else None

        record = {
            'order_id': str(uuid.uuid4().hex)[:12],
            'order_date': order_date.strftime('%Y-%m-%d %H:%M:%S'),
            'shipping_date': shipping_date.strftime('%Y-%m-%d %H:%M:%S'),
            'delivery_date': delivery_date.strftime('%Y-%m-%d %H:%M:%S') if delivery_date < datetime.now() else None,
            'plan_delivery_date': plan_delivery_date.strftime('%Y-%m-%d %H:%M:%S'),
            'distance_km': distance_km,
            'carrier': carrier,
            'shipping_mode': mode_name,
            'source_province': source_province,
            'source_city': source_city,
            'destination_province': destination_province,
            'destination_city': destination_city,
            'destination_address': customer_address,
            'category_name': category_name,
            'product_name': product_name,
            'sales': sales,
            'freight_cost': freight_cost,
            'other_cost': other_cost,
            'total_cost': total_cost,
            'order_profit_per_order': order_profit_per_order,
            'actual_weight_kg': actual_weight,
            'actual_volume_cbm': actual_volume,
            'vehicle_type': vehicle_type,
            'vehicle_capacity_kg': vehicle_capacity_kg,
            'vehicle_loading_rate': round(simulated_vehicle_loading_rate, 4),
            'cost_per_kg': round(final_cost_per_kg, 2),
            'carbon_emission_kg': carbon_emission,
            'order_status': order_status,
            'logistics_track': logistics_track,
            'customer_id': customer_id,
            'customer_name': customer_name,
            'customer_rating': customer_rating,
            'has_cs_issue': has_cs_issue,
            'cs_issue_type': cs_issue_type,
        }
        data.append(record)

    print("数据生成完毕。")

    # --- 3. 转换为DataFrame并进行最终处理 ---
    df = pd.DataFrame(data)

    # is_on_time 现在是最终的权威计算
    df['is_on_time'] = (pd.to_datetime(df['delivery_date']) <= pd.to_datetime(df['plan_delivery_date']))

    # 重命名字段以匹配旧版，如果需要的话
    df.rename(columns={'vehicle_loading_rate': 'loading_rate_by_weight'}, inplace=True)

    output_filename = 'logistics_data_v2.csv'
    df.to_csv(output_filename, index=False, encoding='utf-8-sig')
    print(f"成功将更真实的数据保存到新文件: {output_filename}")


if __name__ == '__main__':
    # 为了快速测试，先生成少量数据
    generate_logistics_data(num_records=50000)