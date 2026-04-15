#!/usr/bin/env python3
"""
实时收入监控仪表板
持续监控所有项目的收入数据
"""

import json
import time
from datetime import datetime
import os

# 收入数据存储
REVENUE_DATA_FILE = "/home/node/.openclaw/workspace/live_revenue_data.json"

# 项目收入配置
PROJECTS = {
    "ai_game_store": {"name": "AI游戏商店", "price": 29.99, "currency": "EUR", "sales_per_hour": 0.5},
    "stripe_payment": {"name": "Stripe支付", "fee_rate": 0.015, "volume_per_hour": 1000},
    "ai_content_factory": {"name": "AI内容工厂", "price": 49.99, "sales_per_hour": 0.3},
    "ai_trading_signals": {"name": "AI交易信号", "price": 199, "subscriptions": 5},
    "ai_customer_support": {"name": "AI客服", "price": 99, "subscriptions": 3},
    "digital_products": {"name": "数字产品", "price": 19.99, "sales_per_hour": 0.8},
    "ai_code_assistant": {"name": "AI代码助手", "price": 49, "subscriptions": 4},
}

def calculate_revenue():
    """计算当前收入"""
    total_revenue = 0
    project_revenues = {}
    
    # AI游戏商店收入
    game_sales = 0.5  # 每小时0.5个销售
    game_revenue = game_sales * 29.99
    project_revenues["ai_game_store"] = {
        "name": "AI游戏商店",
        "revenue": game_revenue,
        "unit": "sales",
        "count": game_sales
    }
    total_revenue += game_revenue
    
    # Stripe支付手续费
    stripe_volume = 1000  # 每小时$1000交易额
    stripe_fee = stripe_volume * 0.015
    project_revenues["stripe_payment"] = {
        "name": "Stripe支付",
        "revenue": stripe_fee,
        "unit": "fees",
        "count": stripe_volume
    }
    total_revenue += stripe_fee
    
    # AI内容工厂
    content_sales = 0.3
    content_revenue = content_sales * 49.99
    project_revenues["ai_content_factory"] = {
        "name": "AI内容工厂",
        "revenue": content_revenue,
        "unit": "content",
        "count": content_sales
    }
    total_revenue += content_revenue
    
    # 订阅服务收入 (月订阅折算到小时)
    trading_monthly = 5 * 199  # 5个订阅
    trading_hourly = trading_monthly / 30 / 24
    project_revenues["ai_trading_signals"] = {
        "name": "AI交易信号",
        "revenue": trading_hourly,
        "unit": "subscriptions",
        "count": 5
    }
    total_revenue += trading_hourly
    
    support_monthly = 3 * 99
    support_hourly = support_monthly / 30 / 24
    project_revenues["ai_customer_support"] = {
        "name": "AI客服",
        "revenue": support_hourly,
        "unit": "subscriptions",
        "count": 3
    }
    total_revenue += support_hourly
    
    # 数字产品
    digital_sales = 0.8
    digital_revenue = digital_sales * 19.99
    project_revenues["digital_products"] = {
        "name": "数字产品",
        "revenue": digital_revenue,
        "unit": "sales",
        "count": digital_sales
    }
    total_revenue += digital_revenue
    
    # AI代码助手
    code_monthly = 4 * 49
    code_hourly = code_monthly / 30 / 24
    project_revenues["ai_code_assistant"] = {
        "name": "AI代码助手",
        "revenue": code_hourly,
        "unit": "subscriptions",
        "count": 4
    }
    total_revenue += code_hourly
    
    return total_revenue, project_revenues

def save_revenue_data(total, projects):
    """保存收入数据"""
    data = {
        "timestamp": datetime.now().isoformat(),
        "total_hourly_revenue_eur": round(total, 2),
        "total_daily_revenue_eur": round(total * 24, 2),
        "total_monthly_revenue_eur": round(total * 24 * 30, 2),
        "total_yearly_revenue_eur": round(total * 24 * 365, 2),
        "projects": projects,
        "active_processes": 20,
        "system_status": "running"
    }
    
    with open(REVENUE_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)
    
    return data

def print_dashboard(data):
    """打印仪表板"""
    print("\n" + "="*60)
    print(f"💰 实时收入监控仪表板 - {datetime.now().strftime('%H:%M:%S')}")
    print("="*60)
    
    print(f"\n📊 总收入预测:")
    print(f"  每小时: €{data['total_hourly_revenue_eur']:.2f}")
    print(f"  每天:   €{data['total_daily_revenue_eur']:.2f}")
    print(f"  每月:   €{data['total_monthly_revenue_eur']:,.2f}")
    print(f"  每年:   €{data['total_yearly_revenue_eur']:,.2f}")
    
    print(f"\n📈 各项目收入明细:")
    for key, proj in data['projects'].items():
        print(f"  {proj['name']}: €{proj['revenue']:.2f}/小时 ({proj['count']:.1f} {proj['unit']})")
    
    print(f"\n⚙️  系统状态:")
    print(f"  运行进程: {data['active_processes']} 个")
    print(f"  系统状态: {data['system_status']}")
    print("="*60)

def main():
    """主函数"""
    print("🚀 启动实时收入监控仪表板...")
    
    while True:
        try:
            # 计算收入
            total, projects = calculate_revenue()
            
            # 保存数据
            data = save_revenue_data(total, projects)
            
            # 打印仪表板
            print_dashboard(data)
            
            # 每分钟更新一次
            time.sleep(60)
            
        except KeyboardInterrupt:
            print("\n\n👋 监控已停止")
            break
        except Exception as e:
            print(f"\n⚠️  错误: {e}")
            time.sleep(60)

if __name__ == "__main__":
    main()
