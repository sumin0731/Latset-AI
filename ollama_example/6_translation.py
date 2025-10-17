# 6) 번역(Translation) — 스타일 전환 포함
import ollama
import json
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

def ask(model, task, system="한국어로 간결하고 정확하게 답해줘.", **options):
    return ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": task}
        ],
        options=options or {}
    )['message']['content']


english = """
We propose a lightweight retrieval-augmented pipeline for customer support emails.
The system combines semantic search with local LLM inference to provide accurate responses.
"""

prompt = f"""
다음 영어 문단을 '대학 강의노트' 스타일의 한국어로 번역해줘.
필요하면 용어를 각주 형식으로 보충 설명 (각주는 괄호로).
텍스트:
{english}
"""

print(ask('gemma3:4b', prompt, temperature=0.2))

load_dotenv()
slack_token = os.getenv("SLACK_BOT_TOKEN")
if not slack_token:
    print("오류: .env 파일에 SLACK_BOT_TOKEN이 설정되지 않았습니다.")
    exit(1)
client = WebClient(token=slack_token)
channel_name = "C09KR4KNKNJ"
message_text = "안녕하세요! Slack API를 통해 보내는 테스트 메시지입니다. [byjslee82]"
try:
    response = client.chat_postMessage(
    channel=channel_name,
    text=ask('gemma3:4b', prompt, temperature=0.2)
    )
    print("메시지가 성공적으로 전송되었습니다.")
except SlackApiError as e:
    print(f"메시지 전송에 실패했습니다: {e.response['error']}")