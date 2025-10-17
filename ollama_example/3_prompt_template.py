# 3) 프롬프트 템플릿화 (함수로 래핑)
import ollama
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


print(ask('gemma3:4b', "대한민국을을 한 문장으로 설명해줘."))

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
    text=ask('gemma3:4b', "대한민국을을 한 문장으로 설명해줘.")
    )
    print("메시지가 성공적으로 전송되었습니다.")
except SlackApiError as e:
    print(f"메시지 전송에 실패했습니다: {e.response['error']}")