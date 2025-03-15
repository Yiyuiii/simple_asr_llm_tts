# Simple Voice-to-Voice LLM Chat
[中文介绍](README.zh.md) | [English](README.md)

A simple voice-to-voice LLM chat repo. All is free and light-weight.

## Features
ASR-LLM-TTS to accomplish voice-to-voice chat:

**ASR (Automatic Speech Recognition)**: FunASR + local SenseVoiceSmall. The model is automatically downloaded in running.

**LLM (Large Language Model)**: Integrates OpenAI API. Use OpenRouter API for free. No dialog memory at time.

**TTS (Text-to-Speech)**: edge_tts

## Installation
Recommendation: Python >= 3.9
1. Clone the repository and `CD` into the DIR.
2. Install the required dependencies: `pip install -r requirements.txt`

## Usage
1. Check settings in `main.py`, especially `OPENAI_API_KEY` and those with languages (default: zh-CN), e.g. character name for edge_tts and the prompt for LLM.
2. `python main.py`

After each recording, the ASR-LLM-TTS procedure is automatically finished.
