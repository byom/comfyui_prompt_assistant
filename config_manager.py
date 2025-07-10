import os
import json

class ConfigManager:
    def __init__(self):
        # 插件目录和配置文件路径
        self.dir_path = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(self.dir_path, "config.json")
        
        # 默认配置
        self.default_config = {
            "__comment": "请在下方配置百度翻译和Google Gemini的API密钥",
            "baidu_translate": {
                "app_id": "",
                "secret_key": ""
            },
            "gemini": {
                "api_key": ""
            }
        }
        
        # 确保配置文件存在
        self.ensure_config_exists()
    
    def ensure_config_exists(self):
        """确保配置文件存在，不存在则创建默认配置"""
        if not os.path.exists(self.config_path):
            print("[PromptAssistant] 配置文件不存在，创建默认配置文件...")
            self.save_config(self.default_config)
    
    def load_config(self):
        """加载配置文件"""
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[PromptAssistant] 加载配置文件失败: {str(e)}")
            return self.default_config
    
    def save_config(self, config):
        """保存配置文件"""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"[PromptAssistant] 保存配置文件失败: {str(e)}")
            return False
    
    def get_baidu_translate_config(self):
        """获取百度翻译配置"""
        config = self.load_config()
        return config.get("baidu_translate", self.default_config["baidu_translate"])
    
    def get_llm_config(self):
        """获取LLM配置（兼容旧配置）"""
        config = self.load_config()
        # 兼容旧的llm配置，如果存在则迁移到gemini
        if "llm" in config and config["llm"].get("api_key"):
            return config["llm"]
        return config.get("gemini", self.default_config["gemini"])

    def get_gemini_config(self):
        """获取Gemini配置"""
        config = self.load_config()
        return config.get("gemini", self.default_config["gemini"])

    def update_baidu_translate_config(self, app_id, secret_key):
        """更新百度翻译配置"""
        config = self.load_config()
        config["baidu_translate"] = {
            "app_id": app_id,
            "secret_key": secret_key
        }
        return self.save_config(config)

    def update_llm_config(self, api_key):
        """更新LLM配置（兼容性方法）"""
        return self.update_gemini_config(api_key)

    def update_gemini_config(self, api_key):
        """更新Gemini配置"""
        config = self.load_config()
        config["gemini"] = {
            "api_key": api_key
        }
        return self.save_config(config)

# 创建全局配置管理器实例
config_manager = ConfigManager() 