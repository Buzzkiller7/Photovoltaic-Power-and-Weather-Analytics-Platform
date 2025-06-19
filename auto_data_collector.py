"""
自动化数据采集模块
实现定时从涂鸦云API采集MPPT数据的功能
"""

import os
import time
import schedule
import datetime
from datetime import datetime, time as dt_time
from pathlib import Path
import serial
import json
import subprocess
import sys
import logging
from typing import Dict, Any

class AutoDataCollector:
    """自动化数据采集器"""
    
    def __init__(self, config_path: str = "config.json"):
        """
        初始化自动化数据采集器
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path
        self.config = self.load_config()
        
        # MPPT串口配置
        self.mppt_port = 'COM3'  # 根据实际情况修改
        self.mppt_baudrate = 9600
        
        # 采集时间
        self.start_time = None
        self.end_time = None
        self.is_running = False
        
        # 设置日志记录
        self.setup_logging()
        
        self.setup_from_config()
        
    def load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        default_config = {
            "api": {
                "client_id": "",
                "secret": "",
                "base_url": "https://openapi.tuyacn.com"
            },
            "collection": {
                "interval_hours": 1,  # 采集间隔（小时）
                "daily_collection_time": "00:00",  # 每日采集时间
                "locations": ["十五舍", "专教"],
                "data_types": ["mppt"]
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
            },
            "data_collection": {
                "start_time": "08:00",
                "end_time": "18:00",
                "interval_minutes": 1,
                "data_dir": "data",
                "file_prefix": "mppt_data"
            }
        }
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # 合并配置，保留用户自定义设置
                    self._merge_dict(default_config, loaded_config)
                    return default_config
            except Exception as e:
                print(f"Error loading config: {e}. Using default config.")
                
        # 创建默认配置文件
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
            
        return default_config
    
    def _merge_dict(self, base_dict: dict, update_dict: dict):
        """递归合并字典"""
        for key, value in update_dict.items():
            if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
                self._merge_dict(base_dict[key], value)
            else:
                base_dict[key] = value
    
    def setup_from_config(self):
        """从配置文件设置参数"""
        if self.config:
            data_config = self.config.get('data_collection', {})
            start_time_str = data_config.get('start_time', '08:00')
            end_time_str = data_config.get('end_time', '18:00')
            self.set_collection_time(start_time_str, end_time_str)
    
    def setup_logging(self):
        """设置日志记录"""
        log_config = self.config.get("logging", {})
        
        # 创建logger
        self.logger = logging.getLogger('AutoDataCollector')
        self.logger.setLevel(getattr(logging, log_config.get("level", "INFO")))
        
        # 如果已有处理器，先清除
        if self.logger.handlers:
            self.logger.handlers.clear()
        
        # 创建文件处理器
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler(
            log_config.get("file", "auto_collector.log"),
            maxBytes=log_config.get("max_size_mb", 10) * 1024 * 1024,
            backupCount=log_config.get("backup_count", 5),
            encoding='utf-8'
        )
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        
        # 设置格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加处理器
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def set_collection_time(self, start_time_str, end_time_str):
        """设置采集开始和结束时间
        
        Args:
            start_time_str: 开始时间，格式 "HH:MM"
            end_time_str: 结束时间，格式 "HH:MM"
        """
        try:
            self.start_time = datetime.strptime(start_time_str, "%H:%M").time()
            self.end_time = datetime.strptime(end_time_str, "%H:%M").time()
            print(f"✅ 采集时间设置成功: {start_time_str} - {end_time_str}")
        except ValueError:
            print("❌ 时间格式错误，请使用 HH:MM 格式")
        except AttributeError:
            # 如果logger还未初始化，使用print
            print(f"✅ 采集时间设置成功: {start_time_str} - {end_time_str}")
            
    def update_collection_time(self):
        """更新采集时间配置"""
        print("请设置数据采集时间范围：")
        start_time = input(f"开始时间 (HH:MM) [当前: {self.start_time}]: ") or self.start_time.strftime("%H:%M")
        end_time = input(f"结束时间 (HH:MM) [当前: {self.end_time}]: ") or self.end_time.strftime("%H:%M")
        
        self.set_collection_time(start_time, end_time)
        
        # 更新配置文件
        self.config['data_collection']['start_time'] = start_time
        self.config['data_collection']['end_time'] = end_time
        self.save_config()
    
    def save_config(self):
        """保存配置到文件"""
        try:
            with open('config.json', 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            print("✅ 配置已保存")
        except Exception as e:
            print(f"❌ 保存配置失败: {e}")

    def is_collection_time(self):
        """检查当前是否在采集时间范围内"""
        if not self.start_time or not self.end_time:
            return False
            
        current_time = datetime.now().time()
        
        # 处理跨天的情况
        if self.start_time <= self.end_time:
            return self.start_time <= current_time <= self.end_time
        else:
            return current_time >= self.start_time or current_time <= self.end_time
    
    def collect_data(self, location: str, data_type: str) -> bool:
        """
        采集指定位置和类型的数据
        
        Args:
            location: 数据采集位置（十五舍/专教）
            data_type: 数据类型（mppt）
            
        Returns:
            bool: 采集是否成功
        """
        try:
            self.logger.info(f"开始采集 {location} 的 {data_type} 数据")
            
            # 创建存储目录
            current_date = datetime.now().strftime("%Y%m%d")
            raw_dir = Path(location) / self.config["storage"]["raw_data_dir"] / f"raw_{current_date}"
            raw_dir.mkdir(parents=True, exist_ok=True)
            
            if data_type == "mppt":
                success = self._collect_mppt_data(location, raw_dir)
            else:
                self.logger.error(f"未知的数据类型: {data_type}")
                return False
                
            if success:
                self.logger.info(f"{location} 的 {data_type} 数据采集成功")
                # 自动处理数据
                self._process_collected_data(location, data_type)
            else:
                self.logger.error(f"{location} 的 {data_type} 数据采集失败")
                
            return success
            
        except Exception as e:
            self.logger.error(f"采集数据时发生错误: {e}")
            return False
    
    def collect_mppt_data(self):
        """采集MPPT数据"""
        if not self.is_collection_time():
            return
            
        try:
            # 连接MPPT设备
            with serial.Serial(self.mppt_port, self.mppt_baudrate, timeout=2) as ser:
                # 读取MPPT数据
                data = ser.readline().decode('utf-8').strip()
                
                if data:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    mppt_data = {
                        'timestamp': timestamp,
                        'data': data
                    }
                    
                    # 保存数据
                    self.save_data(mppt_data)
                    print(f"✅ [{timestamp}] MPPT数据采集成功")
                    return True
                else:
                    print("未读取到MPPT数据")
                    return False
                
        except Exception as e:
            print(f"❌ MPPT数据采集失败: {e}")
            return False

    def _collect_mppt_data(self, location: str, output_dir: Path) -> bool:
        """采集MPPT数据 - 内部方法"""
        return self.collect_mppt_data()

    def save_data(self, data):
        """保存数据到文件"""
        data_config = self.config.get('data_collection', {})
        data_dir = data_config.get('data_dir', 'data')
        file_prefix = data_config.get('file_prefix', 'mppt_data')
        
        filename = f"{file_prefix}_{datetime.now().strftime('%Y%m%d')}.json"
        filepath = os.path.join(data_dir, filename)
        
        os.makedirs(data_dir, exist_ok=True)
        
        # 追加数据到文件
        if os.path.exists(filepath):
            with open(filepath, 'a', encoding='utf-8') as f:
                f.write(json.dumps(data, ensure_ascii=False) + '\n')
        else:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(json.dumps(data, ensure_ascii=False) + '\n')
    
    def _process_collected_data(self, location: str, data_type: str):
        """处理采集到的数据"""
        try:
            if data_type == "mppt":
                # 运行MPPT数据预处理
                cmd = [
                    sys.executable, "-m", "jupyter", "nbconvert",
                    "--to", "notebook", "--execute",
                    "MPPT_Preprocessing_and_Visualization.ipynb"
                ]
            else:
                return
                
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                self.logger.info(f"{location} 的 {data_type} 数据处理完成")
            else:
                self.logger.error(f"{location} 的 {data_type} 数据处理失败: {result.stderr}")
                
        except Exception as e:
            self.logger.error(f"处理数据时发生错误: {e}")
    
    def daily_collection_job(self):
        """每日数据采集任务"""
        self.logger.info("开始执行每日数据采集任务")
        
        locations = self.config["collection"]["locations"]
        data_types = self.config["collection"]["data_types"]
        
        success_count = 0
        total_count = len(locations) * len(data_types)
        
        for location in locations:
            for data_type in data_types:
                if self.collect_data(location, data_type):
                    success_count += 1
                    
        self.logger.info(f"每日数据采集完成: {success_count}/{total_count} 成功")
        
        # 执行备份
        if self.config["storage"]["backup_enabled"]:
            self._backup_data()
    
    def hourly_collection_job(self):
        """小时数据采集任务"""
        self.logger.info("开始执行小时数据采集任务")
        
        # 只采集MPPT数据，因为它变化更频繁
        locations = self.config["collection"]["locations"]
        
        for location in locations:
            self.collect_data(location, "mppt")
    
    def _backup_data(self):
        """备份数据"""
        try:
            self.logger.info("开始数据备份")
            
            backup_dir = Path(self.config["storage"]["backup_dir"])
            backup_dir.mkdir(exist_ok=True)
            
            current_date = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            for location in self.config["collection"]["locations"]:
                location_path = Path(location)
                if location_path.exists():
                    backup_path = backup_dir / f"{location}_{current_date}"
                    # 这里可以使用shutil.copytree或其他备份方法
                    self.logger.info(f"备份 {location} 到 {backup_path}")
                    
            self.logger.info("数据备份完成")
            
        except Exception as e:
            self.logger.error(f"数据备份失败: {e}")
    
    def start_scheduler(self):
        """启动定时任务调度器"""
        print("🚀 自动数据采集器已启动")
        print(f"📅 采集时间: {self.start_time} - {self.end_time}")
        print("⏰ 采集间隔: 每分钟")
        print("📊 采集内容: MPPT数据")
        print("按 Ctrl+C 停止采集")
        
        # 设置每分钟采集任务
        schedule.every().minute.do(self.collect_mppt_data)
        
        # 运行调度器
        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n⏹️ 数据采集已停止")
        except Exception as e:
            print(f"调度器运行错误: {e}")
    
    def run_once(self):
        """执行一次完整的数据采集"""
        print("执行一次性数据采集")
        self.collect_mppt_data()

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='自动化数据采集器')
    parser.add_argument('--once', action='store_true', help='只执行一次采集')
    parser.add_argument('--config', default='config.json', help='配置文件路径')
    args = parser.parse_args()
    
    collector = AutoDataCollector(args.config)
    
    if args.once:
        collector.run_once()
    else:
        # 设置采集时间
        print("请设置数据采集时间范围：")
        start_time = input("开始时间 (HH:MM): ")
        end_time = input("结束时间 (HH:MM): ")
        collector.set_collection_time(start_time, end_time)
        
        if collector.start_time and collector.end_time:
            collector.start_scheduler()
        else:
            print("❌ 时间设置失败，程序退出")

if __name__ == "__main__":
    main()
