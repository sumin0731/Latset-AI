from openai import OpenAI
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# API 키는 환경 변수(`OPENAI_API_KEY`)에서 자동으로 로드됩니다.
client = OpenAI()

try:
    # Chat Completions API 호출
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        # 'messages' 배열에 사용자의 질문을 담아 전달
        messages=[
            {"role": "user", "content": "한국의 수도는 어디인가요?"}
        ]
    )

    # 응답에서 메시지 내용 추출 및 출력
    message_content = response.choices[0].message.content
    print(message_content)

except Exception as e:
    print(f"An error occurred: {e}")
