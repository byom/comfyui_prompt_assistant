import requests
import json
import os
import base64
from io import BytesIO
from PIL import Image

class LLMVisionService:
    BASE_URL = 'https://generativelanguage.googleapis.com/v1beta/models'
    MODEL = 'gemini-2.5-flash'
    
    @staticmethod
    def _make_request(url, json_data, api_key):
        """
        统一处理Gemini API请求
        """
        try:
            # 禁用系统代理
            session = requests.Session()
            session.trust_env = False

            # Gemini API使用URL参数传递API key
            params = {'key': api_key}
            headers = {'Content-Type': 'application/json'}

            # 发送请求
            response = session.post(url, headers=headers, json=json_data, params=params, timeout=30)
            return response
        except requests.exceptions.ProxyError as e:
            # 处理代理错误
            print(f"代理连接错误: {str(e)}")
            # 尝试不使用代理直接连接
            try:
                proxies = {'http': None, 'https': None}
                response = requests.post(url, headers=headers, json=json_data, params=params, proxies=proxies, timeout=30)
                return response
            except Exception as direct_error:
                raise Exception(f"直接连接也失败: {str(direct_error)}")
        except Exception as e:
            raise e
    
    @staticmethod
    def analyze_image(image_data, request_id=None, lang='zh'):
        """
        使用Gemini Vision分析图像
        """
        try:
            # 获取配置
            from ..config_manager import config_manager
            config = config_manager.get_llm_config()

            api_key = config.get('api_key')
            if not api_key:
                return {"success": False, "error": "请先配置Gemini API密钥"}

            # 加载系统提示词
            def load_system_prompts():
                # 获取当前目录
                current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                # 构建提示词文件路径
                prompts_path = os.path.join(current_dir, "js", "config", "system_prompts.json")

                if not os.path.exists(prompts_path):
                    raise Exception(f"系统提示词配置文件不存在: {prompts_path}")

                # 从文件加载提示词
                with open(prompts_path, "r", encoding="utf-8") as f:
                    return json.load(f)

            # 获取系统提示词
            system_prompts = load_system_prompts()
            if not system_prompts or 'vision_prompts' not in system_prompts:
                return {"success": False, "error": "视觉系统提示词加载失败"}

            # 获取对应语言的提示词
            lang_key = lang.upper()
            if lang_key not in system_prompts['vision_prompts']:
                return {"success": False, "error": f"未找到语言 {lang} 的提示词配置"}

            prompt_text = system_prompts['vision_prompts'][lang_key]['content']
            
            # 处理图像数据
            try:
                if isinstance(image_data, str):
                    if image_data.startswith('data:image'):
                        # 处理Base64字符串
                        image_base64 = image_data.split(',')[1]
                    else:
                        # 如果是普通字符串，假设它已经是base64编码
                        image_base64 = image_data
                elif isinstance(image_data, bytes):
                    # 处理字节数据
                    image_base64 = base64.b64encode(image_data).decode('utf-8')
                elif isinstance(image_data, Image.Image):
                    # 处理PIL图像对象
                    buffer = BytesIO()
                    image_data.save(buffer, format="JPEG")
                    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
                elif hasattr(image_data, 'read'):
                    # 处理文件对象
                    image_base64 = base64.b64encode(image_data.read()).decode('utf-8')
                else:
                    return {"success": False, "error": f"不支持的图像数据格式: {type(image_data).__name__}"}
                
                # 验证Base64数据
                if not image_base64:
                    return {"success": False, "error": "Base64数据为空"}
                
                # 尝试解码Base64数据以验证其有效性
                try:
                    base64.b64decode(image_base64)
                except Exception as e:
                    return {"success": False, "error": f"无效的Base64数据: {str(e)}"}
                
            except Exception as e:
                return {"success": False, "error": f"图像数据处理失败: {str(e)}"}
            
            # 构建Gemini Vision API请求
            url = f"{LLMVisionService.BASE_URL}/{LLMVisionService.MODEL}:generateContent"

            data = {
                "contents": [{
                    "parts": [
                        {
                            "text": prompt_text
                        },
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": image_base64
                            }
                        }
                    ]
                }],
                "generationConfig": {
                    "temperature": 0.4,
                    "topP": 0.8,
                    "maxOutputTokens": 1024
                }
            }

            # 发送请求
            response = LLMVisionService._make_request(url, data, api_key)

            # 检查HTTP响应状态码
            if response.status_code != 200:
                return {"success": False, "error": f"HTTP请求失败: 状态码 {response.status_code} - {response.text}"}

            # 解析JSON响应
            try:
                result = response.json()
            except Exception as e:
                return {"success": False, "error": f"解析响应JSON失败: {str(e)}"}

            # 检查错误
            if 'error' in result:
                return {"success": False, "error": result['error'].get('message', '图像分析请求失败')}

            # 处理结果
            if 'candidates' not in result or not result['candidates']:
                return {"success": False, "error": "Gemini Vision响应格式错误: 缺少candidates字段"}

            description = result['candidates'][0]['content']['parts'][0]['text']
            
            return {
                "success": True,
                "data": {
                    "description": description
                }
            }
            
        except Exception as e:
            return {"success": False, "error": f"图像分析过程异常: {str(e)}"} 