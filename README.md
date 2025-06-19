# MPPT数据分析与可视化项目

## 项目概述

本项目主要用于从涂鸦云API提取光伏MPPT控制器数据，并与气象站数据相结合进行预处理、分析和可视化。项目使用Python编程语言，基于Jupyter Notebook作为分析工具，旨在探索光伏系统的性能与气象条件之间的关系。

## 文件夹结构

```
MPPT_cur_power/
│
├── MPPT_Extract.ipynb                    # MPPT数据从涂鸦云API提取脚本
├── MPPT_Preprocessing_and_Visualization.ipynb  # MPPT数据预处理和可视化脚本
├── Weather_Data_Preprocessing_and_Visualization.ipynb  # 气象数据预处理和可视化脚本
├── README.md                              # 项目说明文档
│
├── 十五舍/                                # 十五舍位置数据集
│   ├── Climate_data/                      # 气象站数据
│   │   ├── filtered/                      # 预处理后的气象数据
│   │   ├── raw_20250314/                  # 2025年3月14日收集的原始数据
│   │   └── raw_20250617/                  # 2025年6月17日收集的原始数据
│   │
│   ├── filtered/                          # 预处理后的MPPT数据（按日期分类）
│   ├── raw_20250314/                      # 2025年3月14日收集的原始MPPT数据
│   ├── raw_20250617/                      # 2025年6月17日收集的原始MPPT数据
│   └── test/                              # 测试数据
│
└── 专教/                                  # 专教位置数据集
    ├── Climate_data/                      # 气象站数据
    ├── filtered/                          # 预处理后的MPPT数据
    ├── raw_20250314/                      # 原始数据
    ├── raw_20250617/                      # 原始数据
    └── test/                              # 测试数据
```

## 主要功能

### 1. MPPT数据提取 (MPPT_Extract.ipynb)

该模块负责从涂鸦云API检索MPPT控制器数据，功能包括：
- 使用API身份验证（令牌验签和业务验签）
- 数据提取与保存
- 错误处理和重试机制

### 2. MPPT数据预处理与可视化 (MPPT_Preprocessing_and_Visualization.ipynb)

该模块对原始MPPT数据进行处理和可视化：
- 时间偏移校正（+8小时）
- 数据精确到分钟级别并合并相同时间点的数据
- 按日期分组保存为单独的Excel文件
- 数据可视化分析

### 3. 气象数据预处理与可视化 (Weather_Data_Preprocessing_and_Visualization.ipynb)

该模块处理气象站数据并进行可视化：
- 数据读取和格式化
- 数据精确到分钟级别
- 按日期分组保存为单独的Excel文件
- 气象数据可视化分析

## 使用说明

### 准备工作

确保安装了以下Python包：
```
pandas
numpy
matplotlib
tqdm
requests
hashlib
hmac
json
```

### 运行顺序

1. 首先运行 `MPPT_Extract.ipynb` 从涂鸦云API提取数据
2. 然后运行 `MPPT_Preprocessing_and_Visualization.ipynb` 处理MPPT数据
3. 最后运行 `Weather_Data_Preprocessing_and_Visualization.ipynb` 处理气象数据并进行综合分析

### 数据存储

- 原始数据存储在 `raw_yyyymmdd` 文件夹中
- 处理后的数据存储在 `filtered` 文件夹中，按日期命名为 `yyyy-mm-dd.xlsx`

### 注意事项

- 运行 `MPPT_Extract.ipynb` 前需要确保配置了正确的API密钥和访问令牌
- 数据处理过程中会自动处理时区问题（默认+8小时）
- 可视化功能支持自定义时间范围和特征选择

## 数据说明

### MPPT数据

包含光伏系统的关键性能参数：
- 电流
- 电压
- 功率
- 温度
- 工作模式等

### 气象数据

包含影响光伏系统性能的气象参数：
- 太阳辐照度
- 环境温度
- 湿度
- 风速
- 降雨量等

## 示例分析

项目支持多种分析方式，如：
- 特定时间段内的能源产出分析
- 气象条件对光伏性能的影响分析
- 不同位置（十五舍与专教）的性能比较
- 长期趋势分析

## 新增功能

### 🤖 自动化数据采集 (auto_data_collector.py)

实现了完整的自动化数据采集流程：
- ⏰ 定时数据采集（支持小时和每日采集）
- 📊 多位置、多数据类型支持
- 🔄 自动数据预处理
- 📝 完整的日志记录
- 💾 数据备份功能
- ⚙️ 灵活的配置管理

**使用方法：**
```bash
# 创建配置文件
python launcher.py config

# 启动自动采集器
python launcher.py collector

# 执行一次采集
python launcher.py collector --once
```

### 🎨 交互式可视化界面 (interactive_visualizer.py)

基于Streamlit构建的Web可视化界面：
- 📈 多种图表类型（线图、散点图、柱状图、热力图）
- 📅 灵活的时间范围选择
- 🔍 数据聚合功能（小时、日、周、月）
- 📊 多位置数据比较
- 🔗 MPPT与气象数据相关性分析
- 📥 数据导出功能
- 🎯 响应式设计，支持移动设备

**使用方法：**
```bash
# 启动可视化界面
python launcher.py visualizer
# 或直接运行
streamlit run interactive_visualizer.py
```

### 🚀 系统启动器 (launcher.py)

提供统一的命令行界面：
- 📦 依赖包自动安装
- 🔧 系统状态检查
- ⚙️ 配置文件模板生成
- 🎮 简化的操作界面

**Windows用户可直接运行 `start.bat` 获得图形化菜单**

## 快速开始

### 1. 环境准备
```bash
# 安装依赖包
python launcher.py install
```

### 2. 配置设置
```bash
# 生成配置文件模板
python launcher.py config
# 编辑 config.json 文件，填入API密钥等信息
```

### 3. 启动系统
```bash
# 查看系统状态
python launcher.py status

# 启动可视化界面
python launcher.py visualizer

# 启动数据采集器
python launcher.py collector
```

## 系统架构

```
MPPT数据采集与可视化系统
├── 数据采集层
│   ├── 涂鸦云API接口
│   ├── 气象站数据接口
│   └── 自动化采集调度
├── 数据处理层
│   ├── 数据清洗与预处理
│   ├── 时间校正与聚合
│   └── 数据质量检查
├── 数据存储层
│   ├── 原始数据存储
│   ├── 处理后数据存储
│   └── 备份管理
└── 可视化展示层
    ├── 交互式Web界面
    ├── 图表与报表
    └── 数据导出功能
```

## 高级特性

### 📊 数据分析功能
- 多维度数据可视化
- 时间序列分析
- 相关性分析
- 异常检测（开发中）

### ⚡ 性能优化
- 数据缓存机制
- 增量数据更新
- 异步数据处理
- 内存优化

### 🔒 安全特性
- API密钥安全存储
- 数据传输加密
- 访问日志记录
- 错误处理机制

## 故障排除

### 常见问题

1. **依赖包安装失败**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **API连接失败**
   - 检查网络连接
   - 验证API密钥配置
   - 查看日志文件

3. **可视化界面无法访问**
   ```bash
   streamlit run interactive_visualizer.py --server.port 8501
   ```

4. **数据文件缺失**
   - 检查数据目录权限
   - 验证文件路径配置
   - 运行系统状态检查

## 后续工作

- 🤖 添加机器学习模块进行性能预测
- 🚨 增加系统异常检测功能  
- 📱 开发移动端应用
- 🌐 支持多用户和权限管理
- 📈 增加更多分析算法
- 🔌 支持更多数据源接入

## 部署说明

### 🌐 在线访问

本项目支持多种部署方式，可以轻松发布到云端：

#### 1. 本地运行
```bash
# 方式1：使用启动器
python launcher.py visualizer

# 方式2：直接运行
streamlit run interactive_visualizer.py

# 方式3：Windows批处理（推荐）
./run_visualizer.bat
```

#### 2. GitHub部署

**快速部署：**
```bash
# 检查部署就绪状态
./check_deployment_ready.bat

# 一键部署到GitHub
./deploy_github.bat
```

**详细步骤：**
1. 📖 查看详细指南：`GITHUB_DEPLOY_GUIDE.md`
2. 🚀 创建GitHub仓库
3. 📤 推送代码到仓库
4. 🌐 部署到Streamlit Cloud

#### 3. Streamlit Cloud部署

1. 访问 [Streamlit Cloud](https://share.streamlit.io)
2. 连接GitHub仓库
3. 选择主文件：`interactive_visualizer.py`
4. 点击部署，几分钟后即可在线访问

#### 4. Docker部署

```bash
# 构建镜像
docker build -t mppt-analytics .

# 运行容器
docker run -p 8501:8501 mppt-analytics

# 或使用Docker Compose
docker-compose up -d
```

### 📋 部署检查清单

部署前请确保：
- ✅ 安装了Git和Python 3.8+
- ✅ 配置了GitHub账号和仓库
- ✅ 检查了`requirements.txt`依赖
- ✅ 数据文件已准备（或使用示例数据）
- ✅ 运行了`check_deployment_ready.bat`检查

### 🆘 部署问题解决

常见部署问题及解决方案：

1. **Git推送失败**
   - 检查GitHub Personal Access Token
   - 确认仓库权限和网络连接

2. **Streamlit Cloud部署失败**
   - 检查`requirements.txt`格式
   - 确保所有依赖版本兼容
   - 查看部署日志定位错误

3. **Docker构建失败**
   - 检查Dockerfile语法
   - 确保基础镜像可访问
   - 验证文件路径正确性

详细的部署指南和问题解决方案请参考：
- 📖 `GITHUB_DEPLOY_GUIDE.md` - GitHub部署完整指南
- 📖 `DEPLOYMENT.md` - 多平台部署说明

## 贡献指南

欢迎提交Issue和Pull Request！

### 开发环境设置
```bash
# 克隆仓库
git clone https://github.com/your-username/mppt-analytics.git

# 安装开发依赖
pip install -r requirements.txt

# 运行测试
python test_platform.py
```

### 提交规范
- 🎉 feat: 新功能
- 🐛 fix: 修复bug
- 📝 docs: 文档更新
- 🎨 style: 代码格式
- ♻️ refactor: 重构
- ⚡ perf: 性能优化
- ✅ test: 测试相关

## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 联系方式

- 📧 Email: your-email@example.com
- 🐙 GitHub: https://github.com/your-username/mppt-analytics
- 📝 Issues: https://github.com/your-username/mppt-analytics/issues

---

🎉 **感谢使用MPPT数据分析与可视化平台！**

如果这个项目对您有帮助，请给我们一个 ⭐ Star！
