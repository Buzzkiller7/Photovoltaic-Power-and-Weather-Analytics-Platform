"""
简化版MPPT可视化平台 - 用于测试和调试
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

def main():
    st.set_page_config(
        page_title="MPPT测试平台",
        page_icon="⚡",
        layout="wide"
    )
    
    st.title("⚡ MPPT数据分析测试平台")
    
    # 侧边栏
    st.sidebar.title("控制面板")
    
    # 位置选择
    location = st.sidebar.selectbox("选择位置", ["十五舍", "专教"])
    
    # 日期选择
    start_date = st.sidebar.date_input("开始日期", datetime.now() - timedelta(days=7))
    end_date = st.sidebar.date_input("结束日期", datetime.now())
    
    # 数据类型
    show_mppt = st.sidebar.checkbox("显示MPPT数据", True)
    show_weather = st.sidebar.checkbox("显示气象数据", True)
    
    # 主内容区
    st.write(f"### 📊 {location} 数据分析")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("数据状态", "正常", "✅")
    
    with col2:
        st.metric("时间范围", f"{(end_date - start_date).days}天")
    
    with col3:
        st.metric("分析模式", "实时监控")
    
    # 创建示例图表
    if show_mppt:
        st.write("#### ⚡ MPPT功率数据")
        
        # 生成示例数据
        dates = pd.date_range(start_date, end_date, freq='H')
        power_data = np.random.normal(1000, 200, len(dates))
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=power_data, mode='lines', name='功率'))
        fig.update_layout(title=f"{location} MPPT功率变化", xaxis_title="时间", yaxis_title="功率(W)")
        
        st.plotly_chart(fig, use_container_width=True)
    
    if show_weather:
        st.write("#### 🌤️ 气象数据")
        
        # 生成示例数据
        dates = pd.date_range(start_date, end_date, freq='H')
        temp_data = np.random.normal(25, 5, len(dates))
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=temp_data, mode='lines', name='温度', line=dict(color='red')))
        fig.update_layout(title=f"{location} 环境温度变化", xaxis_title="时间", yaxis_title="温度(°C)")
        
        st.plotly_chart(fig, use_container_width=True)
    
    # 简单的数据表格
    with st.expander("📋 示例数据表格"):
        sample_data = pd.DataFrame({
            'time': pd.date_range(start_date, periods=10, freq='H'),
            'power': np.random.normal(1000, 100, 10),
            'temperature': np.random.normal(25, 3, 10)
        })
        st.dataframe(sample_data)
    
    st.success("✅ 平台运行正常！如果您看到这条消息，说明基本功能没有问题。")

if __name__ == "__main__":
    main()
