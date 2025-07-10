


# ComfyUI Prompt Assistant✨提示词小助手

🎉🎉感谢大家对提示词小助手的喜爱！🎉🎉


欢迎大家提出宝贵意见，我会收集大家的反馈持续优化。让大家的小助手会变得更好用~😄

插件详细使用教程，可以查看我B站主页的视频教程，很详细！如果使用过程遇到问题也可以到我的b站主页或者Github上留言反馈。🫰🏻

> 👉👉👉<a href="https://space.bilibili.com/520680644"><img src="https://img.shields.io/badge/B%E7%AB%99-%E4%BD%BF%E7%94%A8%E8%AF%B4%E6%98%8E-blue?logo=bilibili&logoColor=2300A5DC&labelColor=%23FFFFFF"></a> &ensp;👈👈👈

## ✨插件介绍
  
这是一个无需添加节点，即可实现提示词翻译、扩写、预设标签插入、图片反推提示词、历史记录功能等功能的comfyUI插件。   
> 📍手动安装请从右侧[Releases](https://github.com/yawiii/comfyui_prompt_assistant/releases)下载最新版本。


## 📣更新
<details>
 <summary>[2025-7-10]V1.1.0： </summary>

- 🔥 重大更新：将大语言模型从智谱AI迁移到Google Gemini
- ✨ 支持Google Gemini 2.5 Flash API进行提示词扩写和翻译
- ✨ 支持Google Gemini 2.5 Flash Vision进行图片反推提示词
- 🔧 更新配置管理，支持Gemini API Key配置
- 📚 更新文档和配置说明
- 🔄 保持向后兼容，旧的LLM配置仍然有效

</details>
<details>
 <summary>[2025-6-24]V1.0.6： </summary>

- 修复了一些界面bug

</details>
<details>
 <summary>[2025-6-24]V1.0.5： </summary>
  
- 修复新版创建使用选择工具栏创建kontext节点时，出现小助手UI异常问题
 
- 修复可能网络环境问题造成的智谱无法服务无法使用问题
 
- 修复可能出现实例清除出错导致工作流无法加载问题
  
- 修复AIGODLIKE-COMFYUI-TRANSLATION汉化插件导致标签弹窗打开卡住的问题
  
- 新增标签面板可以调整大小
  
- 优化UI资源加载机制
  
</details>
<details>
 <summary>[2025-6-24]V1.0.3： </summary>
  
- 重构了api请求服务，避免apikey暴露在前端
  
- 修改了配置的保存和读取机制，解决配置无法保存问题
  
- 修复了少许bug
  
</details>

<details>
<summary>[2025-6-21]V1.0.2：</summary>
  
- 修复了少许bug
  
</details>

<details>
<summary>[2025-6-15]V1.0.0:</summary>
  
 - 一键插入tag

- 支持llm扩写

- 支持百度翻译和llm翻译切换

- 图片反推提示词
  
- 历史、撤销、重做
</details>

## ✨ 功能介绍

![810x456-翻译](https://github.com/user-attachments/assets/dd4f282a-f9e3-4f0f-9da3-a141bea03653)

![810x456-扩写](https://github.com/user-attachments/assets/4060c46b-8ece-4917-9679-2e503947a810)

![810x456-反推](https://github.com/user-attachments/assets/38e49900-2375-4fe7-8211-1083e20f5d0d)

![810x456-历史](https://github.com/user-attachments/assets/49b903db-1cfd-40bb-bcb0-c1752474248e)

![810x456-配置功能](https://github.com/user-attachments/assets/673e1787-3110-4ed5-897a-eda192e3af3f)

## 📦 安装方法

#### 从ComfyUI Manager中安装
在Manager中输入“Prompt Assistant”或“提示词小助手”，点击Install，选择最新版本安装。


![安装](https://github.com/user-attachments/assets/8be5cf02-d4ec-4023-b400-84358f46c22c)


#### 手动安装



1. 从[克隆仓库](https://github.com/yawiii/comfyui_prompt_assistant/releases)中下载最新版本
解压缩到ComfyUI/custom_nodes目录下


2. 重启 ComfyUI

## ⚙️ 配置说明
目前小助手的翻译功能支持百度和Google Gemini两种翻译服务。百度机翻速度快，Google Gemini则是 AI翻译，更加准确。你可以根据自己的需求，进行切换。而扩写和提示词反推则必须要使用Google Gemini的服务来实现。

百度翻译申请入口：[通用文本翻译API链接](https://fanyi-api.baidu.com/product/11)

![百度](https://github.com/user-attachments/assets/f3fe2d2d-9507-4bff-887e-003f2e13a19c)

Google Gemini API申请入口：[Google AI Studio](https://aistudio.google.com/app/apikey)

获取Google Gemini API Key的步骤：
1. 访问 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 使用Google账号登录
3. 点击"Create API Key"按钮
4. 选择一个Google Cloud项目（或创建新项目）
5. 复制生成的API Key

#### 填入App id 、密钥、Gemini API key

在插件设置中填入：
- 百度翻译：App ID 和 Secret Key
- Google Gemini：API Key



## 🫰🏻💖如果插件对您有帮助，不妨请我喝杯咖啡吧~💖🫰🏻


![赞赏码](https://github.com/user-attachments/assets/3072ba94-a910-4b32-a874-0aed0662a02f)




