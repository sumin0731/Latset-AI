# 1) "헬로 LLM" — 가장 기본 대화
import ollama
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

resp = ollama.chat(
    model='gemma3:4b',
    messages=[
        {"role": "system", "content": "You are a concise Korean assistant."},
        {"role": "user", "content": "LangChain의 필요성을 한 문장으로 설명해줘."}
    ]
)
print(resp['message']['content'])

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
    text=resp['message']['content']
    )
    print("메시지가 성공적으로 전송되었습니다.")
except SlackApiError as e:
    print(f"메시지 전송에 실패했습니다: {e.response['error']}")
