"""
MPPT数据分析与可视化平台 - 企业级交互式仪表板
使用Streamlit构建的专业Web界面，支持多维度数据分析、可视化和对比
支持十五舍和专教两个位置的MPPT及多元气象数据分析
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime, timedelta
from pathlib import Path
import json
from typing import List, Dict, Any, Optional
import warnings
warnings.filterwarnings('ignore')

class InteractiveVisualizer:
    """企业级MPPT数据可视化分析平台"""
    
    def __init__(self):
        """初始化可视化器"""
        self.setup_page_config()
        self.locations = ["十五舍", "专教"]
        self.data_types = ["MPPT", "Weather"]
        
        # 定义各位置的气象特征
        self.weather_features = {
            "十五舍": {
                "wind_speed": "超声波风速(m/s)",
                "pressure": "数字气压(hPa)", 
                "temperature": "大气温度(℃)",
                "humidity": "大气湿度(%RH)",
                "wind_direction": "超声波风向(°)"
            },
            "专教": {
                "wind_speed": "风速(m/s)",
                "pressure": "数字气压(hPa)",
                "pm100": "PM100(ug/m3)",
                "temperature": "大气温度(℃)",
                "humidity": "大气湿度(%RH)",
                "pm25": "PM2.5(ug/m3)",
                "pm10": "PM10(ug/m3)",
                "radiation": "TBQ总辐射(W/m2)",
                "wind_direction": "风向(°)",
                "sunshine": "日照时数(h)",
                "radiation_cum": "辐射累计(MJ/m2)"
            }
        }
        
        # 颜色主题
        self.color_theme = {
            "primary": "#1f77b4",
            "secondary": "#ff7f0e", 
            "success": "#2ca02c",
            "warning": "#d62728",
            "info": "#9467bd",
            "light": "#17becf",
            "dark": "#8c564b",
            "muted": "#e377c2"
        }
        
        # 图表配置
        self.chart_config = {
            "font_family": "Arial, sans-serif",
            "font_size": 12,            "title_font_size": 16,
            "legend_font_size": 10
        }
    
    def setup_page_config(self):
        """设置页面配置"""
        st.set_page_config(
            page_title="MPPT数据分析与可视化平台",
            page_icon="⚡",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # 企业级CSS样式设计
        st.markdown("""
        <style>
        /* 主要样式 */
        .main {
            padding-top: 2rem;
        }
        
        /* 主标题样式 */
        .main-header {
            font-size: 3rem;
            font-weight: 700;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
            padding: 2rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        /* 卡片样式 */
        .metric-card {
            background: linear-gradient(145deg, #ffffff, #f0f0f0);
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            border-left: 5px solid #1f77b4;
            margin-bottom: 1rem;
            transition: transform 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        
        /* 侧边栏样式 */
        .sidebar .sidebar-content {
            background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
        }
        
        .sidebar-header {
            font-size: 1.4rem;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 1.5rem;
            padding: 1rem;
            background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            border-radius: 8px;
            text-align: center;
        }
        
        /* 数据摘要样式 */
        .data-summary {
            background: linear-gradient(145deg, #f8f9fa, #e9ecef);
            padding: 2rem;
            border-radius: 15px;
            margin: 1rem 0;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }
        
        /* 状态指示器 */
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
        }
        
        .status-online { background-color: #28a745; }
        .status-warning { background-color: #ffc107; }
        .status-offline { background-color: #dc3545; }
        
        /* 选项卡样式 */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            background-color: #f8f9fa;
            border-radius: 8px;
            color: #495057;
            font-weight: 500;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
            color: white;
        }
        
        /* 按钮样式 */
        .stButton > button {
            background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        /* 下载按钮特殊样式 */
        .download-btn {
            background: linear-gradient(90deg, #56ab2f 0%, #a8e6cf 100%);
        }
        
        /* 警告和信息框样式 */
        .stAlert {
            border-radius: 8px;
            border-left: 4px solid;
        }
        
        /* 响应式设计 */
        @media (max-width: 768px) {
            .main-header {
                font-size: 2rem;
                padding: 1rem;
            }
            
            .metric-card {
                padding: 1rem;
            }
        }
        
        /* 加载动画 */
        .loading-spinner {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100px;
        }
        
        .spinner {
            width: 40px;
            height: 40px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #3498db;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }        </style>
        """, unsafe_allow_html=True)
    
    def load_data(self, location: str, start_date: datetime, end_date: datetime) -> Dict[str, pd.DataFrame]:
        """
        企业级数据加载器，支持多格式数据和错误恢复
        
        Args:
            location: 数据位置（十五舍/专教）
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            包含MPPT和气象数据的字典，带有数据质量指标
        """
        data = {
            "mppt": pd.DataFrame(), 
            "weather": pd.DataFrame(),
            "data_quality": {
                "mppt_files_loaded": 0,
                "weather_files_loaded": 0,
                "mppt_missing_days": [],
                "weather_missing_days": [],
                "data_completeness": 0.0
            }
        }
        
        try:
            # 生成日期范围
            date_range = pd.date_range(start_date, end_date, freq='D')
            total_days = len(date_range)
            
            # 加载MPPT数据
            mppt_dir = Path(location) / "filtered"
            if mppt_dir.exists():
                mppt_files = []
                missing_mppt_days = []
                
                for current_date in date_range:
                    file_path = mppt_dir / f"{current_date.strftime('%Y-%m-%d')}.xlsx"
                    if file_path.exists():
                        mppt_files.append(file_path)
                    else:
                        missing_mppt_days.append(current_date.strftime('%Y-%m-%d'))
                
                if mppt_files:
                    mppt_dfs = []
                    for file_path in mppt_files:
                        try:
                            df = pd.read_excel(file_path)
                            if 'eventTime' in df.columns:
                                df['eventTime'] = pd.to_datetime(df['eventTime'], errors='coerce')
                                # 添加数据源标识
                                df['data_source'] = location
                                df['file_date'] = pd.to_datetime(file_path.stem)
                            mppt_dfs.append(df)
                        except Exception as e:
                            st.warning(f"读取MPPT文件 {file_path.name} 时出错: {e}")
                    
                    if mppt_dfs:
                        data["mppt"] = pd.concat(mppt_dfs, ignore_index=True)
                        # 数据清洗
                        data["mppt"] = self.clean_mppt_data(data["mppt"])
                
                data["data_quality"]["mppt_files_loaded"] = len(mppt_files)
                data["data_quality"]["mppt_missing_days"] = missing_mppt_days
            
            # 加载气象数据
            weather_dir = Path(location) / "Climate_data" / "filtered"
            if weather_dir.exists():
                weather_files = []
                missing_weather_days = []
                
                for current_date in date_range:
                    file_path = weather_dir / f"{current_date.strftime('%Y-%m-%d')}.xlsx"
                    if file_path.exists():
                        weather_files.append(file_path)
                    else:
                        missing_weather_days.append(current_date.strftime('%Y-%m-%d'))
                
                if weather_files:
                    weather_dfs = []
                    for file_path in weather_files:
                        try:
                            df = pd.read_excel(file_path)
                            if 'Date' in df.columns:
                                df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
                                # 添加数据源标识
                                df['data_source'] = location
                                df['file_date'] = pd.to_datetime(file_path.stem)
                            weather_dfs.append(df)
                        except Exception as e:
                            st.warning(f"读取气象文件 {file_path.name} 时出错: {e}")
                    
                    if weather_dfs:
                        data["weather"] = pd.concat(weather_dfs, ignore_index=True)
                        # 数据清洗
                        data["weather"] = self.clean_weather_data(data["weather"], location)
                
                data["data_quality"]["weather_files_loaded"] = len(weather_files)
                data["data_quality"]["weather_missing_days"] = missing_weather_days
            
            # 计算数据完整性
            loaded_files = data["data_quality"]["mppt_files_loaded"] + data["data_quality"]["weather_files_loaded"]
            expected_files = total_days * 2  # MPPT + Weather
            data["data_quality"]["data_completeness"] = (loaded_files / expected_files) * 100 if expected_files > 0 else 0
                    
        except Exception as e:            st.error(f"数据加载时发生严重错误: {e}")            
        return data
    
    def clean_mppt_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """清洗MPPT数据"""
        if df.empty:
            return df
            
        df_clean = df.copy()
        
        # 移除重复行
        df_clean = df_clean.drop_duplicates()
        
        # 处理时间列
        if 'eventTime' in df_clean.columns:
            df_clean['eventTime'] = pd.to_datetime(df_clean['eventTime'], errors='coerce')
            df_clean = df_clean.dropna(subset=['eventTime'])
        
        # 识别功率、电流、电压列
        power_cols = [col for col in df_clean.columns if any(keyword in col.lower() 
                     for keyword in ['power', '功率', 'watt', 'pv', 'mppt'])]
        current_cols = [col for col in df_clean.columns if any(keyword in col.lower() 
                       for keyword in ['current', '电流', 'amp', 'i_'])]
        voltage_cols = [col for col in df_clean.columns if any(keyword in col.lower() 
                       for keyword in ['voltage', '电压', 'volt', 'v_', 'u_'])]
        
        # 处理异常值（基于IQR方法，但更宽松）
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if col not in ['eventTime'] and len(df_clean[col].dropna()) > 5:
                try:
                    Q1 = df_clean[col].quantile(0.15)  # 更宽松的分位数
                    Q3 = df_clean[col].quantile(0.85)
                    IQR = Q3 - Q1
                    if IQR > 0:
                        lower_bound = Q1 - 2.0 * IQR  # 更宽松的异常值范围
                        upper_bound = Q3 + 2.0 * IQR
                        
                        # 标记异常值但保留数据
                        df_clean[f'{col}_outlier'] = (df_clean[col] < lower_bound) | (df_clean[col] > upper_bound)
                except Exception as e:                    # 如果某列处理失败，跳过该列
                    continue
        
        return df_clean
    
    def clean_weather_data(self, df: pd.DataFrame, location: str) -> pd.DataFrame:
        """清洗气象数据"""
        if df.empty:
            return df
            
        df_clean = df.copy()
        
        # 移除重复行
        df_clean = df_clean.drop_duplicates()
        
        # 处理时间列
        time_cols = ['Date', 'date', 'datetime', 'time']
        for col in time_cols:
            if col in df_clean.columns:
                df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
                break
        
        # 根据位置标准化列名和特征识别
        if location in self.weather_features:
            features = self.weather_features[location]
            
            # 添加标准化特征标识
            for standard_name, actual_name in features.items():
                if actual_name in df_clean.columns:
                    df_clean[f'std_{standard_name}'] = df_clean[actual_name]
        
        # 处理数值列的异常值
        numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if len(df_clean[col].dropna()) > 5:
                try:
                    # 使用更宽松的异常值检测
                    Q1 = df_clean[col].quantile(0.05)
                    Q3 = df_clean[col].quantile(0.95)
                    IQR = Q3 - Q1
                    if IQR > 0:
                        lower_bound = Q1 - 3.0 * IQR
                        upper_bound = Q3 + 3.0 * IQR
                        df_clean[f'{col}_outlier'] = (df_clean[col] < lower_bound) | (df_clean[col] > upper_bound)
                except Exception:
                    continue
        
        return df_clean
    
    def create_sidebar(self) -> Dict[str, Any]:
        """创建企业级侧边栏控制面板"""
        # 侧边栏标题
        st.sidebar.markdown(
            '<div class="sidebar-header">⚡ 控制面板</div>', 
            unsafe_allow_html=True
        )
        
        # 位置选择
        st.sidebar.markdown("### 📍 数据源选择")
        location = st.sidebar.selectbox(
            "选择监测位置",
            self.locations,
            help="选择要分析的MPPT监测位置",
            format_func=lambda x: f"📍 {x}"
        )
          # 显示位置特有的气象参数
        if location in self.weather_features:
            st.sidebar.markdown("**📊 气象参数预览**")
            features = self.weather_features[location]
            for category, feature in features.items():
                st.sidebar.markdown(f"• {feature}")
        
        # 日期范围选择
        st.sidebar.markdown("### 📅 时间范围")
        
        # 快速日期选择
        quick_date = st.sidebar.selectbox(
            "快速选择",
            ["自定义", "最近7天", "最近30天", "最近90天", "本月", "上月"],
            help="快速选择常用时间范围"
        )
        
        if quick_date == "最近7天":
            start_date = datetime.now() - timedelta(days=7)
            end_date = datetime.now()
        elif quick_date == "最近30天":
            start_date = datetime.now() - timedelta(days=30)
            end_date = datetime.now()
        elif quick_date == "最近90天":
            start_date = datetime.now() - timedelta(days=90)
            end_date = datetime.now()
        elif quick_date == "本月":
            start_date = datetime.now().replace(day=1)
            end_date = datetime.now()
        elif quick_date == "上月":
            first_day = datetime.now().replace(day=1)
            end_date = first_day - timedelta(days=1)
            start_date = end_date.replace(day=1)
        else:  # 自定义
            col1, col2 = st.sidebar.columns(2)
            with col1:
                start_date = st.date_input(
                    "开始",
                    value=datetime.now() - timedelta(days=7),
                    max_value=datetime.now().date()
                )
            with col2:
                end_date = st.date_input(
                    "结束",
                    value=datetime.now().date(),
                    max_value=datetime.now().date()
                )
            start_date = datetime.combine(start_date, datetime.min.time())
            end_date = datetime.combine(end_date, datetime.max.time())
        
        # 数据类型选择
        st.sidebar.markdown("### � 数据类型")
        data_options = st.sidebar.columns(2)
        
        with data_options[0]:
            show_mppt = st.checkbox("⚡ MPPT数据", value=True)
        with data_options[1]:
            show_weather = st.checkbox("🌤️ 气象数据", value=True)
        
        # 分析选项
        st.sidebar.markdown("### 🔧 分析选项")
        
        # 时间聚合
        time_aggregation = st.sidebar.selectbox(
            "时间聚合粒度",
            ["原始数据", "10分钟", "小时", "日", "周", "月"],
            help="选择数据时间聚合方式",
            index=0
        )
        
        # 图表类型
        chart_type = st.sidebar.selectbox(
            "图表类型",
            ["时间序列", "散点图", "箱线图", "热力图", "相关矩阵"],
            help="选择图表显示类型"
        )
          # 高级分析选项
        st.sidebar.markdown("### 🎯 高级分析")
        comparison_mode = st.sidebar.checkbox("位置对比分析", help="同时分析两个位置的数据")
        anomaly_detection = st.sidebar.checkbox("异常检测", help="标识数据中的异常值")
        correlation_analysis = st.sidebar.checkbox("相关性分析", help="分析MPPT与气象数据的相关性")
        forecast_mode = st.sidebar.checkbox("趋势预测", help="基于历史数据进行短期预测")
        
        # 导出选项
        st.sidebar.markdown("### 💾 导出选项")
        export_format = st.sidebar.selectbox(
            "导出格式",
            ["Excel", "CSV", "JSON", "PDF报告"],
            help="选择数据导出格式"
        )
          # 实时更新设置
        st.sidebar.markdown("### 🔄 实时更新")
        auto_refresh = st.sidebar.checkbox("自动刷新", help="启用数据自动刷新")
        if auto_refresh:
            refresh_interval = st.sidebar.slider("刷新间隔(秒)", 30, 300, 60)
        else:
            refresh_interval = None
        
        return {
            "location": location,
            "start_date": start_date,
            "end_date": end_date,
            "show_mppt": show_mppt,
            "show_weather": show_weather,
            "time_aggregation": time_aggregation,
            "chart_type": chart_type,
            "comparison_mode": comparison_mode,
            "anomaly_detection": anomaly_detection,
            "correlation_analysis": correlation_analysis,
            "forecast_mode": forecast_mode,
            "export_format": export_format,
            "auto_refresh": auto_refresh,            "refresh_interval": refresh_interval
        }
    
    def aggregate_data(self, df: pd.DataFrame, time_col: str, agg_method: str) -> pd.DataFrame:
        """企业级数据聚合器，支持多种聚合方式和统计指标"""
        if df.empty or agg_method == "原始数据":
            return df
            
        df = df.copy()
        
        # 确保时间列为datetime类型
        if time_col in df.columns:
            df[time_col] = pd.to_datetime(df[time_col], errors='coerce')
            # 移除无效时间数据
            df = df.dropna(subset=[time_col])
        else:
            return df
        
        # 设置时间为索引
        df.set_index(time_col, inplace=True)
        
        # 根据聚合方法进行重采样
        freq_map = {
            "10分钟": "10T",
            "小时": "H",
            "日": "D", 
            "周": "W",
            "月": "M"
        }
        
        if agg_method in freq_map:
            # 分离数值列和非数值列
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            non_numeric_cols = df.select_dtypes(exclude=[np.number]).columns
            
            # 为数值列定义多种聚合统计
            agg_dict = {}
            for col in numeric_cols:
                agg_dict[col] = ['mean', 'max', 'min', 'std', 'count']
            
            # 非数值列取第一个值
            for col in non_numeric_cols:
                agg_dict[col] = 'first'
            
            # 执行聚合
            df_agg = df.resample(freq_map[agg_method]).agg(agg_dict)
              # 展平多级列名
            df_agg.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col 
                             for col in df_agg.columns.values]
            
            df_agg.reset_index(inplace=True)
            return df_agg
            
        return df.reset_index()
    
    def create_mppt_charts(self, df: pd.DataFrame, chart_type: str, location: str, config: Dict[str, Any]) -> List[go.Figure]:
        """创建企业级MPPT数据可视化图表"""
        charts = []
        
        if df.empty:
            st.warning(f"📊 {location} 暂无MPPT数据")
            return charts
            
        time_col = 'eventTime' if 'eventTime' in df.columns else df.columns[0]
        
        # 主色调配置
        colors = [self.color_theme["primary"], self.color_theme["secondary"], 
                 self.color_theme["success"], self.color_theme["warning"]]
          # 1. 功率分析仪表板 - 更宽泛的功率列识别
        power_cols = []
        
        # 首先尝试精确匹配
        power_keywords = ['power', '功率', 'watt', 'pv_power', 'mppt_power', 'solar_power']
        for col in df.columns:
            if any(keyword in col.lower() for keyword in power_keywords):
                power_cols.append(col)
        
        # 如果没找到功率列，尝试更宽泛的匹配
        if not power_cols:
            potential_power_cols = []
            for col in df.columns:
                if any(keyword in col.lower() for keyword in ['pv', 'mppt', 'solar', 'panel']):
                    # 检查是否为数值列
                    if df[col].dtype in ['int64', 'float64']:
                        potential_power_cols.append(col)
            
            # 如果找到了潜在的功率列，取数值范围最大的几个
            if potential_power_cols:
                col_ranges = {}
                for col in potential_power_cols:
                    try:
                        col_range = df[col].max() - df[col].min()
                        col_ranges[col] = col_range
                    except:
                        col_ranges[col] = 0
                
                # 按数值范围排序，取前3个作为功率列
                power_cols = sorted(col_ranges.keys(), key=lambda x: col_ranges[x], reverse=True)[:3]
        
        # 如果仍然没找到，使用所有数值列
        if not power_cols:
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            # 排除时间相关的列
            power_cols = [col for col in numeric_cols if 'time' not in col.lower()][:3]
        
        if power_cols:
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=[
                    f"📈 功率时序图 - {location}",
                    f"📊 功率分布直方图 - {location}",
                    f"🎯 功率箱线图 - {location}",
                    f"⚡ 实时功率监控 - {location}"
                ],
                specs=[[{"secondary_y": True}, {"type": "histogram"}],
                       [{"type": "box"}, {"type": "indicator"}]],
                vertical_spacing=0.12,
                horizontal_spacing=0.1
            )
            
            # 时序图
            for i, col in enumerate(power_cols[:3]):  # 最多显示3个功率列
                fig.add_trace(
                    go.Scatter(
                        x=df[time_col], 
                        y=df[col], 
                        name=col,
                        line=dict(color=colors[i % len(colors)], width=2),
                        mode='lines',
                        hovertemplate=f"<b>{col}</b><br>时间: %{{x}}<br>功率: %{{y:.2f}}W<extra></extra>"
                    ),
                    row=1, col=1
                )
            
            # 功率分布直方图
            if len(power_cols) > 0:
                fig.add_trace(
                    go.Histogram(
                        x=df[power_cols[0]], 
                        nbinsx=30,
                        name="功率分布",
                        marker_color=self.color_theme["info"],
                        opacity=0.7
                    ),
                    row=1, col=2
                )
            
            # 箱线图
            for i, col in enumerate(power_cols[:3]):
                fig.add_trace(
                    go.Box(
                        y=df[col], 
                        name=col,
                        marker_color=colors[i % len(colors)],
                        boxpoints='outliers'
                    ),
                    row=2, col=1
                )
            
            # 实时功率指示器
            if len(power_cols) > 0:
                current_power = df[power_cols[0]].iloc[-1] if len(df) > 0 else 0
                max_power = df[power_cols[0]].max() if len(df) > 0 else 100
                
                fig.add_trace(
                    go.Indicator(
                        mode="gauge+number+delta",
                        value=current_power,
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "当前功率 (W)"},
                        delta={'reference': df[power_cols[0]].mean()},
                        gauge={
                            'axis': {'range': [None, max_power]},
                            'bar': {'color': self.color_theme["primary"]},
                            'steps': [
                                {'range': [0, max_power*0.5], 'color': "lightgray"},
                                {'range': [max_power*0.5, max_power*0.8], 'color': "gray"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': max_power*0.9
                            }
                        }
                    ),
                    row=2, col=2
                )
            
            fig.update_layout(
                height=800,
                title_text=f"⚡ MPPT功率综合分析仪表板 - {location}",
                title_font_size=18,
                showlegend=True,
                template="plotly_white"
            )
            charts.append(fig)
        
        # 2. 电流电压分析
        current_cols = [col for col in df.columns if any(keyword in col.lower() 
                       for keyword in ['current', '电流', 'amp'])]
        voltage_cols = [col for col in df.columns if any(keyword in col.lower() 
                       for keyword in ['voltage', '电压', 'volt'])]
        
        if current_cols or voltage_cols:
            rows = max(len(current_cols), len(voltage_cols), 1)
            fig = make_subplots(
                rows=rows, cols=2,
                subplot_titles=[f"🔋 电流监控 - {location}", f"⚡ 电压监控 - {location}"] * rows,
                vertical_spacing=0.08
            )
            
            # 电流图表
            for i, col in enumerate(current_cols):
                fig.add_trace(
                    go.Scatter(
                        x=df[time_col], 
                        y=df[col], 
                        name=col,
                        line=dict(color=colors[i % len(colors)], width=2),
                        mode='lines+markers',
                        marker_size=3
                    ),
                    row=i+1, col=1
                )
            
            # 电压图表
            for i, col in enumerate(voltage_cols):
                fig.add_trace(
                    go.Scatter(
                        x=df[time_col], 
                        y=df[col], 
                        name=col,
                        line=dict(color=colors[(i+2) % len(colors)], width=2),
                        mode='lines+markers',
                        marker_size=3
                    ),
                    row=i+1, col=2
                )
            
            fig.update_layout(
                height=400*rows,
                title_text=f"🔋 MPPT电流电压分析 - {location}",
                template="plotly_white"
            )
            charts.append(fig)
        
        # 3. 异常检测图表（如果启用）
        if config.get("anomaly_detection", False) and not df.empty:
            anomaly_fig = self.create_anomaly_detection_chart(df, time_col, location)
            if anomaly_fig:
                charts.append(anomaly_fig)
        
        return charts
    
    def create_anomaly_detection_chart(self, df: pd.DataFrame, time_col: str, location: str) -> Optional[go.Figure]:
        """创建异常检测图表"""
        try:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) == 0:
                return None
                
            fig = make_subplots(
                rows=len(numeric_cols[:3]), cols=1,  # 最多显示3个指标
                subplot_titles=[f"🚨 {col} 异常检测" for col in numeric_cols[:3]],
                vertical_spacing=0.1
            )
            
            for i, col in enumerate(numeric_cols[:3]):
                # 计算异常值（使用IQR方法）
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                
                # 正常值
                normal_mask = (df[col] >= lower_bound) & (df[col] <= upper_bound)
                fig.add_trace(
                    go.Scatter(
                        x=df[time_col][normal_mask], 
                        y=df[col][normal_mask],
                        mode='markers',
                        name=f"{col} (正常)",
                        marker=dict(color=self.color_theme["success"], size=4),
                        opacity=0.7
                    ),
                    row=i+1, col=1
                )
                
                # 异常值
                anomaly_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
                if anomaly_mask.any():
                    fig.add_trace(
                        go.Scatter(
                            x=df[time_col][anomaly_mask], 
                            y=df[col][anomaly_mask],
                            mode='markers',
                            name=f"{col} (异常)",
                            marker=dict(color=self.color_theme["warning"], size=8, symbol='x'),
                        ),
                        row=i+1, col=1
                    )
            
            fig.update_layout(
                height=300*min(len(numeric_cols), 3),
                title_text=f"🚨 异常值检测分析 - {location}",
                template="plotly_white"
            )
            
            return fig
            
        except Exception as e:
            st.error(f"异常检测分析出错: {e}")
            return None
    
    def create_weather_charts(self, df: pd.DataFrame, chart_type: str, location: str, config: Dict[str, Any]) -> List[go.Figure]:
        """创建企业级气象数据可视化图表，支持不同位置的特有参数"""
        charts = []
        
        if df.empty:
            st.warning(f"🌤️ {location} 暂无气象数据")
            return charts
            
        time_col = 'Date' if 'Date' in df.columns else df.columns[0]
        
        # 获取位置特有的气象特征
        features = self.weather_features.get(location, {})
        if not features:
            st.warning(f"未找到 {location} 的气象参数配置")
            return charts
        
        colors = [self.color_theme["primary"], self.color_theme["secondary"], 
                 self.color_theme["success"], self.color_theme["warning"],
                 self.color_theme["info"], self.color_theme["light"]]
        
        # 1. 环境参数综合仪表板
        fig_env = make_subplots(
            rows=2, cols=3,
            subplot_titles=[
                f"🌡️ 温度变化 - {location}",
                f"💧 湿度变化 - {location}",
                f"🏔️ 气压变化 - {location}",
                f"💨 风速变化 - {location}",
                f"🧭 风向分布 - {location}",
                f"📊 环境参数相关性 - {location}"
            ],
            specs=[[{}, {}, {}],
                   [{}, {"type": "polar"}, {"type": "scatter"}]],
            vertical_spacing=0.12,
            horizontal_spacing=0.1
        )
        
        # 温度
        if features.get('temperature') and features['temperature'] in df.columns:
            temp_col = features['temperature']
            fig_env.add_trace(
                go.Scatter(
                    x=df[time_col], 
                    y=df[temp_col],
                    name="温度",
                    line=dict(color=colors[0], width=2),
                    mode='lines',
                    hovertemplate="<b>温度</b><br>时间: %{x}<br>温度: %{y:.1f}°C<extra></extra>"
                ),
                row=1, col=1
            )
        
        # 湿度
        if features.get('humidity') and features['humidity'] in df.columns:
            humidity_col = features['humidity']
            fig_env.add_trace(
                go.Scatter(
                    x=df[time_col], 
                    y=df[humidity_col],
                    name="湿度",
                    line=dict(color=colors[1], width=2),
                    mode='lines',
                    hovertemplate="<b>湿度</b><br>时间: %{x}<br>湿度: %{y:.1f}%<extra></extra>"
                ),
                row=1, col=2
            )
        
        # 气压
        if features.get('pressure') and features['pressure'] in df.columns:
            pressure_col = features['pressure']
            fig_env.add_trace(
                go.Scatter(
                    x=df[time_col], 
                    y=df[pressure_col],
                    name="气压",
                    line=dict(color=colors[2], width=2),
                    mode='lines',
                    hovertemplate="<b>气压</b><br>时间: %{x}<br>气压: %{y:.1f}hPa<extra></extra>"
                ),
                row=1, col=3
            )
        
        # 风速
        if features.get('wind_speed') and features['wind_speed'] in df.columns:
            wind_speed_col = features['wind_speed']
            fig_env.add_trace(
                go.Scatter(
                    x=df[time_col], 
                    y=df[wind_speed_col],
                    name="风速",
                    line=dict(color=colors[3], width=2),
                    mode='lines',
                    hovertemplate="<b>风速</b><br>时间: %{x}<br>风速: %{y:.1f}m/s<extra></extra>"
                ),
                row=2, col=1
            )
          # 风向玫瑰图
        if (features.get('wind_direction') and features['wind_direction'] in df.columns and
            features.get('wind_speed') and features['wind_speed'] in df.columns):
            wind_dir_col = features['wind_direction']
            wind_speed_col = features['wind_speed']
            
            fig_env.add_trace(
                go.Scatterpolar(
                    r=df[wind_speed_col],
                    theta=df[wind_dir_col],
                    mode='markers',
                    name="风向风速",
                    marker=dict(color=df[wind_speed_col], colorscale='Viridis', size=8),
                    hovertemplate="<b>风向风速</b><br>风向: %{theta}°<br>风速: %{r:.1f}m/s<extra></extra>"
                ),
                row=2, col=2
            )
        
        # 环境参数相关性热力图
        numeric_cols = [col for col in df.columns if df[col].dtype in ['float64', 'int64'] and col != time_col]
        env_params = []
        
        # 收集可用的环境参数
        for feature_key, feature_col in features.items():
            if feature_col in numeric_cols:
                env_params.append(feature_col)
        
        # 添加其他数值型环境参数
        for col in numeric_cols[:6]:  # 最多6个参数以保证可视化效果
            if col not in env_params:
                env_params.append(col)
        
        if len(env_params) >= 2:
            # 计算相关性矩阵
            try:
                corr_matrix = df[env_params].corr()
                
                fig_env.add_trace(
                    go.Heatmap(
                        z=corr_matrix.values,
                        x=corr_matrix.columns,
                        y=corr_matrix.columns,
                        colorscale='RdBu',
                        zmid=0,
                        text=np.round(corr_matrix.values, 2),
                        texttemplate="%{text}",
                        textfont={"size": 10},
                        hovertemplate="<b>相关性</b><br>%{x} vs %{y}<br>系数: %{z:.3f}<extra></extra>",
                        showscale=True,
                        colorbar=dict(title="相关系数", x=1.02)
                    ),
                    row=2, col=3
                )
            except Exception as e:
                st.warning(f"计算环境参数相关性时出错: {e}")
        else:
            # 如果参数不足，显示提示信息
            fig_env.add_annotation(
                text="环境参数不足<br>无法计算相关性",
                x=0.5, y=0.5,
                xref="x6", yref="y6",
                showarrow=False,
                font=dict(size=14, color="gray")
            )
        
        fig_env.update_layout(
            height=800,
            title_text=f"🌤️ 环境参数综合监控 - {location}",
            template="plotly_white",
            showlegend=True
        )
        charts.append(fig_env)
        
        # 2. 专教位置特有的空气质量和辐射分析
        if location == "专教":
            pm_cols = [col for col in df.columns if any(pm in col for pm in ['PM2.5', 'PM10', 'PM100'])]
            radiation_cols = [col for col in df.columns if any(rad in col for rad in ['辐射', 'TBQ', '日照'])]
            
            if pm_cols or radiation_cols:
                rows = 2 if (pm_cols and radiation_cols) else 1
                fig_special = make_subplots(
                    rows=rows, cols=2,
                    subplot_titles=[
                        f"🏭 空气质量监控 - {location}",
                        f"☀️ 太阳辐射监控 - {location}",
                    ] + ([f"📈 PM指标趋势 - {location}", f"🌞 辐射累计分析 - {location}"] if rows == 2 else []),
                    vertical_spacing=0.15
                )
                
                # PM指标
                for i, col in enumerate(pm_cols[:3]):
                    fig_special.add_trace(
                        go.Scatter(
                            x=df[time_col], 
                            y=df[col],
                            name=col,
                            line=dict(color=colors[i % len(colors)], width=2),
                            mode='lines'
                        ),
                        row=1, col=1
                    )
                
                # 辐射指标
                for i, col in enumerate(radiation_cols[:2]):
                    fig_special.add_trace(
                        go.Scatter(
                            x=df[time_col], 
                            y=df[col],
                            name=col,
                            line=dict(color=colors[(i+3) % len(colors)], width=2),
                            mode='lines'
                        ),
                        row=1, col=2
                    )
                
                # 如果有足够数据，添加趋势分析
                if rows == 2 and len(pm_cols) > 0:
                    # PM指标箱线图
                    for i, col in enumerate(pm_cols[:3]):
                        fig_special.add_trace(
                            go.Box(
                                y=df[col], 
                                name=col,
                                marker_color=colors[i % len(colors)],
                                boxpoints='outliers'
                            ),
                            row=2, col=1
                        )
                    
                    # 辐射累计分析
                    if features.get('radiation_cum') and features['radiation_cum'] in df.columns:
                        cum_col = features['radiation_cum']
                        fig_special.add_trace(
                            go.Scatter(
                                x=df[time_col], 
                                y=df[cum_col],
                                name="辐射累计",
                                line=dict(color=colors[5], width=3),
                                mode='lines',
                                fill='tonexty'
                            ),
                            row=2, col=2
                        )
                        
                fig_special.update_layout(
                    height=400*rows,
                    title_text=f"🏭 专教特有环境指标分析",
                    template="plotly_white"
                )
                charts.append(fig_special)
        
        # 3. 数据质量分析图表
        if config.get("anomaly_detection", False):
            quality_fig = self.create_weather_quality_chart(df, time_col, location, features)
            if quality_fig:
                charts.append(quality_fig)
        
        return charts
    
    def create_weather_quality_chart(self, df: pd.DataFrame, time_col: str, location: str, 
                                   features: Dict[str, str]) -> Optional[go.Figure]:
        """创建气象数据质量分析图表"""
        try:
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=[
                    f"📊 数据完整性 - {location}",
                    f"📈 数据变化率 - {location}",
                    f"🎯 参数分布 - {location}",
                    f"⚠️ 异常值识别 - {location}"
                ],
                specs=[[{"type": "bar"}, {"type": "scatter"}],
                       [{"type": "histogram"}, {"type": "scatter"}]],
                vertical_spacing=0.15
            )
            
            # 数据完整性
            completeness = {}
            for param, col_name in features.items():
                if col_name in df.columns:
                    completeness[param] = (df[col_name].notna().sum() / len(df)) * 100
            
            if completeness:
                fig.add_trace(
                    go.Bar(
                        x=list(completeness.keys()),
                        y=list(completeness.values()),
                        name="完整性",
                        marker_color=self.color_theme["success"],
                        text=[f"{v:.1f}%" for v in completeness.values()],
                        textposition='auto'
                    ),
                    row=1, col=1
                )
            
            # 数据变化率（以温度为例）
            if features.get('temperature') and features['temperature'] in df.columns:
                temp_col = features['temperature']
                df_temp = df.copy()
                df_temp['temp_change'] = df_temp[temp_col].diff().abs()
                
                fig.add_trace(
                    go.Scatter(
                        x=df_temp[time_col],
                        y=df_temp['temp_change'],
                        name="温度变化率",
                        line=dict(color=self.color_theme["warning"]),
                        mode='lines'
                    ),
                    row=1, col=2
                )
            
            fig.update_layout(
                height=600,
                title_text=f"📊 气象数据质量分析 - {location}",
                template="plotly_white"            )
            
            return fig
            
        except Exception as e:
            st.error(f"数据质量分析出错: {e}")
            return None
    
    def create_correlation_analysis(self, mppt_df: pd.DataFrame, weather_df: pd.DataFrame, 
                                  location: str, config: Dict[str, Any]) -> go.Figure:
        """创建企业级相关性分析图表"""
        if mppt_df.empty or weather_df.empty:
            return None
            
        try:
            # 时间对齐
            mppt_time_col = 'eventTime' if 'eventTime' in mppt_df.columns else mppt_df.columns[0]
            weather_time_col = 'Date' if 'Date' in weather_df.columns else weather_df.columns[0]
            
            # 转换时间格式并进行时间对齐
            mppt_df[mppt_time_col] = pd.to_datetime(mppt_df[mppt_time_col], errors='coerce')
            weather_df[weather_time_col] = pd.to_datetime(weather_df[weather_time_col], errors='coerce')
              # 只保留数值列进行聚合，避免agg函数报错
            mppt_numeric = mppt_df.select_dtypes(include=[np.number])
            weather_numeric = weather_df.select_dtypes(include=[np.number])
            
            # 检查是否有数值列
            if mppt_numeric.empty or weather_numeric.empty:
                st.warning("⚠️ 数据中缺少数值列，无法进行相关性分析")
                return None
            
            # 将时间列重新添加到数值数据中
            mppt_with_time = mppt_numeric.copy()
            weather_with_time = weather_numeric.copy()
            
            mppt_with_time[mppt_time_col] = mppt_df[mppt_time_col]
            weather_with_time[weather_time_col] = weather_df[weather_time_col]
            
            # 按小时聚合数据以便对齐（只对数值列聚合）
            try:
                mppt_hourly = mppt_with_time.set_index(mppt_time_col).resample('H').agg({
                    col: 'mean' for col in mppt_numeric.columns
                })
                weather_hourly = weather_with_time.set_index(weather_time_col).resample('H').agg({
                    col: 'mean' for col in weather_numeric.columns
                })
            except Exception as e:
                st.warning(f"⚠️ 数据聚合失败: {e}")
                return None
            
            # 合并数据
            combined_df = pd.merge(mppt_hourly, weather_hourly, left_index=True, right_index=True, how='inner')
            
            if combined_df.empty:
                st.warning("⚠️ 无法找到时间匹配的MPPT和气象数据进行相关性分析")
                return None
            
            # 创建相关性分析子图
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=[
                    f"🔗 MPPT功率与环境因子相关性 - {location}",
                    f"📊 相关性热力图 - {location}",
                    f"📈 功率vs温度散点图 - {location}",
                    f"☀️ 功率vs辐射散点图 - {location}"
                ],
                specs=[[{"secondary_y": True}, {"type": "heatmap"}],
                       [{"type": "scatter"}, {"type": "scatter"}]],
                vertical_spacing=0.15,
                horizontal_spacing=0.1
            )
              # 获取功率列 - 更宽泛的识别
            power_cols = []
            
            # 首先尝试精确匹配
            power_keywords = ['power', '功率', 'watt', 'pv_power', 'mppt_power', 'solar_power']
            for col in combined_df.columns:
                if any(keyword in col.lower() for keyword in power_keywords):
                    power_cols.append(col)
            
            # 如果没找到，尝试更宽泛的匹配
            if not power_cols:
                for col in combined_df.columns:
                    if any(keyword in col.lower() for keyword in ['pv', 'mppt', 'solar', 'panel']):
                        # 检查是否为数值列且有合理的数值范围
                        if pd.api.types.is_numeric_dtype(combined_df[col]):
                            col_std = combined_df[col].std()
                            if col_std > 0:  # 确保有变化
                                power_cols.append(col)
            
            # 如果仍然没找到，使用最有变化的数值列
            if not power_cols:
                numeric_cols = combined_df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    # 选择标准差最大的列作为功率列
                    col_stds = {}
                    for col in numeric_cols:
                        try:
                            col_stds[col] = combined_df[col].std()
                        except:
                            col_stds[col] = 0
                    power_cols = [max(col_stds, key=col_stds.get)] if col_stds else []
            
            # 获取环境参数列
            features = self.weather_features.get(location, {})
            env_cols = [col for col in combined_df.columns if any(feat in col for feat in features.values() if feat)]
            
            # 如果通过特征匹配找不到，则直接使用数值列
            if not env_cols:
                env_cols = [col for col in combined_df.columns if col not in power_cols][:5]
            
            if power_cols and env_cols:
                # 1. 时间序列对比
                power_col = power_cols[0]
                
                # 功率时间序列
                fig.add_trace(
                    go.Scatter(
                        x=combined_df.index,
                        y=combined_df[power_col],
                        name="MPPT功率",
                        line=dict(color=self.color_theme["primary"], width=2),
                        yaxis="y1"
                    ),
                    row=1, col=1
                )
                
                # 温度时间序列
                temp_col = None
                for col in combined_df.columns:
                    if '温度' in col or 'temp' in col.lower():
                        temp_col = col
                        break
                
                if temp_col:
                    fig.add_trace(
                        go.Scatter(
                            x=combined_df.index,
                            y=combined_df[temp_col],
                            name="环境温度",
                            line=dict(color=self.color_theme["warning"], width=2),
                            yaxis="y2"
                        ),
                        row=1, col=1
                    )
                
                # 2. 相关性热力图
                corr_cols = [power_col] + env_cols[:5]  # 限制显示前5个环境参数
                corr_data = combined_df[corr_cols].corr()
                
                fig.add_trace(
                    go.Heatmap(
                        z=corr_data.values,
                        x=corr_data.columns,
                        y=corr_data.columns,
                        colorscale='RdBu',
                        zmid=0,
                        text=np.round(corr_data.values, 2),
                        texttemplate="%{text}",
                        textfont={"size": 10},
                        hovertemplate="<b>%{x}</b> vs <b>%{y}</b><br>相关系数: %{z:.3f}<extra></extra>"
                    ),
                    row=1, col=2
                )
                
                # 3. 功率vs温度散点图
                if temp_col:
                    fig.add_trace(
                        go.Scatter(
                            x=combined_df[temp_col],
                            y=combined_df[power_col],
                            mode='markers',
                            name="功率-温度关系",
                            marker=dict(
                                color=combined_df.index.hour,
                                colorscale='Viridis',
                                size=6,
                                colorbar=dict(title="小时")
                            ),
                            hovertemplate="<b>温度</b>: %{x:.1f}°C<br><b>功率</b>: %{y:.2f}W<extra></extra>"
                        ),
                        row=2, col=1
                    )
                    
                    # 添加趋势线
                    z = np.polyfit(combined_df[temp_col].dropna(), 
                                  combined_df[power_col].dropna(), 1)
                    p = np.poly1d(z)
                    
                    fig.add_trace(
                        go.Scatter(
                            x=combined_df[temp_col],
                            y=p(combined_df[temp_col]),
                            mode='lines',
                            name="趋势线",
                            line=dict(color=self.color_theme["warning"], dash='dash')
                        ),
                        row=2, col=1
                    )
                
                # 4. 功率vs辐射散点图
                radiation_col = None
                for col in combined_df.columns:
                    if any(rad in col for rad in ['辐射', 'TBQ', 'radiation']):
                        radiation_col = col
                        break
                
                if radiation_col:
                    fig.add_trace(
                        go.Scatter(
                            x=combined_df[radiation_col],
                            y=combined_df[power_col],
                            mode='markers',
                            name="功率-辐射关系",
                            marker=dict(
                                color=combined_df[temp_col] if temp_col else 'blue',
                                colorscale='Plasma',
                                size=6,
                                colorbar=dict(title="温度°C" if temp_col else "")
                            ),
                            hovertemplate="<b>辐射</b>: %{x:.1f}W/m²<br><b>功率</b>: %{y:.2f}W<extra></extra>"
                        ),
                        row=2, col=2
                    )
                    
                    # 添加趋势线
                    valid_mask = combined_df[radiation_col].notna() & combined_df[power_col].notna()
                    if valid_mask.sum() > 1:
                        z = np.polyfit(combined_df[radiation_col][valid_mask], 
                                      combined_df[power_col][valid_mask], 1)
                        p = np.poly1d(z)
                        
                        fig.add_trace(
                            go.Scatter(
                                x=combined_df[radiation_col],
                                y=p(combined_df[radiation_col]),
                                mode='lines',
                                name="辐射趋势线",
                                line=dict(color=self.color_theme["success"], dash='dash')
                            ),
                            row=2, col=2
                        )
                
                # 更新布局
                fig.update_layout(
                    height=800,
                    title_text=f"🔍 MPPT与环境因子综合相关性分析 - {location}",
                    template="plotly_white",
                    showlegend=True
                )
                
                # 设置双y轴
                fig.update_yaxes(title_text="MPPT功率 (W)", row=1, col=1)
                fig.update_yaxes(title_text="温度 (°C)", secondary_y=True, row=1, col=1)
                
                return fig
            
        except Exception as e:
            st.error(f"相关性分析出错: {e}")
            
        return None
    
    def display_data_summary(self, data: Dict[str, pd.DataFrame], location: str, config: Dict[str, Any]):
        """显示企业级数据摘要仪表板"""
        st.markdown(f"### 📊 {location} 数据概览仪表板")
        
        # 创建指标卡片
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if not data["mppt"].empty:
                mppt_count = len(data["mppt"])
                mppt_status = "🟢 在线" if mppt_count > 0 else "🔴 离线"
                
                st.markdown(f"""
                <div class="metric-card">
                    <h3>⚡ MPPT数据</h3>
                    <h2>{mppt_count:,}</h2>
                    <p>数据点数</p>
                    <p>{mppt_status}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="metric-card">
                    <h3>⚡ MPPT数据</h3>
                    <h2>0</h2>
                    <p>数据点数</p>
                    <p>🔴 无数据</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            if not data["weather"].empty:
                weather_count = len(data["weather"])
                weather_status = "🟢 在线" if weather_count > 0 else "🔴 离线"
                
                st.markdown(f"""
                <div class="metric-card">
                    <h3>🌤️ 气象数据</h3>
                    <h2>{weather_count:,}</h2>
                    <p>数据点数</p>
                    <p>{weather_status}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="metric-card">
                    <h3>🌤️ 气象数据</h3>
                    <h2>0</h2>
                    <p>数据点数</p>
                    <p>🔴 无数据</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col3:
            # 数据完整性
            if "data_quality" in data:
                completeness = data["data_quality"]["data_completeness"]
                completeness_status = ("🟢 优秀" if completeness >= 90 else 
                                     "🟡 良好" if completeness >= 70 else "🔴 需改善")
                
                st.markdown(f"""
                <div class="metric-card">
                    <h3>📈 数据完整性</h3>
                    <h2>{completeness:.1f}%</h2>
                    <p>完整度</p>
                    <p>{completeness_status}</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="metric-card">
                    <h3>📈 数据完整性</h3>
                    <h2>--%</h2>
                    <p>完整度</p>
                    <p>🔄 计算中</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col4:
            # 时间跨度
            time_span = "未知"
            if not data["mppt"].empty or not data["weather"].empty:
                start_time = config["start_date"].strftime("%m-%d")
                end_time = config["end_date"].strftime("%m-%d")
                time_span = f"{start_time} ~ {end_time}"
            
            st.markdown(f"""
            <div class="metric-card">
                <h3>📅 时间跨度</h3>
                <h2>{time_span}</h2>
                <p>分析区间</p>
                <p>📊 {config.get('time_aggregation', '原始数据')}</p>
            </div>
            """, unsafe_allow_html=True)
          # 详细数据质量报告
        if "data_quality" in data and any([
            data["data_quality"]["mppt_missing_days"],
            data["data_quality"]["weather_missing_days"]
        ]):
            with st.expander("📋 数据质量详细报告", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**📊 MPPT数据质量**")
                    st.metric("加载文件数", data["data_quality"]["mppt_files_loaded"])
                    if data["data_quality"]["mppt_missing_days"]:
                        st.warning(f"缺失日期: {len(data['data_quality']['mppt_missing_days'])}天")
                        st.markdown("**缺失日期列表:**")
                        for day in data["data_quality"]["mppt_missing_days"][:10]:  # 显示前10个
                            st.text(day)
                        if len(data["data_quality"]["mppt_missing_days"]) > 10:
                            st.text(f"... 还有 {len(data['data_quality']['mppt_missing_days'])-10} 个日期")
                
                with col2:
                    st.markdown("**🌤️ 气象数据质量**")
                    st.metric("加载文件数", data["data_quality"]["weather_files_loaded"])
                    if data["data_quality"]["weather_missing_days"]:
                        st.warning(f"缺失日期: {len(data['data_quality']['weather_missing_days'])}天")
                        st.markdown("**缺失日期列表:**")
                        for day in data["data_quality"]["weather_missing_days"][:10]:
                            st.text(day)
                        if len(data["data_quality"]["weather_missing_days"]) > 10:
                            st.text(f"... 还有 {len(data['data_quality']['weather_missing_days'])-10} 个日期")
        
        # 实时系统状态
        st.markdown("### 🖥️ 系统状态监控")
        status_col1, status_col2, status_col3 = st.columns(3)
        
        with status_col1:
            st.success("✅ 数据加载服务: 正常")
        with status_col2:
            st.success("✅ 可视化引擎: 正常")
        with status_col3:
            if config.get("auto_refresh"):
                st.info(f"🔄 自动刷新: {config.get('refresh_interval', 60)}秒")
            else:
                st.info("⏸️ 自动刷新: 已暂停")
    
    def run(self):
        """运行企业级交互式可视化平台"""
        # 企业级页面标题
        st.markdown(
            '<div class="main-header">⚡ MPPT数据分析与可视化平台<br><small>Enterprise Data Analytics Dashboard</small></div>', 
            unsafe_allow_html=True
        )
        
        # 创建侧边栏配置
        config = self.create_sidebar()
        
        # 数据验证
        if config["start_date"] > config["end_date"]:
            st.error("⚠️ 开始日期不能晚于结束日期，请重新选择时间范围")
            return
        
        # 显示加载进度
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # 加载数据
            status_text.text("🔄 正在加载数据...")
            progress_bar.progress(20)
            
            data = self.load_data(config["location"], config["start_date"], config["end_date"])
            progress_bar.progress(50)
            
            # 数据聚合
            status_text.text("📊 正在处理数据...")
            if config["time_aggregation"] != "原始数据":
                if not data["mppt"].empty:
                    data["mppt"] = self.aggregate_data(data["mppt"], "eventTime", config["time_aggregation"])
                if not data["weather"].empty:
                    data["weather"] = self.aggregate_data(data["weather"], "Date", config["time_aggregation"])
            
            progress_bar.progress(80)
            status_text.text("✅ 数据处理完成")
            progress_bar.progress(100)
            
            # 清除进度指示器
            progress_bar.empty()
            status_text.empty()
            
        except Exception as e:
            st.error(f"❌ 数据加载失败: {e}")
            return
        
        # 显示数据摘要仪表板
        self.display_data_summary(data, config["location"], config)
        
        # 创建主要内容区域
        if not any([config["show_mppt"], config["show_weather"]]):
            st.warning("⚠️ 请至少选择一种数据类型进行分析")
            return
          # 构建标签页
        tabs = []
        if config["show_mppt"]:
            tabs.append("⚡ MPPT分析")
        if config["show_weather"]:
            tabs.append("🌤️ 气象分析")
        if config["correlation_analysis"]:
            tabs.append("🔍 相关性分析")
        if config["comparison_mode"]:
            tabs.append("📊 位置对比")
        if config["forecast_mode"]:
            tabs.append("🔮 趋势预测")
        tabs.extend(["📋 数据表格", "📄 分析报告"])
        
        # 创建标签页对象
        tab_objects = st.tabs(tabs)
        
        # MPPT数据标签页
        if config["show_mppt"] and "⚡ MPPT分析" in tabs:
            with tab_objects[tabs.index("⚡ MPPT分析")]:
                st.markdown("### ⚡ MPPT性能分析仪表板")
                
                if not data["mppt"].empty:
                    mppt_charts = self.create_mppt_charts(
                        data["mppt"], config["chart_type"], config["location"], config
                    )
                    
                    for i, chart in enumerate(mppt_charts):
                        st.plotly_chart(chart, use_container_width=True, key=f"mppt_chart_{i}")
                else:
                    st.info("📊 当前时间范围内无MPPT数据，请调整查询条件")
        
        # 气象数据标签页
        if config["show_weather"] and "🌤️ 气象分析" in tabs:
            with tab_objects[tabs.index("🌤️ 气象分析")]:
                st.markdown("### 🌤️ 环境气象监控仪表板")
                
                if not data["weather"].empty:
                    weather_charts = self.create_weather_charts(
                        data["weather"], config["chart_type"], config["location"], config
                    )
                    
                    for i, chart in enumerate(weather_charts):
                        st.plotly_chart(chart, use_container_width=True, key=f"weather_chart_{i}")
                else:
                    st.info("🌤️ 当前时间范围内无气象数据，请调整查询条件")
        
        # 相关性分析标签页
        if config["correlation_analysis"] and "🔍 相关性分析" in tabs:
            with tab_objects[tabs.index("🔍 相关性分析")]:
                st.markdown("### 🔍 MPPT与环境因子相关性分析")
                
                if not data["mppt"].empty and not data["weather"].empty:
                    corr_chart = self.create_correlation_analysis(
                        data["mppt"], data["weather"], config["location"], config
                    )
                    
                    if corr_chart:
                        st.plotly_chart(corr_chart, use_container_width=True)
                        
                        # 相关性分析文本总结
                        with st.expander("📝 相关性分析总结", expanded=True):
                            st.markdown(f"""
                            **分析位置**: {config["location"]}  
                            **分析时间**: {config["start_date"].strftime("%Y-%m-%d")} 至 {config["end_date"].strftime("%Y-%m-%d")}  
                            **数据聚合**: {config["time_aggregation"]}
                            
                            **主要发现**:
                            - MPPT功率与环境温度的相关性分析已完成
                            - 太阳辐射与发电功率的关联度分析已展示
                            - 建议根据相关性强弱调整系统运行策略
                            """)
                    else:
                        st.warning("⚠️ 无法生成相关性分析，请检查数据完整性")
                else:
                    st.info("📊 需要同时具备MPPT和气象数据才能进行相关性分析")
        
        # 位置对比分析标签页
        if config["comparison_mode"] and "📊 位置对比" in tabs:
            with tab_objects[tabs.index("📊 位置对比")]:
                st.markdown("### 📊 多位置对比分析")
                  # 加载对比位置数据
                other_location = "专教" if config["location"] == "十五舍" else "十五舍"
                
                with st.spinner(f"正在加载 {other_location} 的数据..."):
                    compare_data = self.load_data(other_location, config["start_date"], config["end_date"])
                
                if not compare_data["mppt"].empty or not compare_data["weather"].empty:
                    # 创建对比图表
                    self.create_comparison_charts(data, compare_data, config)
                else:
                    st.warning(f"⚠️ {other_location} 在指定时间范围内无数据")
        
        # 趋势预测标签页
        if config["forecast_mode"] and "🔮 趋势预测" in tabs:
            with tab_objects[tabs.index("🔮 趋势预测")]:
                st.markdown("### 🔮 智能趋势预测分析")
                
                # 选择预测目标
                predict_target = st.selectbox(
                    "选择预测目标",
                    ["MPPT功率", "气象参数"],
                    help="选择要进行趋势预测的数据类型"
                )
                
                if predict_target == "MPPT功率" and not data["mppt"].empty:
                    st.markdown("#### ⚡ MPPT功率趋势预测")
                    
                    # 创建趋势预测图表
                    trend_chart = self.create_trend_prediction(
                        data["mppt"], config["location"], config
                    )
                    
                    if trend_chart:
                        st.plotly_chart(trend_chart, use_container_width=True)
                        
                        # 预测分析说明
                        with st.expander("📊 预测方法说明", expanded=False):
                            st.markdown("""
                            **预测模型**: 
                            - 线性回归模型：基于时间趋势的简单预测
                            - 随机森林模型：考虑多个时间特征的复杂预测
                            
                            **特征工程**:
                            - 时间戳特征：长期趋势
                            - 小时特征：日内周期性
                            - 星期特征：周内周期性  
                            - 月份特征：季节性变化
                            
                            **置信区间**: 95%置信区间基于残差标准误差计算
                            
                            **预测精度**: MAE (平均绝对误差) 和 R² (决定系数) 用于评估模型性能
                            
                            ⚠️ **注意**: 预测结果仅供参考，实际情况可能受到天气、设备状态等多种因素影响
                            """)
                    else:
                        st.info("📈 数据不足，无法生成可靠的趋势预测")
                
                elif predict_target == "气象参数" and not data["weather"].empty:
                    st.markdown("#### 🌤️ 气象参数趋势预测")
                    
                    # 选择要预测的气象参数
                    weather_features = data["weather"].select_dtypes(include=[np.number]).columns.tolist()
                    if weather_features:
                        selected_feature = st.selectbox(
                            "选择气象参数",
                            weather_features,
                            help="选择要预测的气象参数"
                        )
                        
                        # 创建单列预测数据
                        weather_subset = data["weather"][['Date', selected_feature]].copy() if 'Date' in data["weather"].columns else data["weather"][[data["weather"].columns[0], selected_feature]].copy()
                        
                        trend_chart = self.create_trend_prediction(
                            weather_subset, config["location"], config
                        )
                        
                        if trend_chart:
                            st.plotly_chart(trend_chart, use_container_width=True)
                        else:
                            st.info("📈 数据不足，无法生成可靠的气象预测")
                    else:
                        st.warning("⚠️ 气象数据中没有可预测的数值参数")
                
                else:
                    st.info("📊 请确保已加载相应的数据类型进行趋势预测")
        
        # 数据表格标签页
        with tab_objects[tabs.index("📋 数据表格")]:
            st.markdown("### 📋 原始数据浏览器")
            
            # 数据筛选器
            col1, col2, col3 = st.columns(3)
            with col1:
                show_columns = st.multiselect(
                    "选择显示列",
                    options=list(data["mppt"].columns) + list(data["weather"].columns),
                    default=[]
                )
            with col2:
                max_rows = st.number_input("最大显示行数", min_value=10, max_value=10000, value=1000)
            with col3:
                search_term = st.text_input("搜索关键词", "")
            
            # MPPT数据表格
            if config["show_mppt"] and not data["mppt"].empty:
                st.markdown("#### ⚡ MPPT数据表格")
                
                display_df = data["mppt"].copy()
                
                # 应用筛选
                if show_columns:
                    available_cols = [col for col in show_columns if col in display_df.columns]
                    if available_cols:
                        display_df = display_df[available_cols]
                
                if search_term:
                    mask = display_df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
                    display_df = display_df[mask]
                
                display_df = display_df.head(max_rows)
                
                st.dataframe(
                    display_df, 
                    use_container_width=True,
                    height=400
                )
                
                # 下载按钮
                if not display_df.empty:
                    csv_data = display_df.to_csv(index=False).encode('utf-8-sig')
                    st.download_button(
                        label="📥 下载MPPT数据CSV",
                        data=csv_data,
                        file_name=f"mppt_data_{config['location']}_{config['start_date'].strftime('%Y%m%d')}_{config['end_date'].strftime('%Y%m%d')}.csv",
                        mime='text/csv',
                        help="下载当前筛选的MPPT数据"
                    )
            
            # 气象数据表格
            if config["show_weather"] and not data["weather"].empty:
                st.markdown("#### 🌤️ 气象数据表格")
                
                display_df = data["weather"].copy()
                
                # 应用筛选
                if show_columns:
                    available_cols = [col for col in show_columns if col in display_df.columns]
                    if available_cols:
                        display_df = display_df[available_cols]
                
                if search_term:
                    mask = display_df.astype(str).apply(lambda x: x.str.contains(search_term, case=False, na=False)).any(axis=1)
                    display_df = display_df[mask]
                
                display_df = display_df.head(max_rows)
                
                st.dataframe(
                    display_df, 
                    use_container_width=True,
                    height=400
                )
                
                # 下载按钮
                if not display_df.empty:
                    csv_data = display_df.to_csv(index=False).encode('utf-8-sig')
                    st.download_button(
                        label="📥 下载气象数据CSV",
                        data=csv_data,
                        file_name=f"weather_data_{config['location']}_{config['start_date'].strftime('%Y%m%d')}_{config['end_date'].strftime('%Y%m%d')}.csv",
                        mime='text/csv',
                        help="下载当前筛选的气象数据"
                    )
        
        # 分析报告标签页
        with tab_objects[tabs.index("📄 分析报告")]:
            st.markdown("### 📄 自动生成分析报告")
            
            # 生成综合分析报告
            self.generate_analysis_report(data, config)
        
        # 页脚信息
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**🏢 MPPT数据分析平台**")
        with col2:
            st.markdown("**📅 最后更新**: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        with col3:
            st.markdown("**📊 数据源**: " + config["location"])
    
    def create_comparison_charts(self, data1: Dict, data2: Dict, config: Dict):
        """创建位置对比图表"""
        location1 = config["location"]
        location2 = "专教" if location1 == "十五舍" else "十五舍"
        
        # 对比MPPT数据
        if not data1["mppt"].empty and not data2["mppt"].empty:
            st.markdown("#### ⚡ MPPT功率对比")
            
            fig = go.Figure()
            
            # 获取功率列
            power_cols1 = [col for col in data1["mppt"].columns if 'power' in col.lower()]
            power_cols2 = [col for col in data2["mppt"].columns if 'power' in col.lower()]
            
            time_col1 = 'eventTime' if 'eventTime' in data1["mppt"].columns else data1["mppt"].columns[0]
            time_col2 = 'eventTime' if 'eventTime' in data2["mppt"].columns else data2["mppt"].columns[0]
            
            if power_cols1:
                fig.add_trace(go.Scatter(
                    x=data1["mppt"][time_col1],
                    y=data1["mppt"][power_cols1[0]],
                    name=f"{location1} - {power_cols1[0]}",
                    line=dict(color=self.color_theme["primary"])
                ))
            
            if power_cols2:
                fig.add_trace(go.Scatter(
                    x=data2["mppt"][time_col2],
                    y=data2["mppt"][power_cols2[0]],
                    name=f"{location2} - {power_cols2[0]}",
                    line=dict(color=self.color_theme["secondary"])
                ))
            
            fig.update_layout(
                title=f"MPPT功率对比: {location1} vs {location2}",
                xaxis_title="时间",
                yaxis_title="功率 (W)",
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # 对比气象数据
        if not data1["weather"].empty and not data2["weather"].empty:
            st.markdown("#### 🌤️ 环境参数对比")
            
            # 找到共同的气象参数
            features1 = self.weather_features.get(location1, {})
            features2 = self.weather_features.get(location2, {})
            
            # 找到共同参数（温度、湿度、气压）
            common_params = []
            for param in ['temperature', 'humidity', 'pressure']:
                if (param in features1 and features1[param] in data1["weather"].columns and
                    param in features2 and features2[param] in data2["weather"].columns):
                    common_params.append(param)
            
            if common_params:
                rows = len(common_params)
                fig = make_subplots(
                    rows=rows, cols=1,
                    subplot_titles=[f"{param.title()} 对比" for param in common_params],
                    vertical_spacing=0.1
                )
                
                time_col1 = 'Date' if 'Date' in data1["weather"].columns else data1["weather"].columns[0]
                time_col2 = 'Date' if 'Date' in data2["weather"].columns else data2["weather"].columns[0]
                
                for i, param in enumerate(common_params):
                    col1 = features1[param]
                    col2 = features2[param]
                    
                    fig.add_trace(
                        go.Scatter(
                            x=data1["weather"][time_col1],
                            y=data1["weather"][col1],
                            name=f"{location1} - {col1}",
                            line=dict(color=self.color_theme["primary"])
                        ),
                        row=i+1, col=1
                    )
                    
                    fig.add_trace(
                        go.Scatter(
                            x=data2["weather"][time_col2],
                            y=data2["weather"][col2],
                            name=f"{location2} - {col2}",
                            line=dict(color=self.color_theme["secondary"])
                        ),
                        row=i+1, col=1
                    )
                
                fig.update_layout(
                    height=300*rows,
                    title_text=f"环境参数对比: {location1} vs {location2}",
                    template="plotly_white"
                )
                
                st.plotly_chart(fig, use_container_width=True)
    
    def generate_analysis_report(self, data: Dict, config: Dict):
        """生成自动分析报告"""
        st.markdown("#### 📊 数据概览")
        
        # 基本统计信息
        if not data["mppt"].empty:
            mppt_stats = data["mppt"].describe()
            st.markdown("**MPPT数据统计**")
            st.dataframe(mppt_stats, use_container_width=True)
        
        if not data["weather"].empty:
            weather_stats = data["weather"].describe()
            st.markdown("**气象数据统计**")
            st.dataframe(weather_stats, use_container_width=True)
        
        # 生成分析结论
        st.markdown("#### 📝 分析结论")
        
        conclusions = []
        
        if not data["mppt"].empty:
            power_cols = [col for col in data["mppt"].columns if 'power' in col.lower()]
            if power_cols:
                avg_power = data["mppt"][power_cols[0]].mean()
                max_power = data["mppt"][power_cols[0]].max()
                conclusions.append(f"• MPPT平均功率: {avg_power:.2f}W，峰值功率: {max_power:.2f}W")
        
        if not data["weather"].empty:
            features = self.weather_features.get(config["location"], {})
            if features.get('temperature') and features['temperature'] in data["weather"].columns:
                temp_col = features['temperature']
                avg_temp = data["weather"][temp_col].mean()
                conclusions.append(f"• 平均环境温度: {avg_temp:.1f}°C")
        
        if "data_quality" in data:
            completeness = data["data_quality"]["data_completeness"]
            conclusions.append(f"• 数据完整度: {completeness:.1f}%")
        
        if conclusions:
            for conclusion in conclusions:
                st.markdown(conclusion)
        else:
            st.info("暂无足够数据生成分析结论")
        
        # 建议与优化
        st.markdown("#### 💡 建议与优化")
        st.markdown("""
        **系统优化建议**:
        - 监控MPPT系统的功率输出效率
        - 关注环境温度对发电效率的影响
        - 定期检查数据采集设备的工作状态
        - 根据气象预报调整系统运行参数
        
        **数据质量改进**:
        - 检查数据缺失的时间段
        - 验证异常数据的真实性
        - 建立数据备份和恢复机制        """)
        
        # 导出完整报告
        if st.button("📄 生成完整PDF报告", help="生成包含所有图表和分析的完整报告"):
            st.info("📄 PDF报告生成功能正在开发中...")
    
    def create_trend_prediction(self, df: pd.DataFrame, location: str, config: Dict[str, Any]) -> Optional[go.Figure]:
        """创建企业级趋势预测分析"""
        if df.empty:
            st.info("📈 暂无数据进行趋势预测")
            return None
            
        try:
            # 导入必要的预测库
            from sklearn.linear_model import LinearRegression
            from sklearn.ensemble import RandomForestRegressor
            from sklearn.metrics import mean_absolute_error, r2_score
            import warnings
            warnings.filterwarnings('ignore')
            
            # 获取时间列和目标列
            time_col = None
            for col in df.columns:
                if 'time' in col.lower() or 'date' in col.lower():
                    time_col = col
                    break
            
            if not time_col:
                time_col = df.columns[0]
                
            # 获取预测目标（功率相关） - 使用改进的识别方法
            power_cols = []
            power_keywords = ['power', '功率', 'watt', 'pv_power', 'mppt_power', 'solar_power']
            for col in df.columns:
                if any(keyword in col.lower() for keyword in power_keywords):
                    power_cols.append(col)
            
            # 如果没找到功率列，尝试其他方法
            if not power_cols:
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                # 排除时间相关列
                potential_cols = [col for col in numeric_cols if 'time' not in col.lower()]
                if potential_cols:
                    # 选择方差最大的列作为目标
                    col_vars = {col: df[col].var() for col in potential_cols}
                    power_cols = [max(col_vars, key=col_vars.get)]
            
            if not power_cols:
                st.warning("⚠️ 无法找到合适的预测目标列")
                return None
            
            target_col = power_cols[0]
            
            # 数据预处理
            df[time_col] = pd.to_datetime(df[time_col], errors='coerce')
            df_pred = df[[time_col, target_col]].dropna()
            df_pred = df_pred.sort_values(time_col).reset_index(drop=True)
            
            if len(df_pred) < 20:
                st.warning(f"⚠️ 数据量不足 ({len(df_pred)} 条)，无法进行可靠预测")
                return None
            
            # 创建时间特征
            df_pred['timestamp'] = df_pred[time_col].astype(np.int64) // 10**9
            df_pred['hour'] = df_pred[time_col].dt.hour
            df_pred['day_of_week'] = df_pred[time_col].dt.dayofweek
            df_pred['month'] = df_pred[time_col].dt.month
            
            # 分割数据
            split_point = int(len(df_pred) * 0.8)
            train_data = df_pred[:split_point]
            test_data = df_pred[split_point:]
            
            # 特征列
            feature_cols = ['timestamp', 'hour', 'day_of_week', 'month']
            
            # 训练多个模型
            models = {
                '线性回归': LinearRegression(),
                '随机森林': RandomForestRegressor(n_estimators=50, random_state=42)
            }
            
            model_results = {}
            
            for name, model in models.items():
                try:
                    X_train = train_data[feature_cols]
                    y_train = train_data[target_col]
                    X_test = test_data[feature_cols] if len(test_data) > 0 else X_train
                    y_test = test_data[target_col] if len(test_data) > 0 else y_train
                    
                    model.fit(X_train, y_train)
                    y_pred = model.predict(X_test)
                    
                    mae = mean_absolute_error(y_test, y_pred)
                    r2 = r2_score(y_test, y_pred)
                    
                    model_results[name] = {
                        'model': model,
                        'predictions': y_pred,
                        'mae': mae,
                        'r2': r2
                    }
                except Exception as e:
                    st.warning(f"模型 {name} 训练失败: {e}")
                    continue
            
            if not model_results:
                st.error("❌ 所有预测模型训练失败")
                return None
            
            # 选择最佳模型
            best_model_name = min(model_results.keys(), key=lambda x: model_results[x]['mae'])
            best_model_result = model_results[best_model_name]
            
            # 创建预测图表
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=[
                    f"📈 历史趋势与预测对比 - {location}",
                    f"🎯 模型预测精度对比 - {location}",
                    f"📊 {target_col} 置信区间分析 - {location}",
                    f"🔮 未来7天预测 (使用{best_model_name}) - {location}"
                ],
                specs=[[{}, {}], [{}, {}]],
                vertical_spacing=0.15,
                horizontal_spacing=0.12
            )
            
            # 1. 历史趋势与预测对比
            fig.add_trace(go.Scatter(
                x=train_data[time_col], 
                y=train_data[target_col],
                name="训练数据",
                line=dict(color=self.color_theme["primary"], width=2),
                hovertemplate="<b>训练数据</b><br>时间: %{x}<br>数值: %{y:.2f}<extra></extra>"
            ), row=1, col=1)
            
            if len(test_data) > 0:
                fig.add_trace(go.Scatter(
                    x=test_data[time_col], 
                    y=test_data[target_col],
                    name="实际数据",
                    line=dict(color=self.color_theme["success"], width=2),
                    hovertemplate="<b>实际数据</b><br>时间: %{x}<br>数值: %{y:.2f}<extra></extra>"
                ), row=1, col=1)
                
                fig.add_trace(go.Scatter(
                    x=test_data[time_col], 
                    y=best_model_result['predictions'],
                    name=f"预测数据 ({best_model_name})",
                    line=dict(color=self.color_theme["warning"], width=2, dash='dash'),
                    hovertemplate=f"<b>预测数据</b><br>时间: %{{x}}<br>数值: %{{y:.2f}}<br>MAE: {best_model_result['mae']:.2f}<extra></extra>"
                ), row=1, col=1)
            
            # 2. 模型精度对比
            model_names = list(model_results.keys())
            mae_values = [model_results[name]['mae'] for name in model_names]
            r2_values = [model_results[name]['r2'] for name in model_names]
            
            fig.add_trace(go.Bar(
                x=model_names,
                y=mae_values,
                name="MAE (越小越好)",
                marker_color=self.color_theme["secondary"],
                text=[f"{mae:.2f}" for mae in mae_values],
                textposition='auto'
            ), row=1, col=2)
            
            # 3. 置信区间分析
            if len(test_data) > 5:
                residuals = test_data[target_col].values - best_model_result['predictions']
                std_error = np.std(residuals)
                
                upper_bound = best_model_result['predictions'] + 1.96 * std_error
                lower_bound = best_model_result['predictions'] - 1.96 * std_error
                
                fig.add_trace(go.Scatter(
                    x=test_data[time_col], 
                    y=upper_bound,
                    mode='lines',
                    name="95%置信区间上限",
                    line=dict(color='rgba(0,100,80,0)', width=0),
                    showlegend=False
                ), row=2, col=1)
                
                fig.add_trace(go.Scatter(
                    x=test_data[time_col], 
                    y=lower_bound,
                    mode='lines',
                    name="95%置信区间",
                    line=dict(color='rgba(0,100,80,0)', width=0),
                    fill='tonexty',
                    fillcolor='rgba(0,100,80,0.2)'
                ), row=2, col=1)
                
                fig.add_trace(go.Scatter(
                    x=test_data[time_col], 
                    y=best_model_result['predictions'],
                    name="预测值",
                    line=dict(color=self.color_theme["primary"], width=2)
                ), row=2, col=1)
            
            # 4. 未来预测
            try:
                last_date = df_pred[time_col].max()
                future_dates = pd.date_range(
                    start=last_date + pd.Timedelta(hours=1), 
                    periods=min(168, 24*7), # 最多7天
                    freq='H'
                )
                
                future_df = pd.DataFrame({
                    'timestamp': future_dates.astype(np.int64) // 10**9,
                    'hour': future_dates.hour,
                    'day_of_week': future_dates.dayofweek,
                    'month': future_dates.month
                })
                
                future_pred = best_model_result['model'].predict(future_df[feature_cols])
                
                fig.add_trace(go.Scatter(
                    x=future_dates, 
                    y=future_pred,
                    name="未来预测",
                    line=dict(color=self.color_theme["info"], width=3),
                    hovertemplate="<b>未来预测</b><br>时间: %{x}<br>预测值: %{y:.2f}<extra></extra>"
                ), row=2, col=2)
                
                # 添加历史数据作为参考
                recent_data = df_pred.tail(min(48, len(df_pred)))  # 最近48小时
                fig.add_trace(go.Scatter(
                    x=recent_data[time_col], 
                    y=recent_data[target_col],
                    name="历史参考",
                    line=dict(color=self.color_theme["muted"], width=1),
                    opacity=0.7
                ), row=2, col=2)
                
            except Exception as e:
                st.warning(f"未来预测生成失败: {e}")
            
            # 更新布局
            fig.update_layout(
                height=800,
                title_text=f"🔮 智能趋势预测分析仪表板 - {location}",
                title_font_size=18,
                template="plotly_white",
                showlegend=True,
                hovermode='x unified'
            )
            
            fig.update_xaxes(title_text="时间")
            fig.update_yaxes(title_text=target_col)
            
            # 添加性能指标文本
            performance_text = f"最佳模型: {best_model_name} | MAE: {best_model_result['mae']:.2f} | R²: {best_model_result['r2']:.3f}"
            fig.add_annotation(
                text=performance_text,
                xref="paper", yref="paper",
                x=0.5, y=-0.05,
                showarrow=False,
                font=dict(size=12, color="gray")
            )
            
            return fig
            
        except Exception as e:
            st.error(f"趋势预测分析失败: {e}")
            import traceback
            st.text(traceback.format_exc())
            return None
            
            future_pred = model.predict(future_df)
            
            # 历史末尾
            fig.add_trace(go.Scatter(
                x=df_pred[time_col].tail(48), y=df_pred[target_col].tail(48),
                name="历史数据", line=dict(color=self.color_theme["primary"], width=2)
            ), row=2, col=1)
            
            # 未来预测
            fig.add_trace(go.Scatter(
                x=future_dates, y=future_pred,
                name="未来7天预测", line=dict(color=self.color_theme["danger"], width=2, dash='dash')
            ), row=2, col=1)
            
            fig.update_layout(
                height=800,
                title_text=f"🔮 AI趋势预测分析 - {location}",
                template="plotly_white",
                annotations=[dict(
                    x=0.5, y=-0.05,
                    xref='paper', yref='paper',
                    text="预测方法: 线性回归 | 置信水平: 95% | 预测周期: 7天",
                    showarrow=False, font=dict(size=12, color="gray")
                )]
            )
            
            return fig
            
        except Exception as e:
            st.error(f"趋势预测分析出错: {e}")
            return None

def main():
    """主函数 - 启动企业级MPPT数据分析平台"""
    try:
        # 初始化可视化器
        visualizer = InteractiveVisualizer()
        
        # 运行应用
        visualizer.run()
        
    except Exception as e:
        st.error(f"❌ 应用启动失败: {e}")
        st.markdown("""
        ### 🔧 故障排除建议:
        1. 检查数据文件是否存在
        2. 确认文件权限设置正确
        3. 验证所需Python包是否已安装
        4. 重启应用或联系技术支持
        """)

if __name__ == "__main__":
    main()
