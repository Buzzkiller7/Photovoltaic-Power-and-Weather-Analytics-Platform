# GitHub部署指南

## 📋 部署步骤

### 1. 准备工作

确保你已经：
- ✅ 安装了Git
- ✅ 有GitHub账号
- ✅ 创建了GitHub仓库

### 2. 快速部署

#### Windows用户：
```bash
./deploy.bat
```

#### Linux/Mac用户：
```bash
chmod +x deploy.sh
./deploy.sh
```

### 3. 手动部署步骤

如果自动脚本不工作，可以手动执行：

```bash
# 1. 初始化Git仓库
git init

# 2. 添加文件
git add .

# 3. 提交
git commit -m "Initial commit: MPPT数据分析与可视化平台"

# 4. 添加远程仓库（替换为你的仓库URL）
git remote add origin https://github.com/yourusername/mppt-analytics.git

# 5. 推送到GitHub
git branch -M main
git push -u origin main
```

## 🌐 Streamlit Cloud部署

### 步骤：
1. 访问 [https://share.streamlit.io](https://share.streamlit.io)
2. 使用GitHub账号登录
3. 点击 "New app"
4. 选择你的GitHub仓库
5. 设置：
   - **Branch**: `main`
   - **Main file path**: `interactive_visualizer.py`
   - **Python version**: `3.9`
6. 点击 "Deploy"

### 注意事项：
- Streamlit Cloud会自动读取 `requirements.txt`
- 部署过程可能需要几分钟
- 免费版有资源限制

## 🐳 Docker部署

### 本地Docker运行：
```bash
# 构建镜像
docker build -t mppt-analytics .

# 运行容器
docker run -p 8501:8501 mppt-analytics
```

### 使用Docker Compose：
```bash
docker-compose up -d
```

## ⚙️ 配置说明

### 环境变量
可以设置以下环境变量：
- `STREAMLIT_SERVER_PORT`: 服务端口（默认8501）
- `STREAMLIT_SERVER_ADDRESS`: 服务地址（默认0.0.0.0）

### 数据文件
- 确保数据文件路径正确
- 大数据文件建议使用Git LFS
- 敏感数据不要上传到公共仓库

## 🔧 故障排除

### 常见问题：

1. **Git命令失败**
   - 确保Git已正确安装
   - 检查网络连接
   - 验证GitHub认证

2. **Streamlit部署失败**
   - 检查requirements.txt格式
   - 确保所有依赖兼容
   - 查看部署日志

3. **Docker构建失败**
   - 检查Dockerfile语法
   - 确保基础镜像可用
   - 验证文件路径

### 获取帮助：
- 查看GitHub Issues
- 联系项目维护者
- 参考Streamlit官方文档
