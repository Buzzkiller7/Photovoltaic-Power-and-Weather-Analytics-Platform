# 部署脚本 - GitHub上传和Streamlit Cloud部署

# 检查Git是否已初始化
if [ ! -d ".git" ]; then
    echo "初始化Git仓库..."
    git init
fi

# 添加所有文件到Git
echo "添加文件到Git..."
git add .

# 提交更改
echo "提交更改..."
git commit -m "Initial commit: MPPT数据分析与可视化平台"

# 设置远程仓库（需要替换为你的GitHub仓库URL）
echo "设置远程仓库..."
read -p "请输入你的GitHub仓库URL: " repo_url
git remote add origin $repo_url

# 推送到GitHub
echo "推送到GitHub..."
git branch -M main
git push -u origin main

echo "部署完成！"
echo "现在你可以:"
echo "1. 访问你的GitHub仓库查看代码"
echo "2. 在Streamlit Cloud (https://share.streamlit.io) 部署应用"
echo "3. 连接GitHub仓库并选择 interactive_visualizer.py 作为入口文件"
