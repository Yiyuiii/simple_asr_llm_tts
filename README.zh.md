# 简单的语音到语音LLM聊天
中文介绍 | [English](README.md)

一个简单的语音到语音LLM聊天仓库。流程全部免费，轻量化部署。

## 特性
ASR-LLM-TTS实现语音到语音聊天：

- **ASR（自动语音识别）**：FunASR + 本地SenseVoiceSmall。模型在运行时自动下载。
- **LLM（大型语言模型）**：OpenAI API，兼容使用可免费调用的OpenRouter API。目前无对话记忆。
- **TTS（文本到语音）**：edge_tts

## 安装
推荐配置：Python >= 3.9
1. 克隆仓库并`cd`进入目录。
2. 安装所需的依赖：`pip install -r requirements.txt`

## 使用
1. 检查`main.py`中的设置，特别是`OPENAI_API_KEY`和语言相关设置（默认为zh-CN），例如edge_tts的角色名称和LLM的提示。
2. 运行`python main.py`

每次录音后，ASR-LLM-TTS流程将自动完成。