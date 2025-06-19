"""
MPPT数据采集与可视化系统启动脚本
提供命令行界面来运行不同的功能模块
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """安装依赖包"""
    print("正在安装依赖包...")
    
    # 定义需要安装的包列表
    packages = [
        "pandas>=1.5.0",
        "numpy>=1.21.0", 
        "plotly>=5.0.0",
        "streamlit>=1.28.0",
        "matplotlib>=3.5.0",
        "seaborn>=0.11.0",
        "requests>=2.28.0",
        "urllib3>=1.26.0",
        "pytz>=2022.1",
        "pyyaml>=6.0",
        "scipy>=1.9.0",
        "jupyter>=1.0.0",
        "notebook>=6.4.0",
        "ipykernel>=6.15.0",
        "colorlog>=6.6.0",
        "psutil>=5.9.0"
    ]
    
    success_count = 0
    failed_packages = []
    
    for package in packages:
        print(f"正在安装: {package}")
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", package, "--upgrade"],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            
            if result.returncode == 0:
                print(f"  ✅ {package} 安装成功")
                success_count += 1
            else:
                print(f"  ❌ {package} 安装失败")
                failed_packages.append(package)
                if result.stderr:
                    print(f"     错误: {result.stderr.strip()}")
                    
        except Exception as e:
            print(f"  ❌ {package} 安装异常: {e}")
            failed_packages.append(package)
    
    print(f"\n📊 安装结果:")
    print(f"  成功: {success_count}/{len(packages)}")
    if failed_packages:
        print(f"  失败: {len(failed_packages)} 个包")
        print("  失败的包:")
        for pkg in failed_packages:
            print(f"    - {pkg}")
        print("\n💡 建议:")
        print("1. 检查网络连接")
        print("2. 更新pip: python -m pip install --upgrade pip")
        print("3. 手动安装失败的包")
        return False
    else:
        print("✅ 所有依赖包安装成功!")
        # 创建requirements.txt文件作为记录
        create_requirements_file()
        return True

def create_requirements_file():
    """创建requirements.txt文件"""
    requirements_content = """# MPPT数据采集与可视化系统依赖包
# 此文件由系统自动生成，记录已安装的包

pandas>=1.5.0
numpy>=1.21.0
plotly>=5.0.0
streamlit>=1.28.0
matplotlib>=3.5.0
seaborn>=0.11.0
requests>=2.28.0
urllib3>=1.26.0
pytz>=2022.1
pyyaml>=6.0
scipy>=1.9.0
jupyter>=1.0.0
notebook>=6.4.0
ipykernel>=6.15.0
colorlog>=6.6.0
psutil>=5.9.0
"""
    
    try:
        with open("requirements.txt", "w", encoding="utf-8", newline='\n') as f:
            f.write(requirements_content)
        print("📝 requirements.txt文件已更新")
    except Exception as e:
        print(f"⚠️ 创建requirements.txt文件失败: {e}")

def run_data_collector(args):
    """运行数据采集器"""
    print("启动自动化数据采集器...")
    cmd = [sys.executable, "auto_data_collector.py"]
    
    if args.config:
        cmd.extend(["--config", args.config])
    if args.once:
        cmd.append("--once")
    if args.location:
        cmd.extend(["--location", args.location])
    if args.type:
        cmd.extend(["--type", args.type])
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ 数据采集器运行失败: {e}")
    except KeyboardInterrupt:
        print("\n⏹️ 数据采集器已停止")

def run_visualizer():
    """运行交互式可视化界面"""
    print("启动交互式可视化界面...")
    print("🌐 访问地址将在启动后显示")
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "interactive_visualizer.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ 可视化界面启动失败: {e}")
    except KeyboardInterrupt:
        print("\n⏹️ 可视化界面已停止")

def run_jupyter():
    """启动Jupyter Notebook"""
    print("启动Jupyter Notebook...")
    try:
        subprocess.run([sys.executable, "-m", "jupyter", "notebook"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Jupyter Notebook启动失败: {e}")
    except KeyboardInterrupt:
        print("\n⏹️ Jupyter Notebook已停止")

def show_status():
    """显示系统状态"""
    print("📊 MPPT数据采集与可视化系统状态")
    print("=" * 50)
    
    # 检查Python环境
    print("🐍 Python环境:")
    print(f"  Python版本: {sys.version}")
    print(f"  Python路径: {sys.executable}")
    print(f"  当前目录: {os.getcwd()}")
    
    # 检查文件存在性和编码
    files_to_check = [
        "auto_data_collector.py",
        "interactive_visualizer.py", 
        "requirements.txt",
        "config.json"
    ]
    
    print("\n📁 核心文件状态:")
    for file in files_to_check:
        if os.path.exists(file):
            try:
                # 检查文件编码
                with open(file, 'r', encoding='utf-8') as f:
                    f.read(100)  # 尝试读取前100个字符
                print(f"  ✅ {file} (UTF-8编码)")
            except UnicodeDecodeError:
                print(f"  ⚠️ {file} (编码问题)")
            except Exception as e:
                print(f"  ⚠️ {file} (检查失败: {e})")
        else:
            print(f"  ❌ {file} (缺失)")
    
    print("\n📁 数据目录状态:")
    data_dirs = ["十五舍", "专教"]
    for dir_name in data_dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"  ✅ {dir_name}/")
            # 检查子目录
            sub_dirs = ["filtered", "raw_20250314", "raw_20250617", "Climate_data"]
            for sub_dir in sub_dirs:
                sub_path = dir_path / sub_dir
                if sub_path.exists():
                    file_count = len(list(sub_path.glob("*")))
                    print(f"    ✅ {sub_dir}/ ({file_count} 文件)")
                else:
                    print(f"    ❌ {sub_dir}/ (缺失)")
        else:
            print(f"  ❌ {dir_name}/ (缺失)")
    
    print("\n🐍 Python环境:")
    print(f"  Python版本: {sys.version}")
    print(f"  当前目录: {os.getcwd()}")

def create_config_template():
    """创建配置文件模板"""
    config_template = {
        "api": {
            "client_id": "your_client_id_here",
            "secret": "your_secret_here", 
            "base_url": "https://openapi.tuyacn.com"
        },
        "collection": {
            "interval_hours": 1,
            "daily_collection_time": "00:00",
            "locations": ["十五舍", "专教"],
            "data_types": ["mppt", "weather"]
        },
        "storage": {
            "raw_data_dir": "raw_data",
            "processed_data_dir": "filtered", 
            "backup_enabled": True,
            "backup_dir": "backup"
        },
        "logging": {
            "level": "INFO",
            "file": "auto_collector.log",
            "max_size_mb": 10,
            "backup_count": 5
        }
    }
    
    import json
    with open("config.json", "w", encoding="utf-8") as f:
        json.dump(config_template, f, indent=2, ensure_ascii=False)
    
    print("✅ 配置文件模板已创建: config.json")
    print("📝 请编辑config.json文件，填入您的API密钥等信息")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="MPPT数据采集与可视化系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python launcher.py install                    # 安装依赖包
  python launcher.py collector                  # 启动数据采集器
  python launcher.py collector --once           # 执行一次数据采集
  python launcher.py visualizer                 # 启动可视化界面
  python launcher.py jupyter                    # 启动Jupyter Notebook
  python launcher.py status                     # 查看系统状态
  python launcher.py config                     # 创建配置文件模板
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # 安装命令
    subparsers.add_parser("install", help="安装依赖包")
    
    # 数据采集器命令
    collector_parser = subparsers.add_parser("collector", help="启动数据采集器")
    collector_parser.add_argument("--config", help="配置文件路径")
    collector_parser.add_argument("--once", action="store_true", help="只执行一次采集")
    collector_parser.add_argument("--location", help="指定采集位置")
    collector_parser.add_argument("--type", help="指定数据类型（mppt/weather）")
    
    # 可视化器命令
    subparsers.add_parser("visualizer", help="启动交互式可视化界面")
    
    # Jupyter命令
    subparsers.add_parser("jupyter", help="启动Jupyter Notebook")
    
    # 状态命令
    subparsers.add_parser("status", help="查看系统状态")
    
    # 配置命令
    subparsers.add_parser("config", help="创建配置文件模板")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    print(f"🚀 MPPT数据采集与可视化系统")
    print(f"执行命令: {args.command}")
    print("-" * 50)
    
    if args.command == "install":
        install_requirements()
    elif args.command == "collector":
        run_data_collector(args)
    elif args.command == "visualizer":
        run_visualizer()
    elif args.command == "jupyter":
        run_jupyter()
    elif args.command == "status":
        show_status()
    elif args.command == "config":
        create_config_template()
    else:
        print(f"❌ 未知命令: {args.command}")
        parser.print_help()

if __name__ == "__main__":
    main()
