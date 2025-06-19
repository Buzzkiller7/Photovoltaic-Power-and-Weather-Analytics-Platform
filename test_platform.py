"""
MPPT可视化平台测试脚本
用于验证应用的各个功能模块是否正常工作
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

def test_imports():
    """测试所有必要的库是否可以正常导入"""
    try:
        import streamlit as st
        import plotly.express as px
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        print("✅ 所有依赖库导入成功")
        return True
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        return False

def test_data_structure():
    """测试数据结构和文件路径"""
    base_path = Path(".")
    locations = ["十五舍", "专教"]
    
    print("\n📁 数据结构检查:")
    for location in locations:
        mppt_path = base_path / location / "filtered"
        weather_path = base_path / location / "Climate_data" / "filtered"
        
        print(f"\n📍 {location}:")
        print(f"  MPPT数据路径: {mppt_path}")
        print(f"  MPPT数据存在: {'✅' if mppt_path.exists() else '❌'}")
        
        if mppt_path.exists():
            files = list(mppt_path.glob("*.xlsx"))
            print(f"  MPPT文件数量: {len(files)}")
            if files:
                print(f"  示例文件: {files[0].name}")
        
        print(f"  气象数据路径: {weather_path}")
        print(f"  气象数据存在: {'✅' if weather_path.exists() else '❌'}")
        
        if weather_path.exists():
            files = list(weather_path.glob("*.xlsx"))
            print(f"  气象文件数量: {len(files)}")
            if files:
                print(f"  示例文件: {files[0].name}")

def test_visualizer_class():
    """测试可视化器类的初始化"""
    try:
        from interactive_visualizer import InteractiveVisualizer
        
        print("\n🔧 可视化器类测试:")
        visualizer = InteractiveVisualizer()
        print("✅ 可视化器初始化成功")
        
        # 测试气象特征配置
        print(f"✅ 十五舍气象参数: {len(visualizer.weather_features['十五舍'])} 个")
        print(f"✅ 专教气象参数: {len(visualizer.weather_features['专教'])} 个")
        
        # 测试颜色主题
        print(f"✅ 颜色主题配置: {len(visualizer.color_theme)} 种颜色")
        
        return True
    except Exception as e:
        print(f"❌ 可视化器测试失败: {e}")
        return False

def test_sample_data():
    """测试样本数据读取"""
    try:
        print("\n📊 样本数据测试:")
        
        # 创建测试数据
        test_dates = pd.date_range(start='2025-01-01', end='2025-01-07', freq='H')
        
        # 模拟MPPT数据
        mppt_data = pd.DataFrame({
            'eventTime': test_dates,
            'power': np.random.normal(1000, 200, len(test_dates)),
            'voltage': np.random.normal(24, 2, len(test_dates)),
            'current': np.random.normal(42, 5, len(test_dates))
        })
        
        # 模拟气象数据
        weather_data = pd.DataFrame({
            'Date': test_dates,
            '大气温度(℃)': np.random.normal(25, 5, len(test_dates)),
            '大气湿度(%RH)': np.random.normal(60, 10, len(test_dates)),
            '数字气压(hPa)': np.random.normal(1013, 5, len(test_dates))
        })
        
        print(f"✅ 模拟MPPT数据: {len(mppt_data)} 条记录")
        print(f"✅ 模拟气象数据: {len(weather_data)} 条记录")
        
        return mppt_data, weather_data
        
    except Exception as e:
        print(f"❌ 样本数据测试失败: {e}")
        return None, None

def main():
    """主测试函数"""
    print("🧪 MPPT可视化平台测试开始")
    print("=" * 50)
    
    # 测试导入
    if not test_imports():
        print("❌ 依赖库测试失败，请检查安装")
        return False
    
    # 测试数据结构
    test_data_structure()
    
    # 测试可视化器类
    if not test_visualizer_class():
        print("❌ 可视化器类测试失败")
        return False
    
    # 测试样本数据
    mppt_data, weather_data = test_sample_data()
    
    print("\n" + "=" * 50)
    print("🎉 所有测试完成！")
    
    if mppt_data is not None and weather_data is not None:
        print("✅ 应用准备就绪，可以启动可视化平台")
        print("\n📌 启动方式:")
        print("1. 运行 run_visualizer.bat")
        print("2. 或者执行: streamlit run interactive_visualizer.py --server.port 8502")
        print("3. 然后在浏览器中访问: http://localhost:8502")
    else:
        print("⚠️ 样本数据测试失败，但应用仍可运行")
    
    return True

if __name__ == "__main__":
    main()
