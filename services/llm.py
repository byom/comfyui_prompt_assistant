import requests
import json
import os
import sys

class LLMService:
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
    def expand_prompt(prompt, request_id=None):
        """
        使用Gemini扩写提示词，自动判断用户输入语言，并设置大模型回答语言。
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
                current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                prompts_path = os.path.join(current_dir, "js", "config", "system_prompts.json")
                if not os.path.exists(prompts_path):
                    raise Exception(f"系统提示词配置文件不存在: {prompts_path}")
                with open(prompts_path, "r", encoding="utf-8") as f:
                    return json.load(f)

            # 获取系统提示词（只保留ZH）
            system_prompts = load_system_prompts()
            if not system_prompts or 'expand_prompts' not in system_prompts or 'ZH' not in system_prompts['expand_prompts']:
                return {"success": False, "error": "扩写系统提示词加载失败"}
            system_message = system_prompts['expand_prompts']['ZH']['content']

            # 判断用户输入语言
            def is_chinese(text):
                return any('\u4e00' <= char <= '\u9fff' for char in text)

            # 构建提示词
            if is_chinese(prompt):
                full_prompt = f"{system_message}\n\n请用中文回答。\n\n用户输入: {prompt}"
            else:
                full_prompt = f"{system_message}\n\nPlease answer in English.\n\nUser input: {prompt}"

            # 构建Gemini API请求
            url = f"{LLMService.BASE_URL}/{LLMService.MODEL}:generateContent"
            data = {
                "contents": [{
                    "parts": [{
                        "text": full_prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.3,
                    "topP": 0.5,
                    "maxOutputTokens": 1500
                }
            }

            # 使用统一的请求方法
            response = LLMService._make_request(url, data, api_key)

            if response.status_code != 200:
                return {"success": False, "error": f"API请求失败: {response.status_code} - {response.text}"}

            result = response.json()

            if 'error' in result:
                return {"success": False, "error": result['error'].get('message', '扩写请求失败')}

            if 'candidates' not in result or not result['candidates']:
                return {"success": False, "error": "Gemini API返回格式错误"}

            expanded_text = result['candidates'][0]['content']['parts'][0]['text']
            return {
                "success": True,
                "data": {
                    "original": prompt,
                    "expanded": expanded_text
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def translate(text, from_lang='auto', to_lang='zh', request_id=None):
        """
        使用Gemini翻译文本，自动设置提示词语言和输出语言。
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
                current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                prompts_path = os.path.join(current_dir, "js", "config", "system_prompts.json")
                if not os.path.exists(prompts_path):
                    raise Exception(f"系统提示词配置文件不存在: {prompts_path}")
                with open(prompts_path, "r", encoding="utf-8") as f:
                    return json.load(f)

            # 获取系统提示词（只保留ZH）
            system_prompts = load_system_prompts()
            if not system_prompts or 'translate_prompts' not in system_prompts or 'ZH' not in system_prompts['translate_prompts']:
                return {"success": False, "error": "翻译系统提示词加载失败"}
            system_message = system_prompts['translate_prompts']['ZH']['content']

            # 动态替换提示词中的{src_lang}和{dst_lang}
            lang_map = {'zh': '中文', 'en': '英文', 'auto': '原文'}
            src_lang = lang_map.get(from_lang, from_lang)
            dst_lang = lang_map.get(to_lang, to_lang)
            sys_msg_content = system_message.replace('{src_lang}', src_lang).replace('{dst_lang}', dst_lang)

            # 设置输出语言指令
            if to_lang == 'en':
                lang_instruction = "Please answer in English."
            else:
                lang_instruction = "请用中文回答"

            # 构建完整提示词
            full_prompt = f"{sys_msg_content}\n\n{lang_instruction}\n\n需要翻译的文本: {text}"

            # 构建Gemini API请求
            url = f"{LLMService.BASE_URL}/{LLMService.MODEL}:generateContent"
            data = {
                "contents": [{
                    "parts": [{
                        "text": full_prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": 0.5,
                    "topP": 0.5,
                    "maxOutputTokens": 1500
                }
            }

            # 使用统一的请求方法
            response = LLMService._make_request(url, data, api_key)

            if response.status_code != 200:
                return {"success": False, "error": f"API请求失败: {response.status_code} - {response.text}"}

            result = response.json()

            if 'error' in result:
                return {"success": False, "error": result['error'].get('message', '翻译请求失败')}

            if 'candidates' not in result or not result['candidates']:
                return {"success": False, "error": "Gemini API返回格式错误"}

            translated_text = result['candidates'][0]['content']['parts'][0]['text']
            return {
                "success": True,
                "data": {
                    "from": from_lang,
                    "to": to_lang,
                    "original": text,
                    "translated": translated_text
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}