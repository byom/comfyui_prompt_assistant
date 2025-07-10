# 迁移指南：从智谱AI到Google Gemini

## 🔄 概述

本次更新将ComfyUI Prompt Assistant的大语言模型从智谱AI迁移到Google Gemini，提供更好的性能和更广泛的语言支持。

## 📋 主要变更

### 1. API服务商变更
- **之前**: 智谱AI (GLM-4)
- **现在**: Google Gemini (gemini-2.5-flash)

### 2. 配置文件变更
- **之前**: `config.json` 中的 `llm.api_key`
- **现在**: `config.json` 中的 `gemini.api_key`

### 3. API端点变更
- **之前**: `https://open.bigmodel.cn/api/paas/v4/chat/completions`
- **现在**: `https://generativelanguage.googleapis.com/v1beta/models`

## 🚀 迁移步骤

### 步骤1: 获取Google Gemini API Key

1. 访问 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 使用Google账号登录
3. 点击"Create API Key"按钮
4. 选择一个Google Cloud项目（或创建新项目）
5. 复制生成的API Key

### 步骤2: 更新配置文件

#### 新配置格式
```json
{
  "__comment": "请在下方配置百度翻译和Google Gemini的API密钥",
  "baidu_translate": {
    "app_id": "your_baidu_app_id",
    "secret_key": "your_baidu_secret_key"
  },
  "gemini": {
    "api_key": "your_gemini_api_key"
  }
}
```

#### 自动迁移
- 插件会自动检测旧的`llm`配置并保持兼容性
- 建议手动更新到新的`gemini`配置格式

### 步骤3: 重启ComfyUI
更新配置后，重启ComfyUI以应用新设置。

## 🔧 兼容性说明

### 向后兼容
- 旧的`llm`配置仍然有效
- API接口保持不变
- 前端界面无需修改

### 配置优先级
1. 如果存在`gemini`配置，优先使用
2. 如果只有`llm`配置，作为兼容性支持使用

## 🆕 新功能

### 1. 更好的多语言支持
Google Gemini对中文和英文都有更好的理解能力。

### 2. 更稳定的API服务
Google的API服务具有更高的可用性和稳定性。

### 3. 更快的响应速度
Gemini-2.5-flash模型提供更快的响应速度和更好的性能。

## 🐛 故障排除

### 常见问题

#### 1. API Key无效
**错误**: "请先配置Gemini API密钥"
**解决**: 检查config.json中的API Key是否正确配置

#### 2. 网络连接问题
**错误**: "HTTP请求失败"
**解决**: 检查网络连接，确保可以访问Google API

#### 3. 配置文件格式错误
**错误**: JSON解析失败
**解决**: 检查config.json格式是否正确，使用JSON验证工具

### 测试配置

运行测试脚本验证配置：
```bash
python test_gemini_integration.py
```

## 📞 支持

如果在迁移过程中遇到问题：

1. 检查本迁移指南
2. 查看GitHub Issues
3. 联系开发者

## 📝 更新日志

- **V1.1.0**: 迁移到Google Gemini
- 支持Gemini API进行提示词扩写和翻译
- 支持Gemini Vision进行图片反推提示词
- 保持向后兼容性
