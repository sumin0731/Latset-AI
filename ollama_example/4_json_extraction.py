import ollama
import json
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

text = """
주문 3건:
1) 상품: 무선마우스, 수량 2, 가격 25,000원
2) 상품: 기계식 키보드, 수량 1, 가격 89,000원
3) 상품: USB-C 케이블, 수량 3, 가격 9,900원
총 배송지는 서울시 강남구 테헤란로 1
"""

prompt = f"""
아래 텍스트에서 주문 항목을 JSON으로 추출해.
스키마:
{{
  "orders":[{{"item":str,"qty":int,"price_krw":int}}],
  "shipping_address": str,
  "total_price_krw": int
}}
텍스트:
{text}
반드시 JSON만 출력.
"""

resp = ollama.chat(
    model='gemma3:4b',  # 1b 대신 4b로 모델 맞춰주세요
    messages=[{"role": "user", "content": prompt}],
    format='json',  # JSON 모드
    options={"temperature": 0}
)

data = json.loads(resp['message']['content'])
print(json.dumps(data, indent=2, ensure_ascii=False))

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
    text=json.dumps(data, indent=2, ensure_ascii=False)
    )
    print("메시지가 성공적으로 전송되었습니다.")
except SlackApiError as e:
    print(f"메시지 전송에 실패했습니다: {e.response['error']}")